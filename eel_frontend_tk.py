import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk
import components_tk

import eel_backend as eel_bk
import double_scrollbar
import comment_box
import data_input_checks_tk
import file_menu
import components_tk
# from Pycabin_Backend import lopa_draw_redo
# from Pycabin_Backend import ohsc_draw

import treeview_functions

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import copy
import collections

def check_eel_used(self):
	used = False
	eel_comparisons = []
	eel_dict = components_tk.get_all_components(self.mainapp, 'EEL Comparisons')

	for e in eel_dict['All']:
		
		if self.backend.title in [self.mainapp.frames[e].backend.current_eel, self.mainapp.frames[e].backend.go_to_eel]: 

			used = True
			eel_comparisons.append(e)
			
	return used, eel_comparisons

class EEL_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.top_label = tk.Label(self, text=('EEL: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)

		self.backend = eel_bk.EEL_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frames()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_treeviews()
		self.setup_buttons()
		#self.add_plot()

	def setup_label_frames(self):
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="EEL Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.parts_frame = LabelFrame(self.main_scroll_frame.inner,text="Parts:")
		self.parts_frame.grid(row=4, column=0, columnspan = 6, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.summary_frame = LabelFrame(self.main_scroll_frame.inner,text="Summary By P/N:")
		self.summary_frame.grid(row=4, column=6, columnspan = 2, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.summary_item_frame = LabelFrame(self.main_scroll_frame.inner,text="Summary By Item Type:")
		self.summary_item_frame.grid(row=5, column=6, columnspan = 2, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)				
		#self.parts_frame = LabelFrame(self.lopa_frame,text="Summary:")
		#self.parts_frame.grid(row=6, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_labels(self):

		#self.top_label = tk.Label(self, text=('EEL Layout: '),font=self.mainapp.title_font)
		#self.top_label.grid(row=0,column=0,columnspan=24,stick='W')

		self.ac_type_label = gui_styles_tk.create_label(self.main_frame,'')
		self.ac_type_label.grid(row = 2, column = 0,pady=2,padx=2, sticky="nsew")
		
		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 1, columnspan=6,pady=2,padx=2, sticky="nsew")
		self.description_label.configure(width=100)

		self.lopa_label = gui_styles_tk.create_label(self.main_frame,'')
		self.lopa_label.grid(row = 3, column = 0,pady=2,padx=2, sticky="nsew")

		self.ohsc_label = gui_styles_tk.create_label(self.main_frame,'')
		self.ohsc_label.grid(row = 3, column = 1,pady=2,padx=2,sticky="nsew")		
		self.ohsc_label.configure(width=20)
		
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

	def update_component(self, window, type):

		if type != 'new':
			orig_title = self.backend.title
			used, eel_comparisons = check_eel_used(self)
		else:
			used = False

		self.backend.update_component(window, type)

		self.update_label_text()
		self.update_treeviews()

		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)

		if used:
			for eel in eel_comparisons:
				eel = self.mainapp.frames[eel]

				if eel.backend.current_eel == orig_title:
					eel.backend.current_eel = self.backend.title

				if eel.backend.go_to_eel == orig_title:
					eel.backend.go_to_eel = self.backend.title

				eel.update_component(eel.backend, 'ohsc')
		self.mainapp.update_titlebar('edit')
		
	def update_label_text(self):
				
		self.top_label.config(text=f'EEL: {self.backend.title}')
		self.ac_type_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.lopa_label.config(text=f' LOPA: {self.backend.lopa}')
		self.ohsc_label.config(text=f' OHSC: {self.backend.ohsc}')
	
	def update_treeviews(self):
	
		data = []
		
		for loc in self.backend.layout.keys():
			for p in self.backend.layout[loc]:
				data.append(p)
		
		treeview_functions.write_data_to_treeview(self.eel_tree, 'replace', data)

		#highlight location change in eel tree
		last_loc = None
		odd = False
		for child in self.eel_tree.get_children():
			if self.eel_tree.item(child, 'values')[1] != last_loc:
				if not odd:
					odd = True
				else:
					odd = False
			if odd:
				self.eel_tree.item(child,tag='odd_row')

			last_loc = self.eel_tree.item(child, 'values')[1]


		treeview_functions.write_data_to_treeview(self.summary_pn_tree, 'replace', self.backend.summary_table)
		
		#item summary
		data = []
		
		for child in self.summary_pn_tree.get_children():
			if self.summary_pn_tree.item(child, 'text') != '':
				
				self.summary_pn_tree.item(child,tag='header_row')

				item = self.summary_pn_tree.item(child, 'text')
				q = self.summary_pn_tree.item(child, 'values')[1]

				data.append([item, q])

		treeview_functions.write_data_to_treeview(self.summary_item_tree, 'replace', data)

	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def set_grid_configures(self):
	
		self.lopa_frame.grid_columnconfigure(4, weight=1)

	def onFrameConfigure(self, canvas):
		'''Reset the scroll region to encompass the inner frame'''
		canvas.configure(scrollregion=canvas.bbox("all"))

	def FrameWidth(self, event):
		canvas_width = event.width
		self.lopa_frame_canvas.itemconfig(self.canvas_frame, width = canvas_width)		

	def setup_treeviews(self):
		self.eel_tree = ttk.Treeview(self.parts_frame,selectmode="extended",columns=("A","B",'C'), height=25)
		self.eel_tree.grid(row=2,column=0, rowspan=2, columnspan=16,sticky="nsew")
		self.eel_tree.heading("#0", text="Item")
		self.eel_tree.column("#0",minwidth=0,width=250, stretch='NO')
		self.eel_tree.heading("#1", text="Part Number")
		self.eel_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#2", text="Location")
		self.eel_tree.column("#2",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#3", text="Qty")
		self.eel_tree.column("#3",minwidth=0,width=50, stretch='NO')

		self.eel_tree.bind("<Double-1>", lambda event: self.eel_double_click(event))
		
		eel_tree_scrollbar = Scrollbar(self.parts_frame, command=self.eel_tree.yview)
		eel_tree_scrollbar.grid(row=2, rowspan=2, column=16, sticky='nsew')
		self.eel_tree.config(yscrollcommand=eel_tree_scrollbar.set)

		self.eel_tree.tag_configure('odd_row', background='gray65', foreground='black')

		self.summary_pn_tree = ttk.Treeview(self.summary_frame,selectmode="extended",columns=("A","B"))
		self.summary_pn_tree.grid(row=2,column=0, columnspan=6,sticky="nsew")
		self.summary_pn_tree.heading("#0", text="Item")
		self.summary_pn_tree.column("#0",minwidth=0,width=250, stretch='NO')
		self.summary_pn_tree.heading("#1", text="Part Number")
		self.summary_pn_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.summary_pn_tree.heading("#2", text="Qty")
		self.summary_pn_tree.column("#2",minwidth=0,width=50, stretch='NO')

		self.summary_pn_tree.tag_configure('header_row', background='gray24', foreground='white')

		summary_pn_tree_scrollbar = Scrollbar(self.summary_frame, command=self.summary_pn_tree.yview)
		summary_pn_tree_scrollbar.grid(row=2, column=6, sticky='nsew')
		self.summary_pn_tree.config(yscrollcommand=summary_pn_tree_scrollbar.set)

		self.summary_item_tree = ttk.Treeview(self.summary_item_frame,selectmode="extended",columns=("A"))
		self.summary_item_tree.grid(row=2,column=0, columnspan=6,sticky="nsew")
		self.summary_item_tree.heading("#0", text="Item")
		self.summary_item_tree.column("#0",minwidth=0,width=250, stretch='NO')
		self.summary_item_tree.heading("#1", text="Qty")
		self.summary_item_tree.column("#1",minwidth=0,width=50, stretch='NO')

		summary_item_tree_scrollbar = Scrollbar(self.summary_item_frame, command=self.summary_item_tree.yview)
		summary_item_tree_scrollbar.grid(row=2, column=6, sticky='nsew')
		self.summary_item_tree.config(yscrollcommand=summary_item_tree_scrollbar.set)

	def setup_buttons(self):

		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.add_part_btn = Button(self.parts_frame, text = 'Add Part', image = self.mainapp.add_icon2, compound = LEFT,
								command = self.add_part)
		self.add_part_btn.grid(row = 1, column = 0, columnspan = 1, padx=5, pady=5, sticky = 'NW')

		self.del_part_btn = Button(self.parts_frame, text = 'Delete Part',  image = self.mainapp.del_icon2, compound = LEFT,
								command = self.del_part)
		self.del_part_btn.grid(row = 1, column = 1, columnspan = 1, padx=5, pady=5, sticky = 'NW')

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)

	def add_part(self):
	
		self.w=Add_Part_Window_Tk(self.mainapp, self.master, 'add', self, None, None)
		self.master.wait_window(self.w.top)
		
		if self.w.button == 'ok':
			
			self.update_component(self.w, 'edit')

	def del_part(self):

		save_dict = copy.deepcopy(self.backend.gen_save_dict())
		w = file_menu.Load('EEL', save_dict)
		#print(w.attaching_hardware)
		index, data = treeview_functions.get_current_selection(self.eel_tree)

		count = 0
		found = False
		for loc in w.layout.keys():
			
			if found:
				break

			for idx, part in enumerate(w.layout[loc]):
				
				if count == index:

					w.layout[loc].pop(idx)
					found = True
					break
				else:
					count += 1
		#print(w.attaching_hardware)
		#print(self.backend.attaching_hardware)
		
		self.update_component(w, 'edit')

		del(w)

	def edit(self):

		self.w = Edit_EEL_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')

	def eel_double_click(self, event):
		index, data = treeview_functions.get_current_selection(self.eel_tree)

		self.w=Add_Part_Window_Tk(self.mainapp, self.master, 'edit', self, index, data) #lazy nones, not used
		self.master.wait_window(self.w.top)

		if self.w.button == 'ok':

			self.update_component(self.w, 'edit')


class Edit_EEL_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_page):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_page = parent_page

		self.lopa_dict = components_tk.get_all_components(mainapp, 'LOPAs')
		self.lopa_dict['A320'].insert(0, '')
		#self.lopas = components_tk.gen_seat_dict(mainapp, self.seats)
		self.ohsc_dict = components_tk.get_all_components(mainapp, 'OHSCs')
		self.ohsc_dict['A320'].insert(0, '')
		
		eel_bk.setup_variables(self)

		if self.mode == 'edit':
			self.orig_title = parent_page.backend.title
			eel_bk.update_variables(self, self.parent_page.backend)
		else:
			self.orig_title = None

		self.data_checks = {}
		self.setup_label_frames()
		self.setup_widgets()
		self.button = 'cancel'
		
		# if mode == 'new':
			# self.parts = None
		# else:
			# self.parts = treeview_functions.get_all_treeview_items(parent_psu.parts_tree)

	def setup_label_frames(self):		
		self.details_frame = LabelFrame(self.top,text="EEL Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		labels = ['Title:', 'Description:', 'Aircraft:', 'LOPA:', 'OSHC Layout:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)	
		
		self.title_entry=Entry(self.details_frame, width=60)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_title]
		if self.mode == 'edit':
			self.title_entry.insert(0, self.parent_page.backend.title)

		self.description_entry=Entry(self.details_frame, width=60)		
		self.description_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			self.description_entry.insert(0, self.parent_page.backend.description)

		self.ac_combo= ttk.Combobox(self.details_frame, values=['A320'], state='disabled')
		self.ac_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.ac_combo.set('A320')

		self.lopa_combo= ttk.Combobox(self.details_frame, values=self.lopa_dict['A320'], state='readonly')
		self.lopa_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			self.lopa_combo.set(self.parent_page.backend.lopa)
			self.lopa_combo.config(state='disabled')

		self.layout_combo= ttk.Combobox(self.details_frame, values=self.ohsc_dict['A320'], state='readonly')
		self.layout_combo.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			self.layout_combo.set(self.parent_page.backend.ohsc)
			self.layout_combo.config(state='disabled')

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, padx=5, pady=5,sticky="ne")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, padx=5, pady=5,sticky="nw")

	def cleanup(self, button):
	
		self.button = button
		
		if button == 'ok':

			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)

			if data_good:

				self.title = self.title_entry.get()
				self.description = self.description_entry.get()
				self.aircraft_type = self.ac_combo.get()
				self.lopa = self.lopa_combo.get()
				
				if self.lopa == '':
					self.lopa = None
				
				self.ohsc = self.layout_combo.get()
				
				if self.ohsc == '':
					self.ohsc = None
				
				if self.mode == 'new':
					self.locations = ['Cockpit']
					self.layout = {'Cockpit': []}

				self.top.destroy()

			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		
		else:
			self.top.destroy()
			
			
class Add_Part_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_eel, index, parts_data):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_eel = parent_eel
		self.index = index

		self.eel_dict = components_tk.get_all_components(self.mainapp, 'Emergency Equipment')
		
		#setup equipment type filters
		self.equipment_filters = {'All': []}

		for p in self.eel_dict['A320 Family']:
			if self.mainapp.frames[p].backend.equipment_type not in self.equipment_filters.keys():
				self.equipment_filters[self.mainapp.frames[p].backend.equipment_type] = []

			self.equipment_filters[self.mainapp.frames[p].backend.equipment_type].append(p)
			self.equipment_filters['All'].append(p)
		self.equipment_filters = collections.OrderedDict(sorted(self.equipment_filters.items()))

		self.data_checks = {}
		self.setup_label_frames()

		self.setup_widgets()

		if self.mode == 'edit':

			self.location_combo.set(parts_data[2])
			self.location_combo.config(state='disabled')
			self.part_no_combo.set(parts_data[1])
			self.qty_combo.set(parts_data[3])
		self.button = 'cancel'
		
	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.top,text="Options:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)		
		
	def setup_widgets(self):

		labels = ['Location:', 'Equipment Type:', 'Part Number', 'Qty:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.main_frame, labels, row, 2, 20, 2, 2)
		
		self.location_combo = ttk.Combobox(self.main_frame, values=self.parent_eel.backend.locations, width=80)
		self.location_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Location'] = ['combo', self.location_combo, 'not empty', 'Location']

		self.type_combo = ttk.Combobox(self.main_frame, values=list(self.equipment_filters.keys()), state='readonly')
		self.type_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.type_combo.current(list(self.equipment_filters.keys()).index('All'))
		self.type_combo.bind("<<ComboboxSelected>>", self.filter_parts)

		self.part_no_combo = ttk.Combobox(self.main_frame, values=self.eel_dict['A320 Family'], state='readonly')
		self.part_no_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Part Number'] = ['combo', self.part_no_combo, 'not empty', 'Part Number']

		self.qty_combo = ttk.Combobox(self.main_frame, values=[i for i in range(500)], state='readonly')
		self.qty_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Qty'] = ['combo', self.qty_combo, 'not empty', 'Qty']

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=3, padx=5, pady=5,sticky="ne")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=4, padx=5, pady=5,sticky="nw")

	def filter_parts(self, event):

		self.part_no_combo['values'] = self.equipment_filters[self.type_combo.get()]

	def cleanup(self, button):
		
		self.button = button
		
		if self.button == 'ok':
			
			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)

			if data_good:
				eel_bk.setup_variables(self)
				eel_bk.update_variables(self, self.parent_eel.backend)
				
				self.location = self.location_combo.get()
				self.part_no = self.part_no_combo.get()
				self.type = self.mainapp.frames[self.part_no].backend.equipment_type
				self.qty = self.qty_combo.get()
				
				if self.mode != 'edit':
					if self.location in self.layout.keys():

						#check if part number is already in this location
						found = False
						for idx, pn in enumerate(self.layout[self.location]):
							if pn[1] == self.part_no:
								found = True
								self.qty = int(self.qty) + int(pn[3])
								self.layout[self.location][idx] = [self.type, self.part_no, self.location, self.qty]
						
						if not found:
							self.layout[self.location].append([self.type, self.part_no, self.location, self.qty])
					else:
						self.layout[self.location] = [[self.type, self.part_no, self.location, self.qty]]

				else:
					count = 0
					for loc in self.layout.keys():
					
						for idx, part in enumerate(self.layout[loc]):
							
							if count == self.index:
								self.layout[loc][idx] = [self.type, self.part_no, self.location, self.qty]
							count += 1

				self.top.destroy()

			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
			
		else:
			self.top.destroy()