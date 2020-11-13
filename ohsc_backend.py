
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import copy

def setup_variables(w):
	w.type = 'OHSC'
	w.title = None
	w.aircraft_type = None
	w.description = None
	w.layout = {'LHS': [], 'RHS': []}

def update_variables(self, source):
	self.title = source.title
	self.aircraft_type = source.aircraft_type
	self.description = source.description	
	self.layout = copy.deepcopy(source.layout)

	if self.aircraft_type in ['A320', 'A319']:
		self.treeview_node = 'A320 OHSCs'

class OHSC_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		self.setup_plot()
		self.save_class = OHSC_Saved_State
		self.mainapp = self.parent_page.mainapp
		
		
	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, OHSC_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, OHSC_Saved_State)
			
		update_variables(self, source)

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments

		return {'Title': self.title,
				'Description': self.description,
				'Aircraft Type': self.aircraft_type,
				'Layout': self.layout,
				'Comments': comments}
				
	def setup_plot(self):
	
		self.lopa_figure = Figure(figsize=(5,3), dpi=100)
		self.ax1 = self.lopa_figure.add_subplot(111, aspect='equal', adjustable='box')
		
		self.lopa_figure.subplots_adjust(left=0.05, bottom=0.02, right=0.99, top=0.98, wspace=None, hspace=None)

class OHSC_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)