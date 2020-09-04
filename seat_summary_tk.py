import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox

import gui_styles_tk as gui_styles
from tksheet import Sheet

import components_tk

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
		
	def update_table(self, *args):
	
		if self.opt_var.get() == 'Dimensions':
			headers = ['Part Number', 'Width', 'Width Inbd', 'Length Aft', 'Length Fwd', 'Height', 'Cushion Height', 'Stud Distance', 'Armrest Width']
			
		elif self.opt_var.get() == 'Weights & SRP':
			headers = ['Part Number', 'Weight', 'SRP X', 'SRP Y']
	
		self.sheet = Sheet(self.main_frame, column_width = 120,total_columns=len(headers),
						headers= headers)
		self.sheet.grid(row =2, column=1, columnspan=8, sticky='nsew')
		
		self.get_seat_data()
		
		for s in self.seat_data:
			idx = 0
			
			if self.opt_var.get() == 'Dimensions':
				v = (s['Title'], s['Width'], s['Width Inbd'], s['Length Aft'], s['Length Fwd'], s['Height'],
					s['Cushion Height'], s['Stud Distance'], s['Armrest Width'])
			else:
				v = (s['Title'], s['Weight'], s['SRP X'], s['SRP Y'])
				
			self.sheet.insert_row(values = v, idx = idx) 
			idx+=1
	def get_seat_data(self):
		
		self.seat_data = []
		components_dict = components_tk.get_all_components(self.mainapp, 'Seats')
		
		for seat in components_dict['All']:
			seat= self.mainapp.frames[seat].backend
			
			self.seat_data.append(seat.gen_save_dict())
			
			