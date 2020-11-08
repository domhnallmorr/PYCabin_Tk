import treeview_functions

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import copy
import Default_AC_Models

def setup_variables(w):
	w.type = 'PSU'
	w.title = None
	w.aircraft_type = None
	w.description = None
	w.lopa = None
	w.drawing_no = None
	w.drawing_rev = None
	w.parts = []
	w.psu_layout = {'LHS': [], 'RHS': []}
	
class PSU_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		self.setup_plot()
		self.save_class = PSU_Saved_State
		self.mainapp = self.parent_page.mainapp
		

		
	def update_variables(self, source):
		self.title = source.title
		self.aircraft_type = source.aircraft_type
		self.description = source.description		
		self.lopa = source.lopa
		self.drawing_no = source.drawing_no
		self.drawing_rev = source.drawing_rev
		self.parts = copy.deepcopy(source.parts)
		self.psu_layout = copy.deepcopy(source.psu_layout)
		
		if self.aircraft_type in ['A320', 'A319']:
			self.treeview_node = 'A320 PSUs'
			self.psu_y_coords = [70, 75]
			
		elif self.aircraft_type in ['B737-800']:
			self.treeview_node = 'B737 PSUs'
			
	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, PSU_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, PSU_Saved_State)
			
		self.update_variables(source)

	def setup_plot(self):
	
		#self.lopa_figure = Figure(figsize=(5,5), dpi=100)
		self.lopa_figure = Figure(figsize=(5,3), dpi=100)
		self.ax1 = self.lopa_figure.add_subplot(211, aspect='equal', adjustable='box')
		#self.ax2 = self.lopa_figure.add_subplot(111, aspect='equal', adjustable='box')
		self.ax3 = self.lopa_figure.add_subplot(212, aspect='equal', adjustable='box')
		
		self.lopa_figure.subplots_adjust(left=0.05, bottom=0.02, right=0.99, top=0.98, wspace=None, hspace=None)

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments
			
		return {'Title': self.title,
				'Description': self.description,
				'Aircraft Type': self.aircraft_type,
				'LOPA': self.lopa,
				'Drawing Number': self.drawing_no,
				'Drawing Rev': self.drawing_rev,
				'Parts': self.parts,
				'Layout': self.psu_layout,
				'Comments': comments}

	def gen_parts_table(self):
	
		parts_table = [] #[qty, part_no, description]
		
		for part in self.parts:
				
			parts_table.append([part[4], part[2], part[1]])
		
		return parts_table

	def gen_ipc_table(self):

		ipc_table = []

		count = 0

		for part in self.parts:
			count += 1
			ipc_table.append([count, part[2], part[1], '', part[4]])

		return ipc_table

	def auto_assign_psius(self):
		self.psiu_layout = {}
		for side in ['LHS', 'RHS']:
		
			self.psiu_layout[side] = self.assign_320_psius(side)
		
		return self.psiu_layout
		
	def gen_a320_psu_layout(self, psiu_layout, start_lhs, end_lhs, start_rhs, end_rhs, wb_installed, lav_d, lav_e):
		
			
		start_stations = {'LHS': start_lhs, 'RHS': start_rhs}
		end_stations = {'LHS': end_lhs, 'RHS': end_rhs}
		#start = 320
		#end = 1206.98
		
		self.available_parts = {} #tracker for existing parts, decreases in qty as used up
		
		for p in self.parts:
			if 'Filler Panel' in p[1]:
				self.available_parts[int(p[1].split('"')[0])] = int(p[3])
				
		psu_layout = {'LHS': [], 'RHS': []}
		
		if wb_installed[0]:
			psu_layout['LHS'] = [['WB', 'Partition Panel LHS', '-', start_stations['LHS']]]
			start_stations['LHS'] = start_stations['LHS']+2
		if wb_installed[1]:
			psu_layout['RHS'] = [['WB', 'Partition Panel RHS', '-', start_stations['RHS']]]
			start_stations['RHS'] = start_stations['LHS']+2
			
		self.lopa_page = self.mainapp.frames[self.lopa]
		
		oxygen_len = 12
		gasper_len = 3
		
		for side in ['LHS', 'RHS']:
			start = start_stations[side]
			end = end_stations[side]
			
		# 1. Get LOPA layout
			seat_layout = self.lopa_page.backend.seat_layout[side]

			for index, row in enumerate(seat_layout):
				row_number = row[0]
				#2 . get the start and end stations of row
				
				if index == 0:
					row_start = start
				else:
					row_start = row_end
				#if index != len(seat_layout)-1:
				seat = self.mainapp.frames[row[1]]
				station = float(row[3])
				srp = float(seat.backend.srp_x)
				
				row_end = srp + station
				#else:
				#	row_end = end
		
				#3. Calculate gap to filled in front of psiu_layout
				
				psiu = psiu_layout[side][index]
				if '11"' in psiu:
					psiu_len = 11
				elif '8"' in psiu:
					psiu_len = 8
					
				gap_to_fill = row_end - row_start - psiu_len - oxygen_len - gasper_len
				
				local_station = row_start
				count = 0 #counter for panels
			
				while gap_to_fill > 0:
					
					if gap_to_fill >= 8:
						panels = self.select_filler_panels(8)
						gap_to_fill = gap_to_fill - 8
						
					else:
						panels = self.select_filler_panels(gap_to_fill)
						gap_to_fill = gap_to_fill - gap_to_fill
						#break						
					for p in panels:
						text = f'{p}" Filler Panel'
						psu_layout[side].append([row_number, text, '-', local_station])
						local_station += p
						
						self.available_parts[p] -= 1


					
				psu_layout[side].append([row_number, psiu, '-', row_end - psiu_len - oxygen_len - gasper_len])
				psu_layout[side].append([row_number, f'Oxygen Box {side}', '-', row_end - oxygen_len - gasper_len])
				psu_layout[side].append([row_number, 'Gasper', '-', row_end - gasper_len])
				
			# Add panels at end of layout
			if side == 'LHS':
				if lav_d:
					end = 1207
					lav = True
				else:
					end = 1250
					lav = False
			elif side == 'RHS':
				if lav_e:
					end = 1207
					lav = True
				else:
					end = 1250
					lav = False
					
			gap_to_fill = end-row_end
			
			if lav and gap_to_fill >= 6:
				gap_to_fill = gap_to_fill - 6 # account for clamping and adjustment panel
			
			local_station = row_end

			while gap_to_fill > 0:
				
				if gap_to_fill >= 8:
					panels = self.select_filler_panels(8)
					gap_to_fill = gap_to_fill - 8
				else:
					panels = self.select_filler_panels(gap_to_fill)
					gap_to_fill = gap_to_fill - gap_to_fill
					
				for p in panels:
					text = f'{p}" Filler Panel'
					psu_layout[side].append([row_number, text, '-', local_station])
					local_station += p			
			
			if lav:
				psu_layout[side].append([row_number, f'Adjustment Panel {side}', '-', local_station])
				psu_layout[side].append([row_number, 'Clamping Panel', '-', local_station+4])
				

		return psu_layout
		
	def select_filler_panels(self, gap):
	
		possible_solutions = {8: [ [2,2,2,2],  [4,2,2], 
								[6,1,1], [4,4], [6,2], [8]],
							7: [[2,2,2,1], [4,2,1],[6,1]],
							6: [[2,2,1,1],[2,2,2], [4,1,1],
								[4,2],[6]],
							5: [[2,1,1,1],[2,2,1],
								[4,1]],
							4: [[1,1,1,1], [2,1,1],[2,2],[4]],
							3: [[1,1, 1], [2,1]],
							2: [[1, 1], [2]],
							1: [[1]]} 
		
		solutions = reversed(possible_solutions[gap])
		found_solution = False
		for sol in solutions:
			
			if self.check_can_use_existing_filler_panels(sol):
				found_solution = True
				break
		
		if found_solution:
			return sol
		else:
			return possible_solutions[gap][-1]
		
	def check_can_use_existing_filler_panels(self, panels):
		
		can_use = True
		qtys = {}
		for p in panels:
			if p not in qtys.keys():
				qtys[p] = 1
			else:
				qtys[p] += 1

		for p in qtys:
			if qtys[p] > self.available_parts[p]:
				can_use = False
				break
				
		return can_use
		
	def update_parts_table(self):
		
		qtys = {}
		
		for side in ['LHS', 'RHS']:
			for p in self.psu_layout[side]:
				#if 'Filler Panel' in p[1]:
					if p[1] not in qtys.keys():
						qtys[p[1]] = 1
					else:
						qtys[p[1]] += 1
		
		for p in self.parts:	
			if p[1] in qtys.keys():
				existing_qty = int(p[3])
				required_qty = qtys[p[1]]
				additonal_qty = int(p[5])
				
				p[4] = qtys[p[1]]
				if required_qty - existing_qty + additonal_qty< 0: #don't need any additonal items
					p[6] = 0
				else:
					p[6] = required_qty - existing_qty + additonal_qty
		
	def determine_first_psu_station(self, side):

		return 320
		
		
	def determine_last_psu_station(self, side):

		return 1206.98	

	def assign_320_psius(self, side):

		
		# 1. Get LOPA layout
		self.lopa_page = self.mainapp.frames[self.lopa]
		psiu_layout = self.lopa_page.backend.seat_layout[side]
		
		for index, row in enumerate(psiu_layout):
			psiu_layout[index].append(None)

		# 2. Assign every second row 11"
		start_row = 0
		
		psiu_layout[start_row][-1] = '11" PSIU'
		
		for index in range(0, len(psiu_layout),2):
		#for index, row in enumerate(psiu_layout):
			
			psiu_layout[index][-1] = '11" PSIU'
			
		# 3. Find Rows nearest Emergency Exit ans Assign 11"
		
		if self.lopa_page.backend.aircraft_type == 'A320':
			exits = [668.15, 701.5]
		

		for exit in exits:
			closest_dist = None
			closest_row = None
			
			for index, row in enumerate(psiu_layout):
				dist = abs(row[3] - exit)
		
				if not closest_dist:
					#if not psiu_layout[index][-1]:
						closest_dist = dist
						closest_row = index
				
				elif dist < closest_dist:
					#if not psiu_layout[index][-1]:
						closest_dist = dist
						closest_row = index					

			psiu_layout[closest_row][-1] = '11" PSIU'
			
		# 4. Assign all other rows 8" PSIU
		
		for index, row in enumerate(psiu_layout):
		
			if not row[-1]:
				psiu_layout[index][-1] = '8" PSIU'
				
		check_number_11 = 0
		check_number_8 = 0
		
		for index, row in enumerate(psiu_layout):
			if row[-1] == '11" PSIU':
				check_number_11 += 1
			elif row[-1] == '8" PSIU':
				check_number_8 += 1
				

		
		return psiu_layout

	def gen_ipc_data(self, fromto):
	
		#data = treeview_functions.get_all_treeview_items(self.item_tree)
		ipc_data = []
		for d in self.parts:
			#desc = self.mainapp.frames[d[1]].backend.description
			ipc_data.append(['', str(d[2]), str(d[1]), fromto, str(d[4])])	
		
		return ipc_data
class PSU_Saved_State():
	def __init__(self, psu):

		setup_variables(self)
		PSU_Backend.update_variables(self, psu)
		
