import copy

def setup_variables(w):
	w.type = 'Emergency_Equip'
	w.title = None
	w.description = None
	w.equipment_type = None
	w.aircraft_type = None
	w.attaching_hardware = []
	w.weight= 0
	

def update_variables(w, source):
	w.title = source.title
	w.description = source.description
	w.equipment_type = source.equipment_type
	w.attaching_hardware = source.attaching_hardware
	w.weight = source.weight
	
	w.available_equipment= ['Crash Axe', 'ELT', 'Fire Extinguisher', 'Flashlight', 'Life Vest', 'Life Vest Crew', 'Life Vest Infant',
							'Manual Release Tool', 'Megaphone', 'PBE']
	
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
		
class Emergency_Equip_Saved_State():
	def __init__(self, emergency_equip):
	
		setup_variables(self)
		update_variables(self, emergency_equip)
		
		
	