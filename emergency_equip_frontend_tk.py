
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk
import components_tk
import data_input_checks_tk
import emergency_equip_backend as ee_bknd
import double_scrollbar
import treeview_functions
import comment_box
import file_menu
import copy
class Emergency_Equipment_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp
		
		self.top_label = tk.Label(self, text=('PSU Layout: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)
		
		self.backend = ee_bknd.Emergency_Equip_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frames()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_treeviews()
		self.setup_buttons()
		#self.set_grid_configures()


	def setup_scrollable_frames(self):
		
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def setup_notebook(self):
	
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.comments_tab, text = "Comments")
		
		#self.note.grid(row=1,column=0,sticky='NSEW')
		self.note.pack(fill=tk.BOTH, expand=True)
		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="Emergency Equipment Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.attach_frame = LabelFrame(self.main_scroll_frame.inner,text="Attaching Hardware:")
		self.attach_frame.grid(row=4, column=0, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_labels(self):
		self.part_no_label = gui_styles_tk.create_label(self.main_frame,'')
		self.part_no_label.grid(row = 2, column = 0,pady=2,padx=2, sticky="nsew")

		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 1, columnspan=5,pady=2,padx=2, sticky="nsew")
		
		self.manu_label = gui_styles_tk.create_label(self.main_frame,'')
		self.manu_label.grid(row = 3, column = 0,pady=2,padx=2, sticky="nsew")
		#
		self.type_label = gui_styles_tk.create_label(self.main_frame,'')
		self.type_label.grid(row = 3, column = 1,pady=2,padx=2, sticky="nsew")

		self.weight_label = gui_styles_tk.create_label(self.main_frame,'')
		self.weight_label.grid(row = 3, column = 2,pady=2,padx=2, sticky="nsew")

		self.aircraft_label = gui_styles_tk.create_label(self.main_frame,'')
		self.aircraft_label.grid(row = 3, column = 3,pady=2,padx=2, sticky="nsew")

	def setup_treeviews(self):
		self.parts_tree = ttk.Treeview(self.attach_frame, selectmode="extended",columns=("A","B",'C'),height = 15)
		#self.monument_tree.grid(row=1,column=0, columnspan= 6,sticky="nsew")
		self.parts_tree.heading("#0", text="#")
		self.parts_tree.column("#0",minwidth=0,width=60, stretch='NO')
		self.parts_tree.heading("A", text="Type")	  
		self.parts_tree.column("A",minwidth=0,width=200, stretch='NO') 
		self.parts_tree.heading("B", text="Part Number")	  
		self.parts_tree.column("B",minwidth=0,width=250, stretch='NO')
		self.parts_tree.heading("C", text="Qty")	  
		self.parts_tree.column("C",minwidth=0,width=150, stretch='NO')	
		
		self.parts_tree.grid(row = 2, column = 0, columnspan = 8, sticky = 'NSEW')

		self.parts_tree.bind("<Double-1>", lambda event: self.parts_double_click(event))

	def setup_buttons(self):

		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.add_attach_btn = Button(self.attach_frame, text='Add',  image = self.mainapp.add_icon2, compound = LEFT, command= lambda mode='new': self.add_attachment(mode))
		self.add_attach_btn.grid(row = 1, column = 0, columnspan = 1, sticky = 'NSEW', pady=2)

		self.del_attach_btn = Button(self.attach_frame, text='Delete',  image = self.mainapp.del_icon2, compound = LEFT, command= lambda mode='new': self.del_attachment())
		self.del_attach_btn.grid(row = 1, column = 1, columnspan = 1, sticky = 'NSEW', pady=2)

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)


	def update_label_text(self):
		self.top_label.config(text=f' Emergency Equipment: {self.backend.title}')
		self.part_no_label.config(text=f' Part Number: {self.backend.title}')
		self.manu_label.config(text=f' Manufacturer: {self.backend.manufacturer}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.type_label.config(text=f' Type: {self.backend.equipment_type}')
		self.weight_label.config(text=f' Weight (lbs): {self.backend.weight}')
		self.aircraft_label.config(text=f' Aircraft: {self.backend.aircraft_type}')


	def update_component(self, window, type, redraw = True):
		
		self.backend.update_component(window, type)
		self.update_label_text()
		self.update_parts_tree()

		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)

	def update_parts_tree(self):

		treeview_functions.write_data_to_treeview(self.parts_tree, 'replace', self.backend.attaching_hardware)

	def edit(self):

		self.w = Edit_Emergency_Equip_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')


	def add_attachment(self, mode):

		if mode == 'edit':
			index, parts_data = treeview_functions.get_current_selection(self.parts_tree)
		else:
			index = None
			parts_data = None

		self.w=Double_Click_Part_Window_Tk(self, self.mainapp, self.master, parts_data, index, mode)
		self.master.wait_window(self.w.top)

		if self.w.button == 'ok':

			self.update_component(self.w, 'edit', False)

	def del_attachment(self):

		save_dict = copy.deepcopy(self.backend.gen_save_dict())
		w = file_menu.Load('Emergency Equipment', save_dict)
		#print(w.attaching_hardware)
		index, data = treeview_functions.get_current_selection(self.parts_tree)
		w.attaching_hardware.pop(index)
		#print(w.attaching_hardware)
		#print(self.backend.attaching_hardware)
		
		self.update_component(w, 'edit', False)

		del(w)

	def parts_double_click(self, event):
		index, data = treeview_functions.get_current_selection(self.parts_tree)

		self.w=Double_Click_Part_Window_Tk(self, self.mainapp, self.master, data, index, 'edit') #lazy nones, not used
		self.master.wait_window(self.w.top)

		if self.w.button == 'ok':
			save_dict = copy.deepcopy(self.backend.gen_save_dict())
			w = file_menu.Load('Emergency Equipment', save_dict)			
			w.attaching_hardware[index] = [index+1, self.w.attach_type, self.w.attach_part_no, self.w.attach_qty]

			self.update_component(w, 'edit', False)

			del(w)
class Edit_Emergency_Equip_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_ee):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_ee = parent_ee

		ee_bknd.setup_variables(self)
		
		if self.mode == 'edit':
			self.orig_title = parent_ee.backend.title
			ee_bknd.update_variables(self, self.parent_ee.backend)
		else:
			self.orig_part_no = None
			
		self.data_checks = {}
		
		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.top,text="Aircraft Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		labels = ['Title:', 'Description:', 'Equipment Type:', 'Aircraft Type:', 'Weight (lbs):', 'Manufacturer:']
		row = 1
		gui_styles_tk.create_multiple_labels(self.main_frame, labels, row, 2, 20, 2, 2)	
		
		self.title_entry=Entry(self.main_frame, width=20)		
		self.title_entry.grid(row=1,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_title]
		if self.mode == 'edit':
			self.title_entry.insert(0, self.parent_ee.backend.title)
		
		self.description_entry=Entry(self.main_frame, width=50)		
		self.description_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		if self.mode == 'edit':
			self.description_entry.insert(0, self.parent_ee.backend.description)
		
		self.equip_type_combo= ttk.Combobox(self.main_frame, values=self.available_equipment)
		self.equip_type_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		if self.mode == 'edit':
			self.equip_type_combo.set(self.parent_ee.backend.equipment_type)
		
		self.ac_combo= ttk.Combobox(self.main_frame, values=['A320'], state='disabled')
		self.ac_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.ac_combo.set('A320')

		self.weight_entry = Entry(self.main_frame, width=50)
		self.weight_entry.grid(row=5, column=3,padx=2, pady=2,sticky = 'NSEW')
		if self.mode == 'edit':
			self.weight_entry.insert(0, self.parent_ee.backend.weight)

		self.manu_entry = Entry(self.main_frame, width=50)
		self.manu_entry.grid(row=6, column=3,padx=2, pady=2,sticky = 'NSEW')
		if self.mode == 'edit':
			self.manu_entry.insert(0, self.parent_ee.backend.manufacturer)

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, pady=5,sticky="nsew")

		self.button = 'cancel'
		
	def cleanup(self,button):
	
		if button == 'ok':
			
			self.title = self.title_entry.get()
			self.aircraft_type = self.ac_combo.get()
			self.description = self.description_entry.get()
			self.equipment_type = self.equip_type_combo.get()
			self.manufacturer = self.manu_entry.get()
			self.weight = self.weight_entry.get()
			self.button = 'ok'
			self.top.destroy()
			
		else:
			self.top.destroy()
		
		
class Double_Click_Part_Window_Tk(object):			
	def __init__(self, parent_ee, mainapp, master, parts_data, index, mode):
		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp
		self.parent_ee = parent_ee
		self.parts_data = copy.deepcopy(parts_data)
		self.index = index
		self.mode = mode
		
		self.data_checks = {}
		ee_bknd.setup_variables(self)
		ee_bknd.update_variables(self, self.parent_ee.backend)
		
		self.setup_label_frames()
		self.setup_widgets()
		
		if self.mode == 'edit':

			self.type_combo.set(parts_data[1])
			self.pn_entry.insert(0, parts_data[2])
			self.qty_entry.insert(0, parts_data[3])

		self.button = 'cancel'
	def setup_label_frames(self):
	
		self.options_frame = LabelFrame(self.top,text="Options:")
		self.options_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_widgets(self):
	
		labels = ['Type', 'Part Number:', 'Qty:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, labels, row, 2, 20, 2, 2)			

		self.type_combo= ttk.Combobox(self.options_frame, values=['Bracket', 'Screw', 'Washer'])
		self.type_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.pn_entry=Entry(self.options_frame, width=20)		
		self.pn_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.qty_entry=Entry(self.options_frame, width=20)		
		self.qty_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")
		
	def cleanup(self,button):
		
		self.button = button
		if button == 'ok':

			self.attach_type = self.type_combo.get()
			self.attach_part_no = self.pn_entry.get()
			self.attach_qty = self.qty_entry.get()

			self.attaching_hardware.append([len(self.attaching_hardware)+1, self.attach_type, self.attach_part_no, self.attach_qty])
			self.top.destroy()

		else:
			self.top.destroy()