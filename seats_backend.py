
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import seats_draw


class Seat_Backend():

	def __init__(self, parent_page, mainapp):
		self.mainapp = mainapp #main app
		self.parent_page = parent_page #this is the tkinter frame associated with this BE.
		self.setup_variables()	
		self.setup_seat_plot()
	
	def setup_variables(self):
	
		self.type = 'Seat'
		self.aircraft_type = None
		self.description = None
		self.part_no = None
		self.manufacturer = None
		self.side = None
		self.seat_type = None
		self.iat = None
		self.profile = None
		self.width = None #in inches
		self.width_inbd = None
		self.armrest_width = None
		self.length_fwd = None
		self.length_aft = None
		self.cushion_height = None
		self.height = None
		self.stud_distance = None
		self.srp_x = None
		self.srp_y = None
		self.weight_lbs = None
		self.color = 'skyblue' #outline color on canvas
		
		# cmm
		self.cmm_title = None
		self.cmm_ref = None
		self.cmm_version = None
		self.cmm_date = None
		self.cmm_install = None
		
		self.save_class = Seat_Saved_State
		self.treeview_node = None

	def gen_save_dict(self, comments_from_text_widget = True, comments = None):
	
		if comments_from_text_widget:
			comments = self.parent_page.comment_text.get("1.0","end")
		else:
			comments = comments

		return {'Title': self.title,
				'Aircraft Type': self.aircraft_type,
				'Part Number': self.part_no,
				'Description': self.description,
				'Manufacturer': self.manufacturer,
				'Side': self.side,
				'Seat Type': self.seat_type,
				'IAT': self.iat,
				'Profile': self.profile,
				'Width': self.width,
				'Width Inbd': self.width_inbd,
				'Armrest Width': self.armrest_width,
				'Length Fwd': self.length_fwd,
				'Length Aft': self.length_aft,
				'Cushion Height': self.cushion_height,
				'Height': self.height,
				'Stud Distance': self.stud_distance,
				'SRP X': self.srp_x,
				'SRP Y': self.srp_y,
				'Weight': self.weight_lbs,
				'CMM Title': self.cmm_title,
				'CMM Reference': self.cmm_ref,
				'CMM Version': self.cmm_version,
				'CMM Date': self.cmm_date,
				'CMM Install': self.cmm_install,
				'Comments': comments
				}

	def update_variables(self, source):
		
		self.title = source.part_no
		self.aircraft_type = source.aircraft_type
		self.description = source.description
		self.part_no = source.part_no
		self.iat = source.iat
		self.seat_type = source.seat_type
		self.profile = source.profile
		self.manufacturer = source.manufacturer
		self.side = source.side
		self.width = source.width
		self.width_inbd = source.width_inbd
		self.armrest_width = source.armrest_width
		self.length_fwd = source.length_fwd
		self.length_aft = source.length_aft
		self.cushion_height = source.cushion_height
		self.height = source.height
		self.stud_distance = source.stud_distance
		self.srp_x = source.srp_x
		self.srp_y = source.srp_y
		self.weight_lbs = source.weight_lbs

		self.cmm_title = source.cmm_title
		self.cmm_ref = source.cmm_ref
		self.cmm_version = source.cmm_version
		self.cmm_date = source.cmm_date
		self.cmm_install = source.cmm_install
		
		if self.aircraft_type == 'A320' or self.aircraft_type == 'A319' or self.aircraft_type == 'A320 Family':
			self.treeview_node = 'A320 Seats'
		elif self.aircraft_type == 'B737 Family':
			self.treeview_node = '737 Seats'
	
	def set_default_variables(self):

		if self.aircraft == 'A320 Family':
			# self.seat_part_no.set(self.id.get())
			# self.side.set('RHS')
			# self.seat_description.set('')
			# self.seat_weight.set('85.0')
			self.width.set('61.25')
			self.width_inbd.set('21.0')
			self.length_aft.set('24.0')
			self.length_fwd.set('2.2')
			# self.stud_distance.set('19.0')
			# self.headrest_height.set('45.0')
			# self.cushion_height.set('18.5')
			# self.seat_type.set('Triple - Economy')
			# self.srp_x.set('15.0')
			# self.srp_y.set('12.0')
			# self.iat.set('No')
			# self.profile.set('Generic')
			self.armrest_width.set('2.0')

	def update_component(self, source, type):
		#pass current joint through to state class (for undo redo)
		if type != 'undo_redo':
			self.mainapp.states.component_updated(type, self, self.save_class)
		self.update_variables(source)

	def calc_seat_weight(self, life_vest_weight, literature_weight):
	
		if self.seat_type == 'Triple Economy':
			no_pax = 3
			
		
		return float(self.weight_lbs) + no_pax*(float(life_vest_weight) + float(literature_weight))		
		
	def setup_seat_plot(self):
	
		self.seat_figure = Figure(figsize=(5,5), dpi=100)
		self.ax1 = self.seat_figure.add_subplot(121, aspect='equal', adjustable='box')
		self.ax2 = self.seat_figure.add_subplot(122, aspect='equal', adjustable='box')
		
		self.ax1.title.set_text('Top-Down View')
		self.ax2.title.set_text('Side Profile')
	
	def get_top_down_y_datum(self, station=None):
	
		if self.aircraft_type == 'A320 Family':
			if self.side == 'LHS':
				return -30.12
			elif self.side == 'RHS':
				return 30.12
		elif self.aircraft_type == 'B737 Family':
			if self.side == 'LHS':
				return -24.755
			elif self.side == 'RHS':
				return 24.755	

	def draw_seat(self, canvas, canvas_type, draw_top_down, top_down_datum, draw_side, side_datum):

		canvas[0].clear()
		canvas[1].clear()
		'''
		canvas type should be 'matplotlib' or 'dxf'
		'''
		width = float(self.width)
		width_inbd = float(self.width_inbd)
		length_fwd = float(self.length_fwd)
		length_aft = float(self.length_aft)
		armrest_width = float(self.armrest_width)
		height = float(self.height)
		cushion_height = float(self.cushion_height)
		stud_distance = float(self.stud_distance)
		
		srp_x = float(self.srp_x)
		srp_y = float(self.srp_y)
		
		if draw_top_down:
			if canvas_type == 'matplotlib':
				canvas[0].set_xlim([-20,40])
				if self.side == 'LHS':
					canvas[0].set_ylim([-75, 5])
				elif self.side == 'RHS':
					canvas[0].set_ylim([-5,75])
				
			x = top_down_datum[0]
			y = top_down_datum[1]
			
			# _________ Seat Tracks _________
			if self.side == 'LHS':
				f = -1
			else: 
				f = 1
			line, = canvas[0].plot([-20, x-length_fwd],[30.12*f, 30.12*f], color='dimgrey' )
			line.set_dashes([4, 4, 4, 4])
			line, = canvas[0].plot([x+length_aft, 40],[30.12*f, 30.12*f], color='dimgrey' )
			line.set_dashes([4, 4, 4, 4])			
			line, = canvas[0].plot([-20, x-length_fwd],[50.87*f, 50.87*f], color='dimgrey' )
			line.set_dashes([4, 4, 4, 4])
			line, = canvas[0].plot([x+length_aft, 40],[50.87*f, 50.87*f], color='dimgrey' )
			line.set_dashes([4, 4, 4, 4])	
			
			x_coords = [x - length_fwd, x + length_aft, x + length_aft, x - length_fwd, x - length_fwd]
			
			if self.side == 'LHS':
				y_top = y - width + width_inbd + armrest_width
				y_btm = y_top + width - (armrest_width*2)
			elif self.side == 'RHS':
				y_top = y + width - width_inbd - armrest_width
				y_btm = y_top - width + (armrest_width*2)
				
			y_coords = [y_top, y_top, y_btm, y_btm, y_top]
			canvas[0].fill(x_coords, y_coords, color=self.color, linewidth=1)
			canvas[0].plot(x_coords, y_coords, color='black', linewidth=1)
			
			# _________ Armrests _________
			if self.side == 'LHS':
				#outboard
				y_indb = y + width_inbd
				y_outbd = y - width + width_inbd
				x_coords = [x, x + length_aft*0.8, x + length_aft*0.8, x, x]
				y_coords = [y_outbd, y_outbd, y_top, y_top, y_outbd]
				canvas[0].fill(x_coords, y_coords, color=self.color, linewidth=1)
				canvas[0].plot(x_coords, y_coords, color='black', linewidth=1)
				
				#inbd
				y_coords = [y_indb, y_indb, y_btm, y_btm, y_indb]
				canvas[0].fill(x_coords, y_coords, color=self.color, linewidth=1)
				canvas[0].plot(x_coords, y_coords, color='black', linewidth=1)
			
			elif self.side == 'RHS':
				#outboard
				y_indb = y - width_inbd
				y_outbd = y + width - width_inbd
				x_coords = [x, x + length_aft*0.8, x + length_aft*0.8, x, x]
				y_coords = [y_outbd, y_outbd, y_top, y_top, y_outbd]
				canvas[0].fill(x_coords, y_coords, color=self.color, linewidth=1)
				canvas[0].plot(x_coords, y_coords, color='black', linewidth=1)				

				#inbd
				y_coords = [y_indb, y_indb, y_btm, y_btm, y_indb]
				canvas[0].fill(x_coords, y_coords, color=self.color, linewidth=1)
				canvas[0].plot(x_coords, y_coords, color='black', linewidth=1)
			
			# _________ Headrest _________
			canvas[0].plot([x+length_aft*0.7, x+length_aft*0.7], [y_btm, y_top], color='black', linewidth=1)	

			# _________ Seat Lines _________
			if self.side == 'LHS':
				canvas[0].plot([x-length_fwd, x+length_aft], [y_indb-(width*.33), y_indb-(width*.33)], color='black', linewidth=1)
				canvas[0].plot([x-length_fwd, x+length_aft], [y_indb-(width*.67), y_indb-(width*.67)], color='black', linewidth=1)
			elif self.side == 'RHS':
				canvas[0].plot([x-length_fwd, x+length_aft], [y_indb+(width*.33), y_indb+(width*.33)], color='black', linewidth=1)
				canvas[0].plot([x-length_fwd, x+length_aft], [y_indb+(width*.67), y_indb+(width*.67)], color='black', linewidth=1)
				
			# _________ Centerline _________
			line, = canvas[0].plot([-20, 40],[0, 0], color='black' )
			line.set_dashes([4, 4, 4, 4])
			
			# _________ Annotations _________
			#width
			canvas[0].annotate(s='', xy=(x+(length_aft*1.1),y_indb), xytext=(x+(length_aft*1.1),y_outbd), arrowprops=dict(arrowstyle='<->'))
			avg = (y_indb + y_outbd)/2
			canvas[0].text(x+(length_aft*1.1), avg, f'{str(width)}"', ha='left',)
			
			#width inbd
			avg = (y_indb + y)/2
			canvas[0].annotate(s='', xy=(-5,y_indb), xytext=(-5,y), arrowprops=dict(arrowstyle='<->'))
			canvas[0].text(-6, avg, f'{str(width_inbd)}"', ha='right',)
			
			# _________ Axis Limits _________
			canvas[0].set_xlim([-20,40])
			
			# _________ Front stud datum _________
			c = plt.Circle((x,y), 1, color='black')
			canvas[0].add_patch(c)
		
		if draw_side:
			
			if self.seat_type == 'Triple Economy':
				if canvas_type == 'matplotlib':
					canvas[1].set_xlim([-11,32])
					canvas[1].set_ylim([-6,51])
					
				if self.profile == 'Generic':
					seats_draw.economy_seat_generic_side_view(self, canvas[1], canvas_type, side_datum)
			
			# _________ Front Stud Datum _________
			line, = canvas[1].plot([0, 0],[0, height], color='green' )
			line.set_dashes([4, 4, 4, 4])
			
			# _________ SRP _________
			c = plt.Circle((srp_x,srp_y), 1, color='red')
			canvas[1].add_patch(c)
			canvas[1].text(srp_x,srp_y+1, 'SRP', ha='center', va='bottom', color='red')
			# _________ Annotations _________
			#length aft
			canvas[1].annotate(s='', xy=(0,height*1.03), xytext=(length_aft,height*1.03), arrowprops=dict(arrowstyle='<->'))	
			length_aft_text = canvas[1].text(length_aft/2, height*1.05, f'{str(length_aft)}"', ha='center')

			#length fwd
			canvas[1].annotate(s='', xy=(1,height*1.03), xytext=(-length_fwd*1.1,height*1.03), arrowprops=dict(arrowstyle='<-'))	
			canvas[1].text(-length_fwd/2, height*1.05, f'{str(length_fwd)}"', ha='center')

			#Height
			canvas[1].annotate(s='', xy=(length_aft*1.04,-1), xytext=(length_aft*1.04,height), arrowprops=dict(arrowstyle='<->'))	
			height_aft_text = canvas[1].text(length_aft*1.05, height*0.5, f'{str(height)}"', va='center')

			#Cushion Height
			canvas[1].annotate(s='', xy=(length_fwd*-1.5,-1), xytext=(length_fwd*-1.5,cushion_height), arrowprops=dict(arrowstyle='<->'))	
			c_height_aft_text = canvas[1].text(length_fwd*-1.6, cushion_height*0.5, f'{str(cushion_height)}"', ha='right')

			#stud distance
			canvas[1].annotate(s='', xy=(0,-2), xytext=(stud_distance,-2), arrowprops=dict(arrowstyle='<->'))	
			stud_text = canvas[1].text(stud_distance/2, -2.2, f'{str(stud_distance)}"', ha='center', va='top')



			
		for text in [length_aft_text, height_aft_text, c_height_aft_text, stud_text]:
			self.parent_page.canvas.draw()
			bbox = text.get_window_extent()
			ax = self.seat_figure.gca()
			bbox_data = bbox.transformed(ax.transData.inverted())
			ax.update_datalim(bbox_data.corners())
			#ax.autoscale_view()
			
		# _________ FLOOR _________
		xmin,xmax = ax.get_xlim()
		line, = canvas[1].plot([xmin, xmax],[0, 0], color='dimgrey' )

		
class Seat_Saved_State():
	def __init__(self, seat):
	
		Seat_Backend.setup_variables(self)
		Seat_Backend.update_variables(self, seat)
		
		self.treeview_node = seat.parent_page.treeview_iid
		