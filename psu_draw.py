import ezdxf
import Default_AC_Models
import lopa_draw
import math

def draw_psu_rail_side(self, canvas, canvas_type, datum, side):

	x, lav_d, lav_e, wb_installed = self.get_psu_rail_start_end()
	
	if side == 'LHS':
		x = x[0]
		
	else:
		x= x[1]
		
	y1 = [70, 70]
	y2 = [75, 75]
	
	if canvas_type == 'dxf':
		canvas.add_line((x[0], y1[0]), (x[1], y1[1]))
		canvas.add_line((x[0], y2[0]), (x[1], y2[1]))
		
	if canvas_type == 'matplotlib':
		line, = canvas.plot(x,y1, color='black', linewidth=1)
		line, = canvas.plot(x,y2, color='black', linewidth=1)
		
def draw_psu_layout(self, canvas, canvas_type, datum, side):
	
	colors = {'Oxygen Box LHS': 'blue', 'Oxygen Box RHS': 'blue', 'Gasper': 'black', '11" PSIU': 'green', '8" PSIU': 'red', 'Partition Panel': 'cyan',
				'Clamping Panel': 'purple', 'Adjustment Panel': 'brown'}
	widths = {'Oxygen Box LHS': 12, 'Oxygen Box RHS': 12, 'Gasper': 3, '11" PSIU': 11, '8" PSIU': 8, 'Partition Panel LHS': 2, 'Partition Panel RHS': 2, 
				'Clamping Panel': 2, 'Adjustment Panel LHS': 4, 'Adjustment Panel RHS': 4}
	
	
	for index, part in enumerate(self.psu_layout[side]):
		x = float(part[3])
		
		color = 'grey'
		if part[1] in colors.keys():
			color = colors[part[1]]
		
		if part[1] in widths.keys():
			w = widths[part[1]]
		elif 'Filler Panel' in part[1]:
			w = int(part[1].split('"')[0])
			color = 'grey'
			
			
		x_coords = [x, x + w, x + w, x, x]
		y_coords = [70, 70, 75, 75, 70]
		
		canvas.fill(x_coords, y_coords, color=color, linewidth=1)
		
		if 'Oxygen Box' in part[1]:
			
			canvas.plot([x+(w/2),x+(w/2)], [70, 50], color=color, linewidth=2) 
			


def gen_dxf(self):

	canvas_type = 'dxf'
	dxf = ezdxf.new(dxfversion='R2010')
	linetypes = [("CENTER", "Center ____ _ ____ _ ____ _ ____ _ ____ _ ____",
				[70.0, 40.0, -10.0, 10.0, -10.0]),
				("DASHED", "Dashed __ __ __ __ __ __ __ __ __ __ __ __ __ _",
				[21.0, 14.0, -7.0])]
	for name, desc, pattern in linetypes:
		if name not in dxf.linetypes:
			dxf.linetypes.new(name=name, dxfattribs={'description': desc, 'pattern': pattern})
			
	modelspace = dxf.modelspace()

	# Add AC
	ac_block = dxf.blocks.new(name='aircaft model')

	if self.backend.aircraft_type == 'A320':
		ac_model = Default_AC_Models.A320_Family_Model('A320', canvas_type, ac_block, ac_block, ac_block)

	ac_model.draw_all()

	modelspace.add_blockref('aircaft model', (0, 0))

	# Add LOPA
	lopa_backend = self.mainapp.frames[self.backend.lopa].backend
	lopa_model = lopa_draw.LOPA_Drawing(lopa_backend, 'dxf', modelspace, modelspace, modelspace, dxf)
	lopa_model.draw_all(psu=True)

	# Add PSU Parts
	blocks = PSU_Blocks(dxf, lopa_backend, self.backend)
	print(blocks.blocks)
	for side in ['LHS', 'RHS']:
		for i, part in enumerate(self.backend.psu_layout[side]):
			if part[1] in ['Oxygen Box LHS', 'Oxygen Box RHS', 'Partition Panel LHS', 'Adjustment Panel LHS']:
				name = part[1]
			else:
				name = f'{part[1]} {side}'
			print(name)
			if name in blocks.blocks:
				modelspace.add_blockref(name, (float(part[3]), 0))

			elif 'Adjustment Panel' in part[1]:

				width = float(self.backend.psu_layout[side][i+1][3]) - float(part[3])

				block = blocks.create_adjument_panel(width, side)
				modelspace.add_blockref(block, (float(part[3]), 0))

	dxf.saveas(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.10\psu.dxf')
	

def setup_psu_blocks(self, dxf):
	
	psu_blocks = {}
	if self.backend.aircraft_type in ['A320', 'A319']:
		for b in [1, 2, 4, 6, 8]:
			psu_blocks[f'{b}" Filler Panel LHS'] =  dxf.blocks.new(name=f'{b}" Filler Panel LHS')
			psu_blocks[f'{b}" Filler Panel RHS'] =  dxf.blocks.new(name=f'{b}" Filler Panel RHS')
			draw_filler_panel_block(b, psu_blocks[f'{b}" Filler Panel LHS'], 'LHS')
			draw_filler_panel_block(b, psu_blocks[f'{b}" Filler Panel RHS'], 'RHS')
		
		psu_blocks[f'Oxygen Box LHS'] =  dxf.blocks.new(name=f'Oxygen Box LHS')
		psu_blocks[f'Oxygen Box RHS'] =  dxf.blocks.new(name=f'Oxygen Box RHS')
		draw_oxygen_block(psu_blocks[f'Oxygen Box LHS'], 'LHS')
		draw_oxygen_block(psu_blocks[f'Oxygen Box RHS'], 'RHS')
	return psu_blocks
		
def draw_filler_panel_block(breadth, canvas, side):
	
	#side view
	points = [(0, 0), (breadth, 0), (breadth, 5), (0, 5), (0, 0)]
	canvas.add_lwpolyline(points)
	
	if side == 'LHS':
		y = 70
	else:
		y = -170
		
	#top view
	points = [(0, y), (breadth, y), (breadth, y+10), (0, y+10), (0, y)]
	canvas.add_lwpolyline(points)
	
def draw_oxygen_block(canvas, side):

	#side view
	points = [(0, 0), (12, 0), (12, 5), (0, 5), (0, 0)]
	canvas.add_lwpolyline(points)
	
	y = get_top_y_coords(side, 'A320')
	
	#top view
	points = [(0, y), (12, y), (12, y+20), (0, y+20), (0, y)]
	canvas.add_lwpolyline(points)	
	
	canvas.add_text('O', dxfattribs={'rotation': 0, 'height': 5.35}).set_pos((6, y+10),align='CENTER')
	
	#add mask to side view

	points = [(6, 0), (6, -6), (5, -6), (5, -8), (7, -8), (7, -6), (6,-6)]
	canvas.add_lwpolyline(points)
	
	
	
def add_psu_blocks(self, modelspace, psu_blocks):
	print(psu_blocks)
	for side in ['LHS', 'RHS']:
		
		if side == 'LHS':
			side_y = -100
		else:
			side_y = 200

		for part in self.backend.psu_layout[side]:
		
			station = float(part[3])
			type = part[1]
			print(type)
			#if type in psu_blocks.keys():
				#print('here')
				#print(station)
			modelspace.add_blockref(f'{type} {side}', (station, side_y))
	
		
def get_top_y_coords(side, aircraft):
	if aircraft in ['A320', 'A319']:
		# y cordinate for blocks top down view
		if side == 'LHS':
			return 70
		else:
			return -170
		
class PSU_Blocks:

	def __init__(self, dxf, lopa, psu_backend):
	
		self.floor_coords = [-180, 130]

		self.widths = {'Oxygen Box': 12,
						'11" PSIU': 11,
						'8" PSIU': 8,
						'Partition Panel': 2,
						'Clamping Panel': 2,
						'1" Filler Panel': 1,
						'2" Filler Panel': 2,
						'4" Filler Panel': 4,
						'6" Filler Panel': 6,
						'8" Filler Panel': 8,
						'Gasper': 3
						}

		self.colors = {'Oxygen Box': 4,
						'11" PSIU': 3,
						'8" PSIU': 20,
						'Partition Panel': 180,
						'Clamping Panel': 2,
						'1" Filler Panel': 8,
						'2" Filler Panel': 8,
						'4" Filler Panel': 8,
						'6" Filler Panel': 8,
						'8" Filler Panel': 8,
						'Gasper': 6,
						'Adjustment Panel': 25,
						}
						
		if lopa.aircraft_type == 'A320':
			self.dist_cl = dist_cl = 30
			self.breadth = breadth = 10
			self.height = height = 5
			
		self.blocks = {}
		
		self.adjustment_panels = {}

		self.psu_backend = psu_backend
		self.dxf = dxf

		for part in self.widths:
			
			color = self.colors[part]
			for side in ['LHS', 'RHS']:
				block = dxf.blocks.new(name=f'{part} {side}')
				self.blocks[f'{part} {side}'] = block
				w = self.widths[part]
							
				if side == 'LHS':
					# top down
					y1 = dist_cl*-1
					y2 = y1-breadth

					#side
					y3 = self.floor_coords[0] + psu_backend.psu_y_coords[0]
					y4 = self.floor_coords[0] + psu_backend.psu_y_coords[1]

				elif side == 'RHS':
					# top down
					y1 = dist_cl
					y2 = y1+breadth

					#side
					y3 = self.floor_coords[1] + psu_backend.psu_y_coords[0]
					y4 = self.floor_coords[1] + psu_backend.psu_y_coords[1]
				
				# draw main outline
				points = [(0, y1), (w, y1), (w, y2), (0, y2), (0, y1)]
				block.add_lwpolyline(points,dxfattribs={'color': color})
					
				points = [(0, y3), (w, y3), (w, y4), (0, y4), (0, y3)]
				block.add_lwpolyline(points,dxfattribs={'color': color})					
					
				
				# _______ OXYGEN BOX _______
				if part == 'Oxygen Box':
					#horizintal line top view
					if side == 'LHS':
						points = [(0, y1-1.3), (w, y1-1.3)]
						points2 = [(0, y2+1.3), (w, y2+1.3)]
					else:
						points = [(0, y1+1.3), (w, y1+1.3)]
						points2 = [(0, y2-1.3), (w, y2-1.3)]
					block.add_lwpolyline(points,dxfattribs={'color': 4})
					block.add_lwpolyline(points2,dxfattribs={'color': 4})
					
					#circle with text top view
					block.add_circle((w/2, (y1+y2)/2), 3, dxfattribs={'color': 4})
					block.add_text(f"4{side[0]}").set_pos((w/2, (y1+y2)/2), align='MIDDLE_CENTER')
					
					# text side
					block.add_text(f"4{side[0]}").set_pos((w/2, (y3+y4)/2), align='MIDDLE_CENTER')
					
					# oxygen mask
					points = [(w*0.25, y3), (w*0.25, y3-14),(w*0.2, y3-14), (w*0.15, y3-17), (w*0.35, y3-17), (w*0.3, y3-14), (w*0.25, y3-14)]
					block.add_lwpolyline(points,dxfattribs={'color': 4})
					
				# _______ 11" PSIU _______
				if part == '11" PSIU':					
					
					#vertical line top view
					points = [(w*0.4, y1), (w*0.4, y2)]
					block.add_lwpolyline(points,dxfattribs={'color': color})
					
					#top down ellipse/cirlce
					block.add_ellipse((w*0.2, (y1+y2)/2), major_axis=(0, 3), ratio=0.5, dxfattribs={'color': color})
					block.add_circle((w*0.2, (y1+y2)/2), 1, dxfattribs={'color': color})
					
					#concentric circles top down
					for r in [1, 0.75, 0.5, 0.25]:
						for c in [0, 3, -3]:
							block.add_circle((w*0.6, ((y1+y2)/2)+c), r, dxfattribs={'color': color})
					
					# side view
					points = [(w*0.4, y3), (w*0.4, y4)]
					block.add_lwpolyline(points,dxfattribs={'color': color})

					points = [(w*0.1, y3), (w*0.15, y3+1), (w*0.35, y3)]
					block.add_lwpolyline(points,dxfattribs={'color': color})
					
					points = [(w*0.8, y3), (w*0.85, y3-2), (w*0.95, y3-2), (w, y3)]
					block.add_lwpolyline(points,dxfattribs={'color': color})

					points = [(w*0.4, y4), (w*0.45, y4+2), (w*0.55, y4+2), (w*0.6, y4)]
					block.add_lwpolyline(points,dxfattribs={'color': color})

				# _______ 8" PSIU _______
				if part == '8" PSIU':					
					
					#concentric circles top down
					for r in [1, 0.75, 0.5, 0.25]:
						for c in [0, 3, -3]:
							block.add_circle((w*0.2, ((y1+y2)/2)+c), r, dxfattribs={'color': color})
					
					# side view
					
					points = [(0, y3), (w*0.1, y3-2), (w*0.2, y3-2), (w*0.3, y3)]
					block.add_lwpolyline(points,dxfattribs={'color': color})

					points = [(w*0.8, y4), (w*0.85, y4+2), (w*0.95, y4+2), (w, y4)]
					block.add_lwpolyline(points,dxfattribs={'color': color})
					
				# _______ Gasper _______
				if part == 'Gasper':
					mid = (y1+y2)/2
					# Top down
					r = 1.35 #radius
					for c in [mid-(breadth/3), mid, mid+(breadth/3)]:
						block.add_circle((w*0.5, c), r, dxfattribs={'color': color})
						
						points = [(w*0.5, c-r), (w*0.5, c+r)]#vert
						block.add_lwpolyline(points,dxfattribs={'color': color})						

						points = [((w*0.5)-r, c), ((w*0.5)+r, c)]#vert
						block.add_lwpolyline(points,dxfattribs={'color': color})

					# Side
					points = [(0, y3), (w*0.5, y4), (w, y3)]
					block.add_lwpolyline(points,dxfattribs={'color': color})			

				# _______ Filler Panel _______
				if 'Filler Panel' in part:
					
					block.add_text(f"{part[0]}").set_pos((w/2, (y1+y2)/2), align='MIDDLE_CENTER')
					block.add_text(f"{part[0]}").set_pos((w/2, (y3+y4)/2), align='MIDDLE_CENTER')

				# _______ Clamping Panel _______
				if 'Clamping Panel' in part:
					
					block.add_text("C").set_pos((w/2, ((y1+y2)/2)+breadth/4), align='MIDDLE_CENTER')
					block.add_text("P").set_pos((w/2, ((y1+y2)/2)-breadth/4), align='MIDDLE_CENTER')
					
				# _______ Clamping Panel _______
				if 'Partition Panel' in part:
					mid = (y1+y2)/2
					
					block.add_ellipse((w*0.4, mid + 3), major_axis=(0, 0.75), start_param = math.pi, end_param=0, ratio=1, dxfattribs={'color': color})				
					block.add_ellipse((w*0.4, mid-3), major_axis=(0, 0.75), start_param = math.pi, end_param=0, ratio=1, dxfattribs={'color': color})				
				
					points = [(0, mid + 3.75), (w*0.4, mid + 3.75)]
					block.add_lwpolyline(points,dxfattribs={'color': color})
					
					points = [(0, mid + 2.25), (w*0.4, mid + 2.25)]
					block.add_lwpolyline(points,dxfattribs={'color': color})

					points = [(0, mid - 3.75), (w*0.4, mid - 3.75)]
					block.add_lwpolyline(points,dxfattribs={'color': color})
					
					points = [(0, mid - 2.25), (w*0.4, mid - 2.25)]
					block.add_lwpolyline(points,dxfattribs={'color': color})		
	
	def create_adjument_panel(self, w, side):

		color = self.colors['Adjustment Panel']

		count = len(list(self.adjustment_panels.keys()))

		block = self.dxf.blocks.new(name=f'Adjustment_Panel_{count}')

		self.adjustment_panels[f'Adjustment_Panel_{count}'] = block

		if side == 'LHS':
			# top down
			y1 = self.dist_cl*-1
			y2 = y1-self.breadth

			#side
			y3 = self.floor_coords[0] + self.psu_backend.psu_y_coords[0]
			y4 = self.floor_coords[0] + self.psu_backend.psu_y_coords[1]

		elif side == 'RHS':
			# top down
			y1 = self.dist_cl
			y2 = y1+self.breadth

			#side
			y3 = self.floor_coords[1] + self.psu_backend.psu_y_coords[0]
			y4 = self.floor_coords[1] + self.psu_backend.psu_y_coords[1]
		
		# draw main outline
		points = [(0, y1), (w, y1), (w, y2), (0, y2), (0, y1)]
		block.add_lwpolyline(points,dxfattribs={'color': color})
			
		points = [(0, y3), (w, y3), (w, y4), (0, y4), (0, y3)]
		block.add_lwpolyline(points,dxfattribs={'color': color})

		block.add_text("A").set_pos((w/2, ((y1+y2)/2)+self.breadth/4), align='MIDDLE_CENTER')
		block.add_text("P").set_pos((w/2, ((y1+y2)/2)-self.breadth/4), align='MIDDLE_CENTER')

		return f'Adjustment_Panel_{count}'