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
import time

from docx import Document

import pandas as pd

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
		self.gasper_scroll_frame.inner.grid_columnconfigure(4, weight=1)

	def setup_scrollable_frames(self):

		
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.main_tab, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.layout_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.psu_tab, self.mainapp)
		self.layout_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.gasper_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.gasper_tab, self.mainapp)
		self.gasper_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.deu_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.deu_tab, self.mainapp)
		self.deu_scroll_frame.pack(fill=tk.BOTH, expand=True)

	def setup_notebook(self):
	
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.psu_tab = Frame(self.note)
		self.gasper_tab = Frame(self.note)
		self.deu_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.psu_tab, text = "PSU Layout")
		self.note.add(self.gasper_tab, text = "Gasper Hoses")
		self.note.add(self.deu_tab, text = "DEU/VCC")
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

		self.gasper_frame = LabelFrame(self.gasper_scroll_frame.inner,text="Gaspers:")
		self.gasper_frame.grid(row=2, column=0, columnspan = 4, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.gasper_preview_frame = LabelFrame(self.gasper_scroll_frame.inner,text="PSU Layout Preview:")
		self.gasper_preview_frame.grid(row=5, column=0, columnspan = 5, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		self.gasper_preview_frame.grid_columnconfigure(4, weight=1)

		self.deu_frame = LabelFrame(self.deu_scroll_frame.inner,text="DEU/VC:")
		self.deu_frame.grid(row=2, column=0, columnspan = 15, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.deu_preview_frame = LabelFrame(self.deu_scroll_frame.inner,text="PSU Layout Preview:")
		self.deu_preview_frame.grid(row=5, column=0, columnspan = 16, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		self.deu_preview_frame.grid_columnconfigure(7, weight=1)

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
	
		self.parts_tree = ttk.Treeview(self.existing_frame, selectmode="extended",columns=("A","B",'C','D', 'E', 'F'),height = 18)
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
				[12, 'Clamping Panel', 'Clamp', 1],
				[13, 'Gasper Hose 400mm', 'G400', 1],
				[14, 'Gasper Hose 250mm', 'G250', 1],
				[15, 'Gasper Hose 150mm', 'G150', 1],]

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

				 #setup LHS Gasper treeview
		self.LHS_tree_gasper = ttk.Treeview(self.gasper_frame,selectmode="extended",columns=("A","B","C"))
		self.LHS_tree_gasper.grid(row=1,column=0, sticky="nsew")
		self.LHS_tree_gasper.heading("#0", text="Row")
		self.LHS_tree_gasper.column("#0",minwidth=0,width=50, stretch='NO')
		self.LHS_tree_gasper.heading("A", text="Vent Frame")   
		self.LHS_tree_gasper.column("A",minwidth=0,width=100, stretch='NO') 
		self.LHS_tree_gasper.heading("B", text="Vent Station")   
		self.LHS_tree_gasper.column("B",minwidth=0,width=100)
		self.LHS_tree_gasper.heading("C", text="Hose Length")   
		self.LHS_tree_gasper.column("C",minwidth=0,width=100)

		LHS_tree_gasper_scrollbar = Scrollbar(self.gasper_frame, command=self.LHS_tree_gasper.yview)
		LHS_tree_gasper_scrollbar.grid(row=1, column=1, padx=5, sticky='nsew')
		self.LHS_tree_gasper.config(yscrollcommand=LHS_tree_gasper_scrollbar.set)

		self.RHS_tree_gasper = ttk.Treeview(self.gasper_frame,selectmode="extended",columns=("A","B","C"))
		self.RHS_tree_gasper.grid(row=1,column=2, sticky="nsew")
		self.RHS_tree_gasper.heading("#0", text="Row")
		self.RHS_tree_gasper.column("#0",minwidth=0,width=50, stretch='NO')
		self.RHS_tree_gasper.heading("A", text="Vent Frame")   
		self.RHS_tree_gasper.column("A",minwidth=0,width=100, stretch='NO') 
		self.RHS_tree_gasper.heading("B", text="Vent Station")   
		self.RHS_tree_gasper.column("B",minwidth=0,width=100)
		self.RHS_tree_gasper.heading("C", text="Hose Length")   
		self.RHS_tree_gasper.column("C",minwidth=0,width=100)

		RHS_tree_gasper_scrollbar = Scrollbar(self.gasper_frame, command=self.RHS_tree_gasper.yview)
		RHS_tree_gasper_scrollbar.grid(row=1, column=3, sticky='nsew')
		self.RHS_tree_gasper.config(yscrollcommand=RHS_tree_gasper_scrollbar.set)

		#### Treeviews for DEU ###
		self.deu_tree = ttk.Treeview(self.deu_frame,selectmode="extended",columns=("A","B","C"))
		self.deu_tree.grid(row=1,column=1, columnspan=4, sticky="nsew")
		self.deu_tree.heading("#0", text="DEU Title")
		self.deu_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.deu_tree.heading("A", text="Station (cm)")   
		self.deu_tree.column("A",minwidth=0,width=80, stretch='NO') 
		self.deu_tree.heading("B", text="Station (in)")   
		self.deu_tree.column("B",minwidth=0,width=80)
		self.deu_tree.heading("C", text="Side")   
		self.deu_tree.column("C",minwidth=0,width=50)

		deu_scrollbar = Scrollbar(self.deu_frame, command=self.deu_tree.yview)
		deu_scrollbar.grid(row=1, column=5, sticky='nsew')
		self.deu_tree.config(yscrollcommand=deu_scrollbar.set)

		self.lhs_vcc_tree = ttk.Treeview(self.deu_frame,selectmode="extended",columns=("A","B","C","D"))
		self.lhs_vcc_tree.grid(row=1,column=6, sticky="nsew")        
		self.lhs_vcc_tree.heading("#0", text="VC Title")
		self.lhs_vcc_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.lhs_vcc_tree.heading("A", text="Frame")   
		self.lhs_vcc_tree.column("A",minwidth=0,width=80, stretch='NO') 
		self.lhs_vcc_tree.heading("B", text="Station (in)")   
		self.lhs_vcc_tree.column("B",minwidth=0,width=80)
		self.lhs_vcc_tree.heading("C", text="DEU")   
		self.lhs_vcc_tree.column("C",minwidth=0,width=90)
		self.lhs_vcc_tree.heading("D", text="Row")   
		self.lhs_vcc_tree.column("D",minwidth=0,width=50)

		lhs_vcc_scrollbar = Scrollbar(self.deu_frame, command=self.lhs_vcc_tree.yview)
		lhs_vcc_scrollbar.grid(row=1, column=7, sticky='nsew')
		self.lhs_vcc_tree.config(yscrollcommand=lhs_vcc_scrollbar.set)

		self.rhs_vcc_tree = ttk.Treeview(self.deu_frame,selectmode="extended",columns=("A","B","C","D"))
		self.rhs_vcc_tree.grid(row=1,column=8, sticky="nsew")        
		self.rhs_vcc_tree.heading("#0", text="VC Title")
		self.rhs_vcc_tree.column("#0",minwidth=0,width=150, stretch='NO')
		self.rhs_vcc_tree.heading("A", text="Frame")   
		self.rhs_vcc_tree.column("A",minwidth=0,width=80, stretch='NO') 
		self.rhs_vcc_tree.heading("B", text="Station (in)")   
		self.rhs_vcc_tree.column("B",minwidth=0,width=80)
		self.rhs_vcc_tree.heading("C", text="DEU")   
		self.rhs_vcc_tree.column("C",minwidth=0,width=90)
		self.rhs_vcc_tree.heading("D", text="Row")   
		self.rhs_vcc_tree.column("D",minwidth=0,width=50)

		rhs_vcc_scrollbar = Scrollbar(self.deu_frame, command=self.rhs_vcc_tree.yview)
		rhs_vcc_scrollbar.grid(row=1, column=9, sticky='nsew')
		self.rhs_vcc_tree.config(yscrollcommand=rhs_vcc_scrollbar.set)
	
	def setup_buttons(self):

		self.edit_btn = Button(self.main_scroll_frame.inner, text = 'Edit', image = self.mainapp.edit_icon2, compound = LEFT, width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.dxf_btn = Button(self.main_scroll_frame.inner, image = self.mainapp.cad_icon2, compound = LEFT, text = 'Export to DXF',width = 30, command= lambda: self.export_dxf())
		self.dxf_btn.grid(row=1, column=1, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.ms_word_btn = Button(self.main_scroll_frame.inner, image = self.mainapp.word_icon2, compound = LEFT, text = 'Export to Word',width = 30, command= lambda: self.export_word())
		self.ms_word_btn.grid(row=1, column=2, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.excel_btn = Button(self.main_scroll_frame.inner, image = self.mainapp.excel_icon2, compound = LEFT, text = 'Export to Excel',width = 30, command= lambda: self.export_excel())
		self.excel_btn.grid(row=1, column=3, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)
		
		self.gen_btn = Button(self.layout_scroll_frame.inner, text = 'Generate Layout',  width = 30,
						command = self.gen_layout)
		self.gen_btn.grid(row=0,column=0, padx=5, pady=2, ipadx=2, ipady=2, sticky="nw")

		self.edit_gasper_btn = Button(self.gasper_scroll_frame.inner, text = 'Edit Gasper Layout', image = self.mainapp.edit_icon2, compound = LEFT, width = 30,
						command = self.edit_gasper_layout)
		self.edit_gasper_btn.grid(row=0,column=0, padx=5, pady=2, ipadx=2, ipady=2, sticky="nw")

		self.edit_deu_btn = Button(self.deu_scroll_frame.inner, width = 30, text = 'Edit DEU Layout', image = self.mainapp.edit_icon2, compound = LEFT,
						command = self.edit_deu_layout)
		self.edit_deu_btn.grid(row=0,column=0, padx=5, pady=2, ipadx=2, ipady=2, sticky="w")

		self.edit_vc_btn = Button(self.deu_scroll_frame.inner, width = 30, text = 'Edit VC Layout', image = self.mainapp.edit_icon2, compound = LEFT,
						command = self.edit_vc_layout)
		self.edit_vc_btn.grid(row=0,column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="w")

		#self.assign_vc_btn = ttk.Button(self.deu_scroll_frame.inner, width = 30, text = 'Assign VC Layout',
		#				command = self.assign_vc_layout)
		#self.assign_vc_btn.grid(row=0,column=2, padx=5, pady=2, ipadx=2, ipady=2, sticky="w")


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


		#Gasper hoses
		self.gasper_canvas = FigureCanvasTkAgg(self.backend.gasper_figure, self.gasper_preview_frame)
		self.gasper_canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.gasper_canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=8, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.gasper_preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.gasper_canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")

		#DEU
		self.deu_canvas = FigureCanvasTkAgg(self.backend.deu_figure, self.deu_preview_frame)
		self.deu_canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.deu_canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=8, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.deu_preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.deu_canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")

	def update_component(self, window, type, redraw = True):
		
		start_time = time.time()
		self.backend.update_component(window, type)
		self.update_label_text()

		lopa = self.mainapp.frames[self.backend.lopa]

		self.backend.ax1.clear()
		#self.backend.ax2.clear()
		self.backend.ax3.clear()

		self.backend.ax4.clear()
		#self.backend.ax6.clear()
		self.backend.ax7.clear()

		#lopa_draw.draw_aircraft(lopa.backend, self.backend.ax2, 'matplotlib', [0,0])
		for canvas in [[self.backend.ax1, self.backend.ax3]]:#, [self.backend.ax4, self.backend.ax6]]:

			lopa_draw.draw_floor(lopa.backend, canvas[0], 'matplotlib', [0,0])
			lopa_draw.draw_floor(lopa.backend, canvas[1], 'matplotlib', [0,0])

			lopa_draw.draw_seats_side(lopa.backend, canvas[0], 'matplotlib', [0,0], 'RHS')
			lopa_draw.draw_seats_side(lopa.backend, canvas[1], 'matplotlib', [0,0], 'LHS')
		
			lopa_draw.draw_windbreakers_side(lopa.backend, [canvas[0], canvas[1]], 'matplotlib', [0,0])
			lopa_draw.draw_lavs_side(lopa.backend, [canvas[0], canvas[1]], 'matplotlib', [0,0])
			lopa_draw.draw_galleys_side(lopa.backend, [canvas[0], canvas[1]], 'matplotlib', [0,0,0,0])
		
			psu_draw.draw_psu_rail_side(lopa.backend, canvas[1], 'matplotlib', [0,0], 'RHS')
			psu_draw.draw_psu_rail_side(lopa.backend, canvas[0], 'matplotlib', [0,0], 'LHS')

		psu_draw.draw_psu_layout(self.backend, self.backend.ax3, 'matplotlib', [0,0], 'LHS', 'all')
		psu_draw.draw_psu_layout(self.backend, self.backend.ax1, 'matplotlib', [0,0], 'RHS', 'all')

		# Gasper/DEU Top Down
		for canvas in [self.backend.ax4, self.backend.ax7]:
			lopa_draw.draw_aircraft(lopa.backend, canvas, 'matplotlib', [0,0])
			lopa_draw.draw_windbreakers_top_down(lopa.backend, canvas, 'matplotlib', [0,0])	
			lopa_draw.draw_lavs_top_down(lopa.backend, canvas, 'matplotlib', [0,0])
			lopa_draw.draw_galleys_top_down(lopa.backend, canvas, 'matplotlib', [0,0])

			psu_draw.draw_psu_rail_top_down(lopa.backend, canvas, 'matplotlib', [0,0])


		psu_draw.draw_psu_layout(self.backend, self.backend.ax4, 'matplotlib', [0,0], 'LHS', 'gasper', 'top_down')
		psu_draw.draw_psu_layout(self.backend, self.backend.ax4, 'matplotlib', [0,0], 'RHS', 'gasper', 'top_down')
		
		psu_draw.draw_psu_layout(self.backend, self.backend.ax7, 'matplotlib', [0,0], 'LHS', 'psiu', 'top_down')
		psu_draw.draw_psu_layout(self.backend, self.backend.ax7, 'matplotlib', [0,0], 'RHS', 'psiu', 'top_down')

		psu_draw.draw_deus(self.backend, self.backend.ax7, 'matplotlib', [0,0], 'LHS', 'top_down')
		psu_draw.draw_deus(self.backend, self.backend.ax7, 'matplotlib', [0,0], 'RHS', 'top_down')


		self.canvas.draw()
		self.gasper_canvas.draw()
		self.deu_canvas.draw()

		self.backend.update_parts_table()
			
		treeview_functions.write_data_to_treeview(self.parts_tree, 'replace', self.backend.parts)

		treeview_functions.write_data_to_treeview(self.LHS_tree_gasper, 'replace', self.backend.gasper_layout['LHS'])
		treeview_functions.write_data_to_treeview(self.RHS_tree_gasper, 'replace', self.backend.gasper_layout['RHS'])	

		treeview_functions.write_data_to_treeview(self.LHS_tree_psu, 'replace', self.backend.psu_layout['LHS'])	
		treeview_functions.write_data_to_treeview(self.RHS_tree_psu, 'replace', self.backend.psu_layout['RHS'])	

		treeview_functions.write_data_to_treeview(self.deu_tree, 'replace', self.backend.deu_layout['LHS'])	
		treeview_functions.write_data_to_treeview(self.deu_tree, 'append', self.backend.deu_layout['RHS'])	

		treeview_functions.write_data_to_treeview(self.lhs_vcc_tree, 'replace', self.backend.vc_layout['LHS'])	
		treeview_functions.write_data_to_treeview(self.rhs_vcc_tree, 'replace', self.backend.vc_layout['RHS'])	
		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)
		print("--- %s seconds ---" % (time.time() - start_time))
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

	def edit_gasper_layout(self):

		self.w= Edit_Gasper_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)		

		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')

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

	def export_excel(self):
		
		df_parts = treeview_functions.treeview_to_df(self.parts_tree)
		df_parts.set_index('#')

		#Layout
		df_lhs_layout = treeview_functions.treeview_to_df(self.LHS_tree_psu)
		df_lhs_layout.rename(columns={"Row": "LHS Row", "Component": "LHS Component", 'P/N': 'LHS P/N', 'Station': 'LHS Station'}, inplace=True)

		df_rhs_layout = treeview_functions.treeview_to_df(self.RHS_tree_psu)
		df_rhs_layout.rename(columns={"Row": "RHS Row", "Component": "RHS Component", 'P/N': 'RHS P/N', 'Station': 'RHS Station'}, inplace=True)

		df_layout = pd.concat([df_lhs_layout, df_rhs_layout], axis=1,)

		#Gasper Hoses
		df_lhs_gasper = treeview_functions.treeview_to_df(self.LHS_tree_gasper)
		df_lhs_gasper.rename(columns={"Row": "LHS Row", "Vent Frame": "LHS Vent Frame", 'Vent Station': 'LHS Vent Station', 'Hose length': 'LHS Hose Length'}, inplace=True)

		df_rhs_gasper = treeview_functions.treeview_to_df(self.RHS_tree_gasper)
		df_rhs_gasper.rename(columns={"Row": "RHS Row", "Vent Frame": "RHS Vent Frame", 'Vent Station': 'RHS Vent Station', 'Hose length': 'RHS Hose Length'}, inplace=True)

		df_gasper = pd.concat([df_lhs_gasper, df_rhs_gasper], axis=1,)

		df_deu = treeview_functions.treeview_to_df(self.deu_tree)

		df_lhs_vcc = treeview_functions.treeview_to_df(self.lhs_vcc_tree)
		df_lhs_vcc.rename(columns={"VC Title": "LHS VC Title", "Frame": "LHS Frame", 'Station (in)': 'LHS Station (in)', 'DEU': 'LHS DEU', 'Row': 'LHS Row'}, inplace=True)

		df_rhs_vcc = treeview_functions.treeview_to_df(self.rhs_vcc_tree)
		df_rhs_vcc.rename(columns={"VC Title": "RHS VC Title", "Frame": "RHS Frame", 'Station (in)': 'RHS Station (in)', 'DEU': 'RHS DEU', 'Row': 'RHS Row'}, inplace=True)

		df_vcc = pd.concat([df_lhs_vcc, df_rhs_vcc], axis=1,)

		with pd.ExcelWriter(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.15\psu.xlsx') as writer:
   			df_parts.to_excel(writer, sheet_name='Parts')
   			df_layout.to_excel(writer, sheet_name='PSU Layout')
   			df_gasper.to_excel(writer, sheet_name='Gasper Hose Layout')
   			df_deu.to_excel(writer, sheet_name='DEU Layout')
   			df_vcc.to_excel(writer, sheet_name='VCC Layout')

	def export_dxf(self):
		psu_draw.gen_dxf(self)

		

	def edit(self):

		self.w= Edit_PSU_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')

	def edit_deu_layout(self):
		self.w= Edit_DEU_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)	

		if self.w.button == 'ok':

			self.update_component(self.w, 'edit')


	def edit_vc_layout(self):
		self.w=Edit_VCC_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)	

		if self.w.button == 'ok':

			self.update_component(self.w, 'edit')

	def assign_vc_layout(self):
		pass
		
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
		
		self.title_entry=Entry(self.details_frame, width=60)		
		self.title_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_part_no]			
			
		self.description_entry=Entry(self.details_frame, width=60)		
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
						[15, 'Clamping Panel', 'Clamp', 1, 0, 0, 0],
						[16, 'Gasper Hose 400mm', 'G400', 1, 0, 0, 0],
						[17, 'Gasper Hose 250mm', 'G250', 1, 0, 0, 0],
						[18, 'Gasper Hose 150mm', 'G150', 1, 0, 0, 0],]

				self.top.destroy()
			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		else:
			self.top.destroy()
		

class Edit_Gasper_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_psu):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_psu = parent_psu

		#get LOPA row numbers
		self.row_numbers = self.mainapp.frames[self.parent_psu.backend.lopa].backend.get_all_row_numbers()
		self.row_numbers['LHS'].append('N/A')
		self.row_numbers['RHS'].append('N/A')

		psu_bk.setup_variables(self)
		psu_bk.PSU_Backend.update_variables(self, self.parent_psu.backend)

		self.setup_label_frames()
		self.setup_labels()
		self.setup_entries()
		self.setup_buttons()

		self.button = 'cancel'

		self.top.geometry("900x600")

	def setup_label_frames(self):

		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.top, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.lhs_frame = LabelFrame(self.main_scroll_frame.inner, text='LHS')
		self.lhs_frame.grid(row=2, column=0, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		self.rhs_frame = LabelFrame(self.main_scroll_frame.inner, text='RHS')
		self.rhs_frame.grid(row=2, column=16, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.label_frames = {'LHS': self.lhs_frame, 'RHS': self.rhs_frame}

	def setup_labels(self):

		for frame in [self.lhs_frame, self.rhs_frame]:

			Label(frame, text='Row').grid(row=0, column=1, sticky='nsew')
			Label(frame, text='Vent Frame').grid(row=0, column=2, sticky='nsew')
			Label(frame, text='Vent Station').grid(row=0, column=3, sticky='nsew')
			Label(frame, text='Hose Length').grid(row=0, column=4, sticky='nsew')

	def setup_entries(self):

		self.vent_station_entries = {'LHS': [], 'RHS': []}
		self.vent_frame_entries = {'LHS': [], 'RHS': []}
		self.hose_length_combos = {'LHS': [], 'RHS': []}
		self.row_combos = {'LHS': [], 'RHS': []}

		for side in self.vent_station_entries.keys():
			row = 1
			for v in self.parent_psu.backend.gasper_layout[side]:

				#Assigned Row
				c = ttk.Combobox(self.label_frames[side], values=self.row_numbers[side])
				c.grid(row=row, column=1, pady=2, sticky='nsew')
				c.insert(0, v[0])
				self.row_combos[side].append(c)

				# vent frames
				e = Entry(self.label_frames[side])
				e.grid(row=row, column=2, pady=2, sticky='nsew')
				e.insert(0, v[1])
				e.config(state='disabled')
				self.vent_frame_entries[side].append(e)

				# vent stations
				e = Entry(self.label_frames[side])
				e.grid(row=row, column=3, pady=2, sticky='nsew')
				e.insert(0, v[2])
				e.config(state='disabled')
				self.vent_station_entries[side].append(e)

				# hose lengths
				c = ttk.Combobox(self.label_frames[side], values=['400mm', '250mm', '150mm', 'N/A'], state='readonly')
				c.grid(row=row, column=4, pady=2, sticky='nsew')
				c.insert(0, v[3])
				self.hose_length_combos[side].append(c)

				row += 1

	def setup_buttons(self):

		Button(self.main_scroll_frame.inner, text='auto assign', command=self.auto_assign_hoses).grid(row=0, column=0, sticky='nsew')

		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=7, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=8, pady=5,sticky="nsew")

	def auto_assign_hoses(self):

		

		row_stations = copy.deepcopy(self.mainapp.frames[self.parent_psu.backend.lopa].backend.get_all_row_stations())
		available_stations = copy.deepcopy(row_stations)
		gasper_stations = self.parent_psu.backend.get_gasper_stations()

		if len(row_stations['LHS']) == len(gasper_stations['LHS']) and len(row_stations['RHS']) == len(gasper_stations['RHS']):
			self.assigned_vents = {'LHS': {}, 'RHS': {}}
			for side in ['LHS', 'RHS']:
				#get selected vent stations
				available_vents = []
				for vent in self.vent_station_entries[side]:
					available_vents.append(float(vent.get()))

				#loop over each row
				for idx, row in enumerate(row_stations[side]):

					row_gasper = gasper_stations[side][idx]

					closest = min(available_vents, key=lambda x:abs(x-row_gasper))

					available_vents.remove(closest)

					distance = abs(closest-row_gasper)
					
					if distance > 10.5:
						hose = '400mm'
					elif distance > 4.5 and distance < 10.5:
						hose = '250mm'
					else:
						hose = '150mm'
					#print()
					self.assigned_vents[side][self.row_numbers[side][idx]] = [closest, hose]

				#update combos
				for idx, e in enumerate(self.vent_station_entries[side]):
					e = float(e.get())
					#print(f'entry {e}')
					vent_used = False
					for row in self.assigned_vents[side].keys():
						#print(f'Assigned {self.assigned_vents[side][row][0]}')
						if self.assigned_vents[side][row][0] == e:
							vent_used = True
							self.hose_length_combos[side][idx].set(self.assigned_vents[side][row][1])
							self.row_combos[side][idx].set(row)
							break

					if not vent_used:
						self.hose_length_combos[side][idx].set('N/A')
						self.row_combos[side][idx].set('N/A')

	def cleanup(self, button):

		#TODO Add data checks

		self.button = button

		if self.button == 'ok':

			#check for any rows asigned, 
			msg = None

			for side in ['LHS', 'RHS']:
				for i, c in enumerate(self.row_combos[side]):
					if c.get() != 'N/A':
						if self.hose_length_combos[side][i].get() == 'N/A':
							msg = f'Gasper Hose Length Must be Selected for Row {c.get()} {side}'

			if not msg:
				self.gasper_layout = {'LHS': [], 'RHS': []}

				for side in self.gasper_layout.keys():
					
					for idx, row in enumerate(self.row_combos[side]):

						row = self.row_combos[side][idx].get()
						f = self.vent_frame_entries[side][idx].get()
						s = self.vent_station_entries[side][idx].get()
						h = self.hose_length_combos[side][idx].get()

						self.gasper_layout[side].append([row, f, s, h])


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

		self.auto_assign()
		self.count_psius(None)

		for c in self.lhs_combos:
			self.lhs_combos[c].bind("<<ComboboxSelected>>", self.count_psius)

		for c in self.rhs_combos:
			self.rhs_combos[c].bind("<<ComboboxSelected>>", self.count_psius)

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
		
		#self.lhs_11_combo = ttk.Combobox(self.lhs_frame, values=[i for i in range (30)])
		#self.lhs_11_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		#self.lhs_8_combo = ttk.Combobox(self.lhs_frame, values=[i for i in range (30)])
		#self.lhs_8_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')	

		self.lhs_11_label=Label(self.lhs_frame, text='0')
		self.lhs_11_label.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.lhs_8_label=Label(self.lhs_frame, text='0')
		self.lhs_8_label.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.lhs_start_combo = ttk.Combobox(self.lhs_frame, values=start_values)
		self.lhs_start_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.lhs_end_combo = ttk.Combobox(self.lhs_frame, values=end_values)
		self.lhs_end_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		#
		#self.rhs_11_combo = ttk.Combobox(self.rhs_frame, values=[i for i in range (30)])
		#self.rhs_11_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		#self.rhs_8_combo = ttk.Combobox(self.rhs_frame, values=[i for i in range (30)])
		#self.rhs_8_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.rhs_11_label=Label(self.rhs_frame, text='0')
		self.rhs_11_label.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.rhs_8_label=Label(self.rhs_frame, text='0')
		self.rhs_8_label.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

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
					self.lhs_combos[row[0]] = ttk.Combobox(lf, values=values, state='readonly')
					self.lhs_combos[row[0]].grid(row=row_no,column=3,padx=2, pady=2,sticky = 'NSEW')
				if s == 'RHS':
					self.rhs_combos[row[0]] = ttk.Combobox(lf, values=values, state='readonly')
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
			
			#message = self.check_data()
			self.data_ok = True

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
		
	def count_psius(self, event):

		self.count = {'LHS': {'11': 0, '8':0}, 'RHS': {'11': 0, '8':0}}

		for c in self.lhs_combos.keys():

			p = self.lhs_combos[c].get()

			if '11"' in p:
				self.count['LHS']['11'] += 1
			elif '8"' in p:
				self.count['LHS']['8'] += 1

		for c in self.rhs_combos.keys():

			p = self.rhs_combos[c].get()

			if '11"' in p:
				self.count['RHS']['11'] += 1
			elif '8"' in p:
				self.count['RHS']['8'] += 1

		self.lhs_11_label.config(text=str(self.count['LHS']['11']))
		self.lhs_8_label.config(text=str(self.count['LHS']['8']))

		self.rhs_11_label.config(text=str(self.count['RHS']['11']))
		self.rhs_8_label.config(text=str(self.count['RHS']['8']))

	def check_data(self):
		
		self.data_ok = True
		message = None
		
		self.no_of_11_inch_psiu_lhs = self.count['LHS']['11']
		self.no_of_8_inch_psiu_lhs = self.count['LHS']['8']

		self.no_of_11_inch_psiu_rhs = self.count['RHS']['11']
		self.no_of_8_inch_psiu_rhs = self.count['RHS']['8']

		#1. Check numeric entries where required
		# try:
		# 	self.no_of_11_inch_psiu_lhs = int(self.lhs_11_combo.get())
		# 	self.no_of_8_inch_psiu_lhs = int(self.lhs_8_combo.get())
		# 	self.no_of_11_inch_psiu_rhs = int(self.rhs_11_combo.get())
		# 	self.no_of_8_inch_psiu_rhs = int(self.rhs_8_combo.get())
		# except:
		# 	self.data_ok = False
		# 	message = 'Error, Number of PSIUs must be intergers'

		#2. Number PSIUs must equal number rowspan
		# if self.data_ok:
			
		# 	if self.no_of_11_inch_psiu_lhs + self.no_of_8_inch_psiu_lhs != self.no_lhs:
		# 		self.data_ok = False
		# 		message = f'Error, Number of LHS PSIUs must equal {self.no_lhs}'

		# if self.data_ok:
			
		# 	if self.no_of_11_inch_psiu_rhs + self.no_of_8_inch_psiu_rhs != self.no_rhs:
		# 		self.data_ok = False
		# 		message = f'Error, Number of RHS PSIUs must equal {self.no_rhs}'
				
		#3. Number of 11" PSIUs must be sufficient
		
		if self.data_ok:
			
			if self.no_of_11_inch_psiu_lhs < (self.no_lhs/2) + 1:
				self.data_ok = False
				message = f'Error, Number of LHS PSIUs must be greater {ceil(self.no_lhs/2)}'

		if self.data_ok:
			
			if self.no_of_11_inch_psiu_rhs < (self.no_rhs/2) + 1:
				self.data_ok = False
				message = f'Error, Number of RHS PSIUs must be greater {ceil(self.no_rhs/2)}'
				
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

class Edit_DEU_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_psu):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_psu = parent_psu

		psu_bk.setup_variables(self)
		psu_bk.PSU_Backend.update_variables(self, self.parent_psu.backend)

		self.setup_label_frames()
		self.setup_labels()
		self.setup_entries()
		self.setup_buttons()

		self.button = 'cancel'

		self.top.geometry("900x600")

	def setup_label_frames(self):
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.top, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		#self.deu_frame = LabelFrame(self.main_scroll_frame.inner, text='DEUs')
		#self.deu_frame.grid(row=2, column=0, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.lhs_frame = LabelFrame(self.main_scroll_frame.inner, text='LHS DEUs')
		self.lhs_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.rhs_frame = LabelFrame(self.main_scroll_frame.inner, text='RHS DEUs')
		self.rhs_frame.grid(row=2, column=8, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.label_frames = {'LHS': self.lhs_frame, 'RHS': self.rhs_frame}

	def setup_labels(self):

		for side in ['LHS', 'RHS']:
			f = self.label_frames[side]

			Label(f, text='#').grid(row=0, column=1, sticky='nw')
			Label(f, text='DEU Title').grid(row=0, column=2, sticky='nw')
			Label(f, text='DEU Frame').grid(row=0, column=3, sticky='nw')
			Label(f, text='DEU Station (in)').grid(row=0, column=4, sticky='nw')
			Label(f, text='Side').grid(row=0, column=5, sticky='nw')
			# number labels

			count = 1
			for deu in self.parent_psu.backend.deu_layout[side]:
				Label(f, text=str(count)).grid(row=count, column=1, sticky='nw')

				count += 1

	def setup_entries(self):

		self.title_entries = {'LHS': [], 'RHS': []}
		self.frame_entries = {'LHS': [], 'RHS': []}
		self.station_entries = {'LHS': [], 'RHS': []}
		self.side_combos = {'LHS': [], 'RHS': []}
		
		for side in ['LHS', 'RHS']:
			count = 1
			f = self.label_frames[side]
			for deu in self.parent_psu.backend.deu_layout[side]:

				#title
				self.title_entries[side].append(Entry(f, ))
				self.title_entries[side][-1].grid(row=count, column=2, sticky='nw')
				self.title_entries[side][-1].insert(0, deu[0])

				#frame
				self.frame_entries[side].append(Entry(f, state='disabled'))
				self.frame_entries[side][-1].grid(row=count, column=3, sticky='nw')

				#station
				self.station_entries[side].append(Entry(f, ))
				self.station_entries[side][-1].grid(row=count, column=4, sticky='nw')
				self.station_entries[side][-1].insert(0, deu[2])
				self.station_entries[side][-1].config(state='disabled')

				self.side_combos[side].append(ttk.Combobox(f, values=['LHS', 'RHS']))
				self.side_combos[side][-1].grid(row=count, column=5, sticky='nw')
				self.side_combos[side][-1].insert(0, deu[3])
				self.side_combos[side][-1].config(state='disabled')

				count += 1

	def setup_buttons(self):
		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=7, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=8, pady=5,sticky="nsew")

	def cleanup(self, button):

		self.button = button


		if button == 'ok':

			# check all title entries filled
			msg = None
			for side in ['LHS', 'RHS']:
				for c in self.title_entries[side]:
					if c.get() == '':
						msg = 'All DEUs must be Assigned a Title'

			if not msg:
				self.deu_layout = {'LHS': [], 'RHS': []}

				for side in ['LHS', 'RHS']:
					for i, e in enumerate(self.title_entries[side]):
						side = self.side_combos[side][i].get()
						title = self.title_entries[side][i].get()
						f=self.frame_entries[side][i].get()
						s=self.station_entries[side][i].get()

						self.deu_layout[side].append([title, f, s, side])

						# update DEU titles in vc_layout
						orig_title = self.parent_psu.backend.deu_layout[side][i][0]

						if orig_title != title:

							for idx, v in enumerate(self.vc_layout[side]):

								if v[3] == orig_title:

									self.vc_layout[side][idx][3] = title

				self.top.destroy()
			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		else:
			self.top.destroy()

class Edit_VCC_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_psu):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_psu = parent_psu

		psu_bk.setup_variables(self)
		psu_bk.PSU_Backend.update_variables(self, self.parent_psu.backend)

		self.setup_variables()
		self.setup_label_frames()
		self.setup_labels()
		self.setup_entries()
		self.setup_buttons()

		self.button = 'cancel'

		self.top.geometry("900x600")
		print(self.vc_layout)

	def setup_variables(self):

		#get available DEUs
		self.deus = {'LHS': ['N/A'], 'RHS': ['N/A']}

		for side in self.deus.keys():
			for d in self.parent_psu.backend.deu_layout[side]:
				self.deus[side].append(d[0])

		#get LOPA row numbers
		self.row_numbers = self.mainapp.frames[self.parent_psu.backend.lopa].backend.get_all_row_numbers()
		for side in self.row_numbers.keys():
			self.row_numbers[side].append('N/A')

		self.row_stations = copy.deepcopy(self.mainapp.frames[self.parent_psu.backend.lopa].backend.get_all_row_stations())

	def setup_label_frames(self):
		self.main_scroll_frame = double_scrollbar.Double_ScrollableFrame(self.top, self.mainapp)
		self.main_scroll_frame.pack(fill=tk.BOTH, expand=True)

		self.lhs_frame = LabelFrame(self.main_scroll_frame.inner, text='LHS VCCs')
		self.lhs_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.rhs_frame = LabelFrame(self.main_scroll_frame.inner, text='RHS VCCs')
		self.rhs_frame.grid(row=2, column=8, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.label_frames = {'LHS': self.lhs_frame, 'RHS': self.rhs_frame}

	def setup_labels(self):

		sides = ['LHS', 'RHS']
		for i, f in enumerate([self.lhs_frame, self.rhs_frame]):
			Label(f, text='#').grid(row=0, column=1, sticky='nw')
			Label(f, text='VCC Title').grid(row=0, column=2, sticky='nw')
			Label(f, text='VCC Frame').grid(row=0, column=3, sticky='nw')
			Label(f, text='VCC Station (in)').grid(row=0, column=4, sticky='nw')
			Label(f, text='DEU').grid(row=0, column=5, sticky='nw')
			# number labels

			count = 1
			for deu in self.parent_psu.backend.vc_layout[sides[i]]:
				Label(f, text=str(count)).grid(row=count, column=1, sticky='nw')

				count += 1

	def setup_entries(self):

		self.title_entries = {'LHS': [], 'RHS': []}
		self.frame_entries = {'LHS': [], 'RHS': []}
		self.station_entries = {'LHS': [], 'RHS': []}
		self.deu_combos = {'LHS': [], 'RHS': []}
		self.row_combos = {'LHS': [], 'RHS': []}
		
		for side in ['LHS', 'RHS']:
			count = 1
			for vcc in self.parent_psu.backend.vc_layout[side]:

				#title
				self.title_entries[side].append(Entry(self.label_frames[side], ))
				self.title_entries[side][-1].grid(row=count, column=2, sticky='nw')
				self.title_entries[side][-1].insert(0, vcc[0])

				#frame
				self.frame_entries[side].append(Entry(self.label_frames[side], state='disabled'))
				self.frame_entries[side][-1].grid(row=count, column=3, sticky='nw')

				#station
				self.station_entries[side].append(Entry(self.label_frames[side], ))
				self.station_entries[side][-1].grid(row=count, column=4, sticky='nw')
				self.station_entries[side][-1].insert(0, vcc[2])
				self.station_entries[side][-1].config(state='disabled')

				self.deu_combos[side].append(ttk.Combobox(self.label_frames[side], values=self.deus[side]))#, state='readonly'))
				self.deu_combos[side][-1].grid(row=count, column=5, sticky='nw')
				self.deu_combos[side][-1].insert(0, vcc[3])
				self.deu_combos[side][-1].config(state='readonly')

				self.row_combos[side].append(ttk.Combobox(self.label_frames[side], values=self.row_numbers[side]))#, state='readonly'))
				self.row_combos[side][-1].grid(row=count, column=6, sticky='nw')
				self.row_combos[side][-1].insert(0, vcc[4])
				self.row_combos[side][-1].config(state='readonly')
				count += 1

	def setup_buttons(self):

		Button(self.main_scroll_frame.inner, text='auto assign', command=self.auto_assign_vccs).grid(row=0, column=0, sticky='nsew')

		# ok button
		self.ok_button=Button(self.main_scroll_frame.inner,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=11,column=7, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.main_scroll_frame.inner,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=11,column=8, pady=5,sticky="nsew")

	def auto_assign_vccs(self):

		row_stations = copy.deepcopy(self.mainapp.frames[self.parent_psu.backend.lopa].backend.get_all_row_stations())
		available_stations = copy.deepcopy(row_stations)
		psiu_stations = self.parent_psu.backend.get_psiu_stations()

		if len(psiu_stations['LHS']) == len(row_stations['LHS']) and len(psiu_stations['RHS']) == len(row_stations['RHS']):
			self.assigned_vccs = {'LHS': {}, 'RHS': {}}

			for side in ['LHS', 'RHS']:
				#get selected vent stations
				available_vccs = []
				for v in self.station_entries[side]:
					available_vccs.append(float(v.get()))

				#loop over each row
				for idx, row in enumerate(row_stations[side]):
					
					row_psiu = psiu_stations[side][idx]

					closest = min(available_vccs, key=lambda x:abs(x-row_psiu))

					available_vccs.remove(closest)

					distance = abs(closest-row_psiu)
					
					self.assigned_vccs[side][self.row_numbers[side][idx]] = [closest] 
					#print(f'{row}: {closest}')

				#print(self.assigned_vccs)
				#print(self.row_numbers[side])

				#update combos
				for idx, e in enumerate(self.station_entries[side]):
					e = float(e.get())
					#print(f'entry {e}')
					vcc_used = False
					for row in self.assigned_vccs[side].keys():
						#print(f'Assigned {self.assigned_vents[side][row][0]}')
						if self.assigned_vccs[side][row][0] == e:
							vcc_used = True
							self.row_combos[side][idx].set(row)
							break

					if not vcc_used:
						self.row_combos[side][idx].set('N/A')

	def cleanup(self, button):

		self.button = button


		if button == 'ok':

			# check all titles have been entered, and no duplicates
			msg = None
			titles = []
			for side in ['LHS', 'RHS']:
				for e in self.title_entries[side]:
					if e.get() == '':
						msg = 'Title Must be Entered for all VCCs'
						break
					elif e.get() in titles:
						msg = f'VCC Titles must be Unique. {e.get()} has Been Entered More Than Once'
					else:
						titles.append(e.get())

			if not msg:

				self.vc_layout = {'LHS': [], 'RHS': []}

				for side in self.vc_layout.keys():
					for i, e in enumerate(self.title_entries[side]):

						title = self.title_entries[side][i].get()
						f=self.frame_entries[side][i].get()
						s=self.station_entries[side][i].get()
						d = self.deu_combos[side][i].get()
						row = self.row_combos[side][i].get()

						self.vc_layout[side].append([title, f, s, d, row])

				self.top.destroy()

			else:
				tkinter.messagebox.showerror(title='Error', message=msg)
		else:
			self.top.destroy()