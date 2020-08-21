import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk as gui_styles


class Project_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp
		self.setup_notebook()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_entries()
		
		
	def setup_notebook(self):
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.comments_tab, text = "Comments")
		
		self.note.grid(row=1,column=0,sticky='NSEW')

		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50)
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_label_frames(self):

		self.main_frame = LabelFrame(self.main_tab,text="Project Details:")
		self.main_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)		
	
	
	def setup_labels(self):
	
		self.top_label = tk.Label(self, text=('Project: '),font=self.mainapp.title_font)
		self.top_label.grid(row=0,column=0,columnspan=24,sticky='W')

		l = gui_styles.create_multiple_labels(frame = self.main_frame,
			labels = ['Project Number: ', 'Project Title: ', 'Engineer: ', 'Client: ', 'Current Operator: ', 'Go-To Operator: '], row = 2, column = 1)

	def setup_entries(self):
	
		self.prj_no_entry=Entry(self.main_frame, width=120)		
		self.prj_no_entry.grid(row=2,column=2,padx=2, pady=2,sticky = 'NSEW')

		self.prj_title_entry=Entry(self.main_frame, width=120)		
		self.prj_title_entry.grid(row=3,column=2,padx=2, pady=2,sticky = 'NSEW')

		self.eng_entry=Entry(self.main_frame, width=120)		
		self.eng_entry.grid(row=4,column=2,padx=2, pady=2,sticky = 'NSEW')	
		
		self.client_entry=Entry(self.main_frame, width=120)		
		self.client_entry.grid(row=5,column=2,padx=2, pady=2,sticky = 'NSEW')
		
		self.current_entry=Entry(self.main_frame, width=120)		
		self.current_entry.grid(row=6,column=2,padx=2, pady=2,sticky = 'NSEW')
		
		self.go_to_entry=Entry(self.main_frame, width=120)		
		self.go_to_entry.grid(row=7,column=2,padx=2, pady=2,sticky = 'NSEW')	
	
	def gen_save_dict(self):
	
		return {'Project Number': self.prj_no_entry.get(),
				'Project Title': self.prj_title_entry.get(),
				'Engineer': self.eng_entry.get(),
				'Client': self.client_entry.get(),
				'Current Operator': self.current_entry.get(),
				'Go To Operator': self.go_to_entry.get(),
				'Comments': self.comment_text.get("1.0","end")}
	
	def load_project_data(self, data):
		
		if 'Project Number' in data.keys():
			self.prj_no_entry.delete(0, 'end')
			self.prj_no_entry.insert(0, data['Project Number'])
		
		if 'Project Title' in data.keys():
			self.prj_title_entry.delete(0, 'end')
			self.prj_title_entry.insert(0, data['Project Title'])
			
		if 'Engineer' in data.keys():
			self.eng_entry.delete(0, 'end')
			self.eng_entry.insert(0, data['Engineer'])

		if 'Client' in data.keys():
			self.client_entry.delete(0, 'end')
			self.client_entry.insert(0, data['Client'])

		if 'Current Operator' in data.keys():
			self.current_entry.delete(0, 'end')
			self.current_entry.insert(0, data['Current Operator'])	

		if 'Go To Operator' in data.keys():
			self.go_to_entry.delete(0, 'end')
			self.go_to_entry.insert(0, data['Go To Operator'])
			
				
		if 'Comments' in data.keys():
			self.comment_text.delete('1.0', 'end')
			self.comment_text.insert('end', data['Comments'])
			
		
	def clear_project_data(self):

		for e in [self.prj_no_entry, self.prj_title_entry, self.eng_entry, self.client_entry, self.current_entry, self.go_to_entry]:
			e.delete(0, 'end')
			
		self.comment_text.delete('1.0', 'end')
		
		
		
		