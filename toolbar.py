import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

import components_tk
import file_menu as fm
import gui_styles_tk

def create_toolbar(self):

	self.toolbar = tk.Frame(self.parent, bg='white')
	self.toolbar.grid(row=0,column=0, columnspan=4, sticky="ew")

	ttk.Separator(self.toolbar,orient=HORIZONTAL).pack(fill=tk.BOTH, expand=True)

	#new
	b = tk.Button(self.toolbar, background='white', image=self.new_icon2, relief=FLAT, command = lambda self=self: fm.new_project(mainapp=self))
	add_button(b, 'New')
	#open
	b = tk.Button(self.toolbar, background='white', image=self.open_file_icon2, relief=FLAT, command = lambda self=self: fm.load(mainapp=self))
	add_button(b, 'Load')
	#save
	b = tk.Button(self.toolbar, background='white', image=self.save_icon2, relief=FLAT, command = lambda self=self: fm.save(mainapp=self))
	add_button(b, 'Save')
	#save as
	b = tk.Button(self.toolbar, background='white', image=self.save_as_icon2, relief=FLAT, command = lambda self=self: fm.save_as(mainapp=self))
	add_button(b, 'Save As')
	#Seat
	b = tk.Button(self.toolbar, background='white', image=self.seat_icon2, relief=FLAT, command = lambda self=self, type='Seat': components_tk.new_component(self, type))
	add_button(b, 'Add Seat')
	#WB
	b = tk.Button(self.toolbar, background='white', image=self.wb_icon2, relief=FLAT, command = lambda self=self, type='Windbreaker': components_tk.new_component(self, type))
	add_button(b, 'Add Windbreaker')
	#lopa
	b = tk.Button(self.toolbar, background='white', image=self.lopa_icon2, relief=FLAT, command = lambda self=self, type='LOPA': components_tk.new_component(self, type))
	add_button(b, 'Add LOPA')
	#psu
	b = tk.Button(self.toolbar, background='white', image=self.psu_icon2, relief=FLAT, command = lambda self=self, type='PSU': components_tk.new_component(self, type))
	add_button(b, 'Add PSU Layout')
	#ohsc
	b = tk.Button(self.toolbar, background='white', image=self.ohsc_icon2, relief=FLAT, command = lambda self=self, type='OHSC': components_tk.new_component(self, type))
	add_button(b, 'Add OHSC Layout')
	#ee
	b = tk.Button(self.toolbar, background='white', image=self.ee_icon2, relief=FLAT, command = lambda self=self, type='Emergency Equipment': components_tk.new_component(self, type))
	add_button(b, 'Add Emergency Equipment')
	#eel
	b = tk.Button(self.toolbar, background='white', image=self.eel_icon2, relief=FLAT, command = lambda self=self, type='EEL': components_tk.new_component(self, type))
	add_button(b, 'Add EEL')
	#eel comp
	b = tk.Button(self.toolbar, background='white', image=self.mag_icon2, relief=FLAT, command = lambda self=self, type='EEL Comparison': components_tk.new_component(self, type))
	add_button(b, 'Add EEL Comparison')

	#ttk.Separator(self.toolbar,orient=VERTICAL).pack(side = LEFT, expand = True)

	b = tk.Button(self.toolbar, image = self.close_icon2, background='white', relief=FLAT,
		command= lambda action = False: self.open_close_all_nodes(action))
	add_button(b, 'Close all Tree Nodes')
	b = tk.Button(self.toolbar, image = self.open_icon2, background='white', relief=FLAT,
		command= lambda action = True: self.open_close_all_nodes(action))
	add_button(b, 'Expand all Tree Nodes')
	b = tk.Button(self.toolbar, image = self.up_icon2, background='white', relief=FLAT,
		command = self.moveUp)
	add_button(b, 'Move Selected Tree Item Up')
	b = tk.Button(self.toolbar, image = self.down_icon2, background='white', relief=FLAT,
		command = self.moveDown)
	add_button(b, 'Move Selected Tree Item Down')


def add_button(b, text):
	b2 = b.pack(side=LEFT)
	gui_styles_tk.CreateToolTip(b, text)

