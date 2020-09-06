import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import windbreaker_draw

import components_tk

def check_monument_used(self):
	monument_used = False
	lopas, lopa_dict = components_tk.get_all_lopas(self.mainapp)
	
	for l in lopas:
		l = self.mainapp.frames[l]
		for m in l.backend.monuments:
			if m[1] == self.backend.title:
				monument_used = True
				break
		if monument_used:
			break
			
	return monument_used
	

class Windbreaker_Backend():

	def __init__(self, parent_page, controller):
		self.controller = controller #main append
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		self.setup_variables()
		self.setup_plot()
		self.save_class = Windbreaker_Saved_State
		
		
	def setup_variables(self):
		
		self.title = None
		self.type = 'Windbreaker'
		self.aircraft_type = None
		self.part_no = None
		self.description = None
		self.side = None
		self.thickness = None
		self.width = None
		self.height = None
		self.dist_from_cl = None
		self.joggle = None
		self.joggle_width = None
		self.joggle_lower = None
		self.joggle_upper = None
		self.bassinet = None

		# cmm
		self.cmm_title = None
		self.cmm_ref = None
		self.cmm_version = None
		self.cmm_date = None
		self.cmm_install = None
		self.cmm_remove = None
		
		self.treeview_node = None

	def gen_save_dict(self):
	
		return {'Title': self.title,
				'Aircraft Type': self.aircraft_type,
				'Part Number': self.part_no,
				'Description': self.description,
				'Side': self.side,
				'Thickness': self.thickness,
				'Width': self.width,
				'Height': self.height,
				'Dist From C/L': self.dist_from_cl,
				'Joggle': self.joggle,
				'Joggle Width': self.joggle_width,
				'Joggle Lower': self.joggle_lower,
				'Joggle Upper': self.joggle_upper,
				'Bassinet': self.bassinet,
				'CMM Title': self.cmm_title,
				'CMM Reference': self.cmm_ref,
				'CMM Version': self.cmm_version,
				'CMM Date': self.cmm_date,
				'CMM Install': self.cmm_install,
				'CMM Remove': self.cmm_remove,
				'Comments': self.parent_page.comment_text.get("1.0","end")}
				
	def update_variables(self, source):
		self.title = source.title
		self.aircraft_type = source.aircraft_type
		self.part_no = source.part_no 
		self.description = source.description
		self.side = source.side
		self.thickness = source.thickness
		self.width = source.width
		self.height = source.height
		self.dist_from_cl = source.dist_from_cl
		self.joggle = source.joggle
		self.joggle_width = source.joggle_width
		self.joggle_lower = source.joggle_lower
		self.joggle_upper= source.joggle_upper
		self.bassinet = source.bassinet	

		self.cmm_title = source.cmm_title
		self.cmm_ref = source.cmm_ref
		self.cmm_version = source.cmm_version
		self.cmm_date = source.cmm_date
		self.cmm_install = source.cmm_install
		self.cmm_remove = source.cmm_remove
		
		if self.aircraft_type == 'A320 Family':
			self.treeview_node = 'A320 Windbreakers'
			
	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.controller.states.component_updated(type, self, Windbreaker_Saved_State)
		elif type == 'new':
			self.controller.states.component_updated(type, self, Windbreaker_Saved_State)
			
		self.update_variables(source)

	def setup_plot(self):
	
		self.figure = Figure(figsize=(5,5), dpi=100)
		self.ax1 = self.figure.add_subplot(121, aspect='equal', adjustable='box')
		self.ax2 = self.figure.add_subplot(122, aspect='equal', adjustable='box')
		
		self.figure.subplots_adjust(top=0.95)
		
	def draw_wb(self, canvas, canvas_type, draw_top_down, top_down_datum, draw_side, side_datum):

		canvas[0].clear()
		canvas[1].clear()
			
		# _________ Centerline _________
		line, = canvas[0].plot([-20, 40],[0, 0], color='black' )
		line.set_dashes([4, 4, 4, 4])
		
		# _________ Floor _________
		line, = canvas[1].plot([-20, 40],[0, 0], color='black' )
		#line.set_dashes([4, 4, 4, 4])
		
		windbreaker_draw.windbreaker_top_down_view(canvas[0], canvas_type, top_down_datum, self)
		windbreaker_draw.windbreaker_side_view(canvas[1], canvas_type, side_datum, self)

		# _________ Annotations _________
		x = top_down_datum[0]
		y = top_down_datum[1]
		
		if self.side == 'LHS':
			y1 = -1*float(self.dist_from_cl)
			y2 = y1 - float(self.width)
		else:
			y1 = float(self.dist_from_cl)
			y2 = y1 + float(self.width)			
		#width
		canvas[0].annotate(s='', xy=(x+2,y1), xytext=(x+2,y2), arrowprops=dict(arrowstyle='<->'))
		avg = (y1 + y2)/2
		canvas[0].text(x+4, avg, f'{str(self.width)}"', ha='left',)
			
		#thickness
		
		if self.joggle == 'Yes':
			t = float(self.joggle_width)
		else:
			t = float(self.thickness)
		if self.side == 'LHS':
			y1 = -0.8*float(self.dist_from_cl)
		else:
			y1 = float(self.dist_from_cl) * 0.8
			
		#canvas[0].annotate(s='', xy=(x+1,y1), xytext=(x - float(self.thickness),y1), arrowprops=dict(arrowstyle='simple'))
		avg = (x + (x-t))/2
		canvas[0].text(avg, y1, f'{str(t)}"', ha='center',)
		
		# Dist from CL
		if self.side == 'LHS':
			y1 = -1*float(self.dist_from_cl)
		else:
			y1 = float(self.dist_from_cl)		
		
		canvas[0].annotate(s='', xy=(x+7,0), xytext=(x+7,y1), arrowprops=dict(arrowstyle='<->'))
		avg = y1/2
		canvas[0].text(x+9, avg, f'{str(self.dist_from_cl)}"', ha='left',)
		
		# Height
		y1 = float(self.height)
		canvas[1].annotate(s='', xy=(7,0), xytext=(7,y1), arrowprops=dict(arrowstyle='<->'))
		avg = y1/2
		canvas[1].text(9, y1/2, f'{str(self.height)}"', ha='left',)

		if self.joggle == 'Yes':
			y1 = float(self.joggle_lower)
			canvas[1].annotate(s='', xy=(t*-1.1,0), xytext=(t*-1.1,y1), arrowprops=dict(arrowstyle='<->'))
			avg = y1/2
			canvas[1].text(t*-1.2, y1/2, f'{str(self.joggle_lower)}"', ha='right',)

			y1 = float(self.joggle_upper)
			canvas[1].annotate(s='', xy=(-14,0), xytext=(-14,y1), arrowprops=dict(arrowstyle='<->'))
			avg = y1/2
			canvas[1].text(-15, y1/2, f'{str(self.joggle_upper)}"', ha='right',)
		
		self.ax1.set_title('Top-Down View')
		self.ax2.title.set_text('Side Profile')
		
		self.ax1.set(ylabel = 'Distance From Centerline (")', xlabel='Distance Forward/Aft of Rear Face (")')
		self.ax2.set(ylabel = 'Height Above Floor (")', xlabel='Distance Forward/Aft of Rear Face (")')
		
		self.parent_page.canvas.draw()

	def get_top_down_y_datum(self):
	
		if self.aircraft_type == 'A320 Family':
			if self.side == 'LHS':
				return float(self.dist_from_cl)*-1
			elif self.side == 'RHS':
				return float(self.dist_from_cl)
				
class Windbreaker_Saved_State():
	def __init__(self, wb):
	
		Windbreaker_Backend.setup_variables(self)
		Windbreaker_Backend.update_variables(self, wb)
		