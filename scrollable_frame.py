import tkinter as tk
from tkinter import ttk


class ScrollableFrame():
	def __init__(self, container, mainapp):
		
		self.container = container #typicaly a notebook tab
		self.mainapp = mainapp
		
		self.canvas = tk.Canvas(self.container, height=self.mainapp.screen_height-80, bg="blue")
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		self.canvas.grid(row=0,column=0,stick='nsew')
		self.container.grid_columnconfigure(0, weight=1) # ###############
		self.container.grid_rowconfigure(0, weight=1)# ###############
		print(self.canvas.winfo_width())
		self.frame = tk.Frame(self.canvas)
		self.canvas_frame = self.canvas.create_window((0,0), window=self.frame, anchor='nw')
		#self.lopa_frame.grid(row=0,column=0,stick='nsew')

		vsb = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
		hsb = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
		self.canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
		#self.canvas.configure(xscrollcommand=hsb.set)
		vsb.grid(row=0,column=1,stick='nsew')
		hsb.grid(row=1,column=0,stick='nsew')
		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(canvas))
		self.canvas.bind('<Configure>', self.FrameWidth)
		'''
		self.frame = scrollable_frame.ScrollableFrame(self.seat_tab)
		self.frame.grid(row=0,column=0,stick='nsew')
		self.lopa_frame = self.frame.scrollable_frame
		self.seat_tab.grid_columnconfigure(0, weight=1)
		self.seat_tab.grid_rowconfigure(0, weight=1)
		#self.lopa_frame.grid_columnconfigure(4, weight=1)
		'''
	def set_grid_configures(self):
	
		self.frame.grid_columnconfigure(4, weight=1)

	def onFrameConfigure(self, canvas):
		'''Reset the scroll region to encompass the inner frame'''
		canvas.configure(scrollregion=canvas.bbox("all"))

	def FrameWidth(self, event):
		canvas_width = event.width
		self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

		#canvas_height = event.height
		#self.canvas.itemconfig(self.canvas_frame, height = canvas_height)
		