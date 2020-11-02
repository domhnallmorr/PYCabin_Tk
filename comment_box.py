import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

def edit_comments(component):
	mainapp = component.mainapp
	w=Edit_Comments_Window(mainapp, mainapp.master, component)
	mainapp.master.wait_window(w.top)

def insert_comments_text(text_widget, text):

	text_widget.config(state='normal')
	text_widget.delete('1.0', END)
	text_widget.insert('1.0', text)
	text_widget.config(state='disabled')
	
	
class Edit_Comments_Window():

	def __init__(self, mainapp, master, component):

		top=self.top=Toplevel(master)
		top.grab_set()
		
		self.mainapp = mainapp
		self.component = component
		#create text box
		self.text = tk.Text(self.top, width = 110, height = 40)
		self.text.pack()
		
		#get existing text and add
		self.orig_text = component.comment_text.get("1.0","end")
		self.text.insert("1.0", self.orig_text)
		
		
		Button(self.top, text = 'ok', command = lambda button = 'ok': self.cleanup(button)).pack()
		Button(self.top, text = 'cancel', command = lambda button = 'cancel': self.cleanup(button)).pack()
	def cleanup(self, button):
	
		self.button = button
		
		if self.button == 'ok':
			
			#create undo redo component
			
			
			#add new text to the existing text box
			self.component.comment_text.config(state='normal')
			self.component.comment_text.delete('1.0', END)
			self.component.comment_text.insert("1.0", self.text.get("1.0","end"))
			self.component.comment_text.config(state='disabled')
			
			self.mainapp.states.component_updated('comment', self.component, self.orig_text)
			
			self.top.destroy()
		else:
			self.top.destroy()