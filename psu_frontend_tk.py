import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import psu_backend as psu_bk
import gui_styles_tk
import components_tk
import data_input_checks_tk

import treeview_functions
import lopa_draw
#import ipc_generator as ipc_gen
import psu_draw
import double_scrollbar
import comment_box
import word_export

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import copy

from docx import Document

class PSU_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp
		
		self.top_label = tk.Label(self, text=('PSU Layout: '),font=self.mainapp.title_font, anchor="w")
		self.top_label.pack(fill=tk.BOTH, expand=True)
		
		self.backend = psu_bk.PSU_Backend(self, mainapp)
		
		self.treeview_iid = None
		self.setup_notebook()
		self.setup_scrollable_frames()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_treeviews()
		self.setup_buttons()
		self.add_lopa_plot()
		self.set_grid_configures()
		
		#self.dummy_label = gui_styles_tk.create_label(self.lopa_frame,'sdsad')
		#self.dummy_label.grid(row = 8, column = 0,pady=2,padx=2, sticky="nsew")
		#self.dummy_canvas = tk.Canvas(self.lopa_frame, height=200, bg="blue")
		#self.dummy_canvas.grid(row=7, column=0, columnspan = 1, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)

	def onFrameConfigure(self, canvas):
		'''Reset the scroll region to encompass the inner frame'''
		canvas.configure(scrollregion=canvas.bbox("all"))

	def FrameWidth(self, event):
		canvas_width = event.width
		self.lopa_frame_canvas.itemconfig(self.canvas_frame, width = canvas_width)
		
	def set_grid_configures(self):
		
		self.layout_scroll_frame.inner.grid_columnconfigure(4, weight=1)

	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		# self.lopa_frame_canvas = tk.Canvas(self.psu_tab, height=self.mainapp.screen_height-80, bg="blue")
		# self.lopa_frame_canvas.configure(scrollregion=self.lopa_frame_canvas.bbox("all"))
		# self.lopa_frame_canvas.grid(row=0,column=0,stick='nsew')
		# self.psu_tab.grid_columnconfigure(0, weight=1)
		# self.psu_tab.grid_rowconfigure(0, weight=1)

		# self.lopa_frame = tk.Frame(self.lopa_frame_canvas)
		# self.canvas_frame = self.lopa_frame_canvas.create_window((0,0), window=self.lopa_frame, anchor='nw')
		# #self.lopa_frame.grid(row=0,column=0,stick='nsew')

		# vsb = tk.Scrollbar(self.psu_tab, orient="vertical", command=self.lopa_frame_canvas.yview)
		# self.lopa_frame_canvas.configure(yscrollcommand=vsb.set)
		# vsb.grid(row=0,column=1,stick='nsew')
		# self.lopa_frame.bind("<Configure>", lambda event, canvas=self.lopa_frame_canvas: self.onFrameConfigure(canvas))
		# self.lopa_frame_canvas.bind('<Configure>', self.FrameWidth)
		
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.layout_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.psu_tab, self.mainapp)
		self.layout_scroll_frame.pack(fill=tk.BOTH, expand=True)
		
	def setup_notebook(self):
	
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.psu_tab = Frame(self.note)
		self.bom_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.psu_tab, text = "PSU Layout")
		self.note.add(self.bom_tab, text = "BOM")
		self.note.add(self.comments_tab, text = "Comments")
		
		#self.note.grid(row=1,column=0,sticky='NSEW')
		self.note.pack(fill=tk.BOTH, expand=True)
		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50, state='disabled')
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.main_scroll_frame.inner,text="PSU Layout Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.existing_frame = LabelFrame(self.main_scroll_frame.inner,text="Part Numbers:")
		self.existing_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.layout_frame = LabelFrame(self.layout_scroll_frame.inner,text="Parts:")
		self.layout_frame.grid(row=3, column=0, columnspan = 4, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.preview_frame = LabelFrame(self.layout_scroll_frame.inner,text="PSU Layout Preview:")
		self.preview_frame.grid(row=5, column=0, columnspan = 5, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		self.preview_frame.grid_columnconfigure(4, weight=1)

	def setup_labels(self):
	

		self.dwg_no_label = gui_styles_tk.create_label(self.main_frame,'')
		self.dwg_no_label.grid(row = 2, column = 0,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.dwg_rev_label = gui_styles_tk.create_label(self.main_frame,'')
		self.dwg_rev_label.grid(row = 2, column = 2,columnspan=2, pady=2,padx=2, sticky="nsew")
		
		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 4,columnspan=8, pady=2,padx=2, sticky="nsew")
		self.description_label.configure(width=70)
		
		self.lopa_label = gui_styles_tk.create_label(self.main_frame,'')
		self.lopa_label.grid(row = 3, column = 0,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.aircraft_label = gui_styles_tk.create_label(self.main_frame,'')
		self.aircraft_label.grid(row = 3, column = 2,columnspan=2, pady=2,padx=2, sticky="nsew")
		
		
		
	def setup_treeviews(self):
	
		self.parts_tree = ttk.Treeview(self.existing_frame, selectmode="extended",columns=("A","B",'C','D', 'E', 'F'),height = 15)
		#self.monument_tree.grid(row=1,column=0, columnspan= 6,sticky="nsew")
		self.parts_tree.heading("#0", text="#")
		self.parts_tree.column("#0",minwidth=0,width=60, stretch='NO')
		self.parts_tree.heading("A", text="Type")	  
		self.parts_tree.column("A",minwidth=0,width=200, stretch='NO') 
		self.parts_tree.heading("B", text="Part Number")	  
		self.parts_tree.column("B",minwidth=0,width=150, stretch='NO')
		self.parts_tree.heading("C", text="Existing Qty")	  
		self.parts_tree.column("C",minwidth=0,width=150, stretch='NO')	
		self.parts_tree.heading("D", text="Required Qty")	  
		self.parts_tree.column("D",minwidth=0,width=150, stretch='NO')	
		self.parts_tree.heading("E", text="Additional Qty")	  
		self.parts_tree.column("E",minwidth=0,width=150, stretch='NO')
		self.parts_tree.heading("F", text="BOM Qty")	  
		self.parts_tree.column("F",minwidth=0,width=150, stretch='NO')
		
		self.parts_tree.grid(row = 2, column = 0, columnspan = 8, sticky = 'NSEW')

		self.parts_tree.bind("<Double-1>", lambda event: self.parts_double_click(event))

		data = [[1, 'Oxygen Box', 'Oxy Box', 7],
				[2, '11" PSIU', '11in', 7],
				[3, '8" PSIU', '8in', 7],
				[4, '6" PSIU', '6in', 7],
				[5, '1" Filler Panel', '1in Filler', 7],
				[6, '2" Filler Panel', '2in Filler', 7],
				[7, '4" Filler Panel', '4in Filler', 7],
				[8, '6" Filler Panel', '6in Filler', 3],
				[9, '8" Filler Panel', '8in Filler', 1],
				[10, 'Partition Panel', 'Partition', 1],
				[11, 'Adjustment Panel', 'Adjust', 1],
				[12, 'Clamping Panel', 'Clamp', 1],]

		#treeview_functions.write_data_to_treeview(self.parts_tree, 'replace', data)

		
		self.LHS_tree_psu = ttk.Treeview(self.layout_frame,selectmode="extended",columns=("A","B","C"))
		self.LHS_tree_psu.grid(row=1,column=0, columnspan = 3, sticky="nsew")
		self.LHS_tree_psu.heading("#0", text="Row")
		self.LHS_tree_psu.column("#0",minwidth=0,width=50, stretch='NO')
		self.LHS_tree_psu.heading("A", text="Component")   
		self.LHS_tree_psu.column("A",minwidth=0,width=300, stretch='NO') 
		self.LHS_tree_psu.heading("B", text="P/N")   
		self.LHS_tree_psu.column("B",minwidth=0,width=60)
		self.LHS_tree_psu.heading("C", text="Station")   
		self.LHS_tree_psu.column("C",minwidth=0,width=60)
		
		LHS_psu_tree_scrollbar = Scrollbar(self.layout_frame, command=self.LHS_tree_psu.yview)
		LHS_psu_tree_scrollbar.grid(row=1, column=3, sticky='nsew')
		self.LHS_tree_psu.config(yscrollcommand=LHS_psu_tree_scrollbar.set)

		
		self.RHS_tree_psu = ttk.Treeview(self.layout_frame,selectmode="extended",columns=("A","B","C"))
		self.RHS_tree_psu.grid(row=1,column=4, columnspan = 3, sticky="nsew")
		self.RHS_tree_psu.heading("#0", text="Row")
		self.RHS_tree_psu.column("#0",minwidth=0,width=50, stretch='NO')
		self.RHS_tree_psu.heading("A", text="Component")   
		self.RHS_tree_psu.column("A",minwidth=0,width=300, stretch='NO') 
		self.RHS_tree_psu.heading("B", text="P/N")   
		self.RHS_tree_psu.column("B",minwidth=0,width=60)
		self.RHS_tree_psu.heading("C", text="Station")   
		self.RHS_tree_psu.column("C",minwidth=0,width=60)
		
		RHS_psu_tree_scrollbar = Scrollbar(self.layout_frame, command=self.RHS_tree_psu.yview)
		RHS_psu_tree_scrollbar.grid(row=1, column=7, sticky='nsew')
		self.RHS_tree_psu.config(yscrollcommand=RHS_psu_tree_scrollbar.set)

	def setup_buttons(self):

		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.dxf_btn = Button(self.main_scroll_frame.inner, image = self.mainapp.cad_icon2, compound = LEFT, text = 'Export to DXF',width = 30, command= lambda: self.export_dxf())
		self.dxf_btn.grid(row=1, column=1, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.ms_word_btn = Button(self.main_scroll_frame.inner, image = self.mainapp.word_icon2, compound = LEFT, text = 'Export to Word',width = 30, command= lambda: self.export_word())
		self.ms_word_btn.grid(row=1, column=2, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)
		
		self.gen_btn = Button(self.layout_scroll_frame.inner, text = 'Generate Layout',
						command = self.gen_layout)
		self.gen_btn.grid(row=0,column=0, sticky="nsew")

		self.edit_comment_button=Button(self.comments_tab,text='Edit', image = self.mainapp.edit_icon2, compound = LEFT,
										command= lambda self=self :comment_box.edit_comments(self))
		self.edit_comment_button.grid(row=0,column=0, pady=5,sticky="nsew", ipadx=2, ipady=2)
		# self.expand_lopa_tree_btn = Button(self.lopa_frame, text = "Expand Trees",
							  # command = lambda height=30, trees = [self.LHS_lopa_tree,self.RHS_lopa_tree]: self.expand_tree(trees,height))
		# self.expand_lopa_tree_btn.grid(row=0, column=0, columnspan=4, sticky='nsew')

	def add_lopa_plot(self):
		
		self.canvas = FigureCanvasTkAgg(self.backend.lopa_figure, self.preview_frame)
		self.canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=8, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")
		
	def update_component(self, window, type, redraw = True):
		
		self.backend.update_component(window, type)
		self.update_label_text()

		lopa = self.mainapp.frames[self.backend.lopa]

		self.backend.ax1.clear()
		#self.backend.ax2.clear()
		self.backend.ax3.clear()
		
		#lopa_draw.draw_aircraft(lopa.backend, self.backend.ax2, 'matplotlib', [0,0])
		lopa_draw.draw_floor(lopa.backend, self.backend.ax1, 'matplotlib', [0,0])
		lopa_draw.draw_floor(lopa.backend, self.backend.ax3, 'matplotlib', [0,0])

		lopa_draw.draw_seats_side(lopa.backend, self.backend.ax3, 'matplotlib', [0,0], 'LHS')
		lopa_draw.draw_seats_side(lopa.backend, self.backend.ax1, 'matplotlib', [0,0], 'RHS')
		
		lopa_draw.draw_windbreakers_side(lopa.backend, [self.backend.ax1, self.backend.ax3], 'matplotlib', [0,0])
		lopa_draw.draw_lavs_side(lopa.backend, [self.backend.ax1, self.backend.ax3], 'matplotlib', [0,0])
		lopa_draw.draw_galleys_side(lopa.backend, [self.backend.ax1, self.backend.ax3], 'matplotlib', [0,0,0,0])
		
		psu_draw.draw_psu_rail_side(lopa.backend, self.backend.ax3, 'matplotlib', [0,0], 'LHS')
		psu_draw.draw_psu_rail_side(lopa.backend, self.backend.ax1, 'matplotlib', [0,0], 'RHS')
		
		psu_draw.draw_psu_layout(self.backend, self.backend.ax3, 'matplotlib', [0,0], 'LHS')
		psu_draw.draw_psu_layout(self.backend, self.backend.ax1, 'matplotlib', [0,0], 'RHS')
		self.canvas.draw()

		self.backend.update_parts_table()
			
		treeview_functions.write_data_to_treeview(self.parts_tree, 'replace', self.backend.parts)

		treeview_functions.write_data_to_treeview(self.LHS_tree_psu, 'replace', self.backend.psu_layout['LHS'])
		treeview_functions.write_data_to_treeview(self.RHS_tree_psu, 'replace', self.backend.psu_layout['RHS'])	

		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)
		#self.backend.ax1.draw()
		#self.backend.ax2.draw()
		#self.backend.ax3.draw()
	def update_label_text(self):
		self.top_label.config(text=f'PSU Layout: {self.backend.title}')
		self.lopa_label.config(text=f' LOPA: {self.backend.lopa}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.dwg_no_label.config(text=f' Drawing Number: {self.backend.drawing_no}')
		self.dwg_rev_label.config(text=f' Drawing Revision: {self.backend.drawing_rev}')
		self.aircraft_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')

	def gen_layout(self):

		self.w=Gen_PSU_Window_Tk(self.mainapp, self.master, None, None, self)
		self.master.wait_window(self.w.top)
		
		if self.w.button == 'ok':
			start_lhs = 320
			start_rhs = 320
			end_lhs = 1206.98
			end_rhs = 1206.98
			
			x, lav_d, lav_e, wb_installed = self.w.parent_lopa.backend.get_psu_rail_start_end()
				
			psu_layout = self.backend.gen_a320_psu_layout(self.w.psiu_layout, x[0][0], x[0][1], x[1][0], x[1][1], wb_installed, lav_d, lav_e)
			
			treeview_functions.write_data_to_treeview(self.LHS_tree_psu, 'replace', psu_layout['LHS'])
			treeview_functions.write_data_to_treeview(self.RHS_tree_psu, 'replace', psu_layout['RHS'])
			
			self.w.psu_layout = psu_layout
			
			self.update_component(self.w, 'edit', True)
			#psu_draw.draw_psu_layout(self.backend, self.backend.ax3, 'matplotlib', [0,0], 'LHS')
			#psu_draw.draw_psu_layout(self.backend, self.backend.ax1, 'matplotlib', [0,0], 'RHS')

	def parts_double_click(self, event):
	
		item = self.parts_tree.selection()[0]
		index = self.parts_tree.index(item)
		
		parts_data = list(self.parts_tree.item(item,"values"))
		parts_data.insert(0, self.parts_tree.item(item,"text"))

		self.w=Double_Click_Part_Window_Tk(self, self.mainapp, self.master, parts_data, index)
		self.master.wait_window(self.w.top)
		
		if self.w.button == 'ok':

			self.update_component(self.w, 'edit', False)

	def export_word(self):

		mode = 'edit'
		
		self.w=word_export.Export_Word_Window(self.mainapp, self.master, mode, self)
		self.master.wait_window(self.w.top)	

	def export_dxf(self):
		psu_draw.gen_dxf(self)

		

	def edit(self):

		self.w= Edit_PSU_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')
		
class Edit_PSU_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_psu):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_psu = parent_psu

		psu_bk.setup_variables(self)
		if mode=='edit':
			#self.parts = treeview_functions.get_all_treeview_items(parent_psu.parts_tree)
			psu_bk.PSU_Backend.update_variables(self, self.parent_psu.backend)
			
		self.lopas = components_tk.get_all_components(mainapp, 'LOPAs')['All']
		#self.lopas = lopas

		self.orig_part_no = None
		
		if mode == 'edit':
			self.orig_part_no = parent_psu.backend.title
		self.data_checks = {}
		
		self.setup_label_frames()
		self.setup_widgets()
		self.button = 'cancel'
			
		

			
	def setup_label_frames(self):		
		self.details_frame = LabelFrame(self.top,text="PSU Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
		
		labels = ['Title:', 'Description:', 'Drawing Number:', 'Revision:', 'LOPA:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)
		
		self.title_entry=Entry(self.details_frame, width=20)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_part_no]			
			
		self.description_entry=Entry(self.details_frame, width=40)		
		self.description_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
					
		self.drawing_entry=Entry(self.details_frame, width=20)		
		self.drawing_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.revision_combo= ttk.Combobox(self.details_frame, values=[i for i in range(99)])
		self.revision_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.lopa_combo= ttk.Combobox(self.details_frame, values=self.lopas, state='readonly')
		self.lopa_combo.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['LOPA'] = ['combo', self.lopa_combo, 'in values', 'LOPA']
		
		if self.mode == 'edit':
			self.title_entry.insert(0, self.title)
			self.description_entry.insert(0, self.description)
			self.drawing_entry.insert(0, self.drawing_no)
			self.revision_combo.set(self.drawing_rev)
			self.lopa_combo.set(self.lopa)
			self.lopa_combo.config(state='disabled')
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")

	def cleanup(self, button):
		
		self.button = button
		
		if self.button == 'ok':
			
			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)
			
			if data_good:
				self.title = self.title_entry.get()
				self.description = self.description_entry.get()
				self.drawing_no = self.drawing_entry.get()
				self.drawing_rev = self.revision_combo.get()
				self.lopa = self.lopa_combo.get()
				self.aircraft_type = self.mainapp.frames[self.lopa].backend.aircraft_type
				self.parts = [[1, 'Oxygen Box LHS', 'Oxy Box L', 7, 0, 0, 0],
						[2, 'Oxygen Box RHS', 'Oxy Box R', 7, 0, 0, 0],
						[3, '11" PSIU', '11in', 7, 0, 0, 0],
						[4, '8" PSIU', '8in', 7, 0, 0, 0],
						[5, '6" PSIU', '6in', 7, 0, 0, 0],
						[6, '1" Filler Panel', '1in Filler', 20, 0, 0, 0],
						[7, '2" Filler Panel', '2in Filler', 7, 0, 0, 0],
						[8, '4" Filler Panel', '4in Filler', 7, 0, 0, 0],
						[9, '6" Filler Panel', '6in Filler', 7, 0, 0, 0],
						[10, '8" Filler Panel', '8in Filler', 2, 0, 0, 0],
						[11, 'Partition Panel LHS', 'Partition', 1, 0, 0, 0],
						[12, 'Partition Panel RHS', 'Partition', 1, 0, 0, 0],
						[13, 'Adjustment Panel LHS', 'Adjust', 1, 0, 0, 0],
						[14, 'Adjustment Panel LHS', 'Adjust', 1, 0, 0, 0],
						[15, 'Clamping Panel', 'Clamp', 1, 0, 0, 0],]
				self.top.destroy()
			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		else:
			self.top.destroy()
		
		
class Gen_PSU_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_psu):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
			
		self.mainapp = mainapp
		self.mode = mode
		self.parent_psu = parent_psu
		
		self.setup_scrollable_frames()

		self.parent_lopa = self.mainapp.frames[self.parent_psu.backend.lopa]
		
		
		self.setup_label_frames()
		self.setup_widgets()
		
		# get number of rows
		self.no_lhs = int(self.parent_lopa.backend.no_lhs_seats)
		self.no_rhs = int(self.parent_lopa.backend.no_rhs_seats)
		self.top.geometry("900x600")
		
		psu_bk.PSU_Backend.update_variables(self, self.parent_psu.backend)
		
		#determine start end points
		x, lav_d, lav_e, wb_installed = self.parent_lopa.backend.get_psu_rail_start_end()
		
		if wb_installed[0]:
			self.lhs_start_combo.set('Windbreaker')
		else:
			self.lhs_start_combo.set('Station 320')
		self.lhs_start_combo.config(state='disabled')

		if wb_installed[1]:
			self.rhs_start_combo.set('Windbreaker')
		else:
			self.rhs_start_combo.set('Station 320')
		self.rhs_start_combo.config(state='disabled')
		
		if lav_d:
			self.lhs_end_combo.set('Lav Station 1207')
		else:
			self.lhs_end_combo.set('Station 1230')
		self.lhs_end_combo.config(state='disabled')
		#
		if lav_e:
			self.rhs_end_combo.set('Lav Station 1207')
		else:
			self.rhs_end_combo.set('Station 1230')
		self.rhs_end_combo.config(state='disabled')
		
	def setup_label_frames(self):
	
		self.lhs_frame = LabelFrame(self.lopa_frame,text="LHS Options:")
		self.lhs_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
				
		self.rhs_frame = LabelFrame(self.lopa_frame,text="RHS Options:")
		self.rhs_frame.grid(row=2, column=8, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)		

		#self.options_frame = LabelFrame(self.lopa_frame,text="Options:")
		#self.options_frame.grid(row=2, column=16, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	
		
		self.lhs_rows_frame = LabelFrame(self.lopa_frame,text="LHS Rows:")
		self.lhs_rows_frame.grid(row=7, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.rhs_rows_frame = LabelFrame(self.lopa_frame,text="RHS Rows:")
		self.rhs_rows_frame.grid(row=7, column=8, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):

		start_values = ['Station 320', 'Windbreaker']
		end_values = ['Station 1230', 'Lav Station 1207']
		
		labels = ['Number of 11 Inch PSIU:', 'Number of 8 Inch PSIU:', 'Start Station:', 'End Station:']
		row = 2
		gui_styles_tk.create_multiple_labels(self.lhs_frame, labels, row, 2, 20, 2, 2)
		gui_styles_tk.create_multiple_labels(self.rhs_frame, labels, row, 2, 20, 2, 2)
		
		self.lhs_11_combo = ttk.Combobox(self.lhs_frame, values=[i for i in range (30)])
		self.lhs_11_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.lhs_8_combo = ttk.Combobox(self.lhs_frame, values=[i for i in range (30)])
		self.lhs_8_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')	

		self.lhs_start_combo = ttk.Combobox(self.lhs_frame, values=start_values)
		self.lhs_start_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.lhs_end_combo = ttk.Combobox(self.lhs_frame, values=end_values)
		self.lhs_end_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		#
		self.rhs_11_combo = ttk.Combobox(self.rhs_frame, values=[i for i in range (30)])
		self.rhs_11_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.rhs_8_combo = ttk.Combobox(self.rhs_frame, values=[i for i in range (30)])
		self.rhs_8_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.rhs_start_combo = ttk.Combobox(self.rhs_frame, values=start_values)
		self.rhs_start_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.rhs_end_combo = ttk.Combobox(self.rhs_frame, values=end_values)
		self.rhs_end_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
			
		#
		
		self.lhs_combos = {}
		self.rhs_combos = {}
		values = ['11" PSIU', '8" PSIU']
		
		for s in ['LHS', 'RHS']:
			labels = []
			
			if s == 'LHS':
				lf = self.lhs_rows_frame
			else:
				lf = self.rhs_rows_frame
			
			row_no = 2
			for row in self.parent_lopa.backend.seat_layout[s]:
				labels.append(f'Row {row[0]}:')
				
				if s == 'LHS':
					self.lhs_combos[row[0]] = ttk.Combobox(lf, values=values)
					self.lhs_combos[row[0]].grid(row=row_no,column=3,padx=2, pady=2,sticky = 'NSEW')
				if s == 'RHS':
					self.rhs_combos[row[0]] = ttk.Combobox(lf, values=values)
					self.rhs_combos[row[0]].grid(row=row_no,column=3,padx=2, pady=2,sticky = 'NSEW')
				row_no +=1	
			row = 2

			gui_styles_tk.create_multiple_labels(lf, labels, row, 2, 20, 2, 2)
			
		
		self.auto_button=Button(self.lopa_frame,text='Auto Assign', command= self.auto_assign)
		self.auto_button.grid(row=6,column=7, pady=5,sticky="nsew")			
		
		# ok button
		self.ok_button=Button(self.lopa_frame,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=7, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.lopa_frame,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=8, pady=5,sticky="nsew")

	def cleanup(self, button):
		
		self.button = button
		
		if self.button == 'ok':
			
			message = self.check_data()
			
			if self.data_ok:
				self.psiu_layout = {'LHS': [], 'RHS': []}
				
				for c in self.lhs_combos:
					self.psiu_layout['LHS'].append(self.lhs_combos[c].get())
				for c in self.rhs_combos:
					self.psiu_layout['RHS'].append(self.rhs_combos[c].get())
				
				self.lhs_start = self.lhs_start_combo.get()
				self.rhs_start = self.rhs_start_combo.get()
				self.lhs_end = self.lhs_end_combo.get()
				self.rhs_end = self.rhs_end_combo.get()
				
				self.top.destroy()
			else:
				tkinter.messagebox.showerror(title='Error', message=message)
		else:
			self.top.destroy()
		
		
	def check_data(self):
		
		self.data_ok = True
		message = None
		
		#1. Check numeric entries where required
		try:
			self.no_of_11_inch_psiu_lhs = int(self.lhs_11_combo.get())
			self.no_of_8_inch_psiu_lhs = int(self.lhs_8_combo.get())
			self.no_of_11_inch_psiu_rhs = int(self.rhs_11_combo.get())
			self.no_of_8_inch_psiu_rhs = int(self.rhs_8_combo.get())
		except:
			self.data_ok = False
			message = 'Error, Number of PSIUs must be intergers'

		#2. Number PSIUs must equal number rowspan
		if self.data_ok:
			
			if self.no_of_11_inch_psiu_lhs + self.no_of_8_inch_psiu_lhs != self.no_lhs:
				self.data_ok = False
				message = f'Error, Number of LHS PSIUs must equal {self.no_lhs}'

		if self.data_ok:
			
			if self.no_of_11_inch_psiu_rhs + self.no_of_8_inch_psiu_rhs != self.no_rhs:
				self.data_ok = False
				message = f'Error, Number of RHS PSIUs must equal {self.no_rhs}'
				
		#3. Number of 11" PSIUs must be sufficient
		
		if self.data_ok:
			
			if self.no_of_11_inch_psiu_lhs < (self.no_lhs/2) + 1:
				self.data_ok = False
				message = f'Error, Number of LHS PSIUs must be greater {self.no_lhs/2}'

		if self.data_ok:
			
			if self.no_of_11_inch_psiu_rhs < (self.no_rhs/2) + 1:
				self.data_ok = False
				message = f'Error, Number of RHS PSIUs must be greater {self.no_rhs/2}'
				
		return message
		
	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.lopa_frame_canvas = tk.Canvas(self.top, height=self.mainapp.screen_height-380, bg="blue")
		self.lopa_frame_canvas.configure(scrollregion=self.lopa_frame_canvas.bbox("all"))
		self.lopa_frame_canvas.grid(row=0,column=0,stick='nsew')
		self.top.grid_columnconfigure(0, weight=1)
		self.top.grid_rowconfigure(0, weight=1)

		self.lopa_frame = tk.Frame(self.lopa_frame_canvas)
		self.canvas_frame = self.lopa_frame_canvas.create_window((0,0), window=self.lopa_frame, anchor='nw')
		#self.lopa_frame.grid(row=0,column=0,stick='nsew')

		vsb = tk.Scrollbar(self.top, orient="vertical", command=self.lopa_frame_canvas.yview)
		self.lopa_frame_canvas.configure(yscrollcommand=vsb.set)
		vsb.grid(row=0,column=1,stick='nsew')
		self.lopa_frame.bind("<Configure>", lambda event, canvas=self.lopa_frame_canvas: self.onFrameConfigure(canvas))
		self.lopa_frame_canvas.bind('<Configure>', self.FrameWidth)

	def onFrameConfigure(self, canvas):
		'''Reset the scroll region to encompass the inner frame'''
		canvas.configure(scrollregion=canvas.bbox("all"))
		
	def FrameWidth(self, event):
		canvas_width = event.width
		self.lopa_frame_canvas.itemconfig(self.canvas_frame, width = canvas_width)
		
	def auto_assign(self):
	
		psiu_layout = self.parent_psu.backend.auto_assign_psius()
		
		for row in psiu_layout['LHS']:
			self.lhs_combos[row[0]].set(row[-1])
		for row in psiu_layout['RHS']:
			self.rhs_combos[row[0]].set(row[-1])
			
class Double_Click_Part_Window_Tk(object):			
	def __init__(self, parent_psu, mainapp, master, parts_data, index):
		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp
		self.parent_psu = parent_psu
		self.parts_data = copy.deepcopy(parts_data)
		self.index = index
		
		self.data_checks = {}
		psu_bk.setup_variables(self)
		psu_bk.PSU_Backend.update_variables(self, self.parent_psu.backend)
		
		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
	
		self.options_frame = LabelFrame(self.top,text="Options:")
		self.options_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_widgets(self):
	
		labels = ['Part Number:', 'Existing Qty:', 'Additonal Qty:',]
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, labels, row, 2, 20, 2, 2)		
		
		self.pn_entry=Entry(self.options_frame, width=20)		
		self.pn_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		if len(self.parts_data) > 2:
			self.pn_entry.insert(0,self.parts_data[2])	
		
		self.e_qty_entry=Entry(self.options_frame, width=20)		
		self.e_qty_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		if len(self.parts_data) > 3:		
			self.e_qty_entry.insert(0,self.parts_data[3])	
		self.data_checks['Existing Qty'] = ['entry', self.e_qty_entry, 'int positive', 'Existing Qty']
		
		self.a_qty_entry=Entry(self.options_frame, width=20)		
		self.a_qty_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')	
		if len(self.parts_data) > 5:
			self.a_qty_entry.insert(0,self.parts_data[5])	
		self.data_checks['Additional Qty'] = ['entry', self.a_qty_entry, 'int positive', 'Additional Qty']
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")
		
	def cleanup(self,button):
		
		self.button = button
		if button == 'ok':
		
			self.check_data()
			
			if self.data_ok:
				
				self.pn_qty = self.pn_entry.get() #existing qty
				self.e_qty = int(float(self.e_qty_entry.get())) #existing qty
				self.a_qty = int(float(self.a_qty_entry.get())) #additonal qty
				
				self.parts[self.index][2] = self.pn_qty
				self.parts[self.index][3] = self.e_qty
				self.parts[self.index][5] = self.a_qty
				
				# self.lhs_start = self.lhs_start_combo.get()
				# self.lhs_end = self.lhs_end_combo.get()
				# self.rhs_start = self.rhs_start_combo.get()
				# self.rhs_end = self.rhs_end_combo.get()
				self.top.destroy()
				
			else:
				tkinter.messagebox.showerror(title='Error', message=self.message)
		else:
			self.top.destroy()
			
	def check_data(self):
	
		self.data_ok = True
		self.message = None

		try:
			int(float(self.e_qty_entry.get()))
			int(float(self.a_qty_entry.get()))
		except:
			self.data_ok = False
			self.message = 'Error: Quantities must be numeric values'
			
		if self.data_ok:
			
			if int(float(self.e_qty_entry.get())) < 0:
				self.data_ok = False
				self.message = 'Error: Quantities must be greater than or equal to 0'				

			if int(float(self.a_qty_entry.get())) < 0:
				self.data_ok = False
				self.message = 'Error: Quantities must be greater than or equal to 0'
				