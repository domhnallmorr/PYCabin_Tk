import numpy as np
from Pycabin_Backend import seats_draw
from Pycabin_Backend import windbreaker_draw
from Pycabin_Backend import lav_draw
from Pycabin_Backend import aircraft_models
from Pycabin_Backend import LOPA_backend as lopa_bk

from Pycabin_Frontend_Tkinter import lopa_tk
import ezdxf

def draw_lopa(self, canvas, canvas_type, datum, draw_top_down):
	print(self.backend.aircraft_type)
	print('------------------------------------')
	if canvas_type == 'matplotlib':
		#self.backend.ax1.clear()
		self.backend.ax2.clear()
		#self.backend.ax3.clear()
	# ______ DRAW AIRCRAFT _____________
	draw_aircraft(self.backend, canvas, canvas_type, datum[1])
	
	# ______ LHS FLOOR ______________
	if self.backend.aircraft_type == 'A320':
		
		x = [105.4137,1322.52]
		y = [-160, -160]
	
	if canvas_type == 'dxf':
		canvas.add_line((x[0], y[0]), (x[1], y[1]))
		
	if canvas_type == 'matplotlib':
		line, = self.backend.ax3.plot(x,[0.0, 0.0], color='black', linewidth=1)

	# ______ RHS FLOOR ______________
	if self.backend.aircraft_type == 'A320':
		
		x = [105.4137,1322.52]
		y = [115, 115]
	
	if canvas_type == 'dxf':
		canvas.add_line((x[0], y[0]), (x[1], y[1]))
		
	if canvas_type == 'matplotlib':
		line, = self.backend.ax1.plot(x,[0.0, 0.0], color='black', linewidth=1)
		
	# ______ LHS SEATS _____________
	for row in self.backend.seat_layout['LHS']:
		
		if self.backend.aircraft_type in ['A320', 'A319']:
			y_datum = -30.12
		#get the seat
		seat = self.mainapp.frames[row[1]].backend
		
		if canvas_type == 'matplotlib':
			canvas = self.backend.ax2
		top_down_datum = [row[3], y_datum]
		seats_draw.triple_economy_top_down(seat, canvas, canvas_type, top_down_datum)

		if canvas_type == 'matplotlib':
			canvas = self.backend.ax3
			side_datum = [row[3], 0]
		else:
			side_datum = [row[3], -160]
		seats_draw.economy_seat_generic_side_view(seat, canvas, canvas_type, side_datum)

	
	# ______ RHS SEATS _____________
	for row in self.backend.seat_layout['RHS']:
		
		if self.backend.aircraft_type in ['A320', 'A319']:
			y_datum = 30.12
		#get the seat
		seat = self.mainapp.frames[row[1]].backend
		if canvas_type == 'matplotlib':
			canvas = self.backend.ax2

		top_down_datum = [row[3], y_datum]
		seats_draw.triple_economy_top_down(seat, canvas, canvas_type, top_down_datum)
		
		if canvas_type == 'matplotlib':
			canvas = self.backend.ax1
			side_datum = [row[3], 0]
		elif canvas_type == 'dxf':
			side_datum = [row[3], 115]
		seats_draw.economy_seat_generic_side_view(seat, canvas, canvas_type, side_datum)

	if canvas_type == 'matplotlib':	
		# ______ MONUMENTS _____________
		for m in self.backend.monuments:

			if 'Windbreaker' in m[2]:
				wb = self.mainapp.frames[m[1]]
				station = float(m[3])
				canvas = self.backend.ax2
				side = wb.backend.side
				if side == 'LHS':
					f = -1
				else:
					f = 1
				datum = [station, float(wb.backend.dist_from_cl)*f]
				windbreaker_draw.windbreaker_top_down_view(canvas, canvas_type, datum, wb.backend)
		
			if 'Lav' in m[2]:
				lav = self.mainapp.frames[m[1]]
				station = float(m[3])
				canvas = self.backend.ax2
				side = lav.backend.side
				if side == 'LHS':
					f = -1
				else:
					f = 1
				datum = [station, float(lav.backend.dist_from_cl)*f]
				#windbreaker_draw.windbreaker_top_down_view(canvas, canvas_type, datum, lav.backend)
				lav_draw.draw_lav_top_down(lav.backend, canvas, canvas_type, datum)
		self.canvas.draw()
def draw_aircraft(self, canvas, canvas_type, datum):

	if self.aircraft_type in ['A320', 'A319']:
		aircraft_models.draw_a320_family_model(self, canvas, canvas_type, datum)
	elif self.aircraft_type in ['B737-800']:
		aircraft_models.draw_b737_family_model(self, canvas, canvas_type, datum)

def draw_seat_tracks(self, canvas, canvas_type, datum):

	if self.aircraft_type == 'A320':
		offset = 0
	elif self.aircraft_type == 'A319':
		offset = -147
	
	if self.aircraft_type == 'A320' or self.aircraft_type == 'A319':
		#Port Inbd Seat Track
		seat_track = []
		
		x = [340,1244.5+offset]
		y = [-30.12, -30.12]
		if canvas_type == 'matplotlib':
			line, = canvas.plot(x,y, color='black', linewidth=1)
			seat_track.append(line)
		elif canvas_type == 'dxf':
			canvas.add_line((x[0], y[0]), (x[1], y[1]), dxfattribs={'linetype': 'DASHED'})

		#Port Outbrd			
		x = [340,1244.5+offset]
		y = [-50.87, -50.87]
		if canvas_type == 'matplotlib':
			line, = canvas.plot(x,y, color='black', linewidth=1)
			seat_track.append(line)
		elif canvas_type == 'dxf':
			canvas.add_line((x[0], y[0]), (x[1], y[1]), dxfattribs={'linetype': 'DASHED'})
			
		#Starboard Inbd
		x = [340,1244.5+offset]
		y = [30.12, 30.12]
		if canvas_type == 'matplotlib':
			line, = canvas.plot(x,y, color='black', linewidth=1)
			seat_track.append(line)	
		elif canvas_type == 'dxf':
			canvas.add_line((x[0], y[0]), (x[1], y[1]), dxfattribs={'linetype': 'DASHED'})
	
		#Starboard Outboard
		x = [340,1244.5+offset]
		y = [50.87, 50.87]
		if canvas_type == 'matplotlib':
			line, = canvas.plot(x,y, color='black', linewidth=1)
			seat_track.append(line)
		elif canvas_type == 'dxf':
			canvas.add_line((x[0], y[0]), (x[1], y[1]), dxfattribs={'linetype': 'DASHED'})
		
		if canvas_type == 'matplotlib':
			#make seat tracks dashed lines
			for l in seat_track:
				l.set_dashes([2, 2, 10, 2])
				
def draw_floor(self, canvas, canvas_type, datum):
	
	
	offsets = aircraft_models.gen_aircraft_offsets()
	offset = offsets[self.aircraft_type]
	
	if self.aircraft_type == 'A320' or self.aircraft_type == 'A319':
		
		x = [105.4137,1322.52+offset]
		y = [-160, -160]
	
	if self.aircraft_type == 'B737-800':
		x = [130.0+offset, 1124.65 +232+offset]
		y = [-160, -160]
	
	if canvas_type == 'dxf':
		canvas.add_line((x[0], y[0]), (x[1], y[1]))
		
	if canvas_type == 'matplotlib':
		line, = canvas.plot(x,[0.0, 0.0], color='black', linewidth=1)

def draw_seats_top_down(self, canvas, canvas_type, datum, side):

	for row in self.seat_layout[side]:
		print(row)
		#if self.aircraft_type in ['A320', 'A319']:
		#	y_datum = datum[1]
		#get the seat
		seat = self.mainapp.frames[row[1]].backend
		
		#if canvas_type == 'matplotlib':
		#	canvas = self.ax2
		if '(' in str(row[3]):
			station = float(str(row[3]).split('(')[-1].replace(')', ''))
		else:
			station = float(row[3])
		top_down_datum = [station, datum[1]]
		seats_draw.triple_economy_top_down(seat, canvas, canvas_type, top_down_datum)

def draw_seats_side(self, canvas, canvas_type, datum, side):

	for row in self.seat_layout[side]:
		#if self.aircraft_type in ['A320', 'A319']:
		#	y_datum = datum[1]
		#get the seat
		seat = self.mainapp.frames[row[1]].backend
		
		#if canvas_type == 'matplotlib':
		#	canvas = self.ax2
		if '(' in str(row[3]):
			station = float(str(row[3]).split('(')[-1].replace(')', ''))
		else:
			station = float(row[3])
			
		side_datum = [station, float(datum[1])]
		seats_draw.economy_seat_generic_side_view(seat, canvas, canvas_type, side_datum)

def draw_monuments_top_down(self, canvas, canvas_type, datum,):

	for m in self.monuments:
		
		c = self.mainapp.frames[m[1]].backend
		
		x = float(m[3])
		if c.side == 'LHS':
			y = float(c.dist_from_cl)*-1
		else:
			y = float(c.dist_from_cl)
		m_datum = [x,y]
		if 'Windbreaker' in m[2]:
			windbreaker_draw.windbreaker_top_down_view(canvas, canvas_type, m_datum, c)
		
		elif 'Lav' in m[2]:
			lav_draw.draw_lav_top_down(c, canvas, canvas_type, m_datum)

def draw_monuments_side(self, canvas_lhs, canvas_rhs, canvas_type, datum):
	canvases = {'LHS': canvas_lhs, 'RHS': canvas_rhs}
	for m in self.monuments:
		
		c = self.mainapp.frames[m[1]].backend
		x = float(m[3])
		m_datum = [x,0]
		if 'Windbreaker' in m[2]:
			windbreaker_draw.windbreaker_side_view(canvases[c.side], canvas_type, m_datum, c)		
		elif 'Lav' in m[2]:
			lav_draw.draw_lav_side(c, canvases[c.side], canvas_type, m_datum)		

			
def create_points_list(x,y):
	points = []
	for index, v in enumerate(x):
		points.append((v, y[index]))
	
	return points
	
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
	# Aircraft Block
	ac_block = dxf.blocks.new(name='aircaft model')
	draw_aircraft(self.backend, ac_block, 'dxf', [0,0])
	modelspace.add_blockref('aircaft model', (0, 0))
	
	add_seats_to_dxf(self, dxf, modelspace, True, True)
	
	# Insert Stations for seats
	stations, pitches = lopa_bk.process_seat_stations_for_drawing(self.backend.seat_layout)
	for side in ['LHS', 'RHS']:

		if side == 'LHS':
			y = -160
		else:
			y = 90
		for s in stations[side]:
			modelspace.add_text(s, dxfattribs={'rotation': 90, 'height': 5.35}).set_pos((float(s), y),align='CENTER')
			
		for p in pitches[side]:
			dim = modelspace.add_linear_dim(base=(p[3], y+10), p1=(p[2], y), p2=(p[3], y),)
					 #override={'dimtxt': p[1],})
			dim.render()
			#modelspace.add_text(p[1], dxfattribs={'height': 5.35}).set_pos((p[0], y),align='CENTER')
	dxf.saveas(r'C:\Python37\Lib\site-packages\Pycabin_Frontend_Tkinter\lopa.dxf')
	
def add_seats_to_dxf(self, dxf, modelspace, draw_top, draw_side):

	# Create Seat Blocks and insert
	seat_blocks = {}
	for side in ('LHS', 'RHS'):
		for row in self.backend.seat_layout[side]:
			station = lopa_bk.convert_station_to_float(row[3])
			
			if row[1] not in seat_blocks:
				seat_blocks[row[1]] = dxf.blocks.new(name=row[1])
				seat = self.mainapp.frames[row[1]].backend
				if draw_top:
					seats_draw.triple_economy_top_down(seat, seat_blocks[row[1]], 'dxf', [0,0])
				if side == 'LHS':
					y = -150
				else:
					y = 100
				
				if draw_side:
					seats_draw.economy_seat_generic_side_view(seat, seat_blocks[row[1]], 'dxf', [0,y])
			
			y = lopa_tk.get_seat_y_datum(station, self.backend.aircraft_type, side)
			modelspace.add_blockref(row[1], (station, y))