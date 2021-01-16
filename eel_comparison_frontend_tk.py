import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk
import components_tk

import eel_comparison_backend as eel_comp_bk
import eel_draw
import double_scrollbar
import comment_box
import data_input_checks_tk
import file_menu
import word_export


import copy
import treeview_functions
import time

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
		self.bom_tab = Frame(self.note)
		self.comparison_tab = Frame(self.note)
		self.weight_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.instructions_tab, text = "Instructions")
		self.note.add(self.bom_tab, text = "BOM")
		self.note.add(self.comparison_tab, text = "Comparisons")
		self.note.add(self.weight_tab, text = "OHSC Weight")
		self.note.add(self.comments_tab, text = "Comments")
		
		#self.note.grid(row=1,column=0,sticky='NSEW')
		self.note.pack(fill=tk.BOTH, expand=True)
		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_label_frames(self):
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="EEL Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 16, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)		

		self.parts_frame = LabelFrame(self.main_scroll_frame.inner,text="EEL Parts:")
		self.parts_frame.grid(row=4, column=0, columnspan = 4, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.item_numbers_frame = LabelFrame(self.main_scroll_frame.inner,text="Item Numbers:")
		self.item_numbers_frame.grid(row=4, column=4, columnspan = 2, rowspan = 2,sticky='NW',padx=1, pady=5, ipadx=2, ipady=5)	

		self.instr_frame = LabelFrame(self.inst_scroll_frame.inner,text="Instructions:")
		self.instr_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.comp_item_frame = LabelFrame(self.comp_scroll_frame.inner,text="Comparison by Item Type:")
		self.comp_item_frame.grid(row=1, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

		self.comp_part_frame = LabelFrame(self.comp_scroll_frame.inner,text="Comparison by Part Number:")
		self.comp_part_frame.grid(row=3, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.bom_frame = LabelFrame(self.bom_scroll_frame.inner,text="BOM:")
		self.bom_frame.grid(row=3, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.ohsc_frame = LabelFrame(self.ohsc_scroll_frame.inner,text="OHSCs:")
		self.ohsc_frame.grid(row=3, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

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
		self.eel_tree.column("#0",minwidth=0,width=250, stretch='NO')
		self.eel_tree.heading("#1", text="Part Number")
		self.eel_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#2", text="Location")
		self.eel_tree.column("#2",minwidth=0,width=150, stretch='NO')
		self.eel_tree.heading("#3", text="Qty")
		self.eel_tree.column("#3",minwidth=0,width=50, stretch='NO')
		self.eel_tree.heading("#4", text="Existing/New")
		self.eel_tree.column("#4",minwidth=0,width=150, stretch='NO')

		eel_tree_scrollbar = Scrollbar(self.parts_frame, command=self.eel_tree.yview)
		eel_tree_scrollbar.grid(row=2, rowspan=2, column=6, sticky='nsew')
		self.eel_tree.config(yscrollcommand=eel_tree_scrollbar.set)

		self.item_numbers_tree = ttk.Treeview(self.item_numbers_frame,selectmode="extended",columns=("A"), height=23)
		self.item_numbers_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.item_numbers_tree.heading("#0", text="Part Number")
		self.item_numbers_tree.column("#0",minwidth=0,width=250, stretch='NO')
		self.item_numbers_tree.heading("#1", text="Item Number")
		self.item_numbers_tree.column("#1",minwidth=0,width=80, stretch='NO')

		item_tree_scrollbar = Scrollbar(self.item_numbers_frame, command=self.item_numbers_tree.yview)
		item_tree_scrollbar.grid(row=2, rowspan=2, column=6, sticky='nsew')
		self.item_numbers_tree.config(yscrollcommand=item_tree_scrollbar.set)

		self.instructions_tree = ttk.Treeview(self.instr_frame,selectmode="extended",columns=("A","B"), height=25)
		self.instructions_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.instructions_tree.heading("#0", text="#")
		self.instructions_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.instructions_tree.heading("#1", text="Instruction")
		self.instructions_tree.column("#1",minwidth=0,width=550, stretch='NO')

		instructions_tree_scrollbar = Scrollbar(self.instr_frame, command=self.instructions_tree.yview)
		instructions_tree_scrollbar.grid(row=2, rowspan=2, column=6, sticky='nsew')
		self.instructions_tree.config(yscrollcommand=instructions_tree_scrollbar.set)

		self.comp_item_tree = ttk.Treeview(self.comp_item_frame,selectmode="extended",columns=("A","B",'C'), height=25)
		self.comp_item_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.comp_item_tree.heading("#0", text="Item")
		self.comp_item_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.comp_item_tree.heading("#1", text="Current Qty")
		self.comp_item_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.comp_item_tree.heading("#2", text="Go To Qty")
		self.comp_item_tree.column("#2",minwidth=0,width=150, stretch='NO')
		self.comp_item_tree.heading("#3", text="Delta")
		self.comp_item_tree.column("#3",minwidth=0,width=150, stretch='NO')

		comp_item_tree_scrollbar = Scrollbar(self.comp_item_frame, command=self.comp_item_tree.yview)
		comp_item_tree_scrollbar.grid(row=2, rowspan=2, column=6, sticky='nsew')
		self.comp_item_tree.config(yscrollcommand=comp_item_tree_scrollbar.set)

		self.comp_item_tree.tag_configure('positive', background=self.mainapp.green_color, foreground='black')
		self.comp_item_tree.tag_configure('negative', background=self.mainapp.red_color, foreground='white')
		self.comp_item_tree.tag_configure('none', background=self.mainapp.grey_color, foreground='white')

		self.comp_part_tree = ttk.Treeview(self.comp_part_frame,selectmode="extended",columns=("A","B",'C','D'), height=25)
		self.comp_part_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.comp_part_tree.heading("#0", text="Part Number")
		self.comp_part_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.comp_part_tree.heading("#1", text="Item")
		self.comp_part_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.comp_part_tree.heading("#2", text="Current Qty")
		self.comp_part_tree.column("#2",minwidth=0,width=150, stretch='NO')
		self.comp_part_tree.heading("#3", text="Go To Qty")
		self.comp_part_tree.column("#3",minwidth=0,width=150, stretch='NO')
		self.comp_part_tree.heading("#4", text="Delta")
		self.comp_part_tree.column("#4",minwidth=0,width=150, stretch='NO')
		
		self.comp_part_tree.tag_configure('positive', background=self.mainapp.green_color, foreground='black')
		self.comp_part_tree.tag_configure('negative', background=self.mainapp.red_color, foreground='white')

		comp_part_tree_scrollbar = Scrollbar(self.comp_part_frame, command=self.comp_part_tree.yview)
		comp_part_tree_scrollbar.grid(row=2, rowspan=2, column=6, sticky='nsew')
		self.comp_part_tree.config(yscrollcommand=comp_part_tree_scrollbar.set)

		self.bom_tree = ttk.Treeview(self.bom_frame,selectmode="extended",columns=("A","B"), height=25)
		self.bom_tree.grid(row=2,column=0, rowspan=2, columnspan=6,sticky="nsew")
		self.bom_tree.heading("#0", text="Part Number")
		self.bom_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.bom_tree.heading("#1", text="Item")
		self.bom_tree.column("#1",minwidth=0,width=150, stretch='NO')
		self.bom_tree.heading("#2", text="Qty")
		self.bom_tree.column("#2",minwidth=0,width=150, stretch='NO')

		bom_tree_scrollbar = Scrollbar(self.bom_frame, command=self.bom_tree.yview)
		bom_tree_scrollbar.grid(row=2, rowspan=2, column=6, sticky='nsew')
		self.bom_tree.config(yscrollcommand=bom_tree_scrollbar.set)

		tree_height = 15
		self.LHS_ohsc_tree = ttk.Treeview(self.ohsc_frame,selectmode="extended",columns=("A","B",'C','D','E','F'),height = tree_height)
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
		self.LHS_ohsc_tree.heading("E", text="Installed Weight (lbs)")   
		self.LHS_ohsc_tree.column("E",minwidth=0,width=120, stretch='NO')
		self.LHS_ohsc_tree.heading("F", text="Delta (lbs)")   
		self.LHS_ohsc_tree.column("F",minwidth=0,width=120, stretch='NO')

		self.LHS_ohsc_tree.tag_configure('negative', background=self.mainapp.green_color, foreground='black')#limit greater than installed
		self.LHS_ohsc_tree.tag_configure('positive', background=self.mainapp.red_color, foreground='white')

		LHS_ohsc_tree_scrollbar = Scrollbar(self.ohsc_frame, command=self.LHS_ohsc_tree.yview)
		LHS_ohsc_tree_scrollbar.grid(row=1, column=1, sticky='nsew')
		self.LHS_ohsc_tree.config(yscrollcommand=LHS_ohsc_tree_scrollbar.set)


		self.RHS_ohsc_tree = ttk.Treeview(self.ohsc_frame,selectmode="extended",columns=("A","B",'C','D','E','F'),height = tree_height)
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
		self.RHS_ohsc_tree.heading("E", text="Installed Weight (lbs)")   
		self.RHS_ohsc_tree.column("E",minwidth=0,width=120, stretch='NO')
		self.RHS_ohsc_tree.heading("F", text="Delta (lbs)")   
		self.RHS_ohsc_tree.column("F",minwidth=0,width=120, stretch='NO')

		self.RHS_ohsc_tree.tag_configure('negative', background=self.mainapp.green_color, foreground='black')#limit greater than installed
		self.RHS_ohsc_tree.tag_configure('positive', background=self.mainapp.red_color, foreground='white')

		LHS_ohsc_tree_scrollbar = Scrollbar(self.ohsc_frame, command=self.RHS_ohsc_tree.yview)
		LHS_ohsc_tree_scrollbar.grid(row=1, column=3, sticky='nsew')
		self.RHS_ohsc_tree.config(yscrollcommand=LHS_ohsc_tree_scrollbar.set)

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
		self.current_label.config(text=f' Current EEL: {self.backend.current_eel}')
		self.goto_label.config(text=f' Go-To EEL: {self.backend.go_to_eel}')

	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.inst_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.instructions_tab, self.mainapp)
		self.inst_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.comp_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.comparison_tab, self.mainapp)
		self.comp_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.bom_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.bom_tab, self.mainapp)
		self.bom_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.ohsc_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.weight_tab, self.mainapp)
		self.ohsc_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def setup_buttons(self):
		
		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.comp_btn = Button(self.main_scroll_frame.inner, text = 'Gen Final Layout', image = self.mainapp.mag_icon2, compound = LEFT, width = 30, command= lambda: self.gen_final_layout())
		self.comp_btn.grid(row=1, column=1, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.dxf_btn = Button(self.main_scroll_frame.inner, text = 'Export to DXF', image = self.mainapp.cad_icon2, compound = LEFT, width = 30, command= lambda: self.export_dxf())
		self.dxf_btn.grid(row=1, column=2, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.word_btn = Button(self.main_scroll_frame.inner, text = 'Export to Word', image = self.mainapp.word_icon2, compound = LEFT, width = 30, command= lambda: self.export_word())
		self.word_btn.grid(row=1, column=3, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.excel_btn = Button(self.main_scroll_frame.inner, text = 'Export to Excel', image = self.mainapp.excel_icon2, compound = LEFT, width = 30, command= lambda: self.export_excel())
		self.excel_btn.grid(row=1, column=4, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)

		self.edit_item_btn = Button(self.item_numbers_frame, text = 'Edit',image = self.mainapp.edit_icon2, compound = LEFT,
								command = self.edit_item_nos)
		self.edit_item_btn.grid(row = 1, column = 0, columnspan = 2, pady=5, sticky = 'NW')

	def edit(self):

		self.w = Edit_EEL_Comparison_Window_Tk(self.mainapp, self.master, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')

	def edit_item_nos(self):

		mode = 'edit'
		
		self.w=Edit_Item_Window(self.mainapp, self.master, mode, self)
		self.master.wait_window(self.w.top)	
		
		if self.w.button == 'ok':
			#treeview_functions.write_data_to_treeview(self.item_tree, 'replace',self.w.data) 
			self.update_component(self.w, 'edit')

	def export_excel(self):
	
		mode = 'edit'
		
		self.w=word_export.Export_Word_Excel_Window(self.mainapp, self.master, mode, self, 'excel')
		self.master.wait_window(self.w.top)

	def gen_final_layout(self):

		# handle if current and go to layouts the same

		# identify item types
		go_to = self.mainapp.frames[self.backend.go_to_eel]

		if self.backend.current_eel != None:
			current = self.mainapp.frames[self.backend.current_eel]
		else:
			current = None
		go_to.backend.gen_summary_dict()

		# loop through each item, track user input

		canceled = False

		user_selection = {}
		#instructions = {'Existing Remain': [], 'Existing Move': [], 'Existing Remove': [], 'New Install': []}
		
		save_dict = copy.deepcopy(self.backend.gen_save_dict())
		w = file_menu.Load('EEL Comparison', save_dict)
		w.layout = {}
		w.instructions = []
		w.bom = {}
		
		instructions_count = 1

		for item in go_to.backend.summary:
			
			self.w=Gen_Layout_Window_Tk(self.mainapp, self.master, self, item)
			if self.w.current_parts_avail:
				self.master.wait_window(self.w.top)
			else:
				self.w.cleanup('ok')

			if self.w.button == 'cancel':
				canceled = True
				break

			else:
				for loc in self.w.layout:
					if loc not in w.layout.keys():
						w.layout[loc] = []
					for part in self.w.layout[loc]:
						w.layout[loc].append(part)

				for idx, part in enumerate(self.w.instructions):
					part[0] =instructions_count
					instructions_count += 1
					w.instructions.append(part)

				for part in self.w.bom:
					w.bom[part] = self.w.bom[part]

		if not canceled:
			self.update_component(w, 'edit')

	def update_treeviews(self):

		data = []
		for loc in self.backend.layout:
			for part in self.backend.layout[loc]:
				data.append(part)
		treeview_functions.write_data_to_treeview(self.eel_tree, 'replace', data)

		if self.backend.instructions:
			treeview_functions.write_data_to_treeview(self.instructions_tree, 'replace', self.backend.instructions)
		
		go_to_eel = self.mainapp.frames[self.backend.go_to_eel]

		if self.backend.current_eel != None:
			item_comparison, parts_comparison = go_to_eel.backend.compare_eels(self.mainapp.frames[self.backend.current_eel].backend)
		
			treeview_functions.write_data_to_treeview(self.comp_item_tree, 'replace', item_comparison)
			treeview_functions.write_data_to_treeview(self.comp_part_tree, 'replace', parts_comparison)

		for tree in [self.comp_item_tree, self.comp_part_tree]:
			for child in tree.get_children():
				if tree.item(child, 'values')[-1] == '-':
					tree.item(child,tag='none')
				else:
					if float(tree.item(child, 'values')[-1]) >= 0:
						tree.item(child,tag='positive')
					else:
						tree.item(child,tag='negative')
				
		# update BOM table

		data = []
		for part in self.backend.bom:
			part = self.mainapp.frames[part].backend
			type = part.equipment_type
			data.append([part.title, type, self.backend.bom[part.title]])
			
			for a in part.attaching_hardware:
				qty = int(a[3])*self.backend.bom[part.title]
				data.append([a[2], a[1], qty])
			data.append([''])
			
		treeview_functions.write_data_to_treeview(self.bom_tree, 'replace', data)

		# update OHSC Table

		
		go_to = self.mainapp.frames[self.backend.go_to_eel]
		ohsc = self.mainapp.frames[go_to.backend.ohsc].backend

		trees = {'LHS': self.LHS_ohsc_tree, 'RHS': self.RHS_ohsc_tree}
		for side in ['LHS', 'RHS']:
			data = []
			for o in ohsc.layout[side]:

				data.append(copy.deepcopy(o))

				bin_frame = f'OHSC {side} {o[2]} - {o[3]}'

				limit = float(o[4])
				bin_weight = 0

				if bin_frame in self.backend.layout:

					for p in self.backend.layout[bin_frame]:
						part = self.mainapp.frames[p[1]].backend

						weight = float(part.weight)

						bin_weight += weight
						
				delta = bin_weight - limit
				data[-1].append(bin_weight)
				data[-1].append(delta)

			treeview_functions.write_data_to_treeview(trees[side], 'replace', data)

			for child in trees[side].get_children():
				if float(trees[side].item(child, 'values')[-1]) <= 0:
					trees[side].item(child,tag='negative')
				else:
					trees[side].item(child,tag='positive')

		treeview_functions.write_data_to_treeview(self.item_numbers_tree, 'replace', self.backend.equip_item_nos)

	def export_dxf(self):

		mode = 'edit'
		
		self.w=word_export.Export_Word_Excel_Window(self.mainapp, self.master, mode, self, 'dxf')
		self.master.wait_window(self.w.top)
		
	def draw_dxf(self, file):

		eel_draw.gen_dxf(self, file)

	def export_word(self):

		mode = 'edit'
		
		self.w=word_export.Export_Word_Excel_Window(self.mainapp, self.master, mode, self)
		self.master.wait_window(self.w.top)
		
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

		if self.mode == 'edit':
			self.orig_title = parent_page.backend.title
			eel_comp_bk.update_variables(self, self.parent_page.backend)
		else:
			self.orig_title = None

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
		
		self.title_entry=Entry(self.details_frame, width=60)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_title]

		if self.mode == 'edit':
			self.title_entry.insert(0, self.parent_page.backend.title)


		self.description_entry=Entry(self.details_frame, width=60)		
		self.description_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			self.description_entry.insert(0, self.parent_page.backend.description)

		self.ac_combo= ttk.Combobox(self.details_frame, values=['A320'], state='disabled')
		self.ac_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.ac_combo.set('A320')

		self.eel_dict['A320'].insert(0, '')
		self.current_combo= ttk.Combobox(self.details_frame, values=self.eel_dict['A320'])
		self.current_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')

		if self.mode == 'edit':
			self.current_combo.insert(0, self.parent_page.backend.current_eel)

		self.current_combo.config(state='readonly')

		self.goto_combo= ttk.Combobox(self.details_frame, values=self.eel_dict['A320'])
		self.goto_combo.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Go To EEL'] = ['combo', self.goto_combo, 'not empty', 'Go To EEL']

		if self.mode == 'edit':
			self.goto_combo.insert(0, self.parent_page.backend.go_to_eel)

		self.goto_combo.config(state='readonly')

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, padx=5, pady=5,sticky="ne")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, padx=5, pady=5,sticky="nw")

	def cleanup(self, button):
	
		self.button = button
		
		if button == 'ok':

			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)

			if data_good:
				self.title = self.title_entry.get()
				self.aircraft_type = self.ac_combo.get()
				self.description = self.description_entry.get()
				self.current_eel = self.current_combo.get()

				if self.current_eel == '':
					self.current_eel = None

				self.go_to_eel = self.goto_combo.get()
				self.top.destroy()
			else:

				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)

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

		if self.parent_page.backend.current_eel != None:
			self.current_eel = self.mainapp.frames[self.parent_page.backend.current_eel]
			self.current_eel.backend.gen_summary_dict()
		else:
			self.current_eel = None

		self.go_to_eel = self.mainapp.frames[self.parent_page.backend.go_to_eel]
		self.go_to_eel.backend.gen_summary_dict()

		self.check_if_current_parts_available()

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

		self.combo_callback(None)
	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.top, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def check_if_current_parts_available(self):

		if self.parent_page.backend.current_eel == None:
			self.current_parts_avail = False
		else:
			current_locations = self.current_eel.backend.get_item_locations(self.item)

			if len(current_locations) == 0:
				self.current_parts_avail = False
			else:
				self.current_parts_avail = True

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
		
		if self.current_eel:
			current_locations = self.current_eel.backend.get_item_locations(self.item)
			
			for loc in current_locations:
				if loc not in self.locations:
					self.locations.append(loc)
		
		self.locations_frames = {}
		for loc in self.locations:
			lf = LabelFrame(self.main_scroll_frame.inner,text=loc)
			self.locations_frames[loc] = lf
			lf.grid(row=self.label_frame_row, column=0, columnspan = 3, rowspan = 1,sticky='NW',padx=5, pady=25, ipadx=2, ipady=5)
			self.label_frame_row += 1


	def setup_buttons(self):

		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=1, padx=5, pady=5,sticky="ne")

		# cancel button
		self.b=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=2, padx=5, pady=5,sticky="nw")

	def setup_totals(self):

		self.total_labels = {'Current': {}, 'Go To': {}, 'Total': {}}
		
		# Current 
		ttk.Label(self.current_frame, text="Part Number").grid(row = 0, column = 1, columnspan=1, padx=10)
		ttk.Label(self.current_frame, text="Existing Qty").grid(row = 0, column = 2, columnspan=1, padx=10)
		ttk.Label(self.current_frame, text="Selected Qty").grid(row = 0, column = 3, columnspan=1, padx=10)

		row = 1

		if self.current_eel:
			if self.item in self.current_eel.backend.summary.keys():
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
			label.grid(row = 0, column = 4, columnspan=2, padx=10)

			label = ttk.Label(lf, text="Total Required Qty")
			label.grid(row = 0, column = 7, padx=10)

			label = ttk.Label(lf, text="Total Selected Qty")
			label.grid(row = 0, column = 8, padx=10)

			# Add Current Parts
			
			if self.current_eel:
				item_part_nos = self.current_eel.backend.get_item_part_no_by_location(self.item)
				
				row = 1

				if loc in item_part_nos.keys():
					for part_no in item_part_nos[loc]:

						tk.Label(lf,text=part_no,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 1, sticky = 'W')

						for p in self.current_eel.backend.layout[loc]:
							if p[1] == part_no:
								q = int(p[3])
						#q = self.current_eel.backend.summary[self.item][part_no]
						c = ttk.Combobox(lf, values=[q for q in range(q+1)], state='readonly')
						c.grid(row = row, column = 2, sticky = 'W', padx=15)
						c.set(0)

						c.bind('<<ComboboxSelected>>',
								lambda event: self.combo_callback(event))

						self.combos[loc]['Current'][part_no] = c
						row += 1

			#Add Go To Parts

			row = 1
			total_qty = 0

			item_part_nos = self.go_to_eel.backend.get_item_part_no_by_location(self.item)
			
			tk.Label(lf,width=15).grid(row = 1, column = 3, sticky = 'W') #dummy  label to add blank space

			if loc in item_part_nos.keys():
				for part_no in item_part_nos[loc]:

					tk.Label(lf,text=part_no,bg="white",borderwidth=2, relief="groove",width=20).grid(row = row, column = 4, sticky = 'W')

					q = item_part_nos[loc][part_no]

					total_qty += q
					c = ttk.Combobox(lf, values=[q for q in range(q+1)], state='readonly')
					c.grid(row = row, column = 5, sticky = 'W', padx=15)

					c.set(0)

					if not self.current_parts_avail:
						c.set(q)

					c.bind('<<ComboboxSelected>>',
							lambda event: self.combo_callback(event))

					self.combos[loc]['Go To'][part_no] = c
					row += 1

			# Add Total 

			tk.Label(lf,width=15).grid(row = 1, column = 6, sticky = 'W') #dummy  label to add blank space

			self.combos[loc]['Total Required'] = total_qty
			#Total Required
			tk.Label(lf,text=total_qty,bg="white",borderwidth=2, relief="groove",width=20).grid(row = 1, column = 7, sticky = 'W')

			# Total Selected
			label = tk.Label(lf, text="0",bg='SteelBlue1',borderwidth=2, relief="groove",width=20)
			label.grid(row = 1, column = 8, padx=15)

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
		self.bom = {}
		
		instructions_count = 1
		
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
						
						if leftover > 0:
							current_leftovers.append([part_no, loc, leftover])
						
					else:
					
						qty_tracker[loc] += qty_selected*-1
						
					self.layout[loc].append([self.item, part_no, loc, qty_selected, 'Existing'])
					self.instructions.append([instructions_count ,f'x{qty_selected} {part_no} ({self.item}) Remains Installed in {loc}'])

					instructions_count += 1
		# For locations in Current EEL, not present in the Go To EEL, Add those parts to the leftovers

		for loc in self.combos:
			if loc not in qty_tracker.keys():
				for part_no in self.combos[loc]['Current']:
					
					qty_selected = int(self.combos[loc]['Current'][part_no].get())
					
					if qty_selected > 0:
						current_leftovers.append([part_no, loc, qty_selected])

		# Loop through new Items, assign to their location if that location is not full
		for loc in qty_tracker:
			
			qty_required = qty_tracker[loc]

			for part_no in self.combos[loc]['Go To']:
				
				qty_selected = int(self.combos[loc]['Go To'][part_no].get())
				
				if qty_selected > 0:
				
					if qty_selected >= qty_required:
					
						leftover = qty_selected - qty_required
						
						if qty_required > 0: #handles if current items already fill this location
							qty_tracker[loc] += qty_selected*-1
						
						if leftover > 0:
							go_to_leftovers.append([part_no, loc, leftover])
						
					else:
					
						qty_tracker[loc] += qty_selected*-1
					
					if qty_required > 0:
						self.layout[loc].append([self.item, part_no, loc, qty_selected, 'New'])	
						self.instructions.append([instructions_count ,f'Install x{qty_selected} {part_no} ({self.item}) in {loc}'])
	
						instructions_count += 1
						
						if part_no not in self.bom.keys():
							self.bom[part_no] = qty_selected
						else:
							self.bom[part_no] += qty_selected
						
						
		# Assign any left over parts (both existing and new) to any unfilled positions

		for loc in qty_tracker:
			
			# loop through current leftovers first
			qty_required = qty_tracker[loc]
				
			for idx, part in enumerate(current_leftovers):
					
				if qty_required > 0:

					qty_available = part[2]
					
					if qty_available >= qty_required:

						self.layout[loc].append([self.item, part[0], loc, qty_required, 'Existing'])
						
						self.instructions.append([instructions_count ,f'Relocate x{qty_required} {part[0]} ({self.item}) from {part[1]} to {loc}'])
						
						instructions_count += 1
						
						current_leftovers[idx][2] += qty_required*-1

						qty_required = 0

					elif qty_available >0:

						self.layout[loc].append([self.item, part[0], loc, qty_available, 'Existing'])
						self.instructions.append([instructions_count ,f'Relocate x{qty_available} {part[0]} ({self.item}) from {part[1]} to {loc}'])
					
						instructions_count += 1
						
						current_leftovers[idx][2] += qty_available*-1

						qty_required += qty_available*-1

		# Assign any left over parts (both existing and new) to any unfilled positions
		# Repeat for Go To leftovers
		for loc in qty_tracker:
			
			# loop through current leftovers first
			qty_required = qty_tracker[loc]
				
			for idx, part in enumerate(go_to_leftovers):
					
				if qty_required > 0:

					qty_available = part[2]
					
					if qty_available >= qty_required:

						self.layout[loc].append([self.item, part[0], loc, qty_required, 'New'])

						go_to_leftovers[idx][2] += qty_required*-1

						qty_required = 0

						#Add to Instructions
						self.instructions.append([instructions_count ,f'Install x{qty_required} {part[0]} ({self.item}) in {loc}'])
						
						
						#Add to BOM
						if part[0] not in self.bom.keys():
							self.bom[part[0]] = qty_selected
						else:
							self.bom[part[0]] += qty_selected

					elif qty_available >0:

						self.layout[loc].append([self.item, part[0], loc, qty_available, 'New'])
						
						go_to_leftovers[idx][2] += qty_available*-1

						qty_required += qty_available*-1

						#Add to Instructions
						self.instructions.append([instructions_count ,f'Install x{qty_available} {part[0]} ({self.item}) in {loc}'])
						
						#Add to BOM
						if part[0] not in self.bom.keys():
							self.bom[part[0]] = qty_available
						else:
							self.bom[part[0]] += qty_available


class Edit_Item_Window(object):
	def __init__(self, mainapp, master, mode, parent_page):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_page = parent_page

		eel_comp_bk.setup_variables(self)
		eel_comp_bk.update_variables(self, self.parent_page.backend)

		self.setup_label_frames()
		
		self.parts = {}
		
		#current_items = treeview_functions.get_all_treeview_items(self.parent_lopa.item_tree)
		for loc in self.layout:
			for part in self.parent_page.backend.layout[loc]:
				if part[1] not in self.parts:
					self.parts[part[1]] = Entry(self.items_frame)
					
					#insert current number in tree
					for c in self.equip_item_nos:
						if c[0] == part[1]:
							self.parts[part[1]].insert(0, c[1])

		self.setup_widgets()		
		
		self.button = 'cancel'

	def setup_label_frames(self):
	
		self.auto_frame = LabelFrame(self.top,text="Autogen Options:")
		self.auto_frame.grid(row=2, column=0, columnspan = 4, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.items_frame = LabelFrame(self.top,text="Item Numbers:")
		self.items_frame.grid(row=3,column=0, columnspan = 4, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	

	def setup_widgets(self):
	
		# ____ AUTOGEN OPTIONS ____
		
		Button(self.auto_frame, text = 'Autogen Numbers', command=self.autogen).grid(row=0, column = 1, sticky='NSEW')
		# starting number
		Label(self.auto_frame, text = 'Starting Number:').grid(row=1, column = 1, sticky='NSEW')
		self.start_entry = Entry(self.auto_frame)
		self.start_entry.grid(row=1, column = 2, padx=1, pady=1, sticky='NSEW')
		
		# format
		Label(self.auto_frame, text = 'Format:').grid(row=2, column = 1, sticky='NSEW')
		self.format_combo = ttk.Combobox(self.auto_frame, values=['1, 2, 3, etc', '01, 02, 03, etc'], state='readonly')
		self.format_combo.grid(row=2, column = 2, padx=1, pady=1, sticky='NSEW')
		
		# ____ Parts ____

		column = 1

		row = 2
		for part in self.parts:
			Label(self.items_frame, text = part).grid(row=row, column=column, sticky='NSEW')
			self.parts[part].grid(row=row, column=column+1, sticky='NSEW', padx = 2)
			row +=1

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, padx=5, pady=5,sticky="ne")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, padx=5, pady=5,sticky="nw")	

	def autogen(self):
	
		start_no = 1
		
		try:
			start_no = int(self.start_entry.get())
		except:
			pass
			
		no = start_no
		for part in self.parts:
			self.parts[part].delete(0, 'end')
			if self.format_combo.get() == '01, 02, 03, etc'and no < 10:
				text = f'0{no}'
			else:
				text = no
				
			self.parts[part].insert(0, text)
			
			no += 1

	def cleanup(self, button):
	
		self.button = button

		if self.button == 'ok':
			
			count = 1
			self.equip_item_nos = []

			for part in self.parts:

				self.equip_item_nos.append([part, self.parts[part].get()])
				count += 1
					
			self.top.destroy()
			
		else:
			
			self.top.destroy()