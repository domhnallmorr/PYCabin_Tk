
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
import components_tk
import undo_redo_tk
import database_tk

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
		
		self.states = undo_redo_tk.Undo_Redo(self)
		
	def setup_variables(self):
		
		self.version = '0.03'
		self.save_file = None
		self.cabin_database = r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.03\test.db'
		
	def setup_main_frames(self):
	
		self.rootpane = tk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
		self.rootpane.grid(row=1,column=0, columnspan=4,sticky="nsew")
		self.parent.grid_rowconfigure(1, weight=1)
		self.parent.grid_columnconfigure(3, weight=1)
		self.frame = Frame(self.parent)
		
		self.sidebar_frame = tk.Frame()
		self.sidebar_frame.grid_rowconfigure(1, weight=1)
		self.rootpane.add(self.sidebar_frame)
		self.setup_main_treeview()
		self.frame.grid(row=0,column=0, sticky="n")
		
		# the container is where we'll stack a bunch of frames
		self.container = tk.Frame(self.rootpane, bg="pink")
		self.container.grid_columnconfigure(0, weight=1)
		self.rootpane.add(self.container,stretch="always")
		
		self.frames = {}
		
	def setup_main_treeview(self):
	
		tk.Button(self.sidebar_frame, image = self.close_icon2, background='white', relief=FLAT,
			command= lambda action = False: self.open_close_all_nodes(action)).grid(row=0, column=0, sticky='w', padx = 0)
		tk.Button(self.sidebar_frame, image = self.open_icon2, background='white', relief=FLAT,
			command= lambda action = True: self.open_close_all_nodes(action)).grid(row=0, column=1, sticky='w', padx = 0)
		tk.Button(self.sidebar_frame, image = self.up_icon2, background='white', relief=FLAT,
			command = self.moveUp).grid(row=0, column=2, sticky='w', padx = 0)
		tk.Button(self.sidebar_frame, image = self.down_icon2, background='white', relief=FLAT,
			command = self.moveDown).grid(row=0, column=3, sticky='w', padx = 0)

		self.main_treeview = ttk.Treeview(self.sidebar_frame,selectmode='browse', show="tree")
		self.main_treeview.grid(row=1, column=0, columnspan = 20, sticky='nsew')
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
		
		#self.rootpane.add(self.main_treeview)
		
		self.main_treeview.bind('<<TreeviewSelect>>',lambda event, : self.ProcessOnSingleClick_Main_Tree(event))

		self.popup_menu = tk.Menu(self, tearoff=0)
		self.popup_menu.add_command(label="Delete        ",command= lambda mainapp=self: components_tk.delete_component(mainapp))		
		self.popup_menu.add_command(label="Copy          ",command= lambda mainapp=self: components_tk.copy_component(mainapp))
		
		#self.popup_menu.add_separator()
		
		
		self.main_treeview.bind("<Button-3>", self.popup)

		self.ids_not_allowed = ['Project', 'Aircraft', 'A320 Aircraft', '737 Aircraft', 'Aircraft', 'Seats', 'A320 Seats',
								'737 Seats', 'Monuments', 'A320 Monuments', 'A320 Windbreakers', 'A320 LOPAs']		
		
		self.treeview_nodes = {'Seats': ['A320 Seats', '737 Seats']}
		
		

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

		#________ EDIT ________				  
		edit_menu = tk.Menu(menu, tearoff = 0)
		menu.add_cascade(label='Edit',menu=edit_menu)
		
		edit_menu.add_command(label = 'Undo                     Ctrl+Z', command = lambda: self.states.undo())
		edit_menu.add_command(label = 'Redo                      Ctrl+Y', command = lambda: self.states.redo())
		

		#________ INSERT ________					  
		insert_menu = tk.Menu(menu, tearoff = 0)
		menu.add_cascade(label='Insert',menu=insert_menu)

		#insert_menu.add_command(label = 'Aircraft', command = lambda self=self, type='Aircraft': components_tk.new_component(self, type))
		#insert_menu.add_command(label = 'Seats - Multiple', command = lambda self=self, type='Seats - Multiple': components_tk.new_component(self, type))
		
		#
		insert_component_menu = tk.Menu(menu, tearoff = 0)
		insert_menu.add_cascade(label = 'Components',menu = insert_component_menu)
		insert_component_menu.add_command(label = 'Seat', command = lambda self=self, type='Seat': components_tk.new_component(self, type))
		insert_component_menu.add_command(label = 'Multiple Seats', command = lambda self=self, type='Seats - Multiple': components_tk.new_component(self, type))
		
		# ________ DATABASE ________
		db_menu = tk.Menu(menu, tearoff = 0)
		menu.add_cascade(label='Database',menu=db_menu)

		db_menu.add_command(label = 'Add Components to Database', command = lambda self=self: database_tk.add_components(self))
		db_menu.add_command(label = 'Load Components From Database', command = lambda self=self: database_tk.load_components(self))
		
		# ________ ABOUT ________
		about_menu = tk.Menu(menu, tearoff = 0)
		menu.add_cascade(label='About',menu=about_menu)
		
		about_menu.add_command(label = 'About PYCabin', command = lambda self=self: about_tk.about(self))

	def ProcessOnSingleClick_Main_Tree(self, event):
		item_iid = event.widget.selection()[0]
		parent_iid = event.widget.parent(item_iid)
		
		ids_to_ignore = ['A320 Aircraft', '737 Aircraft', 'A320 Seats', '737 Seats',
						'A320 Monuments', 'A320 Windbreakers', 'A320 LOPAs']

		if parent_iid:
			if item_iid not in ids_to_ignore:
				components_tk.show_frame(self, event.widget.item(item_iid, 'text'))
		if not parent_iid:
			if (event.widget.item(item_iid, 'text')) == 'Project':
				components_tk.show_frame(self, "Project")
			
	def open_close_all_nodes(self, action):
		
		for node in self.treeview_nodes:
			self.main_treeview.item(node, open=action)
			
			for node in self.treeview_nodes[node]:
				self.main_treeview.item(node, open=action)

	def moveUp(self):
		leaves = self.main_treeview.selection()
		for i in leaves:
			self.main_treeview.move(i, self.main_treeview.parent(i), self.main_treeview.index(i)-1)

	def moveDown(self):
		leaves = self.main_treeview.selection()
		for i in leaves:
			self.main_treeview.move(i, self.main_treeview.parent(i), self.main_treeview.index(i)+1)
		
	def setup_fonts(self):
	
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		self.title_font.configure(underline=True)

	def setup_project_page(self):
	
		self.frames['Project'] = project_tk.Project_Page_Tk(self.container, self)
		self.frames['Project'].pack(fill="both", expand=True)
		# self.frames['Project'].grid(row=0, column=0, sticky="NSEW")
		# self.frames['Project'].grid_rowconfigure(0, weight=0)
		# self.frames['Project'].grid_rowconfigure(1, weight=1)
		# self.frames['Project'].grid_columnconfigure(0, weight=1)
		
		self.current_frame = self.frames['Project']
	def popup(self,event):
		try:
			self.popup_menu.selection = self.main_treeview.set(self.main_treeview.identify_row(event.y))
			self.main_treeview.focus(self.main_treeview.identify_row(event.y))
			self.main_treeview.selection_set(self.main_treeview.identify_row(event.y))
			#print(self.main_treeview.selection()[0])
			if self.main_treeview.selection()[0] not in self.ids_not_allowed:			
				self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
		finally:
				self.popup_menu.grab_release()	
				
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
	root.bind('<Control-z>', lambda event, MA=MA: MA.states.undo())
	root.bind('<Control-y>', lambda event, MA=MA: MA.states.redo())
	root.mainloop()
		