import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import copy


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
	w.monuments = []
	
def update_variables(w, source):
	w.title = source.title
	w.description = source.description
	w.drawing_no = source.drawing_no
	w.drawing_rev = source.drawing_rev
	w.aircraft_type = source.aircraft_type
	w.no_lhs_seats = source.no_lhs_seats
	w.no_rhs_seats = source.no_rhs_seats
	w.seat_layout = copy.deepcopy(source.seat_layout)
	w.monuments = copy.deepcopy(source.monuments)
	
	if w.aircraft_type == 'A320' or w.aircraft_type == 'A319':
		w.treeview_node = 'A320 LOPAs'
		
def process_boeing_station(aircraft_type,station):
	station = float(station)
	print(station)
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
	for index, row in enumerate(layout['LHS']):
		if index == 1:
			pitch = row[2]
			
		if index == 0:
			stations['LHS'].append(row[3])
			
			count = 1

			
		elif index > 1:
			if row[2] != layout['LHS'][index-1][2]:
				
				#if index-2 >0: #so we don't select first row
					
				avg = (layout['LHS'][index-1][3] + stations['LHS'][-1])/2
				stations['LHS'].append(layout['LHS'][index-1][3])
				
				pitches['LHS'].append([avg, f'{count}x{pitch}"', float(layout['LHS'][index-1][3]), float(stations['LHS'][-1])])
				
				count = 1
				pitch = row[2]
					
			else:
				count += 1
		#add final station
	avg = (layout['LHS'][index][3] + stations['LHS'][-1])/2
	stations['LHS'].append(layout['LHS'][index][3])
	
	pitches['LHS'].append([avg, f'{count}x{pitch}"', float(layout['LHS'][index-1][3]), float(stations['LHS'][-1])])		

	return stations, pitches
class LOPA_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		self.setup_lopa_plot()
		self.save_class = LOPA_Saved_State
		self.mainapp = self.parent_page.mainapp
		
	def gen_save_dict(self):
	
		return {'Title': self.title,
				'Description': self.description,
				'Drawing Number': self.drawing_no,
				'Drawing Rev': self.drawing_rev,
				'Aircraft Type': self.aircraft_type,
				'No LHS Seats': self.no_lhs_seats,
				'No RHS Seats': self.no_rhs_seats,
				'Seat Layout': self.seat_layout,
				'Monuments': self.monuments}

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
		
		self.lopa_figure.subplots_adjust(left=0.05, bottom=None, right=0.99, top=None, wspace=None, hspace=None)
		#self.ax1.title.set_text('Top-Down View')
		#self.ax2.title.set_text('Side Profile')
	
	def update_row_numbers(self, index, side, ref_row):
		
		count = 0
		for idx, row in enumerate(self.seat_layout[side]):
			if idx >= index:
				self.seat_layout[side][idx][0] = ref_row + count
				
				count += 1
		
class LOPA_Saved_State():
	def __init__(self, aircraft):
	
		setup_variables(self)
		update_variables(self, aircraft)

	
	