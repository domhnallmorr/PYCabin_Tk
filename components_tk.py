import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import copy
import seats_frontend_tk as seats_tk
import windbreakers_frontend_tk as windbreakers_tk
import lopa_frontend_tk as lopa_tk
import aircraft_frontend_tk as aircraft_tk
import psu_frontend_tk as psu_tk
import ohsc_frontend_tk as ohsc_tk
import emergency_equip_frontend_tk as ee_tk
import eel_frontend_tk as eel_tk
import eel_comparison_frontend_tk as eel_comp_tk
import changes_frontend_tk as change_tk
'''
V0.02 initial issue
'''
def new_component(self, type):
	mode = 'new'
	
	if type == 'Aircraft':
		self.w=aircraft_tk.Edit_Aircraft_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)
		
	if type == 'Seats - Multiple':
		self.w=seats_tk.Multiple_Seat_Window_Tk(self, self.master)
		self.master.wait_window(self.w.top)	
		mode = 'new multiple'
		
		
		if self.w.button == 'ok':
			data = self.w.data
			self.w=seats_tk.Edit_Seat_Window_Tk(self, self.master, mode, None)
			self.master.wait_window(self.w.top)	
			
			if self.w.button == 'ok':
				self.w.data = data
			
	if type == 'Seat':
		self.w=seats_tk.Edit_Seat_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)
		
	if type == 'Windbreaker':
		self.w=windbreakers_tk.Edit_Windbreaker_Window_Tk(self, self.master, None, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'LOPA':
		self.w=lopa_tk.Edit_LOPA_Window_Tk(self, self.master, None, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'PSU':
		self.w=psu_tk.Edit_PSU_Window_Tk(self, self.master, None, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'OHSC':
		self.w=ohsc_tk.Edit_OHSC_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'Emergency Equipment':
		self.w=ee_tk.Edit_Emergency_Equip_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'EEL':
		self.w=eel_tk.Edit_EEL_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'EEL Comparison':
		self.w=eel_comp_tk.Edit_EEL_Comparison_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)

	if type == 'Change':
		self.w=change_tk.Edit_Change_Window_Tk(self, self.master, mode, None)
		self.master.wait_window(self.w.top)
		
	if self.w.button == 'ok':
		create_component(self, type, self.w, mode)
		

def create_component(self, type, source, update_type, insert=True):
	
	if type == 'Aircraft':
		if update_type == 'new':
			new_component = aircraft_tk.Aircraft_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)			
			
			if new_component.backend.aircraft_type in ['A320', 'A319']:
				node = 'A320 Aircraft'
				
	if type == 'Seats - Multiple':
		if update_type == 'new multiple':
			for d in source.data:
				if d.strip() != '':
					source.part_no = d.split(',')[0].strip()
					source.description = d.split(',')[1].strip()
					source.side = d.split(',')[2].strip()
					#
					new_component = seats_tk.Seat_Page_Tk(container=self.container, mainapp=self,)
					new_component.update_component(source, 'new')
					ac_type = new_component.backend.aircraft_type
					if ac_type == 'A320 Family':
						insert_component(self, new_component, 'A320 Seats')	
		
	if type == 'Seat':
		if update_type == 'new':
			new_component = seats_tk.Seat_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type == 'A320 Family':
				node = 'A320 Seats'
			elif ac_type == 'B737 Family':
				node = '737 Seats'
	
	if type == 'Windbreaker':
		if update_type == 'new':
			new_component = windbreakers_tk.Windbreaker_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type == 'A320 Family':
				node = 'A320 Windbreakers'
			elif ac_type == 'B737 Family':
				node = 'B737 Windbreakers'

	if type == 'LOPA':
		if update_type == 'new':
			new_component = lopa_tk.LOPA_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type in ['A320', 'A319']:
				node = 'A320 LOPAs'

	if type == 'PSU':
		if update_type == 'new':
			new_component = psu_tk.PSU_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type in ['A320', 'A319']:
				node = 'A320 PSUs'

	if type == 'Emergency Equipment':
		if update_type == 'new':
			new_component = ee_tk.Emergency_Equipment_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type in ['A320', 'A319', 'A320 Family']:
				node = 'A320 EE'

	if type == 'OHSC':
		if update_type == 'new':
			new_component = ohsc_tk.OHSC_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type in ['A320', 'A319', ]:
				node = 'A320 OHSCs'

	if type == 'EEL':
		if update_type == 'new':
			new_component = eel_tk.EEL_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type in ['A320', 'A319', ]:
				node = 'A320 EELs'

	if type == 'EEL Comparison':
		if update_type == 'new':
			new_component = eel_comp_tk.EEL_Comparison_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type in ['A320', 'A319', ]:
				node = 'A320 EEL Comparisons'

	if type == 'Change':

		if update_type == 'new':
			new_component = change_tk.Change_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			node = 'Changes'
			
	if insert:
		insert_component(self, new_component, node)
	else:
		return new_component

def insert_component(self, nc, parent_node):
	name = nc.backend.title
	type = nc.backend.type
	self.frames[name] = nc


	nc.pack(fill="both", expand=True)
	iid = insert_new_item_into_side_treeview(self, parent_node, name, nc)
	nc.treeview_iid = iid
	show_frame(self, name)

def insert_new_item_into_side_treeview(mainapp, parent_node, item_name, component_fe):

	
	if 'Aircraft' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.ac_icon2)
	elif 'Seats' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.seat_icon2)
	elif 'Windbreaker' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.wb_icon2)
	elif 'LOPA' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.lopa_icon2)
	elif 'PSU' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.psu_icon2)
	elif 'OHSC' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.ohsc_icon2)
	elif ' EE' in parent_node and 'EEL' not in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.ee_icon2)
	elif 'EEL' in parent_node and 'Comparisons' not in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.eel_icon2)
	elif 'EEL Comparisons' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.mag_icon2)
	else:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name)	
	return iid
	
def show_frame(self, page_name):
	'''Show a frame for the given page name'''
	self.current_frame.pack_forget()
	frame = self.frames[page_name]
	#frame.tkraise()
	frame.pack(fill="both", expand=True)
	self.current_frame = frame

def get_all_components(mainapp, type):

	
	if type == 'all':
		components_dict = {'All': []}
		#types = ['Aircraft', 'Seats', 'Windbreakers', 'LOPAs']
		types = ['Seats', 'Windbreakers', 'LOPAs', 'PSUs', 'OHSCs', 'Emergency Equipment', 'EELs', 'EEL Comparisons']
	else:
		types = [type] # make this into a list, to iterate over any nodes required
	
	if type == 'Aircraft':
		components_dict = {'All': [], 'A320': [], 'A319': [], 'B737-800': []}
	
	if type == 'Seats':
		components_dict = {'All': [], 'A320 Family': [], 'A320 Family LHS': [], 'A320 Family RHS': [],
					'B737 Family': [], 'B737 Family LHS': [], 'B737 Family RHS': []}
	if type == 'Windbreakers':
		components_dict = {'All': [], 'A320 Family LHS': [], 'A320 Family RHS': []}

	if type == 'LOPAs':
		components_dict = {'All': [], 'A320': [], 'A319': []}

	if type == 'PSUs':
		components_dict = {'All': [], 'A320': [], 'A319': []}

	if type == 'OHSCs':
		components_dict = {'All': [], 'A320': [], 'A319': []}

	if type == 'Emergency Equipment':
		components_dict = {'All': [], 'A320': [], 'A319': [], 'A320 Family':[]}

	if type == 'EELs':
		components_dict = {'All': [], 'A320': [], 'A319': []}

	if type == 'EEL Comparisons':
		components_dict = {'All': [], 'A320': [], 'A319': []}

	if type == 'Changes':
		components_dict = {'All': []}
	

	for type in types:
		for node in mainapp.treeview_nodes[type]:

			for component in mainapp.main_treeview.get_children(node):
				component = mainapp.frames[mainapp.main_treeview.item(component,'text')]
				
				if type != 'Changes':
					ac_type = component.backend.aircraft_type
				components_dict['All'].append(component.backend.title)
				
				if type == 'Aircraft':
					if component.backend.aircraft_type in components_dict.keys():
						components_dict[component.backend.aircraft_type].append(component.backend.title)
				
				# # ________________ SEATS ________________
				if type == 'Seats' or type == 'Windbreakers':
					side = component.backend.side
					if f'{ac_type} {side}' in components_dict.keys():
						components_dict[f'{ac_type} {side}'].append(component.backend.title)

				#if type == 'LOPAs' or type == 'PSUs' or type == 'OHSCs' or type == 'Emergency Equipment' or type == 'EELs':
				else:
					if f'{ac_type}' in components_dict.keys():
						components_dict[f'{ac_type}'].append(component.backend.title)


						
	return components_dict
	
def component_renamed(component):

	for f in component.mainapp.frames.keys():
		if component.mainapp.frames[f] == component:
			break
	del(component.mainapp.frames[f])
	component.mainapp.frames[component.backend.title] = component
	
def delete_component(mainapp):
	
	component = mainapp.frames[mainapp.main_treeview.item(mainapp.main_treeview.selection()[0], 'text')]
	
	msg = tkinter.messagebox.askokcancel(title='Delete Component', message=f'Are You Sure You Want to Delete This {component.backend.type}?')
	
	if msg:
		delete_ok = True
		
		if component.backend.type in ['Seat', 'Windbreaker']:
		
			functions = {'Seat': seats_tk.check_seat_used, 'Windbreaker': windbreakers_tk.check_windbreaker_used}
			
			used, lopas = functions[component.backend.type](mainapp, component.backend)
			if used:
				delete_ok = False
				message = f'Cannot Delete {component.backend.type}\n Ensure it is not Installed in any existing LOPAs'
			
		if component.backend.type == 'LOPA':

			used, psus, eels = lopa_tk.check_lopa_used(component)
			if used:
				delete_ok = False

				if len(psus) >0:
					message = f'Cannot Delete {component.backend.type}\nEnsure it is not Installed in any existing PSU Layouts'
				elif len(eels):
					message = f'Cannot Delete {component.backend.type}\nEnsure it is not Installed in any existing Emergency Equipment Layouts'

		if component.backend.type == 'OHSC':

			used, eels = ohsc_tk.check_ohsc_used(component)
			if used:
				delete_ok = False
				message = f'Cannot Delete {component.backend.type}\nEnsure it is not Installed in any existing Emergency Equipment Layouts'

		if component.backend.type == 'Emergency Equipment':

			used, eels = ee_tk.check_ee_used(component)
			if used:
				delete_ok = False
				message = f'Cannot Delete {component.backend.type}\nEnsure it is not Installed in any existing Emergency Equipment Layouts'

		if component.backend.type == 'EEL':

			used, eels = eel_tk.check_eel_used(component)
			if used:
				delete_ok = False
				message = f'Cannot Delete {component.backend.type}\nEnsure it is not Installed in any existing Emergency Equipment Layout Comparisons'

		if delete_ok:
			index = mainapp.main_treeview.index(component.treeview_iid)
			delete_item_from_main_treeview(mainapp, component.backend.title, component.backend)
			mainapp.states.undo_stack.append({'type': 'deleted component', 'component': component.backend,
												'new_class': component.backend.save_class(component.backend), 'index': index})
			
			show_frame(mainapp, 'Project')
			 
		else:
			tkinter.messagebox.showerror(master=mainapp, title='Error', message=message)
	
	
	
def delete_item_from_main_treeview(mainapp, component_name, component_backend, show_project = True):
	
	mainapp.main_treeview.detach(component_backend.parent_page.treeview_iid)		

	if show_project:
		show_frame(mainapp, 'Project')
		
def copy_component(mainapp):

	component = mainapp.frames[mainapp.main_treeview.item(mainapp.main_treeview.selection()[0], 'text')]
	
	i = 1
	while True:
		
		if f'{component.backend.title} ({i})' not in mainapp.frames:
			break
			
		else:
			i += 1
	
	new_component = create_component(mainapp, component.backend.type, component.backend, 'new', False)
	
	#if component.backend.type == 'Seat':
	new_component.backend.title = f'{component.backend.title} ({i})'
	
	if component.backend.type == 'Aircraft':
		new_component.backend.msn = f'{component.backend.title} ({i})'
	if component.backend.type == 'Seat':
		new_component.backend.part_no = f'{component.backend.title} ({i})'
	new_component.update_label_text()
	insert_component(mainapp, new_component, get_treeview_node(component.backend))
	
def get_treeview_node(backend):
	
	if backend.type == 'Aircraft':
		
		if backend.aircraft_type in ['A320', 'A319']:
			node = 'A320 Aircraft'
		elif backend.aircraft_type in ['B737-800']:
			node = '737 Aircraft'
			
	if backend.type == 'Seat':
	
		if backend.aircraft_type == 'A320 Family':
			node = 'A320 Seats'
		elif backend.aircraft_type == 'B737 Family':
			node = '737 Seats'
			
	elif backend.type == 'Windbreaker':
		
		if backend.aircraft_type == 'A320 Family':
			node = 'A320 Windbreakers'
		elif backend.aircraft_type == 'B737 Family':
			node = 'B737 Windbreakers'
			
	elif backend.type == 'LOPA':
		if backend.aircraft_type in ['A320', 'A319']:
			node = 'A320 LOPAs'

	elif backend.type  == 'PSU':
		if backend.aircraft_type in ['A320', 'A319']:
			node = 'A320 PSUs'

	elif backend.type  == 'OHSC':
		#if backend.aircraft_type in ['A320', 'A319']:
			#node = 'A320 PSUs'
		node = backend.treeview_node

	elif backend.type  == 'Emergency Equipment':
		if backend.aircraft_type in ['A320', 'A319']:
			node = 'A320 EE'

	elif backend.type  == 'EEL':
		if backend.aircraft_type in ['A320', 'A319']:
			node = 'A320 EELs'

	return node
	
def update_treeview_iid(mainapp, component_frontend):

	pass

