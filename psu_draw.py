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

def draw_psu_rail_top_down(self, canvas, canvas_type, datum):

	x_both, lav_d, lav_e, wb_installed = self.get_psu_rail_start_end()
	
	for side in ['LHS', 'RHS']:
		if side == 'LHS':
			x = x_both[0]
			y1= [-40, -40]
			y2= [-30, -30]
		else:
			x= x_both[1]
			y1= [40, 40]
			y2= [30, 30]			
		
		if canvas_type == 'dxf':
			canvas.add_line((x[0], y1[0]), (x[1], y1[1]))
			canvas.add_line((x[0], y2[0]), (x[1], y2[1]))
			
		if canvas_type == 'matplotlib':
			line, = canvas.plot(x,y1, color='black', linewidth=1)
			line, = canvas.plot(x,y2, color='black', linewidth=1)

def draw_psu_layout(self, canvas, canvas_type, datum, side, mode='all', view='side'):
	
	#get row numbers and stations

	lopa_bk = self.mainapp.frames[self.lopa].backend

	row_numbers = lopa_bk.get_all_row_numbers()
	row_stations = lopa_bk.get_all_row_stations()

	colors = {'Oxygen Box LHS': 'blue', 'Oxygen Box RHS': 'blue', 'Gasper': 'black', '11" PSIU': 'green', '8" PSIU': 'red', 'Partition Panel': 'cyan',
				'Clamping Panel': 'purple', 'Adjustment Panel': 'brown'}
	widths = {'Oxygen Box LHS': 12, 'Oxygen Box RHS': 12, 'Gasper': 3, '11" PSIU': 11, '8" PSIU': 8, 'Partition Panel LHS': 2, 'Partition Panel RHS': 2, 
				'Clamping Panel': 2, 'Adjustment Panel LHS': 4, 'Adjustment Panel RHS': 4}
	
	gasper_stations = []

	if mode == 'gasper':
		parts_to_draw = ['Gasper']
	elif mode == 'psiu':
		parts_to_draw = ['11" PSIU', '8" PSIU', '6" PSIU']
		
	
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

		if view == 'side':
			y_coords = [70, 70, 75, 75, 70]
		else:
			if side=='LHS':
				y_coords = [-40, -40, -30, -30, -40]
			else:
				y_coords = [40, 40, 30, 30, 40]

		
		draw_part = True

		if mode != 'all':
			if part[1] not in parts_to_draw:
				draw_part = False

		if draw_part:
			canvas.fill(x_coords, y_coords, color=color, linewidth=1)
			
			if 'Oxygen Box' in part[1]:
				
				canvas.plot([x+(w/2),x+(w/2)], [70, 50], color=color, linewidth=2) 

		if part[1] == 'Gasper':
			gasper_stations.append(x)

	# gasper vents
	if mode == 'gasper':
		vents = [[], []]		
		for index, vent in enumerate(self.gasper_layout[side]):

			vents[0].append(float(vent[2]))

			if side == 'LHS':
				vents[1].append(-90)
				y = -90
				y2 = -40
			elif side == 'RHS':
				vents[1].append(90)
				y = 90
				y2= 40

			if vent[0] != 'N/A':
				if int(vent[0]) in row_numbers[side]:
					
					sta = gasper_stations[row_numbers[side].index(int(vent[0]))]
					canvas.plot([float(vent[2]), sta ], [y, y2], color='black', alpha=0.5)
					
		canvas.scatter(vents[0], vents[1], s=25, marker='o', color='blue')

def draw_deus(self, canvas, canvas_type, datum, side, view='side'):

	deus = [[], []]
	deu_stations = {}

	psiu_stations = self.get_psiu_stations()

	psu_count = 0
	for index, deu in enumerate(self.deu_layout[side]):
		x = float(deu[2])
		deus[0].append(x)

		deu_stations[deu[0]] = x

		if view == 'top_down':
			if side == 'LHS':
				deus[1].append(-90)
			else:
				deus[1].append(90)

	if canvas_type == 'matplotlib':
		canvas.scatter(deus[0], deus[1], s=30, marker='o', color='brown')

	vccs = [[], []]
	for index, v in enumerate(self.vc_layout[side]):
		x = float(v[2])
		vccs[0].append(x)

		if view == 'top_down':
			if side == 'LHS':
				vccs[1].append(-60)
				psu_y = -40
			else:
				vccs[1].append(60)
				psu_y = 40

		#Add line from DEU to VCC
		if v[3] in deu_stations.keys():

			if canvas_type == 'matplotlib':
				canvas.plot([x, deu_stations[v[3]]], [vccs[1][0], deus[1][0]], color='black', linewidth=1, alpha=0.5)

		#Add line from vcc to PSIU
		if v[4] != 'N/A':
			canvas.plot([x, psiu_stations[side][psu_count]], [vccs[1][0], psu_y], color='black', linewidth=1, alpha=0.5)
			psu_count +=1

	if canvas_type == 'matplotlib':
		canvas.scatter(vccs[0], vccs[1], s=20, marker='o', color='blue')	

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
			
			if name in blocks.blocks:
				modelspace.add_blockref(name, (float(part[3]), 0))

			elif 'Adjustment Panel' in part[1]:

				width = float(self.backend.psu_layout[side][i+1][3]) - float(part[3])

				block = blocks.create_adjument_panel(width, side)
				modelspace.add_blockref(block, (float(part[3]), 0))

		# Add Gasper Vent/Hose

		gasper_stations = self.backend.get_gasper_stations()
		row_idx = 0
		for i, vent in enumerate(self.backend.gasper_layout[side]):

			hose = vent[3]
			if side == 'LHS':
				y = -50
			else:
				y = 50
			modelspace.add_blockref(f'Gasper Vent {side}', (float(vent[2]), y))

			row = vent[0]

			if row != 'N/A':
				if side == 'LHS':
					y = -10
					y_hose = y-7.5
					y_gasper = -30
				else:
					y = 10	
					y_hose = y+7.5	
					y_gasper= 30
				modelspace.add_blockref(f'Gasper Hose {hose}', (float(vent[2]), y))

				#add line representing hose
				points = [(float(vent[2]), (y_hose)), (gasper_stations[side][row_idx]+1.5, y_gasper)]
				modelspace.add_lwpolyline(points)
				row_idx += 1

		# Add DEU

		for side in ['LHS', 'RHS']:
			for d in self.backend.deu_layout[side]:

				if d[-1] == 'LHS':
					y = -90
					y2 = -90+12
				else:
					y = 90
					y2 = 90-12

				sta = float(d[2])
				modelspace.add_blockref(f'DEU {side}', (sta, y))
				modelspace.add_text(f"{d[0]}", dxfattribs={'rotation': 90}).set_pos((sta+3, y), align='MIDDLE_CENTER')

				#get max and min stations for associated vcc(s)
				sta_s = []
				for v in self.backend.vc_layout[side]:
					if v[3] == d[0]:
						sta_s.append(float(v[2]))

				if len(sta_s) > 0:
					points = [(min(sta_s), y2), (max(sta_s,), y2)]
					modelspace.add_lwpolyline(points,dxfattribs={'color': 50})

		# Add VCC
		psiu_stations = self.backend.get_psiu_stations()

		for side in ['LHS', 'RHS']:

			row_idx = 0
			for d in self.backend.vc_layout[side]:

				if side == 'LHS':
					y = -60
					fac=1
				else:
					y = 60
					fac=-1

				sta = float(d[2])
				modelspace.add_blockref(f'VCC {side}', (sta, y))
				modelspace.add_text(f"{d[0]}", dxfattribs={'rotation': 90}).set_pos((sta+3, y), align='MIDDLE_CENTER')

				# Add connecting lines from VCC to PSIU
				if d[-1] != 'N/A':
					psu_sta = float(psiu_stations[side][row_idx])
					row_idx += 1

					y2 = y+(15*fac)
					y3 = y+(20*fac)

					print(f'{sta}: {psu_sta}')
					#if psu_sta > sta:
						
					points = [(sta-4, y), (sta-5, y), (sta-5, y2), (psu_sta+2, y2), (psu_sta+2, y3)]

					modelspace.add_lwpolyline(points,dxfattribs={'color': 50})


	dxf.saveas(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.15\psu.dxf')
	

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

		# Create the gasper vents

		for side in ['LHS', 'RHS']:
			block = dxf.blocks.new(name=f'Gasper Vent {side}')
			self.blocks[f'Gasper Vent {side}'] = block

			if side == 'RHS':
				f = -1.0
			else:
				f = 1.0
			#go clockwise around
			points = [(0.0, 0.0*f), (1.8, 1.8*f), (2.4, 1.2*f), (1.0, -0.3*f), (-1.0, -0.3*f), (-2.4, 1.2*f), (-1.8, 1.8*f), (0.0, 0.0*f)]
			
			block.add_lwpolyline(points,dxfattribs={'color': color})

			points = [(2.5, 1.9*f), (0.3, -0.3*f)]
			block.add_lwpolyline(points,dxfattribs={'color': color})

			points = [(-2.5, 1.9*f), (-0.3, -0.3*f)]
			block.add_lwpolyline(points,dxfattribs={'color': color})

		#Create hose indicators

		for h in ['400', '250', '150']:
			block = dxf.blocks.new(name=f'Gasper Hose {h}mm')
			self.blocks[f'Gasper Hose {h}mm'] = block	

			points = [(0.0, 7.5), (7.5, 0), (0, -7.5), (-7.5, 0.0), (0.0, 7.5)]		
			block.add_lwpolyline(points,dxfattribs={'color': color})
			block.add_text(f"{h}").set_pos((0, 0), align='MIDDLE_CENTER')

		# Create DEU Block
		for side in ['LHS', 'RHS']:
			block = dxf.blocks.new(name=f'DEU {side}')
			self.blocks[f'DEU'] = block	

			points = [(0.0, 0.0), (0.0, 6.0), (-4.0, 4.0), (-4.0, -4.0), (0.0, -6.0), (0.0, 0.0)]		
			block.add_lwpolyline(points,dxfattribs={'color': 50})

			if side == 'LHS':
				points = [(-4.0, 0.0), (-5.0, 0.0), (-5.0, 12.0)]
			else:
				points = [(-4.0, 0.0), (-5.0, 0.0), (-5.0, -12.0)]

			block.add_lwpolyline(points,dxfattribs={'color': 50})

		# Create VCC Block
		for side in ['LHS', 'RHS']:
			block = dxf.blocks.new(name=f'VCC {side}')
			self.blocks[f'VCC'] = block	

			points = [(0.0, 0.0), (0.0, 6.0), (-4.0, 4.0), (-4.0, -4.0), (0.0, -6.0), (0.0, 0.0)]		
			block.add_lwpolyline(points,dxfattribs={'color': 50})

			if side == 'LHS':
				points = [(0.0, 0.0), (0.5, 0.0), (0.5, -18.0)]
			else:
				points = [(0.0, 0.0), (0.5, 0.0), (0.5, 18.0)]

			block.add_lwpolyline(points,dxfattribs={'color': 50})

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