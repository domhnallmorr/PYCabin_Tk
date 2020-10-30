
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import changes_backend as changes_bk
import gui_styles_tk
import components_tk

import data_input_checks_tk
import comment_box
import double_scrollbar
import treeview_functions

import service_bulletin

class Change_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.top_label = tk.Label(self, text=('Change: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)
		
		self.backend = changes_bk.Change_Backend(self, mainapp)

		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frames()		
		self.setup_label_frames()
		self.setup_labels()
		self.setup_buttons()
		self.setup_treeviews()
		
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
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="Change Details:")
		self.main_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.mod_frame = LabelFrame(self.main_scroll_frame.inner,text="Mods:")
		self.mod_frame.grid(row=4, column=2, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	
		
	def setup_labels(self):
	
		self.sb_label = gui_styles_tk.create_label(self.main_frame,'')
		self.sb_label.grid(row = 3, column = 0,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.sb_ref_label = gui_styles_tk.create_label(self.main_frame,'')
		self.sb_ref_label.grid(row = 3, column = 2,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.out_label = gui_styles_tk.create_label(self.main_frame,'')
		self.out_label.grid(row = 4, column = 0,columnspan=4, pady=2,padx=2, sticky="nsew")
		
	def setup_buttons(self):
	
		self.gen_doc_btn = Button(self.main_frame, text='Write Documents', command = self.gen_documents)
		self.gen_doc_btn.grid(row = 0, column=0, sticky='nsew')

	def setup_treeviews(self):

		self.add_mod_btn = Button(self.mod_frame, text = 'Add', image = self.mainapp.add_icon2, compound = LEFT,
								command =  lambda event=None, mode='new': self.add_mod(event, mode))
		self.add_mod_btn.grid(row = 1, column = 0, columnspan = 1, sticky = 'NSEW')
		
		self.mod_tree = ttk.Treeview(self.mod_frame, selectmode="extended",columns=("A","B",),height = 3)
		self.mod_tree.heading("#0", text="Mod Type")
		self.mod_tree.column("#0",minwidth=0,width=300, stretch='NO')
		self.mod_tree.heading("A", text="Mod Title")	  
		self.mod_tree.column("A",minwidth=0,width=300, stretch='NO') 
		self.mod_tree.heading("B", text="Applicable Aircraft")	  
		self.mod_tree.column("B",minwidth=0,width=300, stretch='NO')
		self.mod_tree.grid(row = 2, column = 0, columnspan = 8, sticky = 'NSEW')
		#self.mod_tree.bind("<Double-1>", lambda event, type='Lav', mode='edit': self.add_monument(event, type, mode))
		
	def setup_scrollable_frames(self):

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def update_label_text(self):
	
		self.top_label.config(text=f'Change: {self.backend.title}')
		self.sb_label.config(text=f' Service Bulletin Title: {self.backend.sb_title}')
		self.sb_ref_label.config(text=f' Service Bulletin Number/Ref: {self.backend.sb_number}')
		self.out_label.config(text=f' Output Dir: {self.backend.output_dir}')
		
		
	def update_component(self, window, type):
		
		self.backend.update_component(window, type)
		self.update_label_text()
		
		
		treeview_functions.write_data_to_treeview(self.mod_tree, 'replace', self.backend.mods)
	
	def add_mod(self, event, mode):
		self.w=Add_Mod_Window(self, self.mainapp, self.master, mode)
		self.master.wait_window(self.w.top)	

		if self.w.button == 'ok':
		
			self.update_component(self.w, 'edit')

	def gen_documents(self):
	
		self.sb = service_bulletin.Service_Bulletin(self.mainapp, self.backend)
		service_bulletin.Service_Bulletin_Writer(self.sb)
		
class Add_Mod_Window():
	def __init__(self, change, mainapp, master, mode):
	
		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp

		self.change = change
		self.mode = mode
		
		self.data_checks = {}
		
		self.avail_aircraft = components_tk.get_all_components(self.mainapp, 'Aircraft')
		self.current_ac = None
		
		changes_bk.setup_variables(self)
		changes_bk.update_variables(self, self.change.backend)

		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
	
		self.options_frame = LabelFrame(self.top,text="Mod:")
		self.options_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		#self.aircraft_frame = LabelFrame(self.top,text="Applicable Aircraft:")
		#self.aircraft_frame.grid(row=6, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		#create label frame for each aircraft type

		self.ac_label_frames = {}
		
		for ac in self.avail_aircraft.keys():
			self.ac_label_frames[ac] = LabelFrame(self.top,text=f"Applicable {ac} Aircraft:")

	def setup_widgets(self):

		labels = ['Mod Type:', 'Mod Title:', ]
			
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, labels, row, 2, 20, 2, 2)
		
		self.type_combo= ttk.Combobox(self.options_frame, values=['LOPA'],state='readonly')
		self.type_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.type_combo.bind("<<ComboboxSelected>>", self.type_selected)

		self.mod_combo= ttk.Combobox(self.options_frame, values=[],state='readonly')
		self.mod_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.mod_combo.bind("<<ComboboxSelected>>", self.mod_selected)
		
		self.ac_checkboxes = {}
		
		for ac_type in self.avail_aircraft.keys():
			
			self.ac_checkboxes[ac_type] = {}
			row = 2
			
			for msn in self.avail_aircraft[ac_type]:
				var = tk.IntVar()
				self.ac_checkboxes[ac_type][msn] = Checkbutton(self.ac_label_frames[ac_type], text=msn, variable=var)
				self.ac_checkboxes[ac_type][msn].grid(row=row,column=3,padx=2, pady=2,sticky = 'NSEW')
				self.ac_checkboxes[ac_type][msn].val = var
				row+= 1

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=10,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=10,column=4, pady=5,sticky="nsew")

		self.button = 'cancel'
		
	
	def type_selected(self, event):
	
		if self.type_combo.get() == 'LOPA':
			
			lopas = components_tk.get_all_components(self.mainapp, 'LOPAs')
		
			self.mod_combo.config(values=lopas['All'])
	
	def mod_selected(self, event):
		
		ac = self.mainapp.frames[self.mod_combo.get()].backend.aircraft_type
		
		if self.current_ac != ac:
			
			if self.current_ac:
				self.ac_label_frames[self.current_ac].grid_forget()
			
		self.ac_label_frames[ac].grid(row=6, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.current_ac = ac

	def cleanup(self, button):
	
		self.button = button
		
		if self.button == 'ok':
			
			ac = []
			
			for msn in self.ac_checkboxes[self.current_ac]:
				if self.ac_checkboxes[self.current_ac][msn].val.get() == 1:
					ac.append(msn)
					
			self.mods.append([self.type_combo.get(), self.mod_combo.get(), ','.join(ac)])
			
			self.top.destroy()
		else:
		
			self.top.destroy()
			
class Edit_Change_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_change):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_change = parent_change

		self.orig_title = None
		
		if mode == 'edit':
			self.orig_title = parent_change.backend.title
			
		changes_bk.setup_variables(self)
		self.data_checks = {}
		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
		self.details_frame = LabelFrame(self.top,text="Change Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		
	def setup_widgets(self):

		labels = ['Title:', 'Serivce Bulletin Title', 'Serivce Bulletin Number/Ref:', 'Output Directory:']
		row = 1
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)
		
		self.title_entry=Entry(self.details_frame, width=40)		
		self.title_entry.grid(row=1,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.title]	

		self.sb_entry=Entry(self.details_frame, width=40)		
		self.sb_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.sb_ref_entry=Entry(self.details_frame, width=40)		
		self.sb_ref_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.out_entry=Entry(self.details_frame, width=80)		
		self.out_entry.grid(row=4,column=3, columnspan=3, padx=2, pady=2,sticky = 'NSEW')
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, pady=5,sticky="nsew")

		self.button = 'cancel'		
	
	def cleanup(self,button):
	
		if button == 'ok':
			#checks
			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)
			
			if data_good:
				
				self.title = self.title_entry.get()
				self.sb_title = self.sb_entry.get()
				self.sb_number = self.sb_ref_entry.get()
				self.output_dir = self.out_entry.get()
				
				self.button = 'ok'
				
				self.top.destroy()
				
		else:
		
			self.top.destroy()
				
