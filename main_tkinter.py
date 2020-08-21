'''
V0.01 Initial Version

'''

import ctypes
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import font as tkfont

import tkinter.messagebox

import project_tk as project_tk
import gui_styles_tk as gui_styles
import file_menu as fm
import about_tkinter as about_tk

class MainApplication(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		user32 = ctypes.windll.user32
		self.screen_width = (user32.GetSystemMetrics(0))
		self.screen_height = (user32.GetSystemMetrics(1))
		
		self.parent = parent
		
		
		self.icons_folder = r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\Icons'
		gui_styles.setup_icons(self)
		self.setup_variables()
		
		self.parent.title(f"PYCabin V{self.version}")
		gui_styles.setup_fonts(self)
		
		self.setup_menu()
		self.setup_main_frames()
		
		
		self.setup_project_page()

	def setup_variables(self):
		
		self.version = '0.01'
		self.save_file = None
		
	def setup_main_frames(self):
	
		self.rootpane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
		self.rootpane.grid(row=1,column=0, columnspan=4,sticky="nsew")
		root.grid_rowconfigure(1, weight=1)
		root.grid_columnconfigure(3, weight=1)
		self.frame = Frame(root)

		self.setup_main_treeview()
		self.frame.grid(row=0,column=0, sticky="n")
		
		# the container is where we'll stack a bunch of frames
		self.container = tk.Frame(self.rootpane, bg="pink")
		self.container.grid_columnconfigure(0, weight=1)
		self.rootpane.add(self.container,stretch="always")
		
		self.frames = {}
		
	def setup_main_treeview(self):
		self.main_treeview = ttk.Treeview(self.rootpane,selectmode='browse')
		fi = self.folder_icon2
		abi = self.airbus_icon2
		bi = self.boeing_icon2

		# ________ Project ________
		item = self.main_treeview.insert("",'end','Project',text='Project',image = fi)
		
		# ________ Aircraft ________
		item = self.main_treeview.insert("",'end','Aircraft',text='Aircraft',image = fi)
		item = self.main_treeview.insert("Aircraft",'end','A320 Aircraft',text=' A320 Family',image = abi)
		item = self.main_treeview.insert("Aircraft",'end','737 Aircraft',text=' B737 Family',image = bi)

		# ________ Seats ________
		item = self.main_treeview.insert("",'end','Seats',text='Seats',image = fi)
		item = self.main_treeview.insert("Seats",'end','A320 Seats',text=' A320 Family',image = abi)
		item = self.main_treeview.insert("Seats",'end','737 Seats',text=' 737 Family',image = bi)
		
		self.rootpane.add(self.main_treeview)	
		#self.main_treeview.bind("<Button-3>", self.popup)

		self.ids_not_allowed = ['Project', 'Aircraft', 'A320 Aircraft', '737 Aircraft', 'Aircraft', 'Seats', 'A320 Seats',
								'Monuments', 'A320 Monuments', 'A320 Windbreakers', 'A320 LOPAs']		

	def setup_menu(self):
		menu = tk.Menu(self.master)
		self.master.config(menu=menu)
		#File					  
		file_menu = tk.Menu(menu, tearoff = 0)
		menu.add_cascade(label='File',menu=file_menu)
		
		file_menu.add_command(label = 'New                     Ctrl+N', command = lambda self=self: fm.new_project(mainapp=self))
		file_menu.add_command(label = 'Load                    Ctrl+O', command = lambda self=self: fm.load(mainapp = self))
		file_menu.add_command(label = 'Save                     Ctrl+S', command = lambda self=self: fm.save(mainapp= self))
		#file_menu.add_command(label = 'Save As', command = lambda self=self, mode='save as': fm.save(self, mode))

		about_menu = tk.Menu(menu, tearoff = 0)
		menu.add_cascade(label='About',menu=about_menu)
		
		about_menu.add_command(label = 'About PYCabin', command = lambda self=self: about_tk.about(self))

		
	def setup_fonts(self):
	
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		self.title_font.configure(underline=True)

	def setup_project_page(self):
	
		self.frames['Project'] = project_tk.Project_Page_Tk(self.container, self)
		self.frames['Project'].grid(row=0, column=0, sticky="NSEW")
		self.frames['Project'].grid_rowconfigure(0, weight=0)
		self.frames['Project'].grid_rowconfigure(1, weight=1)
		self.frames['Project'].grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(width=tk.TRUE, height=tk.TRUE)
	#MainApplication(root).pack(side="top", fill="both", expand=True)
	MA = MainApplication(root)
	MA.grid(row=1, columnspan=4, sticky='nsew')
	#root.bind('<Control-z>', MA.states.undo)
	#root.bind('<Control-y>', MA.states.redo)
	
	root.geometry('{}x{}'.format(1600, 800))    
	
	root.bind('<Control-n>', lambda event, MA=MA: fm.new_project(event, MA))
	root.bind('<Control-o>', lambda event, MA=MA: fm.load(event, MA))
	root.bind('<Control-s>', lambda event, MA=MA: fm.save(event, MA))
	root.mainloop()
		