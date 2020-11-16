
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

	if source.aircraft_type == 'A320':
		self.treeview_node = 'A320 EELs'
		
class EEL_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		self.setup_plot()
		self.save_class = EEL_Saved_State
		self.mainapp = self.parent_page.mainapp
		
		
	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, EEL_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, EEL_Saved_State)
			
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
		index = 0
		
		for item in self.summary.keys():
			
			self.summary_table.append([item, '', 0])
			idx = len(self.summary_table)-1
			for part in self.summary[item].keys():
				self.summary_table.append(['', part, self.summary[item][part]])

				self.summary_table[idx][2] += self.summary[item][part]
class EEL_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)