import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import aircraft_backend as ac_bk
import gui_styles_tk
import components_tk

import data_input_checks_tk
import comment_box

def add_aircraft(main_app):
	#launch the new aircraft Window
	mode = 'new'
	main_app.w=Edit_Aircraft_Window_Tk(mainapp, main_app.master, mode)
	main_app.master.wait_window(main_app.w.top)  

	if main_app.w.button == 'ok':
		
		#create aircraft class
		new_ac = Aircraft_Page_Tk(container=self.container, controller=main_app)
		new_ac.update_component(self.w, 'new')
		#self.id = self.w.id.get()

class Aircraft_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp
		
		self.backend = ac_bk.Aircraft_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		
		self.setup_label_frames()
		self.setup_labels()
		self.setup_buttons()
	def setup_notebook(self):
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.amm_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.amm_tab, text = "AMM Tasks")
		self.note.add(self.comments_tab, text = "Comments")
		
		self.note.grid(row=1,column=0,sticky='NSEW')

		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
	
	def setup_label_frames(self):
		self.main_frame = LabelFrame(self.main_tab,text="Aircraft Details:")
		self.main_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.amm_seats_frame = LabelFrame(self.amm_tab,text="Seat Installation Tasks:")
		self.amm_seats_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	
		
	def setup_labels(self):	
	
		self.top_label = tk.Label(self, text=('Aircraft: '),font=self.mainapp.title_font)
		self.top_label.grid(row=0,column=0,columnspan=24,stick='W')
		
		self.ac_label = gui_styles_tk.create_label(self.main_frame,'')
		self.ac_label.grid(row=2, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.msn_label = gui_styles_tk.create_label(self.main_frame,'')
		self.msn_label.grid(row=3, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.co_label = gui_styles_tk.create_label(self.main_frame,'')
		self.co_label.grid(row=4, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.go_label = gui_styles_tk.create_label(self.main_frame,'')
		self.go_label.grid(row=5, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		# ____ AMM Seats ______
		
		self.amm_seats_uninstl_label = gui_styles_tk.create_label(self.amm_seats_frame,'')
		self.amm_seats_uninstl_label.grid(row=2, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)		

		self.amm_seats_instl_label = gui_styles_tk.create_label(self.amm_seats_frame,'')
		self.amm_seats_instl_label.grid(row=3, column=2, columnspan=3, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	


	def setup_buttons(self):
		self.edit_button=Button(self.main_frame,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT, command= self.edit)
		self.edit_button.grid(row=1,column=2, pady=5,sticky="nsew", ipadx=2, ipady=2)
	
		self.edit_seat_amm_btn=Button(self.amm_seats_frame,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT, command= lambda type='seat': self.edit_ipc(type))
		self.edit_seat_amm_btn.grid(row=1,column=2, pady=5, sticky="nsew", ipadx=2, ipady=2)
		
		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)
		
	def update_label_text(self):
		self.ac_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')
		self.msn_label.config(text=f' MSN: {self.backend.msn}')
		self.co_label.config(text=f' Current Operator: {self.backend.current_operator}')
		self.go_label.config(text=f' Go To Operator: {self.backend.go_to_operator}')
		
		# ____ AMM Seats ____
		self.amm_seats_uninstl_label.config(text=f' Seat Removal: {self.backend.seats_uninstl_task}')
		self.amm_seats_instl_label.config(text=f' Seat Installation: {self.backend.seats_instl_task}')

		
		self.top_label.config(text=f'Aircraft: {self.backend.msn}')


	def update_component(self, window, type):

		self.backend.update_component(window, type)
		self.update_label_text()
		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.msn)
			components_tk.component_renamed(self)
		
	def edit(self):
		orig_treeview_node = self.backend.treeview_node
		self.w=Edit_Aircraft_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top) 	
		
		if self.w.button == 'ok':
			#
			self.update_component(self.w, 'edit')
			
			if orig_treeview_node != self.backend.treeview_node:
				components_tk.aircraft_type_changed(self.mainapp, self)
	
	def edit_ipc(self, type):
		
		self.w=Edit_IPC_Window_Tk(self.mainapp, self.master, self, 'edit', self, type)
		self.master.wait_window(self.w.top)

		if self.w.button == 'ok':
			#
			self.update_component(self.w, 'edit')

			
class Edit_Aircraft_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_ac):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_ac = parent_ac
		
		if self.mode == 'edit':
			self.orig_msn = parent_ac.backend.msn
		else:
			self.orig_msn = None

		self.data_checks = {}
		
		ac_bk.Aircraft_Backend.setup_variables(self)
		#label frame
		self.setup_label_frames()
		
		# ______ Aircraft Type ______
		self.label = tk.Label(self.main_frame,width = 20, text='Aircraft Type:')
		self.label.grid(row=0,column=0,padx=5, pady=5,sticky = 'NSEW')
		#self.id = tk.StringVar()
		#self.ac_entry=Entry(top, width=20)
		self.ac_combo = ttk.Combobox(self.main_frame, values=['A320', 'A319', 'B737-800'], state='readonly')
		self.ac_combo.grid(row=0,column=1,padx=5, pady=5,sticky = 'NSEW')
		
		if mode == 'edit':
			self.ac_combo.set(self.parent_ac.backend.aircraft_type)
			self.ac_combo.config(state='disabled')
		else:
			self.ac_combo.set('A320')
		
		# ______ MSN ______
		self.label = tk.Label(self.main_frame,width = 20, text='MSN:')
		self.label.grid(row=1,column=0,padx=5, pady=5,sticky = 'NSEW')
		self.msn_entry=Entry(self.main_frame, width=20)		
		self.msn_entry.grid(row=1,column=1,padx=5, pady=5,sticky = 'NSEW')
		self.data_checks['MSN'] = ['title', self.msn_entry, self.orig_msn]
		
		# ______ Operators ______
		self.label = tk.Label(self.main_frame,width = 20, text='Current Operator:')
		self.label.grid(row=2,column=0,padx=5, pady=5,sticky = 'NSEW')
		self.current_operator_entry=Entry(self.main_frame, width=20)	
		self.current_operator_entry.grid(row=2,column=1,padx=5, pady=5,sticky = 'NSEW')
		
		self.label = tk.Label(self.main_frame,width = 20, text='Go To Operator:')
		self.label.grid(row=3,column=0,padx=5, pady=5,sticky = 'NSEW')
		self.go_to_operator_entry=Entry(self.main_frame, width=20)
		self.go_to_operator_entry.grid(row=3,column=1,padx=5, pady=5,sticky = 'NSEW')

		if mode == 'edit':
			self.orig_msn = parent_ac.backend.msn
			self.update_variables()
			
		# ok button
		self.ok_button=Button(top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=4,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=4,column=4, pady=5,sticky="nsew")

		self.button = 'cancel'
		
	def setup_label_frames(self):

		self.main_frame = LabelFrame(self.top,text="Aircraft Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
	
	def update_variables(self):
	
		self.msn_entry.insert(0, self.parent_ac.backend.msn)
		self.ac_combo.insert(0, self.parent_ac.backend.aircraft_type)
		self.current_operator_entry.insert(0, self.parent_ac.backend.current_operator)
		self.go_to_operator_entry.insert(0, self.parent_ac.backend.go_to_operator)

	def cleanup(self,button):
	
		if button == 'ok':
			
			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)
			
			if data_good:
				
				self.button = button
				self.aircraft_type = self.ac_combo.get()
				self.msn = self.msn_entry.get()
				self.title = self.msn
				self.current_operator = self.current_operator_entry.get()
				self.go_to_operator = self.go_to_operator_entry.get()
				self.ipc_title = ''
				self.ipc_ref = ''
				self.ipc_version = ''
				self.ipc_date = ''
				self.top.destroy()
					
			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		else:
			self.top.destroy()
			
class Edit_IPC_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_ac, task_type):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_ac = parent_ac
		self.task_type = task_type
		
		#label frame
		self.setup_label_frames()
		self.setup_widgets()
		
		self.setup_variables()
		
		self.button = 'cancel'
				
	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.top,text="Options:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	
		
	def setup_widgets(self):
		
		if self.task_type == 'seat':
			labels = ['Seat Removal Task:', 'Seat Installation Task:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.main_frame, labels, row, 2, 20, 2, 2)
		
		
		if self.task_type == 'seat':
			self.seat_removal_entry=Entry(self.main_frame, width=20)		
			self.seat_removal_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
			
			self.seat_install_entry=Entry(self.main_frame, width=20)		
			self.seat_install_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=4,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=4,column=4, pady=5,sticky="nsew")

	def setup_variables(self):
	
		ac_bk.Aircraft_Backend.setup_variables(self)
		ac_bk.Aircraft_Backend.update_variables(self, self.parent_ac.backend)
		
		if self.task_type == 'seat':
			self.seat_removal_entry.insert(0, self.seats_uninstl_task)
			self.seat_install_entry.insert(0, self.seats_instl_task)

	def cleanup(self, button):
	
		self.button = button
		
		if button == 'ok':
			
			if self.task_type == 'seat':
				print('sdfsdf')
				self.seats_uninstl_task = self.seat_removal_entry.get()
				self.seats_instl_task = self.seat_install_entry.get()
			
			self.top.destroy()
			
		else:
			self.top.destroy()