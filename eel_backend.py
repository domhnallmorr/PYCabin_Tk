
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




class EEL_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)