import numpy as np
import seats_draw
import windbreaker_draw
import lav_draw
import galley_draw
import aircraft_models
import LOPA_backend as lopa_bk

import lopa_frontend_tk
import lopa_draw
import ezdxf


def draw_aircraft(self, canvas, canvas_type, datum):

	if self.aircraft_type in ['A320', 'A319']:
		aircraft_models.draw_a320_family_model(self, canvas, canvas_type, datum)
	elif self.aircraft_type in ['B737-800']:
		aircraft_models.draw_b737_family_model(self, canvas, canvas_type, datum)

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
	#lopa_draw_redo.draw_lopa(self, canvas, canvas_type, datum, True)


	go_to = self.backend.mainapp.frames[self.backend.go_to_eel].backend
	lopa = self.backend.mainapp.frames[go_to.lopa].backend

	# Aircraft Block
	ac_block = dxf.blocks.new(name='aircaft model')
	draw_aircraft(self.backend, ac_block, 'dxf', [0,0])
	modelspace.add_blockref('aircaft model', (0, 0))

	# Add LOPA
	lopa_model = lopa_draw.LOPA_Drawing(lopa, 'dxf', modelspace, modelspace, modelspace, dxf)
	lopa_model.draw_all(eel=True)

	eel_drawing = EEL_Drawing(lopa, self.backend, 'dxf', modelspace, modelspace, modelspace, dxf)

	dxf.saveas(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.16\eel.dxf')


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

		self.dxf=dxf

		self.radius = 20

		self.unknown_locations = 0

		self.setup_location_coords()
		self.create_location_blocks()

	def setup_location_coords(self):

		lhs=-100
		rhs=100

		self.loc_coords={'Lav A CAS': [150, lhs, 278, -30],
						'Lav D CAS': [1270, lhs, 1243, -30],
						'Lav D Bulkhead': [1190, lhs, 1205, -30],
						'Lav E CAS': [1270, rhs, 1243, 30],
						'Lav E Bulkhead': [1190, rhs, 1205, 30],
						}

	def create_location_blocks(self):

		for loc in self.eel_backend.layout:

			block_name = f'Location Block {loc}'
			block = self.dxf.blocks.new(name=block_name)

			no_parts = len(self.eel_backend.layout[loc])

			y = 5

			for part in self.eel_backend.layout[loc]:

				qty = f'x{int(part[3])}'

				block.add_circle((0, y), self.radius, dxfattribs={'color': 4})
				block.add_text(qty, dxfattribs={'height': 12}).set_pos((0, y - (self.radius*0.5)), align='MIDDLE_CENTER')

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

				x2 = self.loc_coords[loc][2]
				y2 = self.loc_coords[loc][3]

				leader_y = self.loc_coords[loc][1] - self.radius

				if leader_y < 0:
					leader_y = leader_y-5
				else:
					leader_y = leader_y+5

				l = self.top_canvas.add_leader(((x2, y2), (x,leader_y)), 
						override={'dimtsz': 0, 'dimblk': "OPEN_30", 'dimasz': 0.2})

