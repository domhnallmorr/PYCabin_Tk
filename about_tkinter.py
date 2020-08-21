import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

import gui_styles_tk as gui_styles_tk

def about(mainapp):

	win = tk.Toplevel()
	win.wm_title("About PYCabin")

	l = tk.Label(win, width = 20, text=f"PYCabin Version {mainapp.version}")
	l.grid(row=0, column=1, columnspan = 3)

	l2 = tk.Label(win, text=f"Icons From https://icons8.com")
	l2.grid(row=1, column=0, columnspan = 5)

	l3 = tk.Label(win, text = '''
	    PYCabin makes no promise of warranty, satisfaction, performance, or
        anything else. Understand that your use of this tool is completely
        at your own risk.''')
	l3.grid(row=2, column=0, columnspan = 5)
	
	b = ttk.Button(win, text="Okay", command=win.destroy)
	b.grid(row=3, column=2)
	
	# mainapp.w=About_Window_Tk(mainapp, mainapp.master)
	# mainapp.master.wait_window(mainapp.w.top)  
	
	
# class About_Window_Tk(tk.Frame):
	# def __init__(self, mainapp, master):
		# super(About_Window_Tk, self).__init__()
		# #self.drawing_dictionary = drawing_dictionary
		# top=self.top=Toplevel(master)
		# top.grab_set()
		# self.mainapp = mainapp

		# labels = [f'PYCabin {mainapp.version}']
		# gui_styles_tk.create_multiple_labels(frame=self,  labels=labels, row=2, column=2,)
		
		# #self.label = tk.Label(self,width = 20, text='Aircraft Type:')
		# #self.label.grid(row=0,column=0,padx=5, pady=5,sticky = 'NSEW')