import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import copy
import seats_frontend_tk as seats_tk

'''
V0.02 initial issue
'''
def new_component(self, type):
	mode = 'new'
	
	if type == 'Seat':
		self.w=seats_tk.Edit_Seat_Window_Tk(self, self.master, mode, None)
		#self.master.wait_window(self.w.top)
		
		
	if self.w.button == 'ok':
		create_component(self, type, self.w, mode)
		

def create_component(self, type, source, update_type, insert=True):

	if type == 'Seat':
		if update_type == 'new':
			new_component = seats_tk.Seat_Page_Tk(container=self.container, mainapp=self,)
			new_component.update_component(source, update_type)
			ac_type = new_component.backend.aircraft_type
			if ac_type == 'A320 Family':
				node = 'A320 Seats'
			elif ac_type == 'B737 Family':
				node = '737 Seats'
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
		icon = component_fe.mainapp.icons.ac_icon2
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = icon)
	elif 'Seats' in parent_node:
		iid = mainapp.main_treeview.insert(parent_node,'end', text=item_name, image = mainapp.seat_icon2 )
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
		types = ['seat']
	else:
		types = [type] # make this into a list, to iterate over any nodes required
		
	
	if type == 'seat':
		components_dict = {'All': [], 'A320 Family': [], 'A320 Family LHS': [], 'A320 Family RHS': [],
					'B737 Family': [], 'B737 Family LHS': [], 'B737 Family RHS': []}
	
	for type in types:
		for node in mainapp.treeview_nodes[type]:
			
			for component in mainapp.main_treeview.get_children(node):
				component = mainapp.frames[mainapp.main_treeview.item(component,'text')]
				ac_type = component.backend.aircraft_type
				components_dict['All'].append(component.backend.title)
				
				# # ________________ SEATS ________________
				#if type == 'seat':
				
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
		
		# if component.backend.type == 'Seat':
			# seat_used = seats_tk.check_seat_used(component)
			# if seat_used:
				# delete_ok = False
				# message = 'Cannot delete seat\n Ensure it is not installed in any existing LOPAs'
				
		if delete_ok:
			index = mainapp.main_treeview.index(component.treeview_iid)
			delete_item_from_main_treeview(mainapp, component.backend.title, component.backend)
			mainapp.states.undo_stack.append({'type': 'deleted component', 'component': component.backend,
												'new_class': component.backend.save_class(component.backend), 'index': index})
			
			 
		else:
			tkinter.messagebox.showerror(master=mainapp, title='Error', message=message)
	
	show_frame(mainapp, 'Project')
	
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
	
	if component.backend.type == 'Seat':
		new_component.backend.title = f'{component.backend.part_no} ({i})'
		new_component.backend.part_no = f'{component.backend.part_no} ({i})'
		new_component.update_label_text()
	insert_component(mainapp, new_component, get_treeview_node(component.backend))
	
def get_treeview_node(backend):

	if backend.type == 'Seat':
	
		if backend.aircraft_type == 'A320 Family':
			node = 'A320 Seats'
		elif backend.aircraft_type == 'B737 Family':
			node = '737 Seats'
			
	return node
	
