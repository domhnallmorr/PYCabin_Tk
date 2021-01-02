import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import copy

import treeview_functions


def setup_variables(w):
	w.type = 'LOPA'
	w.title = None
	w.description = None
	w.drawing_no = None
	w.drawing_rev = None
	w.aircraft_type = None
	w.no_lhs_seats = None
	w.no_rhs_seats = None
	w.seat_layout = {'LHS': [], 'RHS': []}
	#w.monuments = []
	w.lavs = []
	w.windbreakers = []
	w.galleys = []
	w.seat_item_nos = []
	
def update_variables(w, source):
	w.title = source.title
	w.description = source.description
	w.drawing_no = source.drawing_no
	w.drawing_rev = source.drawing_rev
	w.aircraft_type = source.aircraft_type
	w.no_lhs_seats = source.no_lhs_seats
	w.no_rhs_seats = source.no_rhs_seats
	w.seat_layout = copy.deepcopy(source.seat_layout)
	#w.monuments = copy.deepcopy(source.monuments)
	w.windbreakers = copy.deepcopy(source.windbreakers)
	w.lavs = copy.deepcopy(source.lavs)
	w.galleys = copy.deepcopy(source.galleys)
	w.seat_item_nos = copy.deepcopy(source.seat_item_nos)
	
	if w.aircraft_type == 'A320' or w.aircraft_type == 'A319':
		w.treeview_node = 'A320 LOPAs'

def set_default_monumnets(aircraft):

	default_lavs = {'A320': 
						[['Lav A', 'Yes', 278.6, 'Yes', 'No'],
						['Lav D', 'Yes', 1207.0, 'Yes', 'No'],
						['Lav E', 'Yes', 1207.0, 'Yes', 'No']],
					}
	
	default_galleys = {'A320':
							[['Galley 1', 'Yes', 278.6],
							['Galley 5', 'Yes', 1285.0]]
						}
	return default_lavs[aircraft], default_galleys[aircraft]
	
	
def process_boeing_station(aircraft_type,station):
	station = float(station)
	
	if aircraft_type == 'B737-800':
		if station < 522:
			tree_station = str(station)
		elif station >=522 and station < 718:
		
			plugs = {'500A': [522,544], '500B': [544,566], '500C': [566,588], '500D': [588,610],
						'500E': [610,632], '500F': [632,654], '500G': [654,676], '500H': [676,698], '500I': [698,718]}
			
			for plug in plugs.keys():
				if station >= plugs[plug][0] and station < plugs[plug][1]:
					tree_station = plug + '+ ' + str(round(station - plugs[plug][0],2)) + '" (' + str(station) + ')'
		
		elif station >= 718 and station < 747 + 198:
			tree_station = str(station - 198) + '" (' + str(station) + ')'
			
		elif station >= 747 + 198 and station < 1157:
			plugs = {'727A': [945,965], '727B': [965,985], '727C': [985,1007], '727D': [1007,1029],
						'727E': [1029,1051], '727F': [1051,1073], '727G': [1073,1095], '727H': [1095,1117], '727I': [1117,1137],
						'727J': [1137,1157]}
			for plug in plugs.keys():
				if station >= plugs[plug][0] and station < plugs[plug][1]:
					tree_station = plug + '+ ' + str(round(station - plugs[plug][0],2)) + '" (' + str(station) + ')'				
		elif station >= 1157:
			tree_station = str(station -410 ) + '" (' + str(station) + ')'
	return tree_station
		
def convert_station_to_float(station):
	'''
	Function to convert given station to float
	required as boeing stations may have parenthesis in them
	'''
	if '(' in str(station):
		station = float(station.split('(')[1].replace(')', ''))
	else:
		station = float(station)
	
	return station


def process_seat_stations_for_drawing(layout):

	'''
	For dxf, returns stations and pitches for seats in drawing
	'''
	stations = {'LHS': [], 'RHS': []}
	pitches = {'LHS': [], 'RHS': []}
	
	for side in ['LHS', 'RHS']:
		for index, row in enumerate(layout[side]):
			if index == 1:
				pitch = row[2]
				
			if index == 0:
				stations[side].append(row[3])
				
				count = 1
				
			elif index > 1:
				if row[2] != layout[side][index-1][2]:
					
					#if index-2 >0: #so we don't select first row
						
					avg = (layout[side][index-1][3] + stations[side][-1])/2
					stations[side].append(layout[side][index-1][3])
					
					pitches[side].append([avg, f'{count}x{pitch}"',float(stations[side][-2]), float(stations[side][-1])])
					
					count = 1
					pitch = row[2]
						
				else:
					count += 1
					
		
			#add final station
		
		reverse_layout = list(reversed(layout[side]))
		for index, row in enumerate(reverse_layout):
			
			found_pitch_change = False
			
			pitch = reverse_layout[index][2]
			station = reverse_layout[index][3]
			if index == 0:
				count = 1
				last_pitch = pitch
				last_station = station
				
			elif pitch != last_pitch:	
				
				found_pitch_change = True
				
				break
			count += 1
			
		avg = (station +last_station)/2
		stations[side].append(station)
		
		pitches[side].append([avg, f'{count}x{last_pitch}"', float(station), float(last_station)])	

	
		
	return stations, pitches
	
	

class LOPA_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		self.setup_lopa_plot()
		self.save_class = LOPA_Saved_State
		self.mainapp = self.parent_page.mainapp

		self.setup_lav_coords()

	def setup_lav_coords(self):

		self.lav_coords = {'A320': 
									{'Lav A': 278.6,
									'Lav D': 1207,
									'Lav E': 1207
									}
							}

		self.galley_coords = {'A320': 
									{'Galley 1': 278.6,
									'Galley 5': 1280,
									}
							}

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments
			
		return {'Title': self.title,
				'Description': self.description,
				'Drawing Number': self.drawing_no,
				'Drawing Rev': self.drawing_rev,
				'Aircraft Type': self.aircraft_type,
				'No LHS Seats': self.no_lhs_seats,
				'No RHS Seats': self.no_rhs_seats,
				'Seat Layout': self.seat_layout,
				'Lavs': self.lavs,
				'Galleys': self.galleys,
				'Windbreakers': self.windbreakers,
				'Seat Item Numbers': self.seat_item_nos,
				'Comments': comments
				}

	def recalculate_stations(self):
		
		for side in ('LHS', 'RHS'):
			for indx, row in enumerate(self.seat_layout[side]):

				if indx == 0:
					station = float(row[2])
				else:
					pitch = int(row[2])
					station += pitch
				if 'B737' in self.aircraft_type:
					station_text = process_boeing_station(self.aircraft_type, station)
					if '(' in station_text:
						station = float(station_text.split('(')[-1].replace(')', ''))
					else:
						station = float(station)
				
				elif self.aircraft_type in ['A320', 'A319']:
					station_text = station
				row[3] = station_text

		# for indx, row in enumerate(self.seat_layout['RHS']):

			# if indx == 0:
				# station = float(row[2])
			# else:
				# pitch = int(row[2])
				# station += pitch
			# if 'B737' in self.aircraft_type:
				# station = process_boeing_station(self.aircraft_type, station)
			# row[3] = station

	def find_overwing_seats(self):
		
		ow_rows = {'LHS': [], 'RHS': []}

		
		for station in [668.15, 701.5]:
			for side in ['LHS', 'RHS']:
				gaps = []
				abs_gaps = []
				
				
				for row in self.seat_layout[side]:

					gaps.append(station - float(row[3]))
					abs_gaps.append(abs(station - float(row[3])))
					
				abs_min_gap = min(abs_gaps)

				idx = abs_gaps.index(abs_min_gap)
				
				if idx not in ow_rows[side]:
					ow_rows[side].append(idx)
				if idx >0:
					if idx-1 not in ow_rows[side]:
						ow_rows[side].append(idx-1)
				if idx < len(self.seat_layout[side])-1:
					if idx+1 not in ow_rows[side]:
						ow_rows[side].append(idx+1)
				ow_rows[side] = sorted(ow_rows[side])
		return ow_rows
		
	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)

		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, LOPA_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, LOPA_Saved_State)
		update_variables(self, source)
		self.recalculate_stations()
		
	def setup_lopa_plot(self):
	
		self.lopa_figure = Figure(figsize=(5,5), dpi=100)
		self.ax1 = self.lopa_figure.add_subplot(311, aspect='equal', adjustable='box')
		self.ax2 = self.lopa_figure.add_subplot(111, aspect='equal', adjustable='box')
		self.ax3 = self.lopa_figure.add_subplot(313, aspect='equal', adjustable='box')
		
		self.lopa_figure.subplots_adjust(left=0.05, bottom=0.02, right=0.99, top=0.98, wspace=None, hspace=None)
		#self.ax1.title.set_text('Top-Down View')
		#self.ax2.title.set_text('Side Profile')
	
	def update_row_numbers(self, index, side, ref_row):
		
		count = 0
		for idx, row in enumerate(self.seat_layout[side]):
			if idx >= index:
				self.seat_layout[side][idx][0] = ref_row + count
				
				count += 1
		
	def get_all_row_numbers(self):

		row_numbers = {'LHS': [], 'RHS': []}

		for side in ['LHS', 'RHS']:
			for row in self.seat_layout[side]:
				row_numbers[side].append(row[0])
		return row_numbers

	def get_all_row_stations(self):

		row_stations = {'LHS': [], 'RHS': []}

		for side in ['LHS', 'RHS']:
			for row in self.seat_layout[side]:
				row_stations[side].append(float(row[3]))
		return row_stations

	def gen_parts_table(self):
	
		parts = [] #[qty, part_no, description]
		
		for side in ['LHS', 'RHS']:
			for row in self.seat_layout[side]:
				seat = row[1]
				seat_found = False
				
				for part in parts:
					if part[1] == seat:
						seat_found = True
						part[0] += 1
				
				if not seat_found:
					parts.append([1, seat, self.mainapp.frames[seat].backend.description])
		
		return parts

	def gen_ipc_table(self):

		ipc_table = []
		item_numbers = {}
		no_item_numbers = []
		processed_seats = []
		qtys = {}

		for side in ['LHS', 'RHS']:
			for row in self.seat_layout[side]:
				seat = row[1]

				if seat not in processed_seats:

					qtys[seat] = 1
					#try to find the item number for this seat
					found = False
					for s in self.seat_item_nos:
						if s[1] == seat:
							item_numbers[seat] = s[2]
							found = True
							
					if not found:
						no_item_numbers.append(seat)

					processed_seats.append(seat)
				else:
					qtys[seat] += 1
		#stitch all the data together
		for seat in item_numbers.keys():

			ipc_table.append([item_numbers[seat], seat, self.mainapp.frames[seat].backend.description, '', qtys[seat]])

		for seat in no_item_numbers:
			ipc_table.append(['', seat, self.mainapp.frames[seat].backend.description, '', qtys[seat]])

		return ipc_table
		
	def get_psu_rail_start_end(self):
		
		'''
		returns x, a nested list in format [[LHS Start, LHS End], [RHS Start, RHS End]]
		'''
		if self.aircraft_type == 'A320':
			
			lav_d = True
			lav_e = True
			
			x = []
			wb_installed = [False, False] #[LHS, RHS]
			
			start = [320, 320]
			
			for wb in self.windbreakers:
				side = self.mainapp.frames[wb[0]].backend.side
				if side == 'LHS':
					start[0] = float(wb[1])
					wb_installed[0] = True
				else:
					start[1] = float(wb[1])
					wb_installed[1] = True
					
			for lav in self.lavs:
				if lav[0] == 'Lav D' and lav[1] == 'No':
					lav_d = False
				if lav[0] == 'Lav E' and lav[1] == 'No':
					lav_e = False
			
				if lav_d:
					x.append([start[0],1207])
				else:
					x.append([start[0],1250.52])
					
				if lav_e:
					x.append([start[1],1207])
				else:
					x.append([start[1],1250.52])
			
			return x, lav_d, lav_e, wb_installed

	def gen_excel_data(self):

		excel_data = {'type': 'list', 'data': {}}

		#lopa layout

		data = []

		for row in self.seat_layout['LHS']:

			data.append(row)

		for idx, row in enumerate(self.seat_layout['RHS']):

			if idx >= len(data):

				data.append(['', '', '', ''])

			for r in row:
				data[idx].append(r)


		excel_data['data']['Seat Layout'] = data

		return excel_data

class LOPA_Saved_State():
	def __init__(self, lopa):
	
		setup_variables(self)
		update_variables(self, lopa)