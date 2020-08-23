import json
import tkinter.messagebox

import components_tk

def new_project(event=None, mainapp=None):

	msg = tkinter.messagebox.askokcancel(title='Create New Project', message='Any Unsaved Data Will Be Lost, This Cannot Be Undone, Do You Want To Continue?')
	
	if msg:
		mainapp.frames['Project'].clear_project_data()
		
		components = components_tk.get_all_components(mainapp, 'all')
		
		for component in components['All']:
			component = mainapp.frames[component]
			mainapp.main_treeview.delete(component.treeview_iid)
			del mainapp.frames[component.backend.title]
			
	components_tk.show_frame(mainapp, 'Project')
	
def save(event=None, mainapp=None):

	if not mainapp.save_file:
		save_as(mainapp)
	else:
		write_save_file(mainapp)

def save_as(mainapp):

	mainapp.save_file = r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.01\Pycabin_Frontend_Tk\test.json'
	write_save_file(mainapp)
	
def write_save_file(mainapp):


	save_dict = {'Project': mainapp.frames['Project'].gen_save_dict(), 'Seats': []}
	
	# _________________ SEATS _________________
	seats_dict = components_tk.get_all_components(mainapp, 'seat')
	
	for s in seats_dict['All']:
		save_dict['Seats'].append(mainapp.frames[s].backend.gen_save_dict())
		
		
	with open(mainapp.save_file, 'w') as outfile:
		json.dump(save_dict, outfile, indent=4)
		
		
def load(event=None, mainapp=None):

	with open(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.01\Pycabin_Frontend_Tk\test.json') as f:
		data = json.load(f)
		
	# ______ Project _________________
	if 'Project' in data.keys():
	
		mainapp.frames['Project'].load_project_data(data['Project'])
		
	if 'Seats' in data.keys():
	
		for seat in data['Seats']:
			seat = Load('Seat', seat)
			components_tk.create_component(mainapp, 'Seat', seat, 'new')		

class Load():
	def __init__(self, type, component_data):


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