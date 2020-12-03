
import copy

def setup_variables(w):
	w.type = 'EEL Comparison'
	w.title = None
	w.aircraft_type = None
	w.description = None
	w.current_eel = None
	w.go_to_eel = None
	w.bom = {}
	w.layout = {}
	w.instructions = []

def update_variables(self, source):
	self.title = source.title
	self.aircraft_type = source.aircraft_type
	self.description = source.description	
	self.current_eel = source.current_eel
	self.go_to_eel = source.go_to_eel
	#self.locations = copy.deepcopy(source.locations)
	self.layout = copy.deepcopy(source.layout)
	self.instructions = copy.deepcopy(source.instructions)

	#EEL_Backend.gen_summary_dict(self)
	#EEL_Backend.gen_summary_table(self)

	if source.aircraft_type in ['A320']:
		self.treeview_node = 'A320 EEL Comparisons'

class EEL_Comparison_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)
		
		self.save_class = EEL_Comparison_Saved_State
		self.mainapp = self.parent_page.mainapp
		
		
	def update_component(self, source, type, reset_redo = True):
		#pass current joint through to state class (for undo redo)

		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, EEL_Comparison_Saved_State, reset_redo)
		elif type == 'new':
			self.controller.states.component_updated(type, self, EEL_Comparison_Saved_State, reset_redo)
			
		update_variables(self, source)

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments

		return {'Title': self.title,
				'Description': self.description,
				'Aircraft Type': self.aircraft_type,
				'Current EEL': self.current_eel,
				'GoTo EEL': self.go_to_eel,
				'Layout': self.layout,
				'Instructions': self.instructions,
				'Comments': comments}

	def gen_bom(self):
	
		pass
class EEL_Comparison_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)