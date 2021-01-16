import numpy as np
import seats_draw
import windbreaker_draw
import lav_draw
import galley_draw
import aircraft_models
import LOPA_backend as lopa_bk

import lopa_frontend_tk
import lopa_draw
import ohsc_draw
import Default_AC_Models
import ezdxf


def draw_aircraft(self, canvas, canvas_type, datum, dxf=None):

	if self.aircraft_type in ['A320', 'A319']:
		aircraft_models.draw_a320_family_model(self, canvas, canvas_type, datum, dxf)
	elif self.aircraft_type in ['B737-800']:
		aircraft_models.draw_b737_family_model(self, canvas, canvas_type, datum, dxf)

def gen_dxf(self, file):
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
	#lopa_draw_redo.draw_lopa(self, canvas, canvas_type, datum, True)


	go_to = self.backend.mainapp.frames[self.backend.go_to_eel].backend
	lopa = self.backend.mainapp.frames[go_to.lopa].backend
	ohsc = self.backend.mainapp.frames[go_to.ohsc].backend

	# Aircraft Block
	#ac_block = dxf.blocks.new(name='aircaft model')
	#draw_aircraft(self.backend, ac_block, 'dxf', [0,0], dxf)
	#modelspace.add_blockref('aircaft model', (0, 0))

	ac_block = dxf.blocks.new(name='aircaft model')

	if self.backend.aircraft_type == 'A320':
		ac_model = Default_AC_Models.A320_Family_Model('A320', canvas_type, ac_block, ac_block, ac_block, dxf)

	ac_model.draw_eel_items()

	modelspace.add_blockref('aircaft model', (0, 0))

	# Add LOPA
	lopa_model = lopa_draw.LOPA_Drawing(lopa, 'dxf', modelspace, modelspace, modelspace, dxf)
	lopa_model.draw_all(eel=True)

	eel_drawing = EEL_Drawing(lopa, self.backend, 'dxf', modelspace, modelspace, modelspace, dxf)

	# add OHSC
	ohsc_block = dxf.blocks.new(name='OHSC Block')
	ohsc_model = ohsc_draw.OHSC_Drawing(ohsc, 'dxf', ohsc_block, ohsc_block, ohsc_block, dxf)
	modelspace.add_blockref('OHSC Block', (0, 0))

	dxf.saveas(file)


class EEL_Drawing():

	def __init__(self, lopa_backend, eel_backend, canvas_type, top_canvas=None, lhs_canvas=None, rhs_canvas=None, dxf=None):

		self.lopa_backend = lopa_backend
		self.eel_backend = eel_backend
		self.seat_layout = lopa_backend.seat_layout
		self.mainapp = lopa_backend.mainapp

		self.canvas_type = canvas_type
		self.top_canvas = top_canvas
		self.lhs_canvas = lhs_canvas
		self.rhs_canvas = rhs_canvas

		self.location_blocks = {}
		self.unknown_locations = []

		self.dxf=dxf

		self.radius = 20

		self.setup_location_coords()
		self.create_location_blocks()
		self.add_unknown_locations()

	def setup_location_coords(self):

		lhs=-100
		rhs=100

		self.loc_coords={'Cockpit': [100, rhs, 200, 0],
						'Each Seat': [715, 0, 0, 0],
						'Galley 1': [210, rhs, 260, 30],
						'Galley 5': [1430, 0.1, 1300, 0],
						'Lav A CAS': [150, lhs, 278, -30],
						'Lav A Bulkhead': [220, lhs, 278, -62],
						'Lav D CAS': [1365, lhs, 1243, -30],
						'Lav D Bulkhead': [1310, lhs, 1205, -30],
						'Lav D Doghouse': [1260, lhs, 1203, -20],
						'Lav E CAS': [1365, rhs, 1243, 30],
						'Lav E Bulkhead': [1310, rhs, 1205, 30],
						'Lav E Doghouse': [1260, rhs, 1203, 20],
		                "OHSC LHS 20 - 21": [293, lhs, 319, -40],
		                "OHSC LHS 21 - 26": [350, lhs, 370, -40],
		                "OHSC LHS 26 - 30": [425, lhs, 455, -40],
		                "OHSC LHS 30 - 35": [509, lhs, 553,-40],
		                "OHSC LHS 35 - 36": [590, lhs, 605, -40],
		                "OHSC LHS 36 - OW_FWD": [636, lhs, 650, -40],
		                "OHSC LHS 43 - 51": [830, lhs, 845, -40],
		                "OHSC LHS 51 - 55": [950, lhs, 965, -40],
		                "OHSC LHS 55 - 59": [1030, lhs, 1050, -40],
		                "OHSC LHS 59 - 63": [1100, lhs, 1134, -40],
		                "OHSC LHS 63 - 64": [1156, lhs, 1187, -40],
		                "OHSC LHS 64 - Lav D": [1210, lhs, 1200, -40],
		                "OHSC LHS OW_AFT - 43": [736, lhs, 717, -40],
		                "OHSC LHS OW_FWD - OW_AFT": [685, lhs, 685, -40],
						}

		#add rhs OHSC
		rhs_ohscs = {}
		for l in self.loc_coords:
			if 'OHSC LHS' in l:
				if 'Lav D' in l:
					new_l = l.replace('Lav D', 'Lav E')
				else:
					new_l = l
				rhs_ohscs[new_l.replace('OHSC LHS', 'OHSC RHS')] = [self.loc_coords[l][0], rhs, self.loc_coords[l][2], 40]

				

		for o in rhs_ohscs:
			self.loc_coords[o] = rhs_ohscs[o]


	def create_location_blocks(self):

		for loc in self.eel_backend.layout:

			block_name = f'Location Block {loc}'
			block = self.dxf.blocks.new(name=block_name)

			qtys = self.eel_backend.combine_existing_new_items(loc)

			no_parts = len(qtys)

			y = 5

			for part in qtys:

				qty = f'x{int(qtys[part])}'

				block.add_circle((0, y), self.radius, dxfattribs={'color': 4})
				block.add_text(qty, dxfattribs={'height': 12}).set_pos((0, y - (self.radius*0.5)), align='MIDDLE_CENTER')

				item_no = self.eel_backend.get_part_item_number(part)
				block.add_text(item_no, dxfattribs={'height': 12}).set_pos((0, y + (self.radius*0.5)), align='MIDDLE_CENTER')

				points = [(self.radius*-1, y), (self.radius, y)]
				block.add_lwpolyline(points)

				y += (self.radius*2) + 5

			if loc in self.loc_coords:

				x = self.loc_coords[loc][0]

				if self.loc_coords[loc][1] < 0: #LHS
					y = self.loc_coords[loc][1] -y
				else:
					y = self.loc_coords[loc][1]

				self.top_canvas.add_blockref(block_name, (x, y))

				if loc not in ['Each Seat']:
					x2 = self.loc_coords[loc][2]
					y2 = self.loc_coords[loc][3]

					leader_y = self.loc_coords[loc][1] - self.radius

					if leader_y < 0:
						leader_y = leader_y-5
					else:
						leader_y = leader_y+5

					l = self.top_canvas.add_leader(((x2, y2), (x,leader_y)), 
							override={'dimtsz': 0, 'dimblk': "OPEN_30", 'dimasz': 0.2})

			else:
				self.unknown_locations.append(block_name)
			#add text for name of location

			if loc in self.loc_coords:
				if self.loc_coords[loc][1] < 0:
					y = -25
					align = 'MIDDLE_RIGHT'
				else:
					#y = y - 10
					y = len(self.eel_backend.layout[loc])*((self.radius*2) + 5)
					align = 'MIDDLE_LEFT'
			else:
				y = -20
				align='MIDDLE_RIGHT'
			
			if loc in ['Each Seat']:
				rot = 0
				x = self.radius + 2
				y = 0
			else:
				rot=90		
				x = 0
			block.add_text(loc, dxfattribs={'height': 8, 'rotation': rot}).set_pos((x, y), align=align)

	def add_unknown_locations(self):

		x = 1600
		y = 0

		self.top_canvas.add_text('Unknown Locations', dxfattribs={'height': 14,}).set_pos((x, -80), align='MIDDLE_CENTER')
		for l in self.unknown_locations:

			self.top_canvas.add_blockref(l, (x, y))

			x += 50
