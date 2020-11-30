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
import treeview_functions

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
		self.setup_treeviews()
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

		self.parts_frame = LabelFrame(self.main_scroll_frame.inner,text="EEL Details:")
		self.parts_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)		

		self.instr_frame = LabelFrame(self.inst_scroll_frame.inner,text="Instructions:")
		self.instr_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

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

	def setup_treeviews(self):
		self.eel_tree = ttk.Treeview(self.parts_frame,selectmode="extended",columns=("A","B",'C','D'), height=25)
		self.eel_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.eel_tree.heading("#0", text="Item")
		self.eel_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#1", text="Part Number")
		self.eel_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#2", text="Location")
		self.eel_tree.column("#2",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#3", text="Qty")
		self.eel_tree.column("#3",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#4", text="Existing/New")
		self.eel_tree.column("#4",minwidth=0,width=150, stretch='NO')

		self.instructions_tree = ttk.Treeview(self.instr_frame,selectmode="extended",columns=("A","B"), height=25)
		self.instructions_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.instructions_tree.heading("#0", text="#")
		self.instructions_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.instructions_tree.heading("#1", text="Instruction")
		self.instructions_tree.column("#1",minwidth=0,width=550, stretch='NO')

	def update_component(self, window, type):
		self.backend.update_component(window, type)

		self.update_label_text()
		self.update_treeviews()

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
		#instructions = {'Existing Remain': [], 'Existing Move': [], 'Existing Remove': [], 'New Install': []}
		
		save_dict = copy.deepcopy(self.backend.gen_save_dict())
		w = file_menu.Load('EEL Comparison', save_dict)
		w.layout = {}
		w.instructions = []

		for item in go_to.backend.summary:
			print(item)
			self.w=Gen_Layout_Window_Tk(self.mainapp, self.master, self, item)
			self.master.wait_window(self.w.top)

			if self.w.button == 'cancel':
				canceled = True
				break

			else:
				for loc in self.w.layout:
					if loc not in w.layout.keys():
						w.layout[loc] = []
					for part in self.w.layout[loc]:
						w.layout[loc].append(part)

					for part in self.w.instructions:
						w.instructions.append(part)

		self.update_component(w, 'edit')

	def update_treeviews(self):

		data = []
		for loc in self.backend.layout:
			for part in self.backend.layout[loc]:
				data.append(part)
		treeview_functions.write_data_to_treeview(self.eel_tree, 'replace', data)

		if self.backend.instructions:
			treeview_functions.write_data_to_treeview(self.instructions_tree, 'replace', self.backend.instructions)


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
		
		self.setup_totals()

		self.setup_locations()
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

		ttk.Separator(self.main_scroll_frame.inner,orient=HORIZONTAL).grid(row=2, columnspan=3, pady=10, sticky='NSEW')
		self.label_frame_row = 3

		#setup label frame for each location to be process
		self.locations = self.go_to_eel.backend.get_item_locations(self.item)
		
		current_locations = self.current_eel.backend.get_item_locations(self.item)
		
		for loc in current_locations:
			if loc not in self.locations:
				self.locations.append(loc)
		
		self.locations_frames = {}
		for loc in self.locations:
			lf = LabelFrame(self.main_scroll_frame.inner,text=loc)
			self.locations_frames[loc] = lf
			lf.grid(row=self.label_frame_row, column=0, columnspan = 3, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
			self.label_frame_row += 1


	def setup_buttons(self):

		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=2, pady=5,sticky="nsew")

	def setup_totals(self):

		self.total_labels = {'Current': {}, 'Go To': {}, 'Total': {}}
		
		# Current 
		ttk.Label(self.current_frame, text="Part Number").grid(row = 0, column = 1, columnspan=1, padx=10)
		ttk.Label(self.current_frame, text="Existing Qty").grid(row = 0, column = 2, columnspan=1, padx=10)
		ttk.Label(self.current_frame, text="Selected Qty").grid(row = 0, column = 3, columnspan=1, padx=10)

		row = 1
		for part_no in self.current_eel.backend.summary[self.item]:

			tk.Label(self.current_frame,text=part_no,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 1, sticky = 'W')

			qty = self.current_eel.backend.summary[self.item][part_no]

			tk.Label(self.current_frame,text=qty,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 2, sticky = 'W')

			label = tk.Label(self.current_frame,text='0',bg="white",borderwidth=2, relief="groove",width=20)
			label.grid(row = row, column = 3, sticky = 'W')

			self.total_labels['Current'][part_no] = {'Available': qty, 'Label': label}
			row += 1
		# Go To
		ttk.Label(self.goto_frame, text="Part Number").grid(row = 0, column = 1, columnspan=1, padx=10)
		ttk.Label(self.goto_frame, text="Selected Qty").grid(row = 0, column = 2, columnspan=1, padx=10)

		total_qty = 0
		row = 1
		for part_no in self.go_to_eel.backend.summary[self.item]:

			tk.Label(self.goto_frame,text=part_no,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 1, sticky = 'W')

			qty = self.go_to_eel.backend.summary[self.item][part_no]
			total_qty += qty

			label = tk.Label(self.goto_frame,text='0',bg="white",borderwidth=2, relief="groove",width=20)
			label.grid(row = row, column = 2, sticky = 'W')

			self.total_labels['Go To'][part_no] = {'Label': label}
			row += 1

		# Totals
		ttk.Label(self.total_frame, text="Total Required Qty").grid(row = 0, column = 1, columnspan=1, padx=10)
		ttk.Label(self.total_frame, text="Total Selected Qty").grid(row = 0, column = 2, columnspan=1, padx=10)

		tk.Label(self.total_frame,text=str(total_qty),bg="white",borderwidth=2, relief="groove",width=20).grid(row = 1, column = 1, sticky = 'W')

		label = tk.Label(self.total_frame,text='0',bg="white",borderwidth=2, relief="groove",width=20)
		label.grid(row = 1, column = 2, sticky = 'W')

		self.total_labels['Total']['Total Required'] = total_qty
		self.total_labels['Total']['Total Selected Label'] = label

	def setup_locations(self):

		self.combos = {}

		#self.current_eel.backend.gen_summary_dict() #updates backend.summary dict

		for loc in self.locations_frames:

			self.combos[loc] = {'Current': {}, 'Go To': {}, 'Total Required': None, 'Total Selected Label': None}
			# header labels
			lf = self.locations_frames[loc]

			label = ttk.Label(lf, text="Existing Items To Keep")
			label.grid(row = 0, column = 1, columnspan=2, padx=10)

			label = ttk.Label(lf, text="New Items")
			label.grid(row = 0, column = 3, columnspan=2, padx=10)

			label = ttk.Label(lf, text="Total Required Qty")
			label.grid(row = 0, column = 5, padx=10)

			label = ttk.Label(lf, text="Total Selected Qty")
			label.grid(row = 0, column = 6, padx=10)

			# Add Current Parts
			
			item_part_nos = self.current_eel.backend.get_item_part_no_by_location(self.item)
			
			row = 1

			if loc in item_part_nos.keys():
				for part_no in item_part_nos[loc]:
				
		#	for part_no in self.current_eel.backend.summary[self.item]:

					tk.Label(lf,text=part_no,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 1, sticky = 'W')

					q = self.current_eel.backend.summary[self.item][part_no]
					c = ttk.Combobox(lf, values=[q for q in range(q+1)], state='readonly')
					c.grid(row = row, column = 2, sticky = 'W', padx=10)
					c.set(0)

					c.bind('<<ComboboxSelected>>',
							lambda event: self.combo_callback(event))

					self.combos[loc]['Current'][part_no] = c
					row += 1

			#Add Go To Parts

			row = 1
			total_qty = 0

			item_part_nos = self.go_to_eel.backend.get_item_part_no_by_location(self.item)
						if loc in item_part_nos.keys():
				for part_no in item_part_nos[loc]:

					tk.Label(lf,text=part_no,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 3, sticky = 'W')

					q = item_part_nos[loc][part_no]

					total_qty += q
					c = ttk.Combobox(lf, values=[q for q in range(q+1)], state='readonly')
					c.grid(row = row, column = 4, sticky = 'W', padx=10)
					c.set(0)

					c.bind('<<ComboboxSelected>>',
							lambda event: self.combo_callback(event))

					self.combos[loc]['Go To'][part_no] = c
					row += 1

			# Add Total 
			self.combos[loc]['Total Required'] = total_qty
			#Total Required
			tk.Label(lf,text=total_qty,bg="white",borderwidth=2, relief="groove",width=20).grid(row = 1, column = 5, sticky = 'W')

			# Total Selected
			label = tk.Label(lf, text="0",bg='SteelBlue1',borderwidth=2, relief="groove",width=20)
			label.grid(row = 1, column = 6, padx=10)

			self.combos[loc]['Total Selected Label'] = label

	def combo_callback(self, event):

		total_selected = 0
		current_parts = {}
		go_to_parts = {}

		for loc in self.combos:
			location_selected = 0

			for layout in ['Current', 'Go To']:
				for part_no in self.combos[loc][layout]:
					location_selected += int(self.combos[loc][layout][part_no].get())

					if layout == 'Current':
						if part_no not in current_parts.keys():
							current_parts[part_no] = location_selected
						else:
							current_parts[part_no] += location_selected

					if layout == 'Go To':
						if part_no not in go_to_parts.keys():
							go_to_parts[part_no] = location_selected
						else:
							go_to_parts[part_no] += location_selected

			total_selected += location_selected

			required = self.combos[loc]['Total Required']

			color = self.get_label_color(required, location_selected)

			self.combos[loc]['Total Selected Label'].config(text=str(location_selected), bg=color)

		for part_no in current_parts:
			available = self.total_labels['Current'][part_no]['Available']
			selected = current_parts[part_no]

			color = self.get_label_color(available, selected)
			self.total_labels['Current'][part_no]['Label'].config(text=str(selected), bg=color)

		for part_no in go_to_parts:
			selected = go_to_parts[part_no]

			self.total_labels['Go To'][part_no]['Label'].config(text=str(selected))


		required = self.total_labels['Total']['Total Required']

		color =self.get_label_color(required, total_selected)
		self.total_labels['Total']['Total Selected Label'].config(text=str(total_selected), bg=color)

	def get_label_color(self, required, selected):

			if selected > required:
				color = 'IndianRed1'
			elif selected < required:
				color = 'SteelBlue1'
			else:
				color = 'green yellow'

			return color
	def cleanup(self, button):

		self.button = button

		if button == 'ok':

			data_ok = True
			# Check total selected is correct

			required = int(self.total_labels['Total']['Total Required'])
			selected = int(self.total_labels['Total']['Total Selected Label'].cget('text'))

			if required != selected:
				data_ok = False
				msg = f'Total Selected Parts Must be Equal to {required}.\n Current Selected Qty is {selected}'

			# # Check total selected for each location is correct
			# for loc in self.combos:
				# required = int(self.combos[loc]['Total Required'])
				# selected = int(self.combos[loc]['Total Selected Label'].cget('text'))
				# if required != selected:
					# data_ok = False	
					# msg = f'Total Selected Parts for {loc} Must be Equal to {required}.\n Current Selected Qty is {selected}'
					# break

			# # Check not to many current parts selected
			# if data_ok:

				# for part_no in self.total_labels['Current']:
					# available = int(self.total_labels['Current'][part_no]['Available'])
					# selected = int(self.total_labels['Current'][part_no]['Label'].cget('text'))

					# if selected > available:
						# data_ok = False	
						# msg = f'Total Selected Current Parts for {part_no} Must not be greater than {available}.\n Current Selected Qty is {selected}'
						# break

			if not data_ok:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
			else:
				self.process_final_layout()
				self.top.destroy()
		else:
			self.top.destroy()

	def process_final_layout(self):
		
		qty_tracker = self.go_to_eel.backend.get_total_qty_item_per_location(self.item)
		self.layout = {}
		self.instructions = []
		
		instructions_count = 0
		
		current_leftovers = []#tracker existing parts being kept that have not been assigned a location
		go_to_leftovers = []#tracker existing parts being kept that have not been assigned a location
		
		# Loop through each go to location
		# if current item selected, leave it there
		for loc in qty_tracker:
			
			self.layout[loc] = []
			qty_required = qty_tracker[loc]
			
			for part_no in self.combos[loc]['Current']:
				
				qty_selected = int(self.combos[loc]['Current'][part_no].get())
				
				if qty_selected > 0:
				
					if qty_selected >= qty_required:
					
						leftover = qty_selected - qty_required
						
						qty_tracker[loc] += qty_required*-1
						
						current_leftovers.append([part_no, loc, qty])
						
					else:
					
						qty_tracker[loc] += qty_selected*-1
						
					self.layout[loc].append([self.item, part_no, loc, qty_selected, 'Existing'])
						
		# Loop through new Items, assign to their location if that location is not full
		for loc in qty_tracker:
			
			qty_required = qty_tracker[loc]
			
			if qty_required > 0:

				for part_no in self.combos[loc]['Go To']:
					
					qty_selected = int(self.combos[loc]['Go To'][part_no].get())
					
					if qty_selected > 0:
					
						if qty_selected >= qty_required:
						
							leftover = qty_selected - qty_required
							
							qty_tracker[loc] += qty_selected*-1
							
							go_to_leftovers.append([part_no, loc, qty])
							
						else:
						
							qty_tracker[loc] += qty_selected*-1
							
						self.layout[loc].append([self.item, part_no, loc, qty_selected, 'New'])						
			
		# Assign any left over parts (both existing and new) to any unfilled positions
		
		for loc in qty_tracker:
			
			# loop through current leftovers first
			qty_required = qty_tracker[loc]
			
			if qty_required > 0:
				
				for part in current_leftovers:
					
					qty_available = part[2]
					
					if qty_available >= qty_required:
						
						
