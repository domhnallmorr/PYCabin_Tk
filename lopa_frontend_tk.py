import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import LOPA_backend as lopa_bk
# from Pycabin_Backend import ipc_generator as ipc_gen
# from Pycabin_Backend import aircraft_models
import data_input_checks_tk

import gui_styles_tk
import components_tk
import scrollable_frame
#from Pycabin_Backend import lopa_draw
#from Pycabin_Backend import lopa_draw_redo

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import treeview_functions

#import ezdxf

from docx import Document
#from ezdxf.tools.standards import linetypes  # some predefined line types

def check_lopa_used(self):
	lopa_used = False
	psus, psu_dict = components_tk.get_all_psus(self.mainapp)
	
	for p in psus:
		p = self.mainapp.frames[p]
		if self.backend.drawing_no == p.backend.lopa:
			lopa_used = True
			break
	return lopa_used

def get_seat_y_datum(station, aircraft, side):

	if aircraft in ['A320', 'A319']:
		
		y_datum = 30.12
	
	elif aircraft in ['B737-800']:
		y_datum = 24.755
		
	if side == 'LHS':
		y_datum = y_datum*-1
	
	return y_datum

class LOPA_Page_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp
		
		self.backend = lopa_bk.LOPA_Backend(self, mainapp)
		
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
		self.dummy_canvas = tk.Canvas(self.lopa_frame, height=200, bg="blue")
		self.dummy_canvas.grid(row=7, column=0, columnspan = 1, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)

		self.dummy_canvas2 = tk.Canvas(self.weight_scroll_frame.frame, height=200, bg="blue")
		self.dummy_canvas2.grid(row=10, column=0, columnspan = 1, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_scrollable_frames(self):
		### Canvas widgets (for vertical scrollbar)

		self.lopa_frame_canvas = tk.Canvas(self.seat_tab, height=self.mainapp.screen_height-80, bg="blue")
		self.lopa_frame_canvas.configure(scrollregion=self.lopa_frame_canvas.bbox("all"))
		self.lopa_frame_canvas.grid(row=0,column=0,stick='nsew')
		self.seat_tab.grid_columnconfigure(0, weight=1)
		self.seat_tab.grid_rowconfigure(0, weight=1)

		self.lopa_frame = tk.Frame(self.lopa_frame_canvas)
		self.canvas_frame = self.lopa_frame_canvas.create_window((0,0), window=self.lopa_frame, anchor='nw')
		#self.lopa_frame.grid(row=0,column=0,stick='nsew')

		vsb = tk.Scrollbar(self.seat_tab, orient="vertical", command=self.lopa_frame_canvas.yview)
		self.lopa_frame_canvas.configure(yscrollcommand=vsb.set)
		vsb.grid(row=0,column=1,stick='nsew')
		self.lopa_frame.bind("<Configure>", lambda event, canvas=self.lopa_frame_canvas: self.onFrameConfigure(canvas))
		self.lopa_frame_canvas.bind('<Configure>', self.FrameWidth)

	
		self.weight_scroll_frame = scrollable_frame.ScrollableFrame(self.weight_tab, self.mainapp)
		'''
		self.frame = scrollable_frame.ScrollableFrame(self.seat_tab)
		self.frame.grid(row=0,column=0,stick='nsew')
		self.lopa_frame = self.frame.scrollable_frame
		self.seat_tab.grid_columnconfigure(0, weight=1)
		self.seat_tab.grid_rowconfigure(0, weight=1)
		#self.lopa_frame.grid_columnconfigure(4, weight=1)
		'''
	def set_grid_configures(self):
	
		self.lopa_frame.grid_columnconfigure(4, weight=1)
		self.weight_scroll_frame.frame.grid_columnconfigure(7, weight=1)
		
	def onFrameConfigure(self, canvas):
		'''Reset the scroll region to encompass the inner frame'''
		canvas.configure(scrollregion=canvas.bbox("all"))

	def FrameWidth(self, event):
		canvas_width = event.width
		self.lopa_frame_canvas.itemconfig(self.canvas_frame, width = canvas_width)
		
	def setup_notebook(self):
	
		self.note = ttk.Notebook(self)
		self.main_tab = Frame(self.note)
		self.seat_tab = Frame(self.note)
		self.weight_tab = Frame(self.note)
		self.comments_tab = Frame(self.note)
		
		self.note.add(self.main_tab, text = "Main")
		self.note.add(self.seat_tab, text = "Seat Layout")
		self.note.add(self.weight_tab, text = "Seat Weights")
		self.note.add(self.comments_tab, text = "Comments")
		
		self.note.grid(row=1,column=0,sticky='NSEW')

		# ####### COMMENTS TEXT ######################################
		self.comment_text = tk.Text(self.comments_tab, width = 110, height = 50)
		self.comment_text.grid(row=1, column=0, columnspan = 8, sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.main_tab,text="LOPA Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 16, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.monuments_frame = LabelFrame(self.main_tab,text="Monuments:")
		self.monuments_frame.grid(row=4, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.items_frame = LabelFrame(self.main_tab,text="Seat Item Numbers:")
		self.items_frame.grid(row=4, column=8, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.seats_frame = LabelFrame(self.lopa_frame,text="Seats:")
		self.seats_frame.grid(row=3, column=0, columnspan = 4, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
		self.preview_frame = LabelFrame(self.lopa_frame,text="LOPA Preview:")
		self.preview_frame.grid(row=5, column=0, columnspan = 5, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		self.preview_frame.grid_columnconfigure(4, weight=1)
		
		weight_frame = self.weight_scroll_frame.frame
		self.weight_frame = LabelFrame(weight_frame,text="Seat Weights:")
		self.weight_frame.grid(row=3, column=0, columnspan = 4, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_labels(self):
	
		self.top_label = tk.Label(self, text=('LOPA: '),font=self.mainapp.title_font)
		self.top_label.grid(row=0,column=0,columnspan=24,stick='W')
		
		self.dwg_no_label = gui_styles_tk.create_label(self.main_frame,'')
		self.dwg_no_label.grid(row = 2, column = 0,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.dwg_rev_label = gui_styles_tk.create_label(self.main_frame,'')
		self.dwg_rev_label.grid(row = 2, column = 2,columnspan=2, pady=2,padx=2, sticky="nsew")
		
		self.description_label = gui_styles_tk.create_label(self.main_frame,'')
		self.description_label.grid(row = 2, column = 4,columnspan=8, pady=2,padx=2, sticky="nsew")
		self.description_label.configure(width=70)
		
		self.no_lhs_label = gui_styles_tk.create_label(self.main_frame,'')
		self.no_lhs_label.grid(row = 3, column = 0,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.no_rhs_label = gui_styles_tk.create_label(self.main_frame,'')
		self.no_rhs_label.grid(row = 3, column = 2,columnspan=2, pady=2,padx=2, sticky="nsew")

		self.ac_label = gui_styles_tk.create_label(self.main_frame,'')
		self.ac_label.grid(row = 3, column = 4,columnspan=2, pady=2,padx=2, sticky="nsew")
		
		
	def setup_treeviews(self):
	
		self.monument_tree = ttk.Treeview(self.monuments_frame, selectmode="extended",columns=("A","B",'C'),height = 10)
		#self.monument_tree.grid(row=1,column=0, columnspan= 6,sticky="nsew")
		self.monument_tree.heading("#0", text="#")
		self.monument_tree.column("#0",minwidth=0,width=60, stretch='NO')
		self.monument_tree.heading("A", text="Monument")	  
		self.monument_tree.column("A",minwidth=0,width=200, stretch='NO') 
		self.monument_tree.heading("B", text="Type")	  
		self.monument_tree.column("B",minwidth=0,width=150, stretch='NO')
		self.monument_tree.heading("C", text="Station (in)")	  
		self.monument_tree.column("C",minwidth=0,width=130, stretch='NO')	

		self.monument_tree.grid(row = 2, column = 0, columnspan = 8, sticky = 'NSEW')

		self.item_tree = ttk.Treeview(self.items_frame, selectmode="extended",columns=("A","B",'C'),height = 10)
		#self.monument_tree.grid(row=1,column=0, columnspan= 6,sticky="nsew")
		self.item_tree.heading("#0", text="#")
		self.item_tree.column("#0",minwidth=0,width=60, stretch='NO')
		self.item_tree.heading("A", text="Seat")	  
		self.item_tree.column("A",minwidth=0,width=200, stretch='NO') 
		self.item_tree.heading("B", text="Item Number")	  
		self.item_tree.column("B",minwidth=0,width=150, stretch='NO')
		self.item_tree.heading("C", text="Qty")	  
		self.item_tree.column("C",minwidth=0,width=130, stretch='NO')	

		self.item_tree.grid(row = 2, column = 0, columnspan = 8, sticky = 'NSEW')
		
		tree_height = 8
		self.LHS_lopa_tree = ttk.Treeview(self.seats_frame,selectmode="extended",columns=("A","B",'C'),height = tree_height)
		self.LHS_lopa_tree.grid(row=1,column=0, sticky="nsew")
		self.LHS_lopa_tree.heading("#0", text="Row")
		self.LHS_lopa_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.LHS_lopa_tree.heading("A", text="Seat")   
		self.LHS_lopa_tree.column("A",minwidth=0,width=250, stretch='NO') 
		self.LHS_lopa_tree.heading("B", text="Pitch")   
		self.LHS_lopa_tree.column("B",minwidth=0,width=60, stretch='NO')
		self.LHS_lopa_tree.heading("C", text="Station")   
		self.LHS_lopa_tree.column("C",minwidth=0,width=150, stretch='NO')

		LHS_lopa_tree_scrollbar = Scrollbar(self.seats_frame, command=self.LHS_lopa_tree.yview)
		LHS_lopa_tree_scrollbar.grid(row=1, column=1, sticky='nsew')
		self.LHS_lopa_tree.config(yscrollcommand=LHS_lopa_tree_scrollbar.set)
		
		self.LHS_lopa_tree.bind("<Double-1>", lambda event, side='LHS': self.seat_double_click(event, side))
		
		self.RHS_lopa_tree = ttk.Treeview(self.seats_frame,selectmode="extended",columns=("A","B",'C'),height = tree_height)
		self.RHS_lopa_tree.grid(row=1,column=2, sticky="nsew")
		self.RHS_lopa_tree.heading("#0", text="Row")
		self.RHS_lopa_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.RHS_lopa_tree.heading("A", text="Seat")   
		self.RHS_lopa_tree.column("A",minwidth=0,width=250, stretch='NO') 
		self.RHS_lopa_tree.heading("B", text="Pitch")   
		self.RHS_lopa_tree.column("B",minwidth=0,width=60, stretch='NO')
		self.RHS_lopa_tree.heading("C", text="Station")   
		self.RHS_lopa_tree.column("C",minwidth=0,width=150, stretch='NO')

		RHS_lopa_tree_scrollbar = Scrollbar(self.seats_frame, command=self.RHS_lopa_tree.yview)
		RHS_lopa_tree_scrollbar.grid(row=1, column=3, sticky='nsew')
		self.RHS_lopa_tree.config(yscrollcommand=RHS_lopa_tree_scrollbar.set)

		self.RHS_lopa_tree.bind("<Double-1>", lambda event, side='RHS': self.seat_double_click(event, side))
		
		# ___ WEIGHTS ____
		self.LHS_weight_tree = ttk.Treeview(self.weight_frame,selectmode="extended",columns=("A","B",'C','D','E'),height=30)
		self.LHS_weight_tree.grid(row=0,rowspan = 16,column=0,columnspan = 2, sticky="nsew")
		self.LHS_weight_tree.heading("#0", text="Row")
		self.LHS_weight_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.LHS_weight_tree.heading("A", text="Seat")   
		self.LHS_weight_tree.column("A",minwidth=0,width=160, stretch='NO') 
		self.LHS_weight_tree.heading("B", text="Pitch")   
		self.LHS_weight_tree.column("B",minwidth=0,width=50)
		self.LHS_weight_tree.heading("C", text="Weight")   
		self.LHS_weight_tree.column("C",minwidth=0,width=50)
		self.LHS_weight_tree.heading("D", text="Allowable")   
		self.LHS_weight_tree.column("D",minwidth=0,width=80)
		self.LHS_weight_tree.heading("E", text="Delta")   
		self.LHS_weight_tree.column("E",minwidth=0,width=80)     

		LHS_weight_tree_scrollbar = Scrollbar(self.weight_frame, command=self.LHS_weight_tree.yview)
		LHS_weight_tree_scrollbar.grid(row=0, column=2, rowspan = 16,sticky='nsew')
		self.LHS_weight_tree.config(yscrollcommand=LHS_weight_tree_scrollbar.set)
		
		#setup RHS treeview
		self.RHS_weight_tree = ttk.Treeview(self.weight_frame,selectmode="extended",columns=("A","B",'C','D','E'),height=30)
		self.RHS_weight_tree.grid(row=0,rowspan = 16,column=3,columnspan = 3 , sticky="nsew")
		self.RHS_weight_tree.heading("#0", text="Row")
		self.RHS_weight_tree.column("#0",minwidth=0,width=50, stretch='NO')
		self.RHS_weight_tree.heading("A", text="Seat")   
		self.RHS_weight_tree.column("A",minwidth=0,width=160, stretch='NO') 
		self.RHS_weight_tree.heading("B", text="Pitch")   
		self.RHS_weight_tree.column("B",minwidth=0,width=50)
		self.RHS_weight_tree.heading("C", text="Weight")   
		self.RHS_weight_tree.column("C",minwidth=0,width=50)
		self.RHS_weight_tree.heading("D", text="Allowable")   
		self.RHS_weight_tree.column("D",minwidth=0,width=80)
		self.RHS_weight_tree.heading("E", text="Delta")   
		self.RHS_weight_tree.column("E",minwidth=0,width=80)    		

		RHS_weight_tree_scrollbar = Scrollbar(self.weight_frame, command=self.RHS_weight_tree.yview)
		RHS_weight_tree_scrollbar.grid(row=0, column=6, rowspan = 16,sticky='nsew')
		self.RHS_weight_tree.config(yscrollcommand=RHS_weight_tree_scrollbar.set)
		
		#add in entries for life vest and literature weights
		self.weight_description=Label(self.weight_frame,text="Weights below are per Passenger",width=25)
		self.weight_description.grid(row=0,column=7, sticky="nsew")
		
		self.life_vest_weight = tk.StringVar()
		self.life_vest_weight_label=Label(self.weight_frame,text="Life Vest Weight (lbs)",width=25)
		self.life_vest_weight_label.grid(row=2,column=7, sticky="nsew")
		self.life_vest_weight_entry=Entry(self.weight_frame, width=20, textvariable=self.life_vest_weight)
		self.life_vest_weight_entry.insert(END, '2')
		self.life_vest_weight_entry.grid(row=3,column=7, sticky="nsew")

		self.literature_weight = tk.StringVar()
		self.literature_weight_label=Label(self.weight_frame,text="Literature Weight (lbs)",width=25)
		self.literature_weight_label.grid(row=4,column=7, sticky="nsew")
		self.literature_weight_entry=Entry(self.weight_frame, width=20, textvariable=self.literature_weight)
		self.literature_weight_entry.insert(END, '3')
		self.literature_weight_entry.grid(row=5,column=7, sticky="nsew")		

		#configure tags to color treeview
		self.LHS_weight_tree.tag_configure('bad', background='orange')
		self.LHS_weight_tree.tag_configure('good', background='green')
		self.RHS_weight_tree.tag_configure('bad', background='orange')
		self.RHS_weight_tree.tag_configure('good', background='green')        
		

		# Update button
		self.u=Button(self.weight_frame,text='Update Table', command= lambda: self.update_weight_table())
		self.u.grid(row=6,column=7, sticky="nsew")
		
	def setup_buttons(self):

		self.edit_btn = Button(self.main_tab, text = 'Edit',width = 30, command= lambda: self.edit())
		self.edit_btn.grid(row=1, column=0, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.dxf_btn = Button(self.main_tab, text = 'Export to DXF',width = 30, command= lambda: self.export_dxf())
		self.dxf_btn.grid(row=1, column=1, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)

		self.ms_word_btn = Button(self.main_tab, text = 'Export to Word',width = 30, command= lambda: self.export_word())
		self.ms_word_btn.grid(row=1, column=2, columnspan = 1, sticky='W',padx=5, pady=2, ipadx=2, ipady=2)
		
		self.add_monument_btn = Button(self.monuments_frame, text = 'Add Monument',
								command = self.add_monument)
		self.add_monument_btn.grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW')

		self.auto_item_btn = Button(self.items_frame, text = 'Autogen',
								command = self.autogen_items)
		self.auto_item_btn.grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW')
		
		self.expand_lopa_tree_btn = Button(self.lopa_frame, text = "Expand Trees",
							  command = lambda height=30, trees = [self.LHS_lopa_tree,self.RHS_lopa_tree]: self.expand_tree(trees,height))
		self.expand_lopa_tree_btn.grid(row=0, column=0, columnspan=4, sticky='nsew')

	def add_monument(self):
		self.w=Add_Monument_Window(self, self.mainapp, self.master)
		self.master.wait_window(self.w.top)	
		
		if self.w.button == 'ok':

			#treeview_functions.write_data_to_treeview(self.monument_tree, 'append', [data])
			
			self.update_component(self.w, 'edit')
		
	def expand_tree(self,trees,height):
		#print(tree.configure(height))
		for tree in trees:
			if tree['height'] < 30:
				tree.configure(height = 30)
			else:
				tree.configure(height = 6)
			
	def update_label_text(self):
				
		self.top_label.config(text=f'LOPA: {self.backend.title}')
		self.description_label.config(text=f' Description: {self.backend.description}')
		self.dwg_no_label.config(text=f' Drawing Number: {self.backend.drawing_no}')
		self.dwg_rev_label.config(text=f' Drawing Revision: {self.backend.drawing_rev}')
		self.ac_label.config(text=f' Aircraft Type: {self.backend.aircraft_type}')
		self.no_lhs_label.config(text=f' Number of LHS Rows: {self.backend.no_lhs_seats}')
		self.no_rhs_label.config(text=f' Number of RHS Rows: {self.backend.no_rhs_seats}')

	def update_monuments_tree(self):
	
		treeview_functions.write_data_to_treeview(self.monument_tree, 'replace', self.backend.monuments)

	def update_component(self, window, type):
		
		self.backend.update_component(window, type)
		self.update_label_text()
		self.update_monuments_tree()

		if self.treeview_iid:
			self.mainapp.main_treeview.item(self.treeview_iid, text = self.backend.title)
			components_tk.component_renamed(self)
			
		treeview_functions.write_data_to_treeview(self.LHS_lopa_tree, 'replace', self.backend.seat_layout['LHS'])
		treeview_functions.write_data_to_treeview(self.RHS_lopa_tree, 'replace', self.backend.seat_layout['RHS'])
		
		self.backend.ax1.clear()
		self.backend.ax2.clear()
		self.backend.ax3.clear()
		#lopa_draw.draw_lopa(self, self.backend.ax2, 'matplotlib', [[],[0,0],[]], True)
		lopa_draw_redo.draw_aircraft(self.backend, self.backend.ax2, 'matplotlib', [0,0])
		lopa_draw_redo.draw_floor(self.backend, self.backend.ax1, 'matplotlib', [0,0])
		lopa_draw_redo.draw_floor(self.backend, self.backend.ax3, 'matplotlib', [0,0])
		#lopa_draw_redo.draw_seat_tracks(self.backend, self.backend.ax2, 'matplotlib', [0,0])

		lopa_draw_redo.draw_seats_side(self.backend, self.backend.ax3, 'matplotlib', [0,0], 'LHS')
		lopa_draw_redo.draw_seats_side(self.backend, self.backend.ax1, 'matplotlib', [0,0], 'RHS')

		if self.backend.aircraft_type in ['A320', 'A319']:
			y_datum = 30.12
		elif self.backend.aircraft_type in ['B737-800']:
			y_datum = 24.755
		lopa_draw_redo.draw_seats_top_down(self.backend, self.backend.ax2, 'matplotlib', [0,y_datum*-1], 'LHS')
		lopa_draw_redo.draw_seats_top_down(self.backend, self.backend.ax2, 'matplotlib', [0,y_datum], 'RHS')
		lopa_draw_redo.draw_monuments_top_down(self.backend, self.backend.ax2, 'matplotlib', [0,0])
		lopa_draw_redo.draw_monuments_side(self.backend, self.backend.ax3, self.backend.ax1, 'matplotlib', [0,0])
		self.canvas.draw()
	def add_lopa_plot(self):
		
		self.canvas = FigureCanvasTkAgg(self.backend.lopa_figure, self.preview_frame)
		self.canvas.draw()
		#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.canvas.get_tk_widget().grid(row = 3, column = 0, columnspan=8, pady=2,sticky="nsew")	

		toolbarFrame = Frame(master=self.preview_frame)
		
		toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
		toolbar.update()	
		toolbarFrame.grid(row = 2, column = 0, columnspan=5, pady=2,sticky="nsew")
		
	def seat_double_click(self, event, side):
		if side == 'LHS':
			item = self.LHS_lopa_tree.selection()[0]
			tree = self.LHS_lopa_tree
		elif side == 'RHS':
			item = self.RHS_lopa_tree.selection()[0]
			tree = self.RHS_lopa_tree
			
		row_data = list(tree.item(item,"values"))
		row_data.insert(0, tree.item(item,"text"))
		
		index = tree.index(item)
		
		self.w=Double_Click_Seat_Window_Tk(self, self.mainapp, self.master, side, row_data)
		self.master.wait_window(self.w.top)
		
		if self.w.button == 'ok':
			
			self.w.seat_layout[side][index] = [self.w.row_no, self.w.seat, self.w.pitch, None]
			
			if self.w.row_no_changed:
				lopa_bk.LOPA_Backend.update_row_numbers(self.w, index, side, self.w.row_no)
			#lopa_bk.LOPA_Backend.recalculate_stations(self.w)

			#if side == 'LHS':
			self.backend.ax3.clear()
			#else:
			self.backend.ax1.clear()

			self.update_component(self.w, 'edit')

	def edit(self):

		self.w= Edit_LOPA_Window_Tk(self.mainapp, self.master, None, 'edit', self)
		self.master.wait_window(self.w.top)	
			
		if self.w.button == 'ok':
			self.update_component(self.w, 'edit')
			
	def export_dxf(self):
		lopa_draw_redo.gen_dxf(self)
		
	def export_word(self):
	
		document = Document()
		
		ipc_data = self.gen_ipc_data('FROMTO')
		
		ipc_gen.gen_ipc_table(document, ipc_data)
		
		document.save(r'C:\Python37\Lib\site-packages\Pycabin_Backend\ipc.docx')

	def gen_ipc_data(self, fromto):
		data = treeview_functions.get_all_treeview_items(self.item_tree)
		ipc_data = []
		for d in data:
			desc = self.mainapp.frames[d[1]].backend.description
			ipc_data.append([d[2], d[1], desc, fromto, d[3]])	
		
		return ipc_data
	def update_weight_table(self):
		data_ok = True
		try:
			lvw = float(self.life_vest_weight_entry.get())
			lw = float(self.literature_weight_entry.get())
		except:	
			data_ok = False
			
		if data_ok:
			weight_data = {'LHS': [], 'RHS': []}
			
			for side in ['LHS', 'RHS']:
				for row in self.backend.seat_layout[side]:
					seat = self.mainapp.frames[row[1]]
					weight = round(seat.backend.calc_seat_weight(lvw, lw),2)
					weight_data[side].append([row[0], row[1], row[2], weight, '-', '-'])
					
		treeview_functions.write_data_to_treeview(self.LHS_weight_tree, 'replace',weight_data['LHS']) 
		treeview_functions.write_data_to_treeview(self.RHS_weight_tree,'replace', weight_data['RHS']) 

	def autogen_items(self):
	
		seats = {'LHS': {}, 'RHS': {}}
		numbers = {'LHS': 5, 'RHS': 6}
		
		#get quantities
		for side in ['LHS', 'RHS']:
			for row in self.backend.seat_layout[side]:
				if row[1] not in seats[side].keys():
					
					seats[side][row[1]] = 1
					
				else:
					seats[side][row[1]] += 1

		#Assign item numbers
		item_numbers = {}
		for side in ['LHS', 'RHS']:
			for seat in seats[side]:
				item_numbers[numbers[side]] = [seat, numbers[side], seats[side][seat]]
				numbers[side] += 2
		
		tree_list = []
		
		for index, s in enumerate(sorted(list(item_numbers.keys()))):
			
			tree_list.append(item_numbers[s])
			tree_list[-1].insert(0, index+1)#
			
		treeview_functions.write_data_to_treeview(self.item_tree, 'replace', tree_list)	
			
class Edit_LOPA_Window_Tk(object):
	def __init__(self, mainapp, master, ac, mode, parent_lopa):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_lopa = parent_lopa

		self.orig_part_no = None
		
		if mode == 'edit':
			self.orig_part_no = parent_seat.backend.title
			
		lopa_bk.setup_variables(self)
		if self.mode == 'edit':
			lopa_bk.update_variables(self, self.parent_lopa.backend)
		
		self.seats_dict = components_tk.get_all_components(mainapp, 'Seats')

		#if self.mode == 'edit':
			#self.part_no = parent_lopa.backend.part_no
		self.data_checks = {}
		self.setup_label_frames()
		self.setup_widgets()

		if self.mode == 'edit':
			self.set_default_values()
			

	def setup_label_frames(self):
		self.details_frame = LabelFrame(self.top,text="LOPA Details:")
		self.details_frame.grid(row=2, column=0, columnspan = 8, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

		self.seats_frame = LabelFrame(self.top,text="Seat Layout:")
		self.seats_frame.grid(row=6, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
		
		#if self.mode == 'edit':
		#	labels = ['Title:', 'Drawing Number:', 'Revision']
		#else:
		if self.mode == 'edit':
			state = 'disabled'
		else:
			state = 'normal'
		labels = ['Title:', 'Description:', 'Drawing Number:', 'Revision', 'Aircraft:', 'No. Economy Seats:', 'Row 13 Included:']
		row = 1
		gui_styles_tk.create_multiple_labels(self.details_frame, labels, row, 2, 20, 2, 2)

		self.title_entry=Entry(self.details_frame, width=20)		
		self.title_entry.grid(row=1,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_part_no]
		
		self.description_entry=Entry(self.details_frame, width=50)		
		self.description_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.drawing_entry=Entry(self.details_frame, width=20)		
		self.drawing_entry.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.revision_combo= ttk.Combobox(self.details_frame, values=[i for i in range(99)])
		self.revision_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		#self.revision_combo.set(1)
			

		#if self.mode != 'edit':
			
		self.aircraft_combo= ttk.Combobox(self.details_frame, values=['A320', 'A319', 'B737-800'],state=state)
		self.aircraft_combo.grid(row=5,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.aircraft_combo.bind("<<ComboboxSelected>>", self.aircraft_selected)
		self.data_checks['Aircraft Type'] = ['combo', self.aircraft_combo, 'in values', 'Aircraft Type']
		
		self.economy_entry=Entry(self.details_frame, width=20)		
		#self.economy_entry.grid(row=6,column=3,padx=2, pady=2,sticky = 'NSEW')		

		self.row13_ckbx = Checkbutton(self.details_frame, text="")
		self.row13_ckbx.grid(row=7,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		labels = ['Number Rows LHS:', 'Default Seat LHS:', 'Default Pitch LHS (in):']
		row = 2
		gui_styles_tk.create_multiple_labels(self.seats_frame, labels, row, 2, 20, 2, 2)

		self.lhs_rows_combo= ttk.Combobox(self.seats_frame, values=[i for i in range(31)],state=state)
		self.lhs_rows_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Number of LHS Seats'] = ['combo', self.lhs_rows_combo, 'int greater than equal 0', 'LHS No. of Rows']
		
		self.lhs_seat_combo= ttk.Combobox(self.seats_frame,state=state)
		self.lhs_seat_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['LHS Default Seat'] = ['combo', self.lhs_seat_combo, 'in values', 'LHS Seat']
		
		self.lhs_pitch_combo= ttk.Combobox(self.seats_frame, values=[28, 29, 30, 31, 32, 33],state=state)
		self.lhs_pitch_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['LHS Default Pitch'] = ['combo', self.lhs_pitch_combo, 'int greater than 27', 'LHS Pitch']
		
		labels = ['Number Rows RHS:', 'Default Seat RHS:', 'Default Pitch RHS (in):']
		row = 2
		gui_styles_tk.create_multiple_labels(self.seats_frame, labels, row, 4, 20, 2, 2)

		self.rhs_rows_combo= ttk.Combobox(self.seats_frame, values=[i for i in range(31)],state=state)
		self.rhs_rows_combo.grid(row=2,column=5,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Number of RHS Seats'] = ['combo', self.rhs_rows_combo, 'int greater than equal 0', 'RHS No. of Rows']
		
		self.rhs_seat_combo= ttk.Combobox(self.seats_frame,state=state)
		self.rhs_seat_combo.grid(row=3,column=5,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['RHS Default Seat'] = ['combo', self.rhs_seat_combo, 'in values', 'RHS Seat']
		
		self.rhs_pitch_combo= ttk.Combobox(self.seats_frame, values=[28, 29, 30, 31, 32, 33],state=state)
		self.rhs_pitch_combo.grid(row=4,column=5,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['RHS Default Pitch'] = ['combo', self.rhs_pitch_combo, 'int greater than 27', 'RHS Pitch']
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, pady=5,sticky="nsew")

		self.button = 'cancel'
		
	def set_default_values(self):
		
		self.title_entry.insert(0, self.parent_lopa.backend.title)
		self.description_entry.insert(0, self.parent_lopa.backend.description)
		self.drawing_entry.insert(0, self.parent_lopa.backend.drawing_no)
		self.revision_combo.set(self.parent_lopa.backend.drawing_rev)
		self.aircraft_combo.set(self.parent_lopa.backend.aircraft_type)
		self.lhs_rows_combo.set(self.parent_lopa.backend.no_lhs_seats)
		self.rhs_rows_combo.set(self.parent_lopa.backend.no_rhs_seats)

	def aircraft_selected(self, event):
		
		self.lhs_seat_combo.set('')
		self.rhs_seat_combo.set('')
		
		if self.aircraft_combo.get() in ['A320', 'A319']:
			self.lhs_seat_combo['values'] = [self.mainapp.frames[s].backend.title for s in self.seats_dict['A320 Family LHS']]
			self.rhs_seat_combo['values'] = [self.mainapp.frames[s].backend.title for s in self.seats_dict['A320 Family RHS']]
		elif self.aircraft_combo.get() in ['B737-800']:
			self.lhs_seat_combo['values'] = [self.mainapp.frames[s].backend.title for s in self.seats_dict['B737 Family LHS']]
			self.rhs_seat_combo['values'] = [self.mainapp.frames[s].backend.title for s in self.seats_dict['B737 Family RHS']]	
	def cleanup(self,button):
	
		if button == 'ok':
			#checks
			data_good, msg = data_input_checks_tk.check_data_input(self.data_checks, self.mainapp)
			
			if data_good:
				self.button = 'ok'
				
				if self.mode != 'edit':
					self.seat_layout = {'LHS': [], 'RHS': []}
					
					station = 0
					
					for i in range(int(self.lhs_rows_combo.get())):
						if i == 0:
							pitch = 340
						else:
							pitch = int(self.lhs_pitch_combo.get())
						station += pitch
						self.seat_layout['LHS'].append([i+1, self.lhs_seat_combo.get(), pitch, station])

					station = 0
					
					for i in range(int(self.rhs_rows_combo.get())):
						if i == 0:
							pitch = 340
						else:
							pitch = int(self.rhs_pitch_combo.get())
						station += pitch
						self.seat_layout['RHS'].append([i+1, self.rhs_seat_combo.get(), pitch, station])
						
				self.title = self.title_entry.get()
				self.aircraft_type = self.aircraft_combo.get()
				self.no_lhs_seats = self.lhs_rows_combo.get()
				self.no_rhs_seats = self.rhs_rows_combo.get()				
				self.drawing_no = self.drawing_entry.get()
				self.drawing_rev = self.revision_combo.get()

				self.top.destroy()
			
			else:
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
		else:
		
			self.top.destroy()
			
class Double_Click_Seat_Window_Tk(object):			
	def __init__(self, lopa, mainapp, master, side, row_data):
		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp
		self.side = side
		self.lopa = lopa
		self.row_data = row_data
		
		lopa_bk.setup_variables(self)
		lopa_bk.update_variables(self, self.lopa.backend)
		
		self.seats, self.seats_dict = components_tk.get_all_seats(mainapp)
		
		self.setup_label_frames()
		self.setup_widgets()
	
	def setup_label_frames(self):
	
		self.options_frame = LabelFrame(self.top,text="Options:")
		self.options_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)

	def setup_widgets(self):
	
		labels = ['Row Number:', 'Seat Part Number:', 'Pitch (in):',]
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, 20, labels, row, 2, 2, 2)
		
		if self.side == 'LHS':
			if self.lopa.backend.aircraft_type in ['A320', 'A319']:
				key = 'A320 Family LHS'
			elif self.lopa.backend.aircraft_type in ['B737-800']:
				key = 'B737 Family LHS'
				
		elif self.side == 'RHS':
			if self.lopa.backend.aircraft_type in ['A320', 'A319']:
				key = 'A320 Family RHS'
			elif self.lopa.backend.aircraft_type in ['B737-800']:
				key = 'B737 Family RHS'
				
		self.row_entry=Entry(self.options_frame, width=20)		
		self.row_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')	
		self.row_entry.insert(0,self.row_data[0])
		
		self.seat_combo= ttk.Combobox(self.options_frame, values=self.seats_dict[key])
		self.seat_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.seat_combo.set(self.row_data[1])
		
		pitches = [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
		self.pitch_combo= ttk.Combobox(self.options_frame, values=pitches)
		self.pitch_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.pitch_combo.insert(0,self.row_data[2])
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")

		self.button = 'cancel'	

	def cleanup(self,button):
	
		if button == 'ok':
			self.button = 'ok'
			
			self.row_no = int(self.row_entry.get())
			self.seat = self.seat_combo.get()
			self.pitch = self.pitch_combo.get()
			self.top.destroy()
			
			if self.row_no != self.row_data[0]:
				self.row_no_changed = True
			else:
				self.row_no_changed = False
		else:
			self.top.destroy()
			
class Add_Monument_Window():
	def __init__(self, lopa, mainapp, master,):
	
		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp
		self.lopa = lopa

		lopa_bk.setup_variables(self)
		lopa_bk.update_variables(self, self.lopa.backend)
		
		self.wbs = components_tk.get_all_windbreakers(mainapp)
		self.wbs = components_tk.gen_wb_dict(mainapp, self.wbs)
		
		self.lavs =components_tk.get_all_lavs(mainapp)
		self.lavs = components_tk.gen_lav_dict(mainapp, self.lavs)
		
		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
	
		self.options_frame = LabelFrame(self.top,text="Options:")
		self.options_frame.grid(row=2, column=0, columnspan = 4, rowspan = 4,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)	
		
	def setup_widgets(self):

		labels = ['Monument Type:', 'Monument:', 'Station (in):',]
		row = 2
		gui_styles_tk.create_multiple_labels(self.options_frame, 20, labels, row, 2, 2, 2)
		
		self.type_combo= ttk.Combobox(self.options_frame, values=['Windbreakers', 'Lavs'])
		self.type_combo.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.type_combo.bind("<<ComboboxSelected>>", self.type_selected)

		self.monument_combo= ttk.Combobox(self.options_frame, values=[])
		self.monument_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')

		self.station_entry=Entry(self.options_frame, width=20)		
		self.station_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')	
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")

		self.button = 'cancel'

	def type_selected(self, event):
		type = self.type_combo.get()
		if type == 'Windbreakers':
			if self.lopa.backend.aircraft_type in ['A320', 'A319']:
				self.monument_combo['values'] = self.wbs['A320 LHS'] + self.wbs['A320 RHS']
				self.monument_combo.set('')

		if type == 'Lavs':
			if self.lopa.backend.aircraft_type in ['A320', 'A319']:
				self.monument_combo['values'] = self.lavs['A320 LHS'] + self.lavs['A320 RHS']
				self.monument_combo.set('')
				
	def cleanup(self,button):
	
		self.button = button
		
		if self.button == 'ok':
			#self.check_data()
			type = self.type_combo.get()
			monument =self.monument_combo.get()
			station =self.station_entry.get()
			
			index = len(self.lopa.monument_tree.get_children())+1
			data = [index, monument, type, station]
			self.monuments.append(data)
			
			self.top.destroy()
		
		else:
			self.top.destroy()