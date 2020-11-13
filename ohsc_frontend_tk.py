import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk
import double_scrollbar
import comment_box
import data_input_checks_tk
import ohsc_backend as ohsc_bk
import ohsc_draw
import components_tk

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import treeview_functions

import Default_AC_Models

import copy

class OHSC_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.top_label = tk.Label(self, text=('OHSC Layout: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)

		self.backend = ohsc_bk.OHSC_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frames()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_treeviews()
		self.setup_buttons()
		self.add_plot()


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

	def setup_scrollable_frames(self):

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def setup_buttons(self):

		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)

	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="OHSC Layout Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.ohsc_frame = LabelFrame(self.main_scroll_frame.inner,text="OHSCs:")
		self.ohsc_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		
		self.preview_frame = LabelFrame(self.main_scroll_frame.inner,text="Layout Preview:")
		self.preview_frame.grid(row=6, column=0, columnspan = 8, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		self.preview_frame.grid_columnconfigure(4, weight=1)

	def setup_treeviews(self):

		tree_height = 8
		self.LHS_ohsc_tree = ttk.Treeview(self.ohsc_frame,selectmode="extended",columns=("A","B",'C', 'D'),height = tree_height)
		self.LHS_ohsc_tree.grid(row=1,column=0, sticky="nsew")
		self.LHS_ohsc_tree.heading("#0", text="#")
		self.LHS_ohsc_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.LHS_ohsc_tree.heading("A", text="Part Number")   
		self.LHS_ohsc_tree.column("A",minwidth=0,width=250, stretch='NO') 
		self.LHS_ohsc_tree.heading("B", text="Start Frame")  
		self.LHS_ohsc_tree.column("B",minwidth=0,width=100, stretch='NO')
		self.LHS_ohsc_tree.heading("C", text="End Frame")   
		self.LHS_ohsc_tree.column("C",minwidth=0,width=100, stretch='NO')
		self.LHS_ohsc_tree.heading("D", text="Weight Limit (lbs)")   
		self.LHS_ohsc_tree.column("D",minwidth=0,width=120, stretch='NO')
		
		LHS_ohsc_tree_scrollbar = Scrollbar(self.ohsc_frame, command=self.LHS_ohsc_tree.yview)
		LHS_ohsc_tree_scrollbar.grid(row=1, column=1, sticky='nsew')
		self.LHS_ohsc_tree.config(yscrollcommand=LHS_ohsc_tree_scrollbar.set)
		
		self.LHS_ohsc_tree.bind("<Double-1>", lambda event, side='LHS': self.layout_double_click(event, side))
		
		self.RHS_ohsc_tree = ttk.Treeview(self.ohsc_frame,selectmode="extended",columns=("A","B",'C','D'),height = tree_height)
		self.RHS_ohsc_tree.grid(row=1,column=2, sticky="nsew")
		self.RHS_ohsc_tree.heading("#0", text="#")
		self.RHS_ohsc_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.RHS_ohsc_tree.heading("A", text="Part Number")   
		self.RHS_ohsc_tree.column("A",minwidth=0,width=250, stretch='NO') 
		self.RHS_ohsc_tree.heading("B", text="Start Frame")   
		self.RHS_ohsc_tree.column("B",minwidth=0,width=100, stretch='NO')
		self.RHS_ohsc_tree.heading("C", text="End Frame")   
		self.RHS_ohsc_tree.column("C",minwidth=0,width=100, stretch='NO')
		self.RHS_ohsc_tree.heading("D", text="Weight Limit (lbs)")   
		self.RHS_ohsc_tree.column("D",minwidth=0,width=120, stretch='NO')
		
		RHS_ohsc_tree_scrollbar = Scrollbar(self.ohsc_frame, command=self.RHS_ohsc_tree.yview)
		RHS_ohsc_tree_scrollbar.grid(row=1, column=3, sticky='nsew')
		self.RHS_ohsc_tree.config(yscrollcommand=RHS_ohsc_tree_scrollbar.set)

	def setup_labels(self):
		self.ac_label = gui_styles_tk.create_label(self.main_frame,'')
		self.ac_label.grid(row = 2, column = 2,columnspan=2, pady=2,padx=2, sticky="nsew")
		
		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 4,columnspan=8, pady=2,padx=2, sticky="nsew")

	def add_plot(self):

		self.canvas = FigureCanvasTkAgg(self.backend.lopa_figure, self.preview_frame)
		self.canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=8, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")

	def update_component(self, window, type):

		self.backend.update_component(window, type)
		self.update_label_text()

		treeview_functions.write_data_to_treeview(self.LHS_ohsc_tree, 'replace', self.backend.layout['LHS'])
		treeview_functions.write_data_to_treeview(self.RHS_ohsc_tree, 'replace', self.backend.layout['RHS'])

		self.backend.ax1.clear()

		#lopa_draw.draw_aircraft(self.backend, self.backend.ax2, 'matplotlib', [0,0])
		ac_model = Default_AC_Models.A320_Family_Model('A320', 'matplotlib', self.backend.ax1, None, None)

		ac_model.draw_all()

		for side in ['LHS', 'RHS']:
			ohsc_draw.draw_ohsc_layout(self.backend, self.backend.ax1, 'matplotlib',[0,0],side)

		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)
	def update_label_text(self):

		self.top_label.config(text=f'OHSC Layout: {self.backend.title}')
		self.ac_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')
		self.description_label.config(text=f' Description: {self.backend.description}')

	def edit(self):

		self.w = Edit_OHSC_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')

	def layout_double_click(self, event, side):

		if side == 'LHS':
			index, data = treeview_functions.get_current_selection(self.LHS_ohsc_tree)

		self.w=Double_Click_Layout_Window_Tk(self, self.mainapp, self.master, data, index, 'edit', side) #lazy nones, not used
		self.master.wait_window(self.w.top)

		if self.w.button == 'ok':

			self.update_component(self.w, 'edit')

class Edit_OHSC_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_ohsc):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_ohsc = parent_ohsc
		
		self.button = 'cancel'

		self.data_checks = {}
		
		ohsc_bk.setup_variables(self)

		if self.mode == 'edit':
			self.orig_title = parent_ohsc.backend.title
			ohsc_bk.update_variables(self, self.parent_ohsc.backend)
		else:
			self.orig_title = None

		self.setup_label_frames()
		self.setup_widgets()

	def setup_label_frames(self):		
		self.details_frame = LabelFrame(self.top,text="OHSC Layout Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		labels = ['Title:', 'Description:', 'Aircraft:', 'OSHC Layout:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)	
		
		self.title_entry=Entry(self.details_frame, width=20)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_title]
		if self.mode == 'edit':
			self.title_entry.insert(0, self.orig_title)


		self.description_entry=Entry(self.details_frame, width=20)		
		self.description_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		if self.mode == 'edit':
			self.description_entry.insert(0, self.description)

		self.ac_combo= ttk.Combobox(self.details_frame, values=['A320'], state='disabled')
		self.ac_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.ac_combo.set('A320')

		self.layout_combo= ttk.Combobox(self.details_frame, values=['Standard'], state='disabled')
		self.layout_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.layout_combo.set('Standard')

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, pady=5,sticky="nsew")

	def cleanup(self, button):
	
		self.button = button
		
		if self.button == 'ok':

			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)

			if data_good:
				self.title = self.title_entry.get()
				self.description = self.description_entry.get()
				self.aircraft_type = self.ac_combo.get()
				self.layout_type = self.layout_combo.get()

				if self.mode != 'edit':
					bins = [['20','21',10],['21','26',20],['26','30',20],['30','35',20],
						['35','36',20],['36','OW_FWD',10],['OW_FWD','OW_AFT',20],
						['OW_AFT','43',20],['43','51',20], ['51','55',20],
						['55','59',20], ['59','63',20], ['63','64',20]]
				
					for index, b in enumerate(bins):
						b.insert(0, '-')
						b.insert(0, index+1)
					

					self.layout = {'LHS': bins, 'RHS': bins}
				self.top.destroy()
			else:

				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		else:
			self.top.destroy()


class Double_Click_Layout_Window_Tk(object):			
	def __init__(self, parent_ohsc, mainapp, master, bin_data, index, mode, side):
		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp
		self.parent_ohsc = parent_ohsc
		self.bin_data = copy.deepcopy(bin_data)
		self.index = index
		self.mode = mode
		self.bin_data = bin_data
		self.side = side
		
		self.data_checks = {}
		ohsc_bk.setup_variables(self)
		ohsc_bk.update_variables(self, self.parent_ohsc.backend)
		
		self.setup_label_frames()
		self.setup_widgets()
		
		if self.mode == 'edit':
			self.pn_entry.insert(0, bin_data[1])
			self.start_entry.insert(0, bin_data[2])
			self.start_entry.config(state='disabled')
			self.end_entry.insert(0, bin_data[3])
			self.end_entry.config(state='disabled')
			self.weight_entry.insert(0, bin_data[4])

		self.button = 'cancel'
	def setup_label_frames(self):
	
		self.options_frame = LabelFrame(self.top,text="Options:")
		self.options_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_widgets(self):
	
		labels = ['Part Number:', 'Start Frame', 'End Frame', 'Weight Limit (lbs)']
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, labels, row, 2, 20, 2, 2)			

		self.pn_entry=Entry(self.options_frame, width=20)		
		self.pn_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.start_entry=Entry(self.options_frame, width=20)		
		self.start_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.end_entry=Entry(self.options_frame, width=20)		
		self.end_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.weight_entry=Entry(self.options_frame, width=20)		
		self.weight_entry.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Weight'] = ['entry', self.weight_entry, 'float positive', 'Weight']

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")
		
	def cleanup(self,button):
		
		self.button = button
		if button == 'ok':

			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)

			if data_good:

				bin_part_no = self.pn_entry.get()
				bin_start = self.start_entry.get()
				bin_end = self.end_entry.get()
				weight = self.weight_entry.get()

				self.layout[self.side][self.index] = [self.bin_data[0], bin_part_no, bin_start, bin_end, weight]
				self.top.destroy()

			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)

		else:
			self.top.destroy()