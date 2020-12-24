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
	w.gasper_layout = {'LHS': [['N/A','23.0','353.0' ],['N/A','24.25','379.25' ],['N/A','25.75','410.75' ],
					   ['N/A','27.0','437.0' ],['N/A','28.25','463.25' ],['N/A','29.75','494.75' ],
					   ['N/A','31.0','521.0' ],['N/A','32.25','547.25' ],['N/A','33.75','578.75' ],
					   ['N/A','35.0','605.0' ],['N/A','36.25','631.0' ],['N/A','38.25','662.58' ],
					   ['N/A','40.25','695.9' ],['N/A','41.5','724.32' ],['N/A','42.75','751.75' ],
					   ['N/A','44.0','778.0' ],['N/A','45.25','804.25' ],['N/A','46.75','835.75' ],
					   ['N/A','48.0','862.0' ],['N/A','49.25','888.25' ],['N/A','50.75','919.75' ],
					   ['N/A','52.0','946.0' ],['N/A','53.25','972.25' ],['N/A','54.75','1003.75' ],
					   ['N/A','56.0','1030.0' ],['N/A','57.25','1056.25' ],['N/A','58.75','1087.75' ],
					   ['N/A','60.0','1114.0' ],['N/A','61.25','1140.25'],['N/A','62.75','1171.75' ],
					   ['N/A','64.0','1198.0' ]],
					   'RHS': [['N/A','23.0','353.0' ],['N/A','24.25','379.25' ],['N/A','25.75','410.75' ],
					   ['N/A','27.0','437.0' ],['N/A','28.25','463.25' ],['N/A','29.75','494.75' ],
					   ['N/A','31.0','521.0' ],['N/A','32.25','547.25' ],['N/A','33.75','578.75' ],
					   ['N/A','35.0','605.0' ],['N/A','36.25','631.0' ],['N/A','38.25','662.58' ],
					   ['N/A','40.25','695.9' ],['N/A','41.5','724.32' ],['N/A','42.75','751.75' ],
					   ['N/A','44.0','778.0' ],['N/A','45.25','804.25' ],['N/A','46.75','835.75' ],
					   ['N/A','48.0','862.0' ],['N/A','49.25','888.25' ],['N/A','50.75','919.75' ],
					   ['N/A','52.0','946.0' ],['N/A','53.25','972.25' ],['N/A','54.75','1003.75' ],
					   ['N/A','56.0','1030.0' ],['N/A','57.25','1056.25' ],['N/A','58.75','1087.75' ],
					   ['N/A','60.0','1114.0' ],['N/A','61.25','1140.25'],['N/A','62.75','1171.75' ],
					   ['N/A','64.0','1198.0' ]]
						}

	#add blank foe gasper length
	for side in ['LHS', 'RHS']:
		for idx, g in enumerate(w.gasper_layout[side]):
				w.gasper_layout[side][idx].append('')
				
	w.deu_layout = {'LHS': [['200RH1','985','387.795','LHS'],['200RH3','1412','555.9055','LHS'],['200RH7','1849','727.9528','LHS'],
			   ['200RH11','2278','896.8504','LHS'],['200RH13','2704','1064.567','LHS'],['200RH15','2918','1148.819','LHS'],],
			  'RHS': [['200RH2','985','387.795','RHS'],['200RH4','1412','555.9055','RHS'],['200RH8','1849','727.9528','RHS'],
			   ['200RH12','2278','896.8504','RHS'],['200RH14','2704','1064.567','RHS'],['200RH16','2918','1148.819','RHS']]}


	w.vc_layout = {'LHS': [['7381 VC13','22.25','345.125','200RH1','N/A'],['7381 VC14','24.0','374.0','200RH1','N/A'],['7381 VC15','25.5','405.5','200RH1','N/A'],
				  ['7381 VC16','26.75','431.75','200RH1','N/A'],['7381 VC31','28.0','458.0','200RH3','N/A'],['7381 VC32','29.5','489.5','200RH3','N/A'],
				  ['7381 VC33','30.75','515.75','200RH3','N/A'],['7381 VC34','32.0','542.0','200RH3','N/A'],['7381 VC35','33.25','568.25','200RH3','N/A'],
				  ['7381 VC36','34.75','599.75','200RH3','N/A'],['7381 VC71','36.0','626.0','200RH7','N/A'],['7381 VC72','37.75','654.25','200RH7','N/A'],
				  ['7381 VC73','39.75','687.57','200RH7','N/A'],['7381 VC74','41.25','718.48','200RH7','N/A'],['7381 VC75','42.25','741.25','200RH7','N/A'],
				  ['7381 VC76','43.75','772.75','200RH7','N/A'], ['7381 VC111','45.0','799.0','200RH11','N/A'],['7381 VC112','46.25','825.25','200RH11','N/A'],
				  ['7381 VC113','47.75','856.75','200RH11','N/A'], ['7381 VC114','49.0','883.0','200RH11','N/A'],['7381 VC115','50.25','909.25','200RH11','N/A'],
				  ['7381 VC116','51.75','940.75','200RH11','N/A'],['7381 VC131','53.0','967.0','200RH13','N/A'],['7381 VC132','54.25','993.25','200RH13','N/A'],
				  ['7381 VC133','55.75','1024.75','200RH13','N/A'],['7381 VC134','57.0','1051.0','200RH13','N/A'],['7381 VC135','58.5','1082.5','200RH13','N/A'],
				  ['7381 VC136','59.75','1108.75','200RH13','N/A'], ['7381 VC151','61.0','1135.0','200RH15','N/A'],
				  ['7381 VC152','62.25','1161.25','200RH15','N/A'],['7381 VC153','63.5','1187.5','200RH15','N/A']],
				'RHS': [['7382 VC23','22.25','345.125','200RH2','N/A'],['7382 VC24','24.0','374.0','200RH2','N/A'],['7382 VC25','25.5','405.5','200RH2','N/A'],
					  ['7382 VC26','26.75','431.75','200RH2','N/A'],['7382 VC41','28.0','458.0','200RH4','N/A'],['7382 VC42','29.5','489.5','200RH4','N/A'],
					  ['7382 VC43','30.75','515.75','200RH4','N/A'],['7382 VC44','32.0','542.0','200RH4','N/A'],['7382 VC45','33.25','568.25','200RH4','N/A'],
					  ['7382 VC46','34.75','599.75','200RH4','N/A'],['7382 VC81','36.0','626.0','200RH8','N/A'],['7382 VC82','37.75','654.25','200RH8','N/A'],
					  ['7382 VC83','39.75','687.57','200RH8','N/A'],['7382 VC84','41.25','718.48','200RH8','N/A'],['7382 VC85','42.25','741.25','200RH8','N/A'],
					  ['7382 VC86','43.75','772.75','200RH8','N/A'], ['7382 VC121','45.0','799.0','200RH12','N/A'],['7382 VC122','46.25','825.25','200RH12','N/A'],
					  ['7382 VC123','47.75','856.75','200RH12','N/A'], ['7382 VC124','49.0','883.0','200RH12','N/A'],['7382 VC125','50.25','909.25','200RH12','N/A'],
					  ['7382 VC126','51.75','940.75','200RH12','N/A'],['7382 VC141','53.0','967.0','200RH14','N/A'],['7382 VC142','54.25','993.25','200RH14','N/A'],
					  ['7382 VC143','55.75','1024.75','200RH14','N/A'],['7382 VC144','57.0','1051.0','200RH14','N/A'],['7382 VC145','58.5','1082.5','200RH14','N/A'],
					  ['7382 VC146','59.75','1108.75','200RH14','N/A'], ['7382 VC161','61.0','1135.0','200RH16','N/A'],
					  ['7382 VC162','62.25','1161.25','200RH16','N/A'],['7382 VC163','63.5','1187.5','200RH16','N/A']]
				  }

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
		self.gasper_layout = copy.deepcopy(source.gasper_layout)
		self.deu_layout = copy.deepcopy(source.deu_layout)
		self.vc_layout = copy.deepcopy(source.vc_layout)
		
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

		self.gasper_figure = Figure(figsize=(5,3), dpi=100)
		self.ax4 = self.gasper_figure.add_subplot(111, aspect='equal', adjustable='box')
		#self.ax2 = self.lopa_figure.add_subplot(111, aspect='equal', adjustable='box')
		#self.ax6 = self.gasper_figure.add_subplot(212, aspect='equal', adjustable='box')
		
		self.gasper_figure.subplots_adjust(left=0.05, bottom=0.02, right=0.99, top=0.98, wspace=None, hspace=None)

		self.deu_figure = Figure(figsize=(5,3), dpi=100)
		self.ax7 = self.deu_figure.add_subplot(111, aspect='equal', adjustable='box')

		self.deu_figure.subplots_adjust(left=0.05, bottom=0.02, right=0.99, top=0.98, wspace=None, hspace=None)

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
				'Gasper Layout': self.gasper_layout,
				'DEU Layout': self.deu_layout,
				'VCC Layout': self.vc_layout,
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
				
				row_end = srp + station+4
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

			# Add the gasper hoses
			for p in self.gasper_layout[side]:

				if 'mm' in p[3]:
					hose = f'Gasper Hose {p[3]}'

					if hose not in qtys.keys():
						qtys[hose] = 1
					else:
						qtys[hose] += 1



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


	def get_gasper_stations(self):

		gasper_stations = {'LHS': [], 'RHS': []}

		for side in ['LHS', 'RHS']:

			for part in self.psu_layout[side]:
				if part[1] == 'Gasper':
					gasper_stations[side].append(float(part[3]))

		return gasper_stations

	def get_psiu_stations(self):

		psiu_stations = {'LHS': [], 'RHS': []}

		for side in ['LHS', 'RHS']:

			for part in self.psu_layout[side]:
				if 'PSIU' in part[1]:
					psiu_stations[side].append(float(part[3]))

		return psiu_stations

class PSU_Saved_State():
	def __init__(self, psu):

		setup_variables(self)
		PSU_Backend.update_variables(self, psu)
		
