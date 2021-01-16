
import copy

import openpyxl
import excel_functions
import treeview_functions


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
	w.equip_item_nos = []

def update_variables(self, source):
	self.title = source.title
	self.aircraft_type = source.aircraft_type
	self.description = source.description	
	self.current_eel = source.current_eel
	self.go_to_eel = source.go_to_eel
	#self.locations = copy.deepcopy(source.locations)
	self.layout = copy.deepcopy(source.layout)
	self.instructions = copy.deepcopy(source.instructions)
	self.bom = copy.deepcopy(source.bom)
	self.equip_item_nos = copy.deepcopy(source.equip_item_nos)

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
				'BOM': self.bom,
				'Item Numbers': self.equip_item_nos,
				'Comments': comments}

	def gen_bom(self):
	
		pass
		
	def gen_excel_data(self):
		
		excel_data = {'type': 'list', 'data': {}}

		#Current EEL
		if self.current_eel:
			excel_data['data']['Current EEL'] = self.mainapp.frames[self.current_eel].backend.compile_data_for_excel()
	
		#GoTo EEL

		excel_data['data']['Go To EEL'] =  self.mainapp.frames[self.go_to_eel].backend.compile_data_for_excel()

		
		#Comparison By Item		
		excel_data['data']['Comparison by Item'] =  treeview_functions.get_all_treeview_items(self.parent_page.comp_item_tree)
		excel_data['data']['Comparison by Item'].insert(0, ['Item', 'Current Qty', 'Go To Qty', 'Delta'])
		
		#Comparison By Part	
		
		excel_data['data']['Comparison by Part No'] =  treeview_functions.get_all_treeview_items(self.parent_page.comp_part_tree)
		excel_data['data']['Comparison by Part No'].insert(0, ['Part Number', 'Item', 'Current Qty', 'Go To Qty', 'Delta'])

		
		#Final Layout

		excel_data['data']['Final Layout'] = [['Item', 'Part Number', 'Location', 'Qty', 'Existing/New']]

		for loc in self.layout.keys():
			for part in self.layout[loc]:
				excel_data['data']['Final Layout'].append(part)


		#Item Numbers
		excel_data['data']['Item Numbers']= self.equip_item_nos

		#BOM
		excel_data['data']['BOM'] = [['Part Number', 'Item', 'Qty']]	

		for part in self.bom.keys():
			item = self.mainapp.frames[part].backend.equipment_type
			excel_data['data']['BOM'].append([part, item, self.bom[part]])

		return excel_data
	def gen_parts_table(self):
		parts_table = []

		item_number = 1

		for p in self.bom:
			parts_table.append([self.bom[p], p, self.mainapp.frames[p].backend.description])

			item_number += 1

			#add attaching hardware
			part=self.mainapp.frames[p].backend
			for a in part.attaching_hardware:
				qty = int(a[3])*self.bom[part.title]

				parts_table.append([qty, a[2], a[1]])
				item_number += 1

		return parts_table


	def gen_ipc_table(self):

		ipc_table = []

		item_number = 1

		for p in self.bom:
			ipc_table.append([item_number, p, self.mainapp.frames[p].backend.description, '', self.bom[p]])

			item_number += 1

			#add attaching hardware
			part=self.mainapp.frames[p].backend
			for a in part.attaching_hardware:
				qty = int(a[3])*self.bom[part.title]

				ipc_table.append([item_number, a[2], a[1], '', qty])
				item_number += 1

		return ipc_table	

	def get_part_item_number(self, part):

		item_number = None

		for i in self.equip_item_nos:
			if i[0] == part:
				item_number = i[1]
				break

		return item_number	

	def combine_existing_new_items(self, loc):

		#for a given location, combine qtys of existing and new items
		qtys = {}
		if loc in self.layout.keys():
			for part in self.layout[loc]:
				if part[1] not in qtys.keys():
					qtys[part[1]] = int(part[3])
				else:
					qtys[part[1]] += int(part[3])

		return qtys

		
class EEL_Comparison_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)