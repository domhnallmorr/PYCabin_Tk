import copy

def setup_variables(w):
	w.type = 'Change'
	w.title = None
	w.description = None
	w.sb_title = None
	w.sb_number = None
	w.output_dir = None
	w.mods = []

def update_variables(w, source):

	w.title = source.title
	w.sb_title = source.sb_title
	w.sb_number = source.sb_number
	w.output_dir = source.output_dir
	w.mods = copy.deepcopy(source.mods)

class Change_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		setup_variables(self)

		self.save_class = Change_Saved_State
		self.mainapp = self.parent_page.mainapp
	
	
	def update_component(self, source, type):
	
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, Change_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, Change_Saved_State)
		update_variables(self, source)
			
	def gen_save_dict(self, comments_from_text_widget = True, comments = None):

		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments
			
		return {'Title': self.title,
				'SB Title': self.sb_title,
				'SB Number': self.sb_number,
				'Output Dir': self.output_dir,
				'Mods': self.mods,
				'Comments': comments}
	
	def get_change_drawings(self):
		
		drawings = []
		for mod in self.mods:
		
			if mod[0] in ['LOPA']:
				
				mod = self.parent_page.mainapp.frames[mod[1]].backend
				
				drawings.append([mod.drawing_no, mod.drawing_rev, mod.title])
		
		return drawings
		
	def get_change_oem_docs(self):
	
		oem_docs = []
		
		for mod in self.mods:
		
			if mod[0] in ['LOPA']:
				seats = []
				
				#get all seat CMMs
				lopa = self.parent_page.mainapp.frames[mod[1]].backend
				
				for side in ['LHS', 'RHS']:
					for row in lopa.seat_layout[side]:
						
						if row[1] not in seats:
							seats.append(row[1])
							
							seat = self.parent_page.mainapp.frames[row[1]].backend
							
							cmm_title = seat.cmm_title
							cmm_ref = seat.cmm_ref
							cmm_version = seat.cmm_version
							cmm_date = seat.cmm_date
							
							text = ''.join([cmm_title, cmm_ref, cmm_version, cmm_date])
							
							found_doc = False
							
							for d in oem_docs:
								if d[-1] == text:
									found_doc = True
									break
									
							if not found_doc:
								oem_docs.append([cmm_title, cmm_date, cmm_ref, cmm_version, text])
		
		for i, d in enumerate(oem_docs):
			del oem_docs[i][-1] #delete text at end
		print(oem_docs)
		return oem_docs
		
class Change_Saved_State():
	def __init__(self, change):
	
		setup_variables(self)
		update_variables(self, change)			
		
		