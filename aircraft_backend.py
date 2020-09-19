

class Aircraft_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		self.setup_variables()
		
	def setup_variables(self):
		
		self.title = None
		self.type = 'Aircraft'
		self.aircraft_type = None
		self.msn = None
		self.current_operator = None
		self.go_to_operator = None
		self.go_to_lopa = None
		
		#AMM
		self.seats_instl_task = ''
		self.seats_uninstl_task = ''
		
		self.treeview_node = None
		
		self.save_class = Aircraft_Saved_State
	def update_variables(self, source):

		self.title = source.msn
		self.msn = source.msn
		self.aircraft_type =source.aircraft_type
		self.current_operator =source.current_operator
		self.go_to_operator =source.go_to_operator

		if self.aircraft_type == 'A320' or self.aircraft_type == 'A319':
			self.treeview_node = 'A320 Aircraft'
		elif self.aircraft_type == 'B737-800':
			self.treeview_node = '737 Aircraft'
		
		self.seats_uninstl_task = source.seats_uninstl_task
		self.seats_instl_task = source.seats_instl_task

		
		
	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, Aircraft_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, Aircraft_Saved_State)
			
		self.update_variables(source)
	
	def gen_save_dict(self):
	
		return {'Title': self.title,
				'MSN': self.msn,
				'Aircraft Type': self.aircraft_type,
				'Current Operator': self.current_operator,
				'Go To Operator': self.go_to_operator,
				'Seat Removal Task': self.seats_uninstl_task,
				'Seat Installation Task': self.seats_instl_task,
				'Comments': self.parent_page.comment_text.get("1.0","end")
				}
class Aircraft_Saved_State():
	def __init__(self, aircraft):
	
		Aircraft_Backend.setup_variables(self)
		Aircraft_Backend.update_variables(self, aircraft)
		
	