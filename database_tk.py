import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import components_tk
import gui_styles_tk
import double_scrollbar

import sqlite3
import getpass
from datetime import date


def add_components(mainapp):

	type = 'Seats'
	mainapp.w=Add_Components_To_DB(mainapp, mainapp.master, type)
	mainapp.master.wait_window(mainapp.w.top)	

def load_components(mainapp):

	mainapp.w=Load_Components_From_DB(mainapp, mainapp.master, type)
	mainapp.master.wait_window(mainapp.w.top)	

def connect_to_database(self):
	self.conn = sqlite3.connect(self.mainapp.cabin_database)
	self.c = self.conn.cursor()

def disconnect_from_database(self):
	self.c.close()
	self.conn.close()
		
class Add_Components_To_DB():

	def __init__(self, mainapp, master, type):

		top=self.top=Toplevel(master)
		top.grab_set()
		self.master = master
		self.mainapp = mainapp
		double_scrollbar.setup_scrollable_frame(self, self.top, self.mainapp) #creates self.main_scroll_frame
		
		self.type = type
		self.checkboxes = {}
		
		self.components_dict = components_tk.get_all_components(mainapp, type)
		self.check_which_components_in_database()
		self.setup_label_frames()
		
		self.setup_widgets()
		
		self.top.geometry('{}x{}'.format(600, 400))    

		
	def setup_label_frames(self):
		
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text=f"Select {self.type}:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
		
		Button(self.main_frame,text='Select All', command= lambda option = 1: self.select(option)).grid(row=0, column = 1, sticky='NSEW')
		Button(self.main_frame,text='Select None', command= lambda option = 0: self.select(option)).grid(row=0, column = 2, sticky='NSEW')
		
		tk.Label(self.main_frame, text = 'Seat', width=20).grid(row=1, column = 1, sticky='NSEW')
		tk.Label(self.main_frame, text = 'Aircraft Type', width=20).grid(row=1, column = 2, sticky='NSEW')
		tk.Label(self.main_frame, text = 'Currently in Database', width = 20).grid(row=1, column = 3, sticky='NSEW')
		
		colors = {'A320 Family': 'LightSkyBlue2', 'B737 Family': 'tomato'}
		row = 2
		for component in self.components_dict['All']:
			self.checkboxes[component] = {}
			
			ac = self.mainapp.frames[component].backend.aircraft_type
			var = tk.IntVar()
			self.checkboxes[component]['checkbox'] = tk.Checkbutton(self.main_frame, relief='solid', borderwidth = 5, padx=0,pady=0,bd=0, variable= var)
			self.checkboxes[component]['checkbox'].grid(row=row, column = 0, sticky='NSEW')
			self.checkboxes[component]['var'] = var
			
			tk.Label(self.main_frame, text = component, bg = 'white', relief='solid', borderwidth=0.5).grid(row=row, column = 1, sticky='NSEW')
			tk.Label(self.main_frame, text = ac, bg = colors[ac], relief='solid', borderwidth=0.5).grid(row=row, column = 2, sticky='NSEW')
			
			if component in self.components_in_db:
				if self.components_in_db_dict[component]['is same'] == True:
					text = 'Yes'
				else:
					text = 'Yes but different values'
			else:
				text = 'No'
			l = tk.Label(self.main_frame, text = text, bg = 'light grey', relief='solid', borderwidth=0.5)
			l.grid(row=row, column = 3, sticky='NSEW')
			if text == 'Yes but different values':
				l.bind("<Button-1>",lambda event, component=component: self.show_comparison(event, component))
			row += 1
		
		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=4,column=2,columnspan=2, pady=5,sticky="nsew")

		# cancel button
		self.cancel_button=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.cancel_button.grid(row=4,column=4, columnspan=2, pady=5,sticky="nsew")

		self.button = 'cancel'
		
		
	def select(self, option):
	
		for component in self.checkboxes:
		
			self.checkboxes[component]['var'].set(option)
			
			
	def cleanup(self, button):
	
		self.button = button
		
		if self.button == 'ok':
			connect_to_database(self)
			self.get_components_to_add()
			self.add_components_to_db()
			
			self.conn.commit()
			disconnect_from_database(self)
			
		else:
			self.top.destroy()
			


	def get_components_to_add(self):
		self.components_too_add = []
		
		for component in self.checkboxes:
			
			if self.checkboxes[component]['var'].get() == 1:
				self.components_too_add.append(self.mainapp.frames[component].backend)
			
	def add_components_to_db(self):
		
		msg = tkinter.messagebox.askokcancel(title=None, message='Do You Wish to Commit the Selected Components to the Database? This Cannot be Undone')
		if msg:
			for component_bkend in self.components_too_add:
				try:
					user = getpass.getuser()
				except:
					user = 'unknown'
				save_dict = component_bkend.gen_save_dict()
				
				if save_dict['Title'] in self.components_in_db:
					command = f'UPDATE seats SET "Data" = "{str(save_dict)}" WHERE Title = "{save_dict["Title"]}"'
					print(command)
					self.c.execute(command)
				else:
					self.c.execute('INSERT INTO seats ("Title", "Data", "Date", "User", "Project") VALUES (?, ?, ?, ?, ?)',
										(save_dict['Title'], str(save_dict), date.today().strftime("%b-%d-%Y"), user, "Project"))
					
				self.conn.commit()
				
			tkinter.messagebox.showinfo(title=None, message='Database Successfully Updated')
	def check_which_components_in_database(self):
	
		connect_to_database(self)
		
		search_terms = str(tuple(self.components_dict['All']))
		if search_terms[-2] == ',': #remove trailing comma (causes sql syntax error)
			search_terms = search_terms[:-2] + ')'

		self.c.execute(f'SELECT * FROM seats WHERE "Title" IN {search_terms}')
		data = self.c.fetchall()
		
		col_names = [description[0] for description in self.c.description]
		
		self.components_in_db_dict = {}
		for d in data:		
			component_bkend = self.mainapp.frames[d[0]].backend
			component_dict = eval(d[1])
				
			is_same, component_bkend_dict = self.compare_db_and_mainapp_data(component_bkend, component_dict)
			self.components_in_db_dict[d[0]] = {'db data': component_dict, 'is same': is_same, 'tk_data': component_bkend_dict}
			
		self.components_in_db = [d[0] for d in data]

	def compare_db_and_mainapp_data(self, component_bkend, component_db_dict):
		
		is_same = True
		component_bkend_dict = component_bkend.gen_save_dict()
		
		for col in component_db_dict:
			
			if isinstance(component_db_dict[col], float):
				component_bkend_dict[col] = float(component_bkend_dict[col])
				if component_db_dict[col] != component_bkend_dict[col]:
					is_same = False
			else:
				if component_db_dict[col] != component_bkend_dict[col]:
					is_same = False				
			
		return is_same, component_bkend_dict
		

	def show_comparison(self, event, component):
		self.top.withdraw()
		self.w = Comparison_Screen(self, component)
		self.w.top.wait_window(self.w.top)	
		self.top.deiconify()
		self.top.grab_set()
		
class Comparison_Screen():

	def __init__(self, db_page, component):
	
		self.top = Toplevel()
		self.top.grab_set()

		self.db_page = db_page
		self.component = component
		
		self.setup_widgets()
		
	def setup_widgets(self):
		
		tk.Label(self.top, text = 'Parameter', relief='solid', borderwidth=0.5).grid(row=2, column=1, sticky='NSEW')
		tk.Label(self.top, text = 'App Data', relief='solid', borderwidth=0.5).grid(row=2, column=2, sticky='NSEW')
		tk.Label(self.top, text = 'Database Data', relief='solid', borderwidth=0.5).grid(row=2, column=3, sticky='NSEW')
		row = 3
		for widget in self.db_page.components_in_db_dict[self.component]['db data']:
			tk.Label(self.top, text = widget, bg = 'white', relief='solid', borderwidth=0.5).grid(row=row, column=1, sticky='NSEW')
			
			tk_data = self.db_page.components_in_db_dict[self.component]['tk_data'][widget]
			db_data = self.db_page.components_in_db_dict[self.component]['db data'][widget]
			
			if tk_data != db_data:
				color = 'orange'
			else:
				color = 'light grey'
			tk.Label(self.top, text = tk_data, bg = color, relief='solid', borderwidth=0.5).grid(row=row, column=2, sticky='NSEW')
			tk.Label(self.top, text = db_data, bg = color, relief='solid', borderwidth=0.5).grid(row=row, column=3, sticky='NSEW')
			
			row += 1
			
class Load_Components_From_DB():

	def __init__(self, mainapp, master, type):

		top=self.top=Toplevel(master)
		top.grab_set()
		self.master = master
		self.mainapp = mainapp
		double_scrollbar.setup_scrollable_frame(self, self.top, self.mainapp) #creates self.main_scroll_frame
		
		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
		
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text=f"Options:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.table_frame = LabelFrame(self.main_scroll_frame.inner,text=f"Database Components:")
		self.table_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
	
	def setup_widgets(self):
	
		self.type_combo= ttk.Combobox(self.main_frame, values=['Seat'], state='readonly')
		self.type_combo.grid(row=1,column=1,padx=2, pady=2,sticky = 'NSEW')
		
		self.search_entry = Entry(self.main_frame, width=60)		
		self.search_entry.grid(row=1,column=2, columnspan=2, padx=2, pady=2,sticky = 'NSEW')
		
		self.search_button=Button(self.main_frame,text='Search', command= self.search)
		self.search_button.grid(row=1,column=4,columnspan=2, pady=5,sticky="nsew")
		
	def search(self):
		
		search = self.search_entry.get()
		
		if search.strip() != '':
			connect_to_database(self)
			self.c.execute(f"SELECT * FROM seats WHERE Title LIKE '%{search}%'")
			data = self.c.fetchall()
			
			print(data)
			
			disconnect_from_database(self)
		
		