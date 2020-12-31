import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

import docx_functions

from docx import Document
from docx.enum.text import WD_BREAK

class Export_Word_Window(object):
	def __init__(self, mainapp, master, mode, parent_component):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_component = parent_component

		self.setup_label_frames()		
		self.setup_widgets()
		
		self.button = 'cancel'

		self.component_type = parent_component.backend.type


	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.top, text='Options:')
		self.main_frame.grid(row=2, column=0, columnspan = 4, rowspan = 1,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		Label(self.main_frame, text='Output File:').grid(row=1, column = 1, ipadx=1, ipady=1, padx=2, pady=2, sticky='NW')
		
		self.file_entry = Entry(self.main_frame, width = 80)
		self.file_entry.grid(row=1, column = 2, ipadx=1, ipady=1, padx=2, pady=2, sticky='NW')
		
		self.file_entry.insert(0, r'C:/Users/domhn/Documents/Python/Pycabin_Tkinter/V0.16/test.docx')
		Button(self.main_frame, text='Browse', command=self.browse).grid(row=1, column = 3, ipadx=1, ipady=1, padx=2, pady=2, sticky='NW')

		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=1, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=2, pady=5,sticky="nsew")	
		
	def browse(self):
		
		filename = filedialog.asksaveasfilename()
		
		self.file_entry.delete(0, 'end')
		self.file_entry.insert(0, filename)
		
	def cleanup(self, button):
	
		self.button = button
		
		if self.button == 'ok':
			
			self.filename = self.file_entry.get()
			#Checks
			msg = None
			# is extension .docx
			if self.filename[-5:] != '.docx':
				msg = 'Extension must be .docx'
				
			# 
			if msg:	
				tkinter.messagebox.showerror(master=self.top, title='Error', message=msg)
			else:
				self.document = Document()
				parts = self.parent_component.backend.gen_parts_table()
				#SB table
				docx_functions.write_table(self.document, ['Qty', 'Part Number', 'Description'],parts)
				
				p = self.document.add_paragraph()
				run = p.add_run()
				run.add_break(WD_BREAK.PAGE)
		
				ipc_table = self.parent_component.backend.gen_ipc_table()
				
				docx_functions.write_table(self.document, ['ITEM NO.', 'PART NUMBER', 'DESCRIPTION', 'FROMTO', 'QTY'],ipc_table)
				
				self.document.save(self.filename)
				self.top.destroy()
			
		else:
			
			self.top.destroy()