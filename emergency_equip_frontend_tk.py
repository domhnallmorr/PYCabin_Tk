
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

	def setup_treeviews(self):
		pass

	def setup_buttons(self):
		pass

	def update_label_text(self):
		self.top_label.config(text=f' Emergency Equipment: {self.backend.title}')
		self.part_no_label.config(text=f' Part Number: {self.backend.title}')
		self.manu_label.config(text=f' Manufacturer: {self.backend.manufacturer}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.type_label.config(text=f' Type: {self.backend.equipment_type}')


	def update_component(self, window, type, redraw = True):
		
		self.backend.update_component(window, type)
		self.update_label_text()



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
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_part_no]
		
		self.description_entry=Entry(self.main_frame, width=50)		
		self.description_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.equip_type_combo= ttk.Combobox(self.main_frame, values=self.available_equipment)
		self.equip_type_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.ac_combo= ttk.Combobox(self.main_frame, values=['A320'])
		self.ac_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.weight_entry = Entry(self.main_frame, width=50)
		self.weight_entry.grid(row=5, column=3,padx=2, pady=2,sticky = 'NSEW')

		self.manu_entry = Entry(self.main_frame, width=50)
		self.manu_entry.grid(row=6, column=3,padx=2, pady=2,sticky = 'NSEW')

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
			self.button = 'ok'
			self.top.destroy()
			
		else:
			self.top.destroy()
		
		
		