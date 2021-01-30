import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk as gui_styles
import gui_styles_tk
import comment_box

class Project_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.backend = ProjectBackend(self, mainapp)
		self.setup_notebook()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_buttons()
		#self.setup_entries()
		self.update_component(None, None)
		
	def setup_notebook(self):
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.comments_tab, text = "Comments")
		
		self.note.grid(row=1,column=0,sticky='NSEW')

		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_label_frames(self):

		self.main_frame = LabelFrame(self.main_tab,text="Project Details:")
		self.main_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)		
	
	def setup_buttons(self):

		self.edit_btn = Button(self.main_frame, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)

	def setup_labels(self):
	
		self.top_label = tk.Label(self, text=('Project: '),font=self.mainapp.title_font)
		self.top_label.grid(row=0,column=0,columnspan=24,sticky='W')

		self.proj_no_label = gui_styles_tk.create_label(self.main_frame,'')
		self.proj_no_label.grid(row = 2, column = 0,pady=2,padx=2, sticky="nsew")

		self.proj_title_label = gui_styles_tk.create_label(self.main_frame,'')
		self.proj_title_label.grid(row = 3, column = 0,pady=2,padx=2, sticky="nsew")

		self.proj_eng_label = gui_styles_tk.create_label(self.main_frame,'')
		self.proj_eng_label.grid(row = 4, column = 0,pady=2,padx=2, sticky="nsew")

		self.proj_client_label = gui_styles_tk.create_label(self.main_frame,'')
		self.proj_client_label.grid(row = 5, column = 0,pady=2,padx=2, sticky="nsew")

		self.proj_current_label = gui_styles_tk.create_label(self.main_frame,'')
		self.proj_current_label.grid(row = 6, column = 0,pady=2,padx=2, sticky="nsew")

		self.proj_goto_label = gui_styles_tk.create_label(self.main_frame,'')
		self.proj_goto_label.grid(row = 7, column = 0,pady=2,padx=2, sticky="nsew")


	def update_label_text(self):

		self.proj_no_label.config(text=f'  Project Number: {self.backend.project_number}', width=100)
		self.proj_title_label.config(text=f'  Project Title: {self.backend.project_title}')
		self.proj_eng_label.config(text=f'  Engineer: {self.backend.engineer}')
		self.proj_client_label.config(text=f'  Client: {self.backend.client}')
		self.proj_current_label.config(text=f'  Current Operator: {self.backend.current_operator}')
		self.proj_goto_label.config(text=f'  Go-To Operator: {self.backend.go_to_operator}')

	def update_component(self, window, type):
		#self.backend.update_component(window, type)

		self.backend.update_component(window, type)
		self.update_label_text()

		self.mainapp.update_titlebar('edit')
	
	def load_project_data(self, data):

		if 'Project Number' in data.keys():
			self.backend.project_number = data['Project Number']
		
		if 'Project Title' in data.keys():
			self.backend.project_title = data['Project Title']	
			
		if 'Engineer' in data.keys():
			self.backend.engineer = data['Engineer']

		if 'Client' in data.keys():
			self.backend.client = data['Client']

		if 'Current Operator' in data.keys():
			self.backend.current_operator = data['Current Operator']

		if 'Go To Operator' in data.keys():
			self.backend.go_to_operator = data['Go To Operator']
			
		if 'Comments' in data.keys():
			self.comment_text.delete('1.0', 'end')
			self.comment_text.insert('end', data['Comments'])
			
		self.update_component(self.backend, 'edit')
		
	def clear_project_data(self):

		for e in [self.prj_no_entry, self.prj_title_entry, self.eng_entry, self.client_entry, self.current_entry, self.go_to_entry]:
			e.delete(0, 'end')
			
		self.comment_text.delete('1.0', 'end')
		
	def edit(self):

		self.w = Edit_EEL_Comparison_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')
		
class ProjectBackend:

	def __init__(self, parent_page, controller):

		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		self.setup_variables()

		self.save_class = Emergency_Equip_Saved_State

	def setup_variables(self):
		self.title = 'Project'
		self.project_number = ''
		self.project_title = ''
		self.engineer = ''
		self.client = ''
		self.current_operator = ''
		self.go_to_operator = ''

	def update_variables(self, source):

		if source:
			self.title = 'Project'
			self.project_number = source.project_number
			self.project_title = source.project_title
			self.engineer = source.engineer
			self.client = source.client
			self.current_operator = source.current_operator
			self.go_to_operator = source.go_to_operator

	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, Emergency_Equip_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, Emergency_Equip_Saved_State)
		ProjectBackend.update_variables(self, source)		

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments

		return {'Project Number': self.project_number,
				'Project Title': self.project_title,
				'Engineer': self.engineer,
				'Client': self.client,
				'Current Operator': self.current_operator,
				'Go To Operator': self.go_to_operator,
				'Comments': comments}

class Emergency_Equip_Saved_State():
	def __init__(self, emergency_equip):
	
		ProjectBackend.setup_variables(self)
		ProjectBackend.update_variables(self, emergency_equip)


class Edit_EEL_Comparison_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_page):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_page = parent_page

		self.setup_label_frames()
		self.setup_widgets()

	def setup_label_frames(self):

		self.details_frame = LabelFrame(self.top,text="Project Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_widgets(self):

		labels = ['Project Number:', 'Project Title:', 'Engineer:', 'Client:', 'Current Operator:', 'Go To Operator:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 1, 20, 2, 2)	
	
		self.prj_no_entry=Entry(self.details_frame, width=120)		
		self.prj_no_entry.grid(row=2,column=2,padx=2, pady=2,sticky = 'NSEW')
		self.prj_no_entry.insert(0, self.parent_page.backend.project_number)

		self.prj_title_entry=Entry(self.details_frame, width=120)		
		self.prj_title_entry.grid(row=3,column=2,padx=2, pady=2,sticky = 'NSEW')
		self.prj_title_entry.insert(0, self.parent_page.backend.project_title)

		self.eng_entry=Entry(self.details_frame, width=120)		
		self.eng_entry.grid(row=4,column=2,padx=2, pady=2,sticky = 'NSEW')
		self.eng_entry.insert(0, self.parent_page.backend.engineer)
		
		self.client_entry=Entry(self.details_frame, width=120)		
		self.client_entry.grid(row=5,column=2,padx=2, pady=2,sticky = 'NSEW')
		self.client_entry.insert(0, self.parent_page.backend.client)
		
		self.current_entry=Entry(self.details_frame, width=120)		
		self.current_entry.grid(row=6,column=2,padx=2, pady=2,sticky = 'NSEW')
		self.current_entry.insert(0, self.parent_page.backend.current_operator)
		
		self.go_to_entry=Entry(self.details_frame, width=120)		
		self.go_to_entry.grid(row=7,column=2,padx=2, pady=2,sticky = 'NSEW')
		self.go_to_entry.insert(0, self.parent_page.backend.go_to_operator)	

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, padx=5, pady=5,sticky="ne")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, padx=5, pady=5,sticky="nw")

	def cleanup(self, button):
	
		self.button = button
		
		if button == 'ok':
			self.project_number = self.prj_no_entry.get()
			self.project_title = self.prj_title_entry.get()
			self.engineer = self.eng_entry.get()
			self.client = self.client_entry.get()
			self.current_operator = self.current_entry.get()
			self.go_to_operator = self.go_to_entry.get()

			self.top.destroy()
		else:

			self.top.destroy()



