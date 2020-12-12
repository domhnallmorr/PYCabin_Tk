
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
		
	def export_excel(self):
	
		wb = openpyxl.Workbook()
		
		sheet_styles = excel_functions.setup_styles()
		#Current EEL
		
		wb.create_sheet(index=1, title=('Current EEL'))
		wb.active = 1
		sheet = wb.active
		
		data = self.mainapp.frames[self.current_eel].backend.compile_data_for_excel()
		excel_functions.add_data_to_sheet(wb, sheet, data, 1, 1, sheet_styles['Normal'])
		
		#GoTo EEL

		wb.create_sheet(index=2, title=('Go To EEL'))
		wb.active = 2
		sheet = wb.active
		
		data = self.mainapp.frames[self.go_to_eel].backend.compile_data_for_excel()
		excel_functions.add_data_to_sheet(wb, sheet, data, 1, 1, sheet_styles['Normal'])
		
		#Comparison By Item
		
		wb.create_sheet(index=3, title=('Comparison by Item'))
		wb.active = 3
		sheet = wb.active		
		
		data = treeview_functions.get_all_treeview_items(self.parent_page.comp_item_tree)
		data.insert(0, ['Item', 'Current Qty', 'Go To Qty', 'Delta'])
		excel_functions.add_data_to_sheet(wb, sheet, data, 1, 1, sheet_styles['Normal'])
		
		#Comparison By Part
		wb.create_sheet(index=4, title=('Comparison by Part No'))
		wb.active = 4
		sheet = wb.active		
		
		data = treeview_functions.get_all_treeview_items(self.parent_page.comp_part_tree)
		data.insert(0, ['Part Number', 'Item', 'Current Qty', 'Go To Qty', 'Delta'])
		excel_functions.add_data_to_sheet(wb, sheet, data, 1, 1, sheet_styles['Normal'])
		
		#Final Layout
		wb.create_sheet(index=5, title=('Final Layout'))
		wb.active = 5
		sheet = wb.active


		data = [['Item', 'Part Number', 'Location', 'Qty', 'Existing/New']]

		for loc in self.layout.keys():
			for part in self.layout[loc]:
				data.append(part)
		excel_functions.add_data_to_sheet(wb, sheet, data, 1, 1, sheet_styles['Normal'])

		#BOM
		print(self.bom)

		wb.create_sheet(index=6, title=('BOM'))
		wb.active = 6
		sheet = wb.active

		data = [['Part Number', 'Item', 'Qty']]	

		for part in self.bom.keys():
			item = self.mainapp.frames[part].backend.equipment_type
			data.append([part, item, self.bom[part]])

		excel_functions.add_data_to_sheet(wb, sheet, data, 1, 1, sheet_styles['Normal'])

		#wb.save(r'C:\Users\domhnall.morrisey.WOODGROUP\Downloads\PYCabin_Tk-master\PYCabin_Tk-master\eel.xlsx')
		wb.save(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.14\eel.xlsx')
		
class EEL_Comparison_Saved_State():
	def __init__(self, ohsc):

		setup_variables(self)
		update_variables(self, ohsc)