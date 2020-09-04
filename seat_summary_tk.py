import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk as gui_styles
from tksheet import Sheet
from colour import Color
import components_tk
import seats_frontend_tk as seats_tk

class Seat_Page_Summary_Tk(tk.Frame):

	def __init__(self, container, mainapp):
		tk.Frame.__init__(self, container)
		
		self.mainapp = mainapp
		self.setup_label_frames()
		self.setup_labels()
		self.setup_widgets()
		self.setup_table()
		
		
	def setup_label_frames(self):

		self.main_frame = LabelFrame(self,text="Seats Details:")
		self.main_frame.grid(row=2, column=2, columnspan = 8, rowspan = 2,sticky='NSEW',padx=5, pady=5, ipadx=2, ipady=5)
		self.grid_columnconfigure(9, weight = 1)
		self.main_frame.grid_columnconfigure(8, weight = 1)
	def setup_labels(self):
	
		self.top_label = tk.Label(self, text=('Seats: '),font=self.mainapp.title_font)
		self.top_label.grid(row=0,column=0,columnspan=24,sticky='W')
		
	def setup_table(self):
	
		pass
		
	def setup_widgets(self):
		self.opt_var = tk.StringVar()
		self.opt_var.trace("w", self.update_table)
		self.opt = tk.OptionMenu(self.main_frame, self.opt_var, *['Dimensions', 'Weights & SRP'])
		self.opt.grid(row=1, column=1, sticky='nsew')
		
		self.apply_var = tk.StringVar()
		self.apply_var.trace("w", self.apply_multiple_values)
		self.apply = tk.OptionMenu(self.main_frame, self.apply_var, *['Apply Dimensions to Multiple Seats'])
		self.apply.grid(row=1, column=2, sticky='nsew')	
		
	def update_table(self, *args):
	
		if self.opt_var.get() == 'Dimensions':
			headers = ['Part Number', 'Width', 'Width Inbd', 'Length Aft', 'Length Fwd', 'Height', 'Cushion Height', 'Stud Distance', 'Armrest Width']
			
		elif self.opt_var.get() == 'Weights & SRP':
			headers = ['Part Number', 'Weight', 'SRP X', 'SRP Y']
	
		self.sheet = Sheet(self.main_frame, column_width = 120,total_columns=len(headers),
						headers= headers)
		self.sheet.grid(row =2, column=1, columnspan=8, sticky='nsew')
		
		self.get_seat_data()
		
		if len(self.seat_data) != 0:
			idx = 0
			for s in self.seat_data:
				
				if self.opt_var.get() == 'Dimensions':
					v = (s['Title'], s['Width'], s['Width Inbd'], s['Length Aft'], s['Length Fwd'], s['Height'],
						s['Cushion Height'], s['Stud Distance'], s['Armrest Width'])
				else:
					v = (s['Title'], s['Weight'], s['SRP X'], s['SRP Y'])
					
				self.sheet.insert_row(values = v, idx = idx) 
			
				idx+=1
				
			#Apply color gradients
			for i in range(len(v)):
				if i != 0: #skip part number column
					self.apply_color_gradiant(i)

	def apply_color_gradiant(self, col):

		values = self.sheet.get_column_data(col)
		unique_values = sorted(list(set(self.sheet.get_column_data(col)))) #unique values

		colors = list(Color("#98f573").range_to(Color("#f08c78"),len(unique_values))) #light green to light red

		color_dict = {}
		for i, c in enumerate(colors):

			color_dict[unique_values[i]] = c

		for i, v in enumerate(values):
			self.sheet.highlight_cells(row = i, column = col, bg = color_dict[v].hex)
			
	def apply_multiple_values(self, *args):

		self.w=seats_tk.Edit_Seat_Window_Tk(self, self.master, 'edit multiple', None)
		self.master.wait_window(self.w.top)	
		
	def get_seat_data(self):
		
		self.seat_data = []
		components_dict = components_tk.get_all_components(self.mainapp, 'Seats')
		
		for seat in components_dict['All']:
			seat= self.mainapp.frames[seat].backend
			
			self.seat_data.append(seat.gen_save_dict())
			
			