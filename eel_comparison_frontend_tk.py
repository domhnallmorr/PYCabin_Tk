import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk
import components_tk

import eel_comparison_backend as eel_comp_bk
import double_scrollbar
import comment_box
import data_input_checks_tk
import file_menu

import copy

class EEL_Comparison_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp

		self.top_label = tk.Label(self, text=('EEL Comparison: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)

		self.backend = eel_comp_bk.EEL_Comparison_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frames()
		self.setup_label_frames()
		self.setup_labels()
		#self.setup_treeviews()
		self.setup_buttons()

	def setup_notebook(self):
	
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.instructions_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.instructions_tab, text = "Instructions")
		self.note.add(self.comments_tab, text = "Comments")
		
		#self.note.grid(row=1,column=0,sticky='NSEW')
		self.note.pack(fill=tk.BOTH, expand=True)
		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_label_frames(self):
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="EEL Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)		


	def setup_labels(self):

		#self.top_label = tk.Label(self, text=('EEL Layout: '),font=self.mainapp.title_font)
		#self.top_label.grid(row=0,column=0,columnspan=24,stick='W')

		self.ac_type_label = gui_styles_tk.create_label(self.main_frame,'')
		self.ac_type_label.grid(row = 2, column = 0,pady=2,padx=2, sticky="nsew")
		
		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 1, columnspan=6,pady=2,padx=2, sticky="nsew")
		self.description_label.configure(width=100)

		self.current_label = gui_styles_tk.create_label(self.main_frame,'')
		self.current_label.grid(row = 3, column = 0,pady=2,padx=2, sticky="nsew")

		self.goto_label = gui_styles_tk.create_label(self.main_frame,'')
		self.goto_label.grid(row = 3, column = 1,pady=2,padx=2,sticky="nsew")		
		#self.goto_label.configure(width=20)

	def update_component(self, window, type):
		self.backend.update_component(window, type)

		self.update_label_text()
		#self.update_treeviews()

		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)

	def update_label_text(self):
				
		self.top_label.config(text=f'EEL Comparison: {self.backend.title}')
		self.ac_type_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.current_label.config(text=f' LOPA: {self.backend.current_eel}')
		self.goto_label.config(text=f' OHSC: {self.backend.go_to_eel}')

	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.inst_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.instructions_tab, self.mainapp)
		self.inst_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def setup_buttons(self):
		
		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.comp_btn = Button(self.main_scroll_frame.inner, text = 'Gen Final Layout', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.gen_final_layout())
		self.comp_btn.grid(row=1, column=1, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

	def edit(self):

		pass

	def gen_final_layout(self):

		# handle if current and go to layouts the same

		# identify item types
		go_to = self.mainapp.frames[self.backend.go_to_eel]
		current = self.mainapp.frames[self.backend.current_eel]
		go_to.backend.gen_summary_dict()

		# loop through each item, track user input

		canceled = False

		user_selection = {}
		instructions = {'Existing Remain': [], 'Existing Move': [], 'Existing Remove': [], 'New Install': []}

		for item in go_to.backend.summary:
			print(item)
			self.w=Gen_Layout_Window_Tk(self.mainapp, self.master, self, item)
			self.master.wait_window(self.w.top)

			if self.w.button == 'cancel':
				canceled = True
				break

			else:
				user_selection[item] = copy.deepcopy(self.w.user_selection)


		print(user_selection)
		# process user input
		for item in user_selection:

			# handle existing items that don't move
			for pn in user_selection[item]['Current']:

				qty = user_selection[item]['Current'][pn]

				if qty > 0:

					#find location in go to
					for loc in go_to_eel.backend.layout:
						for item in go_to_eel.layout[loc]:
							item_type = item[0]
							pn = item[1]
							qty = int(item[3])

							#if pn 

			# handle existing items that do move

			# handle new items 


		# update treeview with final layout


		# BOM for attach hardware


class Edit_EEL_Comparison_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_page):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_page = parent_page

		self.eel_dict = components_tk.get_all_components(mainapp, 'EELs')
		eel_comp_bk.setup_variables(self)

		self.data_checks = {}
		self.setup_label_frames()
		self.setup_widgets()
		self.button = 'cancel'

	def setup_label_frames(self):		
		self.details_frame = LabelFrame(self.top,text="EEL Comparison Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		labels = ['Title:', 'Description:', 'Aircraft:', 'Current EEL:', 'Go To EEL:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)	
		
		self.title_entry=Entry(self.details_frame, width=20)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		#self.data_checks['Title'] = ['title', self.title_entry, self.orig_title]

		if self.mode == 'edit':
			self.title_entry.insert(0, self.parent_page.backend.title)


		self.description_entry=Entry(self.details_frame, width=20)		
		self.description_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			self.description_entry.insert(0, self.parent_page.backend.description)

		self.ac_combo= ttk.Combobox(self.details_frame, values=['A320'], state='disabled')
		self.ac_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.ac_combo.set('A320')

		self.current_combo= ttk.Combobox(self.details_frame, values=self.eel_dict['A320'], state='readonly')
		self.current_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.goto_combo= ttk.Combobox(self.details_frame, values=self.eel_dict['A320'], state='readonly')
		self.goto_combo.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, pady=5,sticky="nsew")

	def cleanup(self, button):
	
		self.button = button
		
		if button == 'ok':

			self.title = self.title_entry.get()
			self.aircraft_type = self.ac_combo.get()
			self.description = self.description_entry.get()
			self.current_eel = self.current_combo.get()
			self.go_to_eel = self.goto_combo.get()
			self.top.destroy()

		else:
			self.top.destroy()

class Gen_Layout_Window_Tk(object):
	def __init__(self, mainapp, master, parent_page, item):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		#self.mode = mode
		self.parent_page = parent_page
		self.item = item

		self.total_required = 0
		self.total_selected = 0

		self.current_eel = self.mainapp.frames[self.parent_page.backend.current_eel]
		self.go_to_eel = self.mainapp.frames[self.parent_page.backend.go_to_eel]

		self.current_eel.backend.gen_summary_dict()
		self.go_to_eel.backend.gen_summary_dict()

		self.combos = {'Current': {}, 'Go To': {}}
		self.setup_scrollable_frames()

		self.top_label = tk.Label(self.main_scroll_frame.inner, text=(item),font=self.mainapp.title_font, anchor="w")
		self.top_label.grid(row = 0, column=0, columnspan=3, sticky='NSEW')

		self.setup_label_frames()
		self.setup_labels()
		self.setup_buttons()

		self.top.geometry("1300x600")

		self.button = 'cancel'
	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.top, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def setup_label_frames(self):

		self.current_frame = LabelFrame(self.main_scroll_frame.inner,text="Current Items:")
		self.current_frame.grid(row=1, column=0, columnspan = 1, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)				

		self.goto_frame = LabelFrame(self.main_scroll_frame.inner,text="Go To Items:")
		self.goto_frame.grid(row=1, column=1, columnspan = 1, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.total_frame = LabelFrame(self.main_scroll_frame.inner,text="Total Items:")
		self.total_frame.grid(row=1, column=2, columnspan = 1, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

	def setup_buttons(self):

		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=2, pady=5,sticky="nsew")

	def setup_labels(self):

		frames = [self.current_frame, self.goto_frame]
		for i, f in enumerate(frames):
			tk.Label(f,text='Part Number',width=20).grid(row = 0, column = 1, sticky = 'W')
			if i == 0:
				tk.Label(f,text='Current Qty',width=10).grid(row = 0, column = 2, sticky = 'W')
				tk.Label(f,text='Qty to Keep',width=20).grid(row = 0, column = 3, sticky = 'W')
			else:
				tk.Label(f,text='Go To Qty',width=10).grid(row = 0, column = 2, sticky = 'W')
				tk.Label(f,text='Qty to Install',width=20).grid(row = 0, column = 3, sticky = 'W')

		for i, layout in enumerate([self.current_eel, self.go_to_eel]):
			row = 1
			f = frames[i]
			for pn in layout.backend.summary[self.item]:
				tk.Label(f,text=pn,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 1, sticky = 'W')

				q = layout.backend.summary[self.item][pn]
				tk.Label(f,text=q,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 2, sticky = 'W')
				
				c = ttk.Combobox(f, values=[q for q in range(q+1)], state='readonly')
				c.grid(row = row, column = 3, sticky = 'W')
				c.set(0)
				c.bind('<<ComboboxSelected>>',
                      lambda event: self.combo_callback(event))

				if i == 0:
					self.combos['Current'][pn] = c
				else:
					self.combos['Go To'][pn] = c

					self.total_required += q
				row += 1

		tk.Label(self.total_frame,text='Total Required',width=20).grid(row = 0, column = 1, sticky = 'W')
		tk.Label(self.total_frame,text='Total Selected',width=20).grid(row = 0, column = 2, sticky = 'W')

		tk.Label(self.total_frame,bg="white",borderwidth=2, relief="groove",text=str(q),width=20).grid(row = 1, column = 1, sticky = 'W')

		self.total_label = (tk.Label(self.total_frame,bg="SteelBlue1",borderwidth=2, relief="groove",text='0',width=20))
		self.total_label.grid(row = 1, column = 2, sticky = 'W')

	def combo_callback(self, event):
		print('callback')
		total_qty = 0

		for layout in self.combos.keys():
			for pn in self.combos[layout]:
				c = self.combos[layout][pn]
				try:
					q = int(c.get())
				except:
					q = 0
				
				total_qty += q
		
		if total_qty > self.total_required:
			color = 'firebrick1'
		elif total_qty == self.total_required:
			color = 'green yellow'
		elif total_qty < self.total_required:
			color = 'SteelBlue1'
			
		self.total_label.config(text = str(total_qty), bg=color)

		self.total_selected = total_qty


	def cleanup(self, button):

		self.button = button

		if button == 'ok':

			if self.total_selected != self.total_required:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=f'Total Selected Must Equal {self.total_required}')
			else:

				self.user_selection = {'Current': {}, 'Go To': {}}

				for layout in self.user_selection:
					for pn in self.combos[layout]:
						print(self.combos[layout][pn])
						print(self.combos[layout][pn].get())

						self.user_selection[layout][pn] = self.combos[layout][pn].get()

				self.user_selection['Total'] = self.total_required
				self.user_selection['Processed'] = 0

				self.top.destroy()
		else:
			self.top.destroy()
