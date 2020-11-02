import ezdxf

from Pycabin_Backend import lopa_draw_redo

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
	
	colors = {'Oxygen Box': 'blue', 'Gasper': 'black', '11" PSIU': 'green', '8" PSIU': 'red', 'Partition Panel': 'cyan',
				'Clamping Panel': 'purple', 'Adjustment Panel': 'brown'}
	widths = {'Oxygen Box': 12, 'Gasper': 3, '11" PSIU': 11, '8" PSIU': 8, 'Partition Panel': 2, 
				'Clamping Panel': 2, 'Adjustment Panel': 4}
	
	
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
	datum = [[],[0,0],[]]

	ac_block = dxf.blocks.new(name='aircaft model')
	lopa_draw_redo.draw_aircraft(self.backend, ac_block, 'dxf', [0,0])
	modelspace.add_blockref('aircaft model', (0, 0))
	
	lopa = self.mainapp.frames[self.backend.lopa]
	lopa_draw_redo.add_seats_to_dxf(lopa, dxf, modelspace, False, True)	
	
	psu_blocks = setup_psu_blocks(self, dxf)
	
	add_psu_blocks(self, modelspace, psu_blocks)
	
	#modelspace.add_blockref('1 Filler Panel', (0, 0))
	
	dxf.saveas(r'C:\Python37\Lib\site-packages\Pycabin_Frontend_Tkinter\psu.dxf')
	
	
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
		
		
	