
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import copy

def setup_variables(w):
	w.type = 'EEL'
	w.title = None
	w.aircraft_type = None
	w.description = None
	w.lopa = None
	w.ohsc = None
	w.locations = ['Cockpit']
	w.layout = {'Cockpit': []}
	w.summary = {}
	w.summary_table = []

def update_variables(self, source):
	self.title = source.title
	self.aircraft_type = source.aircraft_type
	self.description = source.description	
	self.lopa = source.lopa
	self.ohsc = source.ohsc
	self.locations = copy.deepcopy(source.locations)
	self.layout = copy.deepcopy(source.layout)
	self.summary = copy.deepcopy(source.summary)
	self.summary_table = copy.deepcopy(source.summary_table)

	EEL_Backend.gen_summary_dict(self)
	EEL_Backend.gen_summary_table(self)

	if source.aircraft_type in ['A320']:
		self.treeview_node = 'A320 EELs'
		
class EEL_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		self.setup_plot()
		self.save_class = EEL_Saved_State
		self.mainapp = self.parent_page.mainapp
		
		
	def update_component(self, source, type, reset_redo = True):
		#pass current joint through to state class (for undo redo)

		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, EEL_Saved_State, reset_redo)
		elif type == 'new':
			self.controller.states.component_updated(type, self, EEL_Saved_State, reset_redo)
			
		update_variables(self, source)

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments

		return {'Title': self.title,
				'Description': self.description,
				'Aircraft Type': self.aircraft_type,
				'LOPA': self.lopa,
				'OHSC': self.ohsc,
				'Locations': self.locations,
				'Layout': self.layout,
				'Summary': self.summary,
				'Summary Table': self.summary_table,
				'Comments': comments}
				
	def setup_plot(self):
	
		self.lopa_figure = Figure(figsize=(5,5), dpi=100)
		self.ax1 = self.lopa_figure.add_subplot(311, aspect='equal', adjustable='box')
		
	def gen_summary_dict(self):
		
		self.summary = {}
		for loc in self.layout.keys():
			
			for part in self.layout[loc]:
				item_type = part[0]
				part_no = part[1]
				if item_type not in self.summary.keys():
					self.summary[item_type] = {}
				if part_no not in self.summary[item_type].keys():
					self.summary[item_type][part_no] = int(part[3])
				else:
					self.summary[item_type][part_no] += int(part[3])
	
					
	def gen_summary_table(self):
		self.summary_table = []

		summary_dict = {}
		items = []

		index = 0
		
		for loc in self.layout:

			for item in self.layout[loc]:
				item_type = item[0]
				pn = item[1]
				qty = int(item[3])

				if item_type not in summary_dict.keys():
					summary_dict[item_type] = {}
					summary_dict[item_type][pn] = qty
				else:
					if pn not in summary_dict[item_type].keys():
						summary_dict[item_type][pn] = qty
					else:
						summary_dict[item_type][pn] += qty

		for item_type in summary_dict.keys():

			total_qty = 0
			
			for pn in summary_dict[item_type]:
				
				total_qty += summary_dict[item_type][pn]

			self.summary_table.append([item_type, '', total_qty])

			for pn in summary_dict[item_type]:
				self.summary_table.append(['', pn, summary_dict[item_type][pn]])

	def get_item_locations(self, item_to_find, part_no=None):
		#get all locations where an item is found
		# if part_no is None, will return all part numbers for that item type

		locations = []

		for loc in self.layout:
			for item in self.layout[loc]:
				item_type = item[0]

				if item_type == item_to_find:
					if not part_no:
						locations.append(loc)
					else:
						if item[1] == part_no:
							locations.append(loc)

		return locations

	def get_item_part_no_by_location(self, item_to_find):

		# returns dict (locations are keys) showing all part numbers for a given item in that location

		item_part_numbers = {}

		for loc in self.layout:
			for item in self.layout[loc]:
				if item[0]==item_to_find:

					part_no = item[1]
					if loc in item_part_numbers.keys():
						pass
					else:
						item_part_numbers[loc] = {}
					
					item_part_numbers[loc][part_no] = int(item[3])
		return item_part_numbers

	def get_total_qty_item_per_location(self, item_to_find):

		# returns dict (locations are keys) showing total qty for a given item in that location
		# e.g. {'Cockpit': 1} 

		item_part_numbers = {}

		for loc in self.layout:
			for item in self.layout[loc]:
				if item[0]==item_to_find:

					part_no = item[1]
					if loc in item_part_numbers.keys():
						pass
					else:
						item_part_numbers[loc] = 0
					
					item_part_numbers[loc] += int(item[3])
		return item_part_numbers	

	def count_items(self):
		'''
		Counts the different item types e.g. {crash axe: 1, lifevest: 2, etc}
		'''
		item_count = {}
		
		for loc in self.layout:
			for part in self.layout[loc]:
				item_type = part[0]
				
				if item_type not in item_count.keys():
					item_count[item_type] = int(part[3])
				else:
					item_count[item_type] += int(part[3])
					
		return item_count

	def count_part_nos(self):

		'''
		Counts the different part nos e.g. {pn1: 1, pn2: 2, etc}
		'''
		pn_count = {}
		
		for loc in self.layout:
			for part in self.layout[loc]:
				part_no = part[1]
				
				if part_no not in pn_count.keys():
					pn_count[part_no] = int(part[3])
				else:
					pn_count[part_no] += int(part[3])
					
		return pn_count	
		
		
	def compare_eels(self, current_eel):
		# self should refer to the go to eel
		# other eel should refer to the backend object
		item_comparison = []
		parts_comparison = []
			
		# Item Type Comparison
		item_count_go_to = self.count_items()
		item_count_current = current_eel.count_items()
		
		for item in item_count_go_to.keys():
			goto_qty = item_count_go_to[item]
			
			if item in item_count_current.keys():
				current_qty = item_count_current[item]
				delta = current_qty - goto_qty
			else:
				current_qty = 0
				delta = goto_qty*-1
			item_comparison.append([item, current_qty, goto_qty, delta])
		
		# add any current items not in go to
		for item in item_count_current.keys():
			if item not in item_count_go_to.keys():
				current_qty = item_count_current[item]
				item_comparison.append([item, current_qty, '-', '-'])
		
		# Part Number Comparison
		item_count_go_to = self.count_part_nos()
		item_count_current = current_eel.count_part_nos()
		
		for item in item_count_go_to.keys():
			goto_qty = item_count_go_to[item]
			
			if item in item_count_current.keys():
				current_qty = item_count_current[item]
				delta = current_qty - goto_qty
			else:
				current_qty = 0
				delta = goto_qty*-1
				
			#get item type
			type = self.mainapp.frames[item].backend.equipment_type
			parts_comparison.append([item, type, current_qty, goto_qty, delta])
		
		return item_comparison, parts_comparison
		
class EEL_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)