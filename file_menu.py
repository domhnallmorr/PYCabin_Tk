import json
import tkinter.messagebox

import components_tk
import comment_box
import word_export
from tkinter.filedialog import askopenfilename, asksaveasfilename

import os

def new_project(event=None, mainapp=None):
	
	if mainapp.done_something == True:
		msg = check_clear_project(mainapp)
	else:
		msg = True
	
	if msg:
		#mainapp.frames['Project'].clear_project_data()
		
		components = components_tk.get_all_components(mainapp, 'all')
		
		for component in components['All']:
			component = mainapp.frames[component]
			mainapp.main_treeview.delete(component.treeview_iid)
			del mainapp.frames[component.backend.title]
			
	components_tk.show_frame(mainapp, 'Project')

	return msg

def check_clear_project(mainapp):

	if len(mainapp.frames.keys()) > mainapp.no_of_default_pages-1: 
		msg = tkinter.messagebox.askokcancel(title='Create New Project', message='Any Unsaved Data Will Be Lost, This Cannot Be Undone, Do You Want To Continue?')
	else:
		msg = False

	return msg	
	
def save(event=None, mainapp=None):

	if mainapp.save_file == None:
		save_as(mainapp = mainapp)
	else:
		write_save_file(mainapp)

def save_as(event=None, mainapp=None):

	#mainapp.save_file = r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.21\test.json'
	filename = asksaveasfilename(filetypes=[('JSON files', '*.json')])

	if filename[-5:] != '.json':
		filename = f'{filename}.json'

	msg = check_filename(filename, 'save')

	if not msg:
		mainapp.save_file = filename
		write_save_file(mainapp)
	else:
		tkinter.messagebox.showerror(master=mainapp, title='Error', message=msg)
	
def write_save_file(mainapp):


	save_dict = {'Project': mainapp.frames['Project'].backend.gen_save_dict(), 'Aircraft': [], 'Seats': [],
					'Windbreakers': [], 'LOPAs': [], 'PSUs': [], 'OHSCs': [], 'Emergency Equipment': [], 'EELs': [],
					'EEL Comparisons': []}
	
	# _________________ AIRCRAFT _________________
	# ac_dict = components_tk.get_all_components(mainapp, 'Aircraft')
	# for a in ac_dict['All']:
		# save_dict['Aircraft'].append(mainapp.frames[a].backend.gen_save_dict())	
	
	# _________________ SEATS _________________
	seats_dict = components_tk.get_all_components(mainapp, 'Seats')
	
	for s in seats_dict['All']:
		save_dict['Seats'].append(mainapp.frames[s].backend.gen_save_dict())
	
	# _________________ WINDBREAKERS _________________
	wb_dict = components_tk.get_all_components(mainapp, 'Windbreakers')

	for w in wb_dict['All']:
		save_dict['Windbreakers'].append(mainapp.frames[w].backend.gen_save_dict())

	# _________________ LOPAS _________________
	lopa_dict = components_tk.get_all_components(mainapp, 'LOPAs')

	for l in lopa_dict['All']:
		save_dict['LOPAs'].append(mainapp.frames[l].backend.gen_save_dict())

	# _________________ PSUs _________________
	psu_dict = components_tk.get_all_components(mainapp, 'PSUs')

	for p in psu_dict['All']:
		save_dict['PSUs'].append(mainapp.frames[p].backend.gen_save_dict())

	# _________________ OHSCs _________________
	ohsc_dict = components_tk.get_all_components(mainapp, 'OHSCs')

	for o in ohsc_dict['All']:
		save_dict['OHSCs'].append(mainapp.frames[o].backend.gen_save_dict())

	# _________________ Emergency Equipment _________________
	ee_dict = components_tk.get_all_components(mainapp, 'Emergency Equipment')

	for e in ee_dict['All']:
		save_dict['Emergency Equipment'].append(mainapp.frames[e].backend.gen_save_dict())

	# _________________ EELs _________________
	eel_dict = components_tk.get_all_components(mainapp, 'EELs')

	for e in eel_dict['All']:
		save_dict['EELs'].append(mainapp.frames[e].backend.gen_save_dict())

	# _________________ EEL Comparisons _________________
	eel_dict = components_tk.get_all_components(mainapp, 'EEL Comparisons')

	for e in eel_dict['All']:
		save_dict['EEL Comparisons'].append(mainapp.frames[e].backend.gen_save_dict())

	# _________________ Changes _________________
	# change_dict = components_tk.get_all_components(mainapp, 'Changes')

	# for c in change_dict['All']:
		# save_dict['Changes'].append(mainapp.frames[c].backend.gen_save_dict())
		
	with open(mainapp.save_file, 'w') as outfile:
		json.dump(save_dict, outfile, indent=4)
		

	mainapp.update_titlebar('save')

def check_filename(filename, mode):

	msg = None

	if mode == 'load':
		#check file exists
		if not os.path.isfile(filename):
			msg = f'File Not Found'

	#check file is .json
	if not msg:
		if filename[-5:].lower() != '.json':
			msg = 'File Extension Must be .json'

	return msg

def load(event=None, mainapp=None):


	filename = askopenfilename(filetypes=[('JSON files', '*.json')])

	if filename != '':

		msg = check_filename(filename, 'load')

		#load the file
		if not msg:
			#check if we have to clear the existing project
			msg = new_project(event, mainapp)

			if msg:
				load_file(filename, event, mainapp)

				mainapp.save_file = filename
				mainapp.update_titlebar('save')
		else:
			tkinter.messagebox.showerror(master=mainapp, title='Error', message=msg)


def load_file(file, event=None, mainapp=None):

	#with open(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.21\test.json') as f:
	with open(file) as f:
	#with open(r'C:\Users\domhnall.morrisey.WOODGROUP\Downloads\PYCabin_Tk-master\PYCabin_Tk-master\test.json') as f:
		data = json.load(f)
		
	# ______ Project _________________
	if 'Project' in data.keys():
		pass
		mainapp.frames['Project'].load_project_data(data['Project'])
	
	if 'Aircraft' in data.keys():
	
		for ac in data['Aircraft']:
			ac = Load('Aircraft', ac)
			components_tk.create_component(mainapp, 'Aircraft', ac, 'new')
			comment_box.insert_comments_text(mainapp.frames[ac.title].comment_text, ac.comments) 
			
	if 'Seats' in data.keys():
	
		for seat in data['Seats']:
			seat = Load('Seat', seat)
			components_tk.create_component(mainapp, 'Seat', seat, 'new')
			comment_box.insert_comments_text(mainapp.frames[seat.title].comment_text, seat.comments)
			
	if 'Windbreakers' in data.keys():
		
		for wb in data['Windbreakers']:
			wb = Load('Windbreaker', wb)
			components_tk.create_component(mainapp, 'Windbreaker', wb, 'new')
			comment_box.insert_comments_text(mainapp.frames[wb.title].comment_text, wb.comments)
			
	if 'LOPAs' in data.keys():
		
		for l in data['LOPAs']:
			l = Load('LOPA', l)
			components_tk.create_component(mainapp, 'LOPA', l, 'new')
			comment_box.insert_comments_text(mainapp.frames[l.title].comment_text, l.comments)

	if 'PSUs' in data.keys():
		
		for p in data['PSUs']:
			p = Load('PSU', p)
			components_tk.create_component(mainapp, 'PSU', p, 'new')
			comment_box.insert_comments_text(mainapp.frames[p.title].comment_text, p.comments)

	if 'OHSCs' in data.keys():
		
		for o in data['OHSCs']:
			o = Load('OHSC', o)
			components_tk.create_component(mainapp, 'OHSC', o, 'new')
			comment_box.insert_comments_text(mainapp.frames[o.title].comment_text, o.comments)

	if 'Emergency Equipment' in data.keys():
		
		for p in data['Emergency Equipment']:
			p = Load('Emergency Equipment', p)
			components_tk.create_component(mainapp, 'Emergency Equipment', p, 'new')
			comment_box.insert_comments_text(mainapp.frames[p.title].comment_text, p.comments)

	if 'EELs' in data.keys():
		
		for p in data['EELs']:
			p = Load('EEL', p)
			components_tk.create_component(mainapp, 'EEL', p, 'new')
			comment_box.insert_comments_text(mainapp.frames[p.title].comment_text, p.comments)

	if 'EEL Comparisons' in data.keys():
		
		for p in data['EEL Comparisons']:
			p = Load('EEL Comparison', p)
			components_tk.create_component(mainapp, 'EEL Comparison', p, 'new')
			comment_box.insert_comments_text(mainapp.frames[p.title].comment_text, p.comments)

	if 'Changes' in data.keys():
		
		for l in data['Changes']:
			l = Load('Change', l)
			components_tk.create_component(mainapp, 'Change', l, 'new')
			comment_box.insert_comments_text(mainapp.frames[l.title].comment_text, l.comments)			
	# reset undo and redo stacks
	mainapp.states.reset(undo=True, redo=True)
	
	
class Load():
	def __init__(self, type, component_data):
		
		self.update_variables(type, component_data)

	def update_variables(self, type, component_data):
	
		if type == 'Aircraft':
		
			self.title = component_data["Title"]
			self.msn = component_data["MSN"]
			self.aircraft_type = component_data["Aircraft Type"]
			self.current_operator = component_data["Current Operator"]
			self.go_to_operator = component_data["Go To Operator"]
			self.seats_uninstl_task = component_data["Seat Removal Task"]
			self.seats_instl_task = component_data["Seat Installation Task"]
			self.comments = component_data["Comments"]	
			
		if type == 'Seat':
			
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]
			self.part_no = component_data["Part Number"]
			self.manufacturer = component_data["Manufacturer"]
			self.side = component_data["Side"]
			self.seat_type = component_data["Seat Type"]
			self.iat = component_data["IAT"]
			self.profile = component_data["Profile"]
			self.width = component_data["Width"]
			self.width_inbd = component_data["Width Inbd"]
			self.armrest_width = component_data["Armrest Width"]
			self.length_fwd = component_data["Length Fwd"]
			self.length_aft = component_data["Length Aft"]
			self.cushion_height = component_data["Cushion Height"]
			self.height = component_data["Height"]
			self.stud_distance = component_data["Stud Distance"]
			self.srp_x = component_data["SRP X"]
			self.srp_y = component_data["SRP Y"]
			self.weight_lbs = component_data["Weight"]
			self.cmm_title = component_data["CMM Title"]
			self.cmm_ref = component_data["CMM Reference"]
			self.cmm_version = component_data["CMM Version"]
			self.cmm_date = component_data["CMM Date"]
			self.cmm_install = component_data["CMM Install"]
			self.comments = component_data["Comments"]	
			
		if type == 'Windbreaker':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]
			self.part_no = component_data["Part Number"]
			self.side = component_data["Side"]
			self.thickness = component_data["Thickness"]
			self.width = component_data["Width"]
			self.height = component_data["Height"]
			self.dist_from_cl = component_data["Dist From C/L"]
			self.joggle = component_data["Joggle"]
			self.joggle_width = component_data["Joggle Width"]
			self.joggle_lower = component_data["Joggle Lower"]
			self.joggle_upper = component_data["Joggle Upper"]
			self.bassinet = component_data["Bassinet"]
			self.cmm_title = component_data["CMM Title"]
			self.cmm_ref = component_data["CMM Reference"]
			self.cmm_version = component_data["CMM Version"]
			self.cmm_date = component_data["CMM Date"]
			self.cmm_install = component_data["CMM Install"]
			self.cmm_remove = component_data["CMM Remove"]
			self.comments = component_data["Comments"]		
			
		if type == 'LOPA':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]			
			self.drawing_no = component_data["Drawing Number"]
			self.drawing_rev = component_data["Drawing Rev"]
			self.no_lhs_seats = component_data["No LHS Seats"]
			self.no_rhs_seats = component_data["No RHS Seats"]
			self.seat_layout = component_data["Seat Layout"]
			self.lavs = component_data["Lavs"]
			self.galleys = component_data["Galleys"]
			self.windbreakers = component_data["Windbreakers"]
			self.seat_item_nos = component_data["Seat Item Numbers"]
			self.comments = component_data["Comments"]

		if type == 'PSU':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]			
			self.lopa = component_data["LOPA"]
			self.drawing_no = component_data["Drawing Number"]
			self.drawing_rev = component_data["Drawing Rev"]
			self.parts = component_data["Parts"]
			self.psu_layout = component_data["Layout"]
			self.gasper_layout = component_data["Gasper Layout"]
			self.deu_layout = component_data["DEU Layout"]
			self.vc_layout = component_data["VCC Layout"]
			self.comments = component_data["Comments"]


		if type == 'OHSC':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]			
			self.layout = component_data["Layout"]
			self.comments = component_data["Comments"]

		if type == 'Emergency Equipment':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]
			self.equipment_type = component_data["Equipment Type"]
			self.attaching_hardware = component_data["Attaching Hardware"]
			self.weight = component_data["Weight"]
			self.manufacturer = component_data["Manufacturer"]
			self.comments = component_data["Comments"]

		if type == 'EEL':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]			
			self.lopa = component_data["LOPA"]			
			self.ohsc = component_data["OHSC"]			
			self.locations = component_data["Locations"]			
			self.layout = component_data["Layout"]
			self.summary = component_data["Summary"]
			self.summary_table = component_data["Summary Table"]
			self.comments = component_data["Comments"]			

		if type == 'EEL Comparison':
			self.title = component_data["Title"]
			self.description = component_data["Description"]
			self.aircraft_type = component_data["Aircraft Type"]			
			self.current_eel = component_data["Current EEL"]			
			self.go_to_eel = component_data["GoTo EEL"]						
			self.layout = component_data["Layout"]
			self.instructions = component_data["Instructions"]
			self.bom = component_data['BOM']
			self.equip_item_nos = component_data['Item Numbers']
			self.comments = component_data["Comments"]		

		if type == 'Change':
			self.title = component_data["Title"]
			self.sb_title = component_data["SB Title"]
			self.sb_number = component_data["SB Number"]
			self.output_dir = component_data["Output Dir"]
			self.mods = component_data["Mods"]
			self.comments = component_data["Comments"]
			
			