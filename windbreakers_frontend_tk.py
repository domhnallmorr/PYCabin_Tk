import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import windbreaker_backend as wb_bk
import gui_styles_tk
import components_tk
import data_input_checks_tk

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import double_scrollbar
import comment_box

def check_windbreaker_used(mainapp, wb_backend):
	
	wb_used = False
	lopas = []
	lopa_dict = components_tk.get_all_components(mainapp, 'LOPAs')
	
	for l in lopa_dict['All']:
		for w in mainapp.frames[l].backend.windbreakers:
			if wb_backend.title == w[0]:
				wb_used = True
				lopas.append(l)
				break
	
	return wb_used, lopas
	
class Windbreaker_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.top_label = tk.Label(self, text=('Windbreaker: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)
		
		self.backend = wb_bk.Windbreaker_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frame()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_buttons()
		self.add_plot()
		self.set_grid_configures()


	def setup_scrollable_frame(self):
		
		#self.main_scroll_frame = scrollable_frame.ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)
		
	def set_grid_configures(self):
	
		self.main_scroll_frame.inner.grid_columnconfigure(7, weight=1)
		self.main_frame.grid_columnconfigure(4, weight=1)
		self.preview_frame.grid_columnconfigure(10, weight=1)
		#self.main_scroll_frame.frame.grid_rowconfigure(9, weight=1)		
		
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
		
		
	def setup_label_frames(self):
		main_frame = self.main_scroll_frame.inner
		self.main_frame = LabelFrame(main_frame,text="Windbreaker Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.dimensions_frame = LabelFrame(main_frame,text="Windbreaker Dimensions:")
		self.dimensions_frame.grid(row=4, column=0, columnspan = 2, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.options_frame = LabelFrame(main_frame,text="Windbreaker Reference:")
		self.options_frame.grid(row=6, column=0, columnspan = 2, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.preview_frame = LabelFrame(main_frame,text="Windbreaker Preview:")
		self.preview_frame.grid(row=4, column=2, columnspan = 6, rowspan = 6,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.cmm_frame = LabelFrame(self.docs_tab,text="CMM Details:")
		self.cmm_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)		
		
	def setup_labels(self):

		#self.top_label.config(background='red')
		self.part_no_label = gui_styles_tk.create_label(self.main_frame,'')
		self.part_no_label.grid(row = 2, column = 0,pady=2,padx=2, sticky="nsew")
		
		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 1, columnspan=6,pady=2,padx=2, sticky="nsew")
		self.description_label.configure(width=100)
			
		self.side_label = gui_styles_tk.create_label(self.main_frame,'')
		self.side_label.grid(row = 3, column = 0,pady=2,padx=2, sticky="nsew")

		self.aircraft_label = gui_styles_tk.create_label(self.main_frame,'')
		self.aircraft_label.grid(row = 3, column = 1,pady=2,padx=2,sticky="nsew")		
		self.aircraft_label.configure(width=25)
		
		#self.preview_frame.grid_columnconfigure(10, weight=1)
		# ___ Dimensions ____

		self.thickness_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.thickness_label.grid(row = 2, column = 0,pady=2,sticky="nsew")	

		self.width_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.width_label.grid(row = 3, column = 0,pady=2,sticky="nsew")	

		self.height_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.height_label.grid(row = 4, column = 0,pady=2,sticky="nsew")	

		self.dist_cl_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.dist_cl_label.grid(row = 5, column = 0,pady=2,sticky="nsew")	
		
		self.joggle_width_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.joggle_width_label.grid(row = 6, column = 0,pady=2,sticky="nsew")	

		self.joggle_lower_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.joggle_lower_label.grid(row = 7, column = 0,pady=2,sticky="nsew")	

		self.joggle_upper_label = gui_styles_tk.create_label(self.dimensions_frame,'')
		self.joggle_upper_label.grid(row = 8, column = 0,pady=2,sticky="nsew")
		
		# ___ Options ____
		self.joggle_label = gui_styles_tk.create_label(self.options_frame,'')
		self.joggle_label.grid(row = 3, column = 0,pady=2,sticky="nsew")	

		self.bassinet_label = gui_styles_tk.create_label(self.options_frame,'')
		self.bassinet_label.grid(row = 4, column = 0,pady=2,sticky="nsew")

		# ___ CMM ___
		
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

		self.cmm_remove_label = gui_styles_tk.create_label(self.cmm_frame,'')
		self.cmm_remove_label.grid(row=7, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2)
		
	def setup_buttons(self):
		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 2, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.edit_cmm=Button(self.cmm_frame,text='Edit', command= self.edit_cmm)
		self.edit_cmm.grid(row=1,column=2, pady=5,sticky="nsew")

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)
		
	def update_label_text(self):
				
		self.top_label.config(text=f'Windbreaker: {self.backend.title}')
		self.part_no_label.config(text=f' Part Number: {self.backend.part_no}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.side_label.config(text=f' Side: {self.backend.side}')
		self.aircraft_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')
		
		# ___ Dimensions ____
		self.thickness_label.config(text=f' Thickness (in): {self.backend.thickness}')
		self.width_label.config(text=f' Width (in): {self.backend.width}')
		self.height_label.config(text=f' Height (in): {self.backend.height}')
		self.dist_cl_label.config(text=f' Distance From C/L (in): {self.backend.dist_from_cl}')
		
		if self.backend.joggle == 'Yes':
			self.joggle_width_label.config(text=f' Joggle Width (in): {self.backend.joggle_width}')
			self.joggle_lower_label.config(text=f' Joggle Lower Height (in): {self.backend.joggle_lower}')
			self.joggle_upper_label.config(text=f' Joggle Upper Height (in): {self.backend.joggle_upper}')
		else:
			self.joggle_width_label.config(text=f' Joggle Width (in): N/A')
			self.joggle_lower_label.config(text=f' Joggle Lower Height (in): N/A')
			self.joggle_upper_label.config(text=f' Joggle Upper Height (in): N/A')		
		# ___ Options ____
		self.joggle_label.config(text=f' Joggle: {self.backend.joggle}')
		self.bassinet_label.config(text=f' Bassinet: {self.backend.bassinet}')

		# ___ CMM ___
		self.cmm_title_label.config(text=f' Title: {self.backend.cmm_title}')
		self.cmm_ref_label.config(text=f' Reference: {self.backend.cmm_ref}')
		self.cmm_v_label.config(text=f' Version: {self.backend.cmm_version}')
		self.cmm_d_label.config(text=f' Date: {self.backend.cmm_date}')
		self.cmm_install_label.config(text=f' Install Task: {self.backend.cmm_install}')
		self.cmm_remove_label.config(text=f' Remove Task: {self.backend.cmm_remove}')
		
	def update_component(self, window, type):
		
		self.backend.update_component(window, type)
		self.update_label_text()

		canvas = [self.backend.ax1, self.backend.ax2]
		canvas_type = 'matplotlib'
		draw_top_down = True
		y = self.backend.get_top_down_y_datum()
		top_down_datum = [0,y]
		draw_side = True
		side_datum = [0,0]
		self.backend.draw_wb(canvas, canvas_type, draw_top_down, top_down_datum, draw_side, side_datum)

		# redraw LOPAs if required
		wb_used, lopas = check_windbreaker_used(self.mainapp, self.backend)
		if wb_used:
			for l in lopas:
				self.mainapp.frames[l].update_lopa_plot()
		self.mainapp.update_titlebar('edit')
				
	def edit(self):
		orig_treeview_node = self.backend.treeview_node
		self.w=Edit_Windbreaker_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)
		if self.w.button == 'ok':
				self.update_component(self.w, self.w.mode)
				
	def add_plot(self):
		
		self.canvas = FigureCanvasTkAgg(self.backend.figure, self.preview_frame)
		self.canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=11, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")	
		self.preview_frame.grid_columnconfigure(10, weight=1)

	def edit_cmm(self):
	
		self.w=Edit_CMM_Window_Tk(self.mainapp, self.master, self, 'edit', self)
		self.master.wait_window(self.w.top)

		if self.w.button == 'ok':
			#
			self.update_component(self.w, 'edit')
			
class Edit_Windbreaker_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_wb):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_wb = parent_wb

		self.orig_part_no = None
		
		if mode == 'edit':
			self.orig_part_no = parent_wb.backend.title
			self.wb_used, lopas = check_windbreaker_used(mainapp, self.parent_wb.backend)
		else:
			self.wb_used = False
			
		self.data_checks = {}
		
		self.setup_label_frames()
		self.setup_widgets()
		
		if mode =='new':
			self.set_default_values()
		else:
			self.set_values()
		self.joggle_selected()
		
		self.button = 'cancel'
	def setup_label_frames(self):
	
		self.details_frame = LabelFrame(self.top,text="Windbreaker Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.dimen_frame = LabelFrame(self.top,text="Windbreaker Dimensions:")
		self.dimen_frame.grid(row=6, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.options_frame = LabelFrame(self.top,text="Additonal Options:")
		self.options_frame.grid(row=2, column=8, columnspan = 8, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
		
		if self.mode == 'edit':
			state = 'disabled' #for combobox
		else:
			state = 'normal'
		labels = ['Title:', 'Part No.:', 'Description:', 'Side:', 'Aircraft:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)

		self.title_entry=Entry(self.details_frame, width=60)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_part_no]
		
		self.part_no_entry=Entry(self.details_frame, width=60)		
		self.part_no_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		#self.data_checks['Part Number'] = ['title', self.part_no_entry, self.orig_part_no]
		
		self.description_entry=Entry(self.details_frame, width=60)		
		self.description_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.side_combo= ttk.Combobox(self.details_frame, values=['LHS', 'RHS'])
		self.side_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Side'] = ['combo', self.side_combo, 'in values']
		if self.wb_used:
			self.side_combo.config(state='disabled')
		
		self.aircraft_combo= ttk.Combobox(self.details_frame, values=['A320 Family'], state=state)
		self.aircraft_combo.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.aircraft_combo.set('A320 Family')
		self.data_checks['Aircraft Type'] = ['combo', self.aircraft_combo, 'in values']
		
		labels = ['Thickness (in)', 'Width (in) ', 'Height (in):', 'Distance From C/L (in):',
				'Joggle Width (in)','Lower Joggle Height (in)', 'Upper Joggle Height (in)']
		row = 2
		gui_styles_tk.create_multiple_labels(self.dimen_frame, labels, row, 2, 20, 2, 2)		
		
		self.thick_entry=Entry(self.dimen_frame, width=20)		
		self.thick_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')	
		self.data_checks['Thickness'] = ['entry', self.thick_entry, 'float positive', 'Width Inbd']
		
		self.width_entry=Entry(self.dimen_frame, width=20)		
		self.width_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Width'] = ['entry', self.width_entry, 'float positive', 'Width Inbd']
		
		self.height_entry=Entry(self.dimen_frame, width=20)		
		self.height_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Height'] = ['entry', self.height_entry, 'float positive', 'Width Inbd']
		
		self.dist_cl_entry=Entry(self.dimen_frame, width=20)		
		self.dist_cl_entry.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Distance From Center Line'] = ['entry', self.dist_cl_entry, 'float positive', 'Width Inbd']
		
		self.joggle_width_entry=Entry(self.dimen_frame, width=20)		
		self.joggle_width_entry.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Joggle Width'] = ['entry', self.joggle_width_entry, 'float positive', 'Joggle Width']
		
		self.joggle_lower_entry=Entry(self.dimen_frame, width=20)		
		self.joggle_lower_entry.grid(row=7,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Joggle Lower'] = ['entry', self.joggle_lower_entry, 'float positive', 'Joggle Lower']

		self.joggle_upper_entry=Entry(self.dimen_frame, width=20)		
		self.joggle_upper_entry.grid(row=8,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Joggle Upper'] = ['entry', self.joggle_upper_entry, 'float positive', 'Joggle Upper']
		
		labels = ['Joggle:', 'Bassinet']
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, labels, row, 2, 20, 2, 2)

		self.joggle_combo= ttk.Combobox(self.options_frame, values=['Yes', 'No'], state='readonly')
		self.joggle_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.joggle_combo.bind("<<ComboboxSelected>>", self.joggle_selected)
		self.data_checks['Joggle'] = ['combo', self.joggle_combo, 'in values']
		
		self.bassinet_combo= ttk.Combobox(self.options_frame, values=['Yes', 'No'], state='readonly')
		self.bassinet_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Bassinet'] = ['combo', self.bassinet_combo, 'in values']
		


		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=4, columnspan=2, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=6, columnspan=2, pady=5,sticky="nsew")

		self.button = 'cancel'

	def set_default_values(self):

		self.thick_entry.insert(0,'1.18')
		self.width_entry.insert(0,'56.53')
		self.height_entry.insert(0,'59.72')
		self.dist_cl_entry.insert(0,'11.496')
		self.joggle_width_entry.insert(0,'3.0')
		self.joggle_lower_entry.insert(0,'20.0')
		self.joggle_upper_entry.insert(0,'30.0')
		
		self.description_entry.insert(0, 'Windbreaker')
		
		self.joggle_combo.set('No')
		self.bassinet_combo.set('No')

	def set_values(self):
		self.title_entry.insert(0, self.parent_wb.backend.title)
		self.aircraft_combo.set(self.parent_wb.backend.aircraft_type)
		self.part_no_entry.insert(0, self.parent_wb.backend.part_no)
		self.description_entry.insert(0, self.parent_wb.backend.description)
		self.side_combo.set(self.parent_wb.backend.side)
		self.thick_entry.insert(0, self.parent_wb.backend.thickness)
		self.width_entry.insert(0, self.parent_wb.backend.width)
		self.height_entry.insert(0, self.parent_wb.backend.height)
		self.dist_cl_entry.insert(0, self.parent_wb.backend.dist_from_cl)
		self.joggle_combo.set(self.parent_wb.backend.joggle)
		self.joggle_width_entry.insert(0, self.parent_wb.backend.joggle_width)
		self.joggle_lower_entry.insert(0, self.parent_wb.backend.joggle_lower)
		self.joggle_upper_entry.insert(0, self.parent_wb.backend.joggle_upper)
		self.bassinet_combo.set(self.parent_wb.backend.bassinet)
				
	def joggle_selected(self, event=None):
		
		if self.joggle_combo.get() == 'No':
			self.joggle_width_entry.grid_remove()
			self.joggle_lower_entry.grid_remove()
			self.joggle_upper_entry.grid_remove()
			
		elif self.joggle_combo.get() == 'Yes':
			self.joggle_width_entry.grid()
			self.joggle_lower_entry.grid()
			self.joggle_upper_entry.grid()

	def cleanup(self, button):
		self.button = button
		if button == 'ok':
			
			data_checks = {}
			for d in self.data_checks:
				add = True
				if d in ['Joggle Width', 'Joggle Upper', 'Joggle Width',]:
					if self.joggle_combo.get() != 'Yes':
						add = False
						
				if add:
					data_checks[d] = self.data_checks[d]
		
			data_good, msg = data_input_checks_tk.check_data_input(data_checks, self.mainapp)
			
			if data_good:
				self.title = self.title_entry.get()
				self.aircraft_type = self.aircraft_combo.get()
				self.part_no = self.part_no_entry.get()
				self.description = self.description_entry.get()
				self.side = self.side_combo.get()
				self.thickness = self.thick_entry.get()
				self.width = self.width_entry.get()
				self.height = self.height_entry.get()
				self.dist_from_cl = self.dist_cl_entry.get()
				self.joggle = self.joggle_combo.get()
				self.joggle_width = self.joggle_width_entry.get()
				self.joggle_lower = self.joggle_lower_entry.get()
				self.joggle_upper = self.joggle_upper_entry.get()
				self.bassinet = self.bassinet_combo.get()

				if self.mode == 'edit':
					self.cmm_title = self.parent_wb.backend.cmm_title
					self.cmm_ref = self.parent_wb.backend.cmm_ref
					self.cmm_version = self.parent_wb.backend.cmm_version
					self.cmm_date= self.parent_wb.backend.cmm_date
					self.cmm_install= self.parent_wb.backend.cmm_install
					self.cmm_remove= self.parent_wb.backend.cmm_install
				else:
					print('i am here')
					self.cmm_title = 'blah'
					self.cmm_ref = ''
					self.cmm_version = ''
					self.cmm_date= ''					
					self.cmm_install= ''
					self.cmm_remove= ''
					
				self.top.destroy()
				
			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
				
		else:
			self.top.destroy()



class Edit_CMM_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_seat):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_seat = parent_seat
			
		#label frame
		self.setup_label_frames()
		self.setup_widgets()
		
		self.setup_variables()
		
		self.button = 'cancel'
				
	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.top,text="Options:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	
		
	def setup_widgets(self):
	
		labels = ['Title:', 'Reference:', 'Version:', 'Date:', 'Install Task', 'Remove Task']
		row = 2
		gui_styles_tk.create_multiple_labels(self.main_frame, 20, labels, row, 2, 2, 2)
		
		self.title_entry=Entry(self.main_frame, width=20)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.ref_entry=Entry(self.main_frame, width=20)		
		self.ref_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.v_entry=Entry(self.main_frame, width=20)		
		self.v_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.d_entry=Entry(self.main_frame, width=20)		
		self.d_entry.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.install_entry=Entry(self.main_frame, width=20)		
		self.install_entry.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.remove_entry=Entry(self.main_frame, width=20)		
		self.remove_entry.grid(row=7,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=4,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=4,column=4, pady=5,sticky="nsew")

	def setup_variables(self):
	
		wb_bk.Windbreaker_Backend.setup_variables(self)
		wb_bk.Windbreaker_Backend.update_variables(self, self.parent_seat.backend)

		self.title_entry.insert(0, self.cmm_title)
		self.ref_entry.insert(0, self.cmm_ref)
		self.v_entry.insert(0, self.cmm_version)
		self.d_entry.insert(0, self.cmm_date)
		self.install_entry.insert(0, self.cmm_install)
		self.remove_entry.insert(0, self.cmm_remove)
	def cleanup(self, button):
	
		self.button = button
		
		if button == 'ok':
			
			self.cmm_title = self.title_entry.get()
			self.cmm_ref = self.ref_entry.get()
			self.cmm_version = self.v_entry.get()
			self.cmm_date = self.d_entry.get()
			self.cmm_install = self.install_entry.get()
			self.cmm_remove = self.remove_entry.get()
			
			self.top.destroy()
			
		else:
			self.top.destroy()					