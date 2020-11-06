

class Edit_Emergency_Equip_Window_Tk(object):
	def __init__(self, mainapp, master, mode, parent_ee):
		#self.drawing_dictionary = drawing_dictionary
		top=self.top=Toplevel(master)
		top.grab_set()
		self.mainapp = mainapp
		self.mode = mode
		self.parent_ee = parent_ee
		
		if self.mode == 'edit':
			self.orig_title = parent_ee.backend.title
		else:
			self.orig_msn = None
			
		self.data_checks = {}
		
		self.setup_label_frames()
		self.setup_widgets()
		
	def setup_label_frames(self):
	
		self.main_frame = LabelFrame(self.top,text="Aircraft Details:")
		self.main_frame.grid(row=2, column=0, columnspan = 8, rowspan = 2,sticky='NW',padx=5, pady=5, ipadx=2, ipady=5)
		
	def setup_widgets(self):
	
		labels = ['Title:', 'Description:', 'Equipment Type:', 'Aircraft Type:', 'Weight (lbs):']
		row = 1
		gui_styles_tk.create_multiple_labels(self.main_frame, labels, row, 2, 20, 2, 2)	
		
		self.title_entry=Entry(self.main_frame, width=20)		
		self.title_entry.grid(row=1,column=3,padx=2, pady=2,sticky = 'NSEW')
		self.data_checks['Title'] = ['title', self.title_entry, self.orig_part_no]
		
		self.description_entry=Entry(self.main_frame, width=50)		
		self.description_entry.grid(row=2,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.equip_type_combo= ttk.Combobox(self.main_frame, values=self.available_equipment)
		self.equip_type_combo.grid(row=3,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.equip_type_combo= ttk.Combobox(self.main_frame, values=['A320'])
		self.equip_type_combo.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		self.weight_entry = Entry(self.main_frame, width=50)
		self.weight_entry.grid(row=4,column=3,padx=2, pady=2,sticky = 'NSEW')
		
		# ok button
		self.ok_button=Button(self.top,text='OK', command= lambda button = 'ok': self.cleanup(button))
		self.ok_button.grid(row=8,column=3, pady=5,sticky="nsew")

		# cancel button
		self.b=Button(self.top,text='Cancel', command= lambda button = 'cancel': self.cleanup(button))
		self.b.grid(row=8,column=4, pady=5,sticky="nsew")

		self.button = 'cancel'
		
	def cleanup(self,button):
	
		if button == 'ok':
			
			self.top.destroy()
			
		else:
			self.top.destroy()
		
		
		