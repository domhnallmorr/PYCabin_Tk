import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import seats_backend as seat_bk
import gui_styles_tk
import components_tk
import data_input_checks_tk

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import treeview_functions
import double_scrollbar
import comment_box

import inspect
import copy
'''
V0.02 Initial Issue
To Do
	check if seat used in any LOPA
'''

def check_seat_used(mainapp, seat_backend):
	
	seat_used = False
	lopas = []
	lopa_dict = components_tk.get_all_components(mainapp, 'LOPAs')
	
	print(lopa_dict)
	for l in lopa_dict['All']:
		for row in mainapp.frames[l].backend.seat_layout[seat_backend.side]:
			if seat_backend.title == row[1]:
				seat_used = True
				lopas.append(l)
				break
				
	return seat_used, lopas
	
class Seat_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.top_label = tk.Label(self, text=('Seat: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)
		self.setup_notebook()
		self.setup_scrollable_frame()
		self.setup_label_frames()
		self.backend = seat_bk.Seat_Backend(self, mainapp)
		
		self.treeview_iid = None
		
		self.add_seat_plot()
		self.setup_labels()
		self.setup_buttons()
		
		
		self.set_grid_configures()

	def setup_notebook(self):
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.docs_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		#self.note.add(self.docs_tab, text = "Documentation")
		self.note.add(self.comments_tab, text = "Comments")
		
		#self.note.grid(row=1,column=0,sticky='NSEW')
		self.note.pack(fill=tk.BOTH, expand=True)
		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_scrollable_frame(self):
		
		#self.main_scroll_frame = scrollable_frame.ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)
	def add_seat_plot(self):
		
		self.canvas = FigureCanvasTkAgg(self.backend.seat_figure, self.preview_frame)
		self.canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=11, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")

	def setup_label_frames(self):
		main_frame = self.main_scroll_frame.inner
		self.main_frame = LabelFrame(main_frame,text="Seat Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.dimensions_frame = LabelFrame(main_frame,text="Seat Dimensions:")
		self.dimensions_frame.grid(row=4, column=0, columnspan = 2, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.reference_frame = LabelFrame(main_frame,text="Seat Reference:")
		self.reference_frame.grid(row=6, column=0, columnspan = 2, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.weight_frame = LabelFrame(main_frame,text="Seat Weight:")
		self.weight_frame.grid(row=8, column=0, columnspan = 2, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.preview_frame = LabelFrame(main_frame,text="Seat Preview:")
		self.preview_frame.grid(row=4, column=2, columnspan = 6, rowspan = 6,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)


		self.cmm_frame = LabelFrame(self.docs_tab,text="CMM Details:")
		self.cmm_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

	def setup_labels(self):
		
		self.part_no_label = gui_styles_tk.create_label(self.main_frame,'')
		self.part_no_label.grid(row = 2, column = 0,pady=2,padx=2, sticky="nsew")

		self.seat_description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.seat_description_label.grid(row = 2, column = 1, columnspan=5,pady=2,padx=2, sticky="nsew")
		
		self.manu_label = gui_styles_tk.create_label(self.main_frame,'')
		self.manu_label.grid(row = 3, column = 0,pady=2,padx=2, sticky="nsew")
		#
		self.seat_type_label = gui_styles_tk.create_label(self.main_frame,'')
		self.seat_type_label.grid(row = 3, column = 1,pady=2,padx=2, sticky="nsew")
		#
		self.iat_label = gui_styles_tk.create_label(self.main_frame,'')
		self.iat_label.grid(row = 3, column = 2,pady=2,padx=2, sticky="nsew")
		self.iat_label.configure(width=10)
		#
		self.profile_label = gui_styles_tk.create_label(self.main_frame,'')
		self.profile_label.grid(row = 3, column = 3,pady=2,padx=2, sticky="nsew")
		self.profile_label.configure(width=20)
		#
		self.side_label = gui_styles_tk.create_label(self.main_frame,'')
		self.side_label.grid(row = 3, column = 4,pady=2,padx=2, sticky="nsew")
		self.side_label.configure(width=20)
		#
		self.aircraft_label = gui_styles_tk.create_label(self.main_frame,'')
		self.aircraft_label.grid(row = 3, column = 5,pady=2,padx=2,sticky="nsew")
		self.aircraft_label.configure(width=20)
		#
		self.width_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.width_label.grid(row = 2, column = 0,pady=2,sticky="nsew")

		self.width_inbd_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.width_inbd_label.grid(row = 3, column = 0,pady=2,sticky="nsew")

		self.length_aft_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.length_aft_label.grid(row = 4, column = 0,pady=2,sticky="nsew")

		self.length_fwd_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.length_fwd_label.grid(row = 5, column = 0,pady=2,sticky="nsew")	

		self.cushion_height_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.cushion_height_label.grid(row = 6, column = 0,pady=2,sticky="nsew")		

		self.height_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.height_label.grid(row = 7, column = 0,pady=2,sticky="nsew")

		self.stud_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.stud_label.grid(row = 8, column = 0,pady=2,sticky="nsew")

		self.arm_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.arm_label.grid(row = 9, column = 0,pady=2,sticky="nsew")	

		self.srpx_label = gui_styles_tk.create_label(self.reference_frame,'')
		self.srpx_label.grid(row = 1, column = 0,pady=2,sticky="nsew")

		self.srpy_label = gui_styles_tk.create_label(self.reference_frame,'')
		self.srpy_label.grid(row = 2, column = 0,pady=2,sticky="nsew")

		self.weight_label = gui_styles_tk.create_label(self.weight_frame,'')
		self.weight_label.grid(row = 2, column = 0,pady=2,sticky="nsew")

		# ___ CMM ______
		self.cmm_title_label = gui_styles_tk.create_label(self.cmm_frame,'')
		self.cmm_title_label.grid(row=2, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2)		

		self.cmm_ref_label = gui_styles_tk.create_label(self.cmm_frame,'')
		self.cmm_ref_label.grid(row=3, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2)	

		self.cmm_v_label = gui_styles_tk.create_label(self.cmm_frame,'')
		self.cmm_v_label.grid(row=4, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2)

		self.cmm_d_label = gui_styles_tk.create_label(self.cmm_frame,'')
		self.cmm_d_label.grid(row=5, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2)
		
		self.cmm_install_label = gui_styles_tk.create_label(self.cmm_frame,'')
		self.cmm_install_label.grid(row=6, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2)	
		
	def setup_buttons(self):
		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit',image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 2, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)
		
		#self.edit_cmm=Button(self.cmm_frame,text='Edit', command= self.edit_cmm)
		#self.edit_cmm.grid(row=1,column=2, pady=5,sticky="nsew")

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)
		
	def set_grid_configures(self):
	
		self.main_scroll_frame.inner.grid_columnconfigure(7, weight=1)
		#self.main_frame.grid_columnconfigure(4, weight=1)
		self.preview_frame.grid_columnconfigure(10, weight=1)
		#self.main_scroll_frame.inner.grid_rowconfigure(9, weight=1)
		
	def update_component(self, window, type):
		
		if type != 'new':
			orig_part_no = self.backend.part_no
			seat_used, lopas = check_seat_used(self.mainapp, self.backend)
		else:
			seat_used = False
			
		self.backend.update_component(window, type)
		self.update_label_text()
		# Redraw the seat
		canvas = [self.backend.ax1, self.backend.ax2]
		canvas_type = 'matplotlib'
		draw_top_down = True
		y = self.backend.get_top_down_y_datum()
		top_down_datum = [0,y]
		draw_side = True
		side_datum = [0,0]
		self.backend.draw_seat(canvas, canvas_type, draw_top_down, top_down_datum, draw_side, side_datum)
		self.canvas.draw()
		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.part_no)
			components_tk.component_renamed(self)
		
		# redraw LOPAs if required
		
		if seat_used:
			for l in lopas:
				l = self.mainapp.frames[l]
				for index, row in enumerate(l.backend.seat_layout[self.backend.side]):
					
					if row[1] == orig_part_no:			
						l.backend.seat_layout[self.backend.side][index][1] = self.backend.title
				l.update_component(l.backend, 'seat')
				#self.mainapp.frames[l].update_lopa_plot()
		#update lopas if part number has changed
		# if orig_part_no != self.backend.part_no:
			# self.update_lopa_tables(orig_part_no)
			# print(self.backend.part_no)		

	def update_label_text(self):
				
		self.top_label.config(text=f'Seat: {self.backend.part_no}')
		self.part_no_label.config(text=f' Part Number: {self.backend.part_no}')
		self.seat_description_label.config(text=f' Description: {self.backend.description}')
		self.manu_label.config(text=f' Manufacturer: {self.backend.manufacturer}')
		self.side_label.config(text=f' Side: {self.backend.side}')
		self.seat_type_label.config(text=f' Seat Type: {self.backend.seat_type}')
		self.iat_label.config(text=f' IAT: {self.backend.iat}')
		self.profile_label.config(text=f' Profile: {self.backend.profile}')
		self.aircraft_label.config(text=f' Aircraft: {self.backend.aircraft_type}')
		#
		self.width_label.config(text=f' Seat Width (in): {self.backend.width}')
		self.width_inbd_label.config(text=f' Seat Width Inbd (in): {self.backend.width_inbd}')
		self.length_aft_label.config(text=f' Length Aft (in): {self.backend.length_aft}')
		self.length_fwd_label.config(text=f' Length Fwd (in): {self.backend.length_fwd}')
		self.cushion_height_label.config(text=f' Cushion Height (in): {self.backend.cushion_height}')
		self.height_label.config(text=f' Total Height (in): {self.backend.height}')
		self.stud_label.config(text=f' Stud Distance (in): {self.backend.stud_distance}')
		self.arm_label.config(text=f' Armrest Width (in): {self.backend.armrest_width}')
		#
		self.srpx_label.config(text=f' SRP X (in): {self.backend.srp_x}')
		self.srpy_label.config(text=f' SRP Y (in): {self.backend.srp_y}')
		#
		self.weight_label.config(text=f' Seat Weight (lbs): {self.backend.weight_lbs}')
		#
		self.cmm_title_label.config(text=f' Title: {self.backend.cmm_title}')
		self.cmm_ref_label.config(text=f' Reference: {self.backend.cmm_ref}')
		self.cmm_v_label.config(text=f' Version: {self.backend.cmm_version}')
		self.cmm_d_label.config(text=f' Date: {self.backend.cmm_date}')
		self.cmm_install_label.config(text=f' Install Task: {self.backend.cmm_install}')

	def edit(self):
		orig_treeview_node = self.backend.treeview_node
		self.w=Edit_Seat_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top)
		
		if self.w.button == 'ok':
				self.update_component(self.w, self.w.mode)
				if orig_treeview_node != self.backend.treeview_node:
					components_tk.aircraft_type_changed(self.mainapp, self)		
					
class Edit_Seat_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_seat):

		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.parent_seat = parent_seat
		self.mode = mode
		self.orig_part_no = None
		
		if mode == 'edit':
			self.orig_part_no = parent_seat.backend.title
			self.seat_used, lopas = check_seat_used(mainapp, parent_seat.backend)
		else:
			self.seat_used = True
			
		self.data_checks = {}
		
		self.setup_label_frames()
		self.setup_widgets()
		
		
		if 'new' in self.mode: #also covers 'new - multiple'
			self.set_default_values()
		elif self.mode != 'edit multiple':
			self.set_values()
			
	def setup_label_frames(self):

		self.details_frame = LabelFrame(self.top,text="Seat Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.dimen_frame = LabelFrame(self.top,text="Seat Dimensions:")
		self.dimen_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.weight_frame = LabelFrame(self.top,text="Seat Weight:")
		self.weight_frame.grid(row=2, column=8, columnspan = 8, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.ref_frame = LabelFrame(self.top,text="Seat Reference:")
		self.ref_frame.grid(row=3, column=8, columnspan = 8, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		if self.mode == 'new multiple':
			self.mul_frame = LabelFrame(self.top,text="Multiple Seats:")
			self.mul_frame.grid(row=2, column=16, columnspan = 8, rowspan = 50,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
			
	def setup_widgets(self):
		# __________ Seat Details __________
		#setup labels
		#if self.mode != 'new multiple':
		labels = ['Seat Part No.:', 'Description:', 'Side:', 'Aircraft:', 'Seat Type:', 'IAT:', 'Profile:', 'Manufacturer:']
		row = 2
		#else:
		#	labels = ['Aircraft:', 'Seat Type:', 'IAT:', 'Profile:', 'Manufacturer:']
		#	row = 5
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)
			
		style = gui_styles_tk.create_entry_style()
		#entries/comboboxes
		if self.mode == 'new multiple' or self.mode == 'edit multiple':
			state = 'disabled'
		else:
			state = 'normal'

		self.part_no_entry=Entry(self.details_frame, width=60, state=state)		
		self.part_no_entry.grid(row=2,column=3, columnspan = 2, padx=2, pady=2,sticky = 'NSEW')
		
		if self.mode not in ['new multiple', 'edit multiple']:
			self.data_checks['Part Number'] = ['title', self.part_no_entry, self.orig_part_no]
			
		self.description_entry=Entry(self.details_frame, width=60, state = state)		
		self.description_entry.grid(row=3,column=3, columnspan=2, padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			if self.seat_used:
				state = 'disabled'
			else:
				state = 'normal'
				
		self.side_combo= ttk.Combobox(self.details_frame, values=['LHS', 'RHS'], state=state)
		self.side_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		if self.mode != 'new multiple':
			self.data_checks['Side'] = ['combo', self.side_combo, 'in values']
		
		
		if 'edit' in self.mode:
			state = 'disabled'
		else:
			state = 'normal'
		
		#self.aircraft_combo= ttk.Combobox(self.details_frame, values=['A320 Family', 'B737 Family'], state=state)
		self.aircraft_combo= ttk.Combobox(self.details_frame, values=['A320 Family'], state=state)
		self.aircraft_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Aircraft Type'] = ['combo', self.aircraft_combo, 'in values', 'Aircraft Type']
		
		self.seat_type_combo= ttk.Combobox(self.details_frame, values=['Triple Economy'], state = 'readonly')
		self.seat_type_combo.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Seat Type'] = ['combo', self.seat_type_combo, 'in values', 'Seat Type']
		
		self.iat_combo= ttk.Combobox(self.details_frame, values=['Yes', 'No'], state='readonly')
		self.iat_combo.grid(row=7,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['IAT'] = ['combo', self.iat_combo, 'in values', 'IAT']
		
		self.profile_combo= ttk.Combobox(self.details_frame, values=['Generic'], state='readonly')
		self.profile_combo.grid(row=8,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Profile'] = ['combo', self.profile_combo, 'in values', 'Profile']
		
		self.manufacturer_entry=Entry(self.details_frame, width=20)		
		self.manufacturer_entry.grid(row=9,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Manufacturer'] = [None, self.manufacturer_entry, None, 'Manufacturer']
		# __________ Seat Dimensions __________
		#setup labels	
		labels = ['Seat Width (in):', 'Seat Width Inbd (in):', 'Seat Length Aft of Front Stud (in):',
					'Seat Length Fwd of Front Stud (in):', 'Stud Distance (in):', 'Headrest Height (in):',
					'Cushion Height (in):', 'Armrest Width (in):']
		gui_styles_tk.create_multiple_labels(self.dimen_frame, labels, 2, 2, 30, 2, 2)
		
		self.w_entry=Entry(self.dimen_frame, width=20, style='Custom.Entry')		
		self.w_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Seat Width'] = ['entry', self.w_entry, 'float positive', 'Width'] #last value used for gen_save_dict_function
		
		self.w_inbd_entry=Entry(self.dimen_frame, width=20)		
		self.w_inbd_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Inboard Width'] = ['entry', self.w_inbd_entry, 'float positive', 'Width Inbd']
		
		self.l_aft_entry=Entry(self.dimen_frame, width=20)		
		self.l_aft_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Aft Length'] = ['entry', self.l_aft_entry, 'float positive', 'Length Aft']
		
		self.l_fwd_entry=Entry(self.dimen_frame, width=20)		
		self.l_fwd_entry.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Forward Length'] = ['entry', self.l_fwd_entry, 'float positive', 'Length Fwd']
		
		self.stud_entry=Entry(self.dimen_frame, width=20)		
		self.stud_entry.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Stud Distance'] = ['entry', self.stud_entry, 'float positive', 'Stud Distance']
		
		self.h_entry=Entry(self.dimen_frame, width=20)		
		self.h_entry.grid(row=7,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Height'] = ['entry', self.h_entry, 'float positive', 'Height']
		
		self.c_entry=Entry(self.dimen_frame, width=20)		
		self.c_entry.grid(row=8,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Cushion Height'] = ['entry', self.c_entry, 'float positive', 'Cushion Height']
		
		self.a_entry=Entry(self.dimen_frame, width=20)		
		self.a_entry.grid(row=9,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Armrest Width'] = ['entry', self.a_entry, 'float positive', 'Armrest Width']
		
		# __________ Seat Weight __________
		#setup labels
		labels = ['Seat Weight (lbs):']
		gui_styles_tk.create_multiple_labels(self.weight_frame, labels, 2, 2, 20, 2, 2)

		self.weight_entry=Entry(self.weight_frame, width=20)		
		self.weight_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Seat Weight'] = ['entry', self.weight_entry, 'float positive', 'Weight']
		
		# __________ Seat Reference Points__________
		#setup labels
		labels = ['SRP X (in):', 'SRP Y (in):']
		gui_styles_tk.create_multiple_labels(self.ref_frame, labels, 2, 2, 20, 2, 2)

		self.srp_x_entry=Entry(self.ref_frame, width=20)		
		self.srp_x_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['SRP X'] = ['entry', self.srp_x_entry, 'float positive', 'SRP X']
		
		self.srp_y_entry=Entry(self.ref_frame, width=20)		
		self.srp_y_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['SRP Y'] = ['entry', self.srp_y_entry, 'float positive', 'SRP Y']
		
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=10,columnspan=2, pady=5,sticky="nsew")

		# cancel button
		self.cancel_button=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.cancel_button.grid(row=8,column=12, columnspan=2, pady=5,sticky="nsew")

		self.button = 'cancel'
		
		#Add blank option if editing multiple seat
		if self.mode == 'edit multiple':
			for c in [self.seat_type_combo, self.iat_combo, self.profile_combo]:
				v = list(c.config()['values'][-1])
				v.append(' ')
				c.config(values=v)
				
	def cleanup(self, button):
	
		if button == 'ok':
			
			if self.mode == 'edit multiple':
				data_checks = {}
				for widget in self.data_checks:
					if self.data_checks[widget][1].get().strip() != '': #ignore blank inputs
						data_checks[widget] = [x for x in self.data_checks[widget]]
						
				data_good, msg = data_input_checks_tk.check_data_input(data_checks, self.mainapp)
			else:
				data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)
		
			if not data_good:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		
			else:
				
				if self.mode != 'edit multiple':
					self.update_variables()
				else:
					self.data_checks = data_checks
					self.updated_variables = {}
					for d in data_checks:
						self.updated_variables[data_checks[d][-1]] = data_checks[d][1].get()

				self.button = 'ok'
				self.top.destroy()
		else: #cancel
			self.top.destroy()
			
	def set_default_values(self):
	
		self.iat_combo.set('No')
		self.profile_combo.set('Generic')
		self.seat_type_combo.set('Triple Economy')
		
		#if self.aircraft_combo.get() == 'A320 Family':
			
		self.w_entry.insert(0,'61.25') #total width
		self.w_inbd_entry.insert(0,'21.0') #width from front stud seat edge
		self.l_aft_entry.insert(0,'24.0') #length aft
		self.l_fwd_entry.insert(0,'2.2') #length fwd
		self.stud_entry.insert(0,'19.0') #distance between studs
		self.h_entry.insert(0,'45.0') #Total height
		self.c_entry.insert(0,'18.5') #cushion height
		self.a_entry.insert(0,'2.0') #cushion height
		
		self.weight_entry.insert(0,'85.0')
		
		self.srp_x_entry.insert(0,'15.0')
		self.srp_y_entry.insert(0,'12.0')

	def set_values(self):

		self.part_no_entry.insert(0,self.parent_seat.backend.part_no)
		self.description_entry.insert(0,self.parent_seat.backend.description)
		self.manufacturer_entry.insert(0,self.parent_seat.backend.manufacturer)
		self.side_combo.set(self.parent_seat.backend.side)
		self.aircraft_combo.set(self.parent_seat.backend.aircraft_type)
		self.seat_type_combo.set(self.parent_seat.backend.seat_type)
		self.iat_combo.set(self.parent_seat.backend.iat)
		self.profile_combo.set(self.parent_seat.backend.profile)
		
		self.w_entry.insert(0,self.parent_seat.backend.width)
		self.w_inbd_entry.insert(0,self.parent_seat.backend.width_inbd)
		self.l_aft_entry.insert(0,self.parent_seat.backend.length_aft)
		self.l_fwd_entry.insert(0,self.parent_seat.backend.length_fwd)
		self.stud_entry.insert(0,self.parent_seat.backend.stud_distance)
		self.h_entry.insert(0,self.parent_seat.backend.height)
		self.c_entry.insert(0,self.parent_seat.backend.cushion_height)
		self.a_entry.insert(0,self.parent_seat.backend.armrest_width)
		self.weight_entry.insert(0,self.parent_seat.backend.weight_lbs)
		self.srp_x_entry.insert(0,self.parent_seat.backend.srp_x)
		self.srp_y_entry.insert(0,self.parent_seat.backend.srp_y)
		
		self.cmm_title = self.parent_seat.backend.cmm_title
		
	def update_variables(self):

		if self.mode != 'new multiple':
			self.part_no = self.part_no_entry.get().strip()
			self.description = self.description_entry.get()
			self.side = self.side_combo.get()

		self.manufacturer = self.manufacturer_entry.get()
		self.aircraft_type = self.aircraft_combo.get()
		self.seat_type = self.seat_type_combo.get()
		self.iat = self.iat_combo.get()
		self.profile = self.profile_combo.get()
		self.width = self.w_entry.get()
		self.width_inbd = self.w_inbd_entry.get()
		self.length_fwd = self.l_fwd_entry.get()
		self.length_aft = self.l_aft_entry.get()
		self.cushion_height = self.c_entry.get()
		self.height = self.h_entry.get()
		self.stud_distance = self.stud_entry.get()
		self.armrest_width = self.a_entry.get()
		self.srp_x = self.srp_x_entry.get()
		self.srp_y = self.srp_y_entry.get()
		self.weight_lbs = self.weight_entry.get()
		#
		if self.parent_seat:
			self.cmm_title = self.parent_seat.backend.cmm_title
			self.cmm_ref = self.parent_seat.backend.cmm_ref
			self.cmm_version = self.parent_seat.backend.cmm_version
			self.cmm_date= self.parent_seat.backend.cmm_date
			self.cmm_install= self.parent_seat.backend.cmm_install
		else:
			self.cmm_title = ''
			self.cmm_ref = ''
			self.cmm_version = ''
			self.cmm_date= ''					
			self.cmm_install= ''					

class Multiple_Seat_Window_Tk(object):
	def __init__(self, mainapp, master):

		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		
		self.setup_label_frames()
		
		self.setup_widgets()
		
	def setup_label_frames(self):
	
		self.details_frame = LabelFrame(self.top,text="Enter Seat Details Below:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		self.comment_text = tk.Text(self.details_frame, width = 90, height = 20)
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		self.default_text = 'Part No., Description, Side (LHS or RHS)'
		self.comment_text.insert('end', self.default_text)
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=4,column=3,columnspan=1, pady=5,sticky="nsew")

		# cancel button
		self.cancel_button=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.cancel_button.grid(row=4,column=4, columnspan=1, pady=5,sticky="nsew")

		self.button = 'cancel'
		
	def cleanup(self, button):
	
		self.button = button
		
		if self.button == 'ok':
		

			self.check_data_input()

			if self.data_ok:
				
				self.top.destroy()
					
		else:
			self.top.destroy()
				
	def check_data_input(self):
		
		self.data_ok = True
		
		titles = []
		
		data = self.comment_text.get("1.0",'end')
		data = data.split('\n')
		
		if data[0] == self.default_text:
			data.pop(0)
		
		if len(data) == 1:
			self.data_ok = False
			msg = 'Enter at Least 1 Seat into Text Box'
		else:
			for d in data:
				if d.strip() != '':
					if len(d.split(',')) != 3: # check format is correct with 2 commas
						self.data_ok = False
						msg = f'{d}\n must be in format Part Number, Description, LHS or RHS'
						break
					
					else:
						if d.split(',')[-1].strip().lower() not in ['lhs', 'rhs']: #check side is LHS or RHS
							self.data_ok = False
							msg = f'{d}\n Side (3rd Field) must be either LHS or RHS'
							break
							
					if self.data_ok: #check for clash with existing components
						
						self.data_ok, msg = data_input_checks_tk.check_title_clash(d.split(',')[0].strip(), None, self.mainapp, 'Part Number')
						
						if not self.data_ok:
							break
							
					if self.data_ok:
						
						if d.split(',')[0].strip() in titles:
							
							self.data_ok = False
							msg = f'{d.split(",")[0].strip()} Entered More Than Once'
							break
						else:
							titles.append(d.split(',')[0].strip())
						
		if not self.data_ok:
			tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
			
		else:
			self.data = data