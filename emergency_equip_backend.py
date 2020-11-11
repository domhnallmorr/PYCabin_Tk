import copy

def setup_variables(w):
	w.type = 'Emergency Equipment'
	w.title = None
	w.description = None
	w.aircraft_type = None
	w.equipment_type = None
	w.aircraft_type = None
	w.manufacturer = None
	w.attaching_hardware = []
	w.weight= 0

	w.available_equipment= ['Crash Axe', 'ELT', 'Fire Extinguisher', 'Flashlight', 'Life Vest', 'Life Vest Crew', 'Life Vest Infant',
							'Manual Release Tool', 'Megaphone', 'PBE']	

def update_variables(w, source):

	w.title = source.title
	w.description = source.description
	w.aircraft_type = source.aircraft_type
	w.equipment_type = source.equipment_type
	w.attaching_hardware = copy.deepcopy(source.attaching_hardware)
	w.weight = source.weight
	w.manufacturer = source.manufacturer

	if w.aircraft_type in ['A320', 'A319']:
		w.treeview_node = 'A320 EE'
	
class Emergency_Equip_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)

		self.save_class = Emergency_Equip_Saved_State
		self.mainapp = self.parent_page.mainapp

	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, Emergency_Equip_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, Emergency_Equip_Saved_State)
		update_variables(self, source)		

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments

		return {'Title': self.title,
				'Description': self.description,
				'Aircraft Type': self.aircraft_type,
				'Equipment Type': self.equipment_type,
				'Attaching Hardware': self.attaching_hardware,
				'Weight': self.weight,
				'Manufacturer': self.manufacturer,
				'Comments': comments}
		
class Emergency_Equip_Saved_State():
	def __init__(self, emergency_equip):
	
		setup_variables(self)
		update_variables(self, emergency_equip)
		
		
	