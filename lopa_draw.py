import numpy as np
import seats_draw
import windbreaker_draw
import lav_draw
import galley_draw
import aircraft_models
import Default_AC_Models
import LOPA_backend as lopa_bk

import lopa_frontend_tk
import ezdxf

def draw_lopa(self, canvas, canvas_type, datum, draw_top_down):
	
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
		# # ______ Windbreakers _____________
		for w in self.backend.windbreakers:

			wb = self.mainapp.frames[w[1]]
			station = float(w[2])
			canvas = self.backend.ax2
			side = wb.backend.side
			if side == 'LHS':
				f = -1
			else:
				f = 1
			datum = [station, float(wb.backend.dist_from_cl)*f]
			windbreaker_draw.windbreaker_top_down_view(canvas, canvas_type, datum, wb.backend)
		
			# if 'Lav' in m[2]:
				# lav = self.mainapp.frames[m[1]]
				# station = float(m[3])
				# canvas = self.backend.ax2
				# side = lav.backend.side
				# if side == 'LHS':
					# f = -1
				# else:
					# f = 1
				# datum = [station, float(lav.backend.dist_from_cl)*f]
				# #windbreaker_draw.windbreaker_top_down_view(canvas, canvas_type, datum, lav.backend)
				# lav_draw.draw_lav_top_down(lav.backend, canvas, canvas_type, datum)
		self.canvas.draw()
def draw_aircraft(self, canvas, canvas_type, datum, dxf=None):

	if self.aircraft_type in ['A320', 'A319']:
		aircraft_models.draw_a320_family_model(self, canvas, canvas_type, datum, dxf)
	elif self.aircraft_type in ['B737-800']:
		aircraft_models.draw_b737_family_model(self, canvas, canvas_type, datum, dxf)

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
		y = [datum[1], datum[1]]
	
	if self.aircraft_type == 'B737-800':
		x = [130.0+offset, 1124.65 +232+offset]
		y = [-160, -160]
	
	if canvas_type == 'dxf':
		canvas.add_line((x[0], y[0]), (x[1], y[1]))
		
	if canvas_type == 'matplotlib':
		line, = canvas.plot(x,[0.0, 0.0], color='black', linewidth=1)

def draw_seats_top_down(self, canvas, canvas_type, datum, side):

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

def draw_windbreakers_top_down(self, canvas, canvas_type, datum,):

	for wb in self.windbreakers:
		
		c = self.mainapp.frames[wb[0]].backend
		
		x = float(wb[1])
		if c.side == 'LHS':
			y = float(c.dist_from_cl)*-1
		else:
			y = float(c.dist_from_cl)
		m_datum = [x,y]

		windbreaker_draw.windbreaker_top_down_view(canvas, canvas_type, m_datum, c)

def draw_windbreakers_side(self, canvas, canvas_type, datum):

	for wb in self.windbreakers:
		
		c = self.mainapp.frames[wb[0]].backend
		x = float(wb[1])
		if c.side == 'LHS':
			side_canvas = canvas[1]
			
			if canvas_type == 'dxf':
				y = datum[3]
			else:
				y = 0
		else:
			side_canvas = canvas[0]

			if canvas_type == 'dxf':
				y = datum[1]
			else:
				y = 0
				
		m_datum = [x,y]

		windbreaker_draw.windbreaker_side_view(side_canvas, canvas_type, m_datum, c)
		
		
def draw_lavs_top_down(lopa_bk, canvas, canvas_type, datum,dxf=None):

	for lav in lopa_bk.lavs:
		
		if lav[1] == 'Yes':

			if canvas_type == 'dxf':
				block = dxf.blocks.new(name=lav[0])

				lav_draw.draw_lav_top_down(lopa_bk, lav, block, canvas_type, datum)
			
			else:
				lav_draw.draw_lav_top_down(lopa_bk, lav, canvas, canvas_type, datum)

def draw_lavs_side(lopa_bk, canvas, canvas_type, datum):

	for lav in lopa_bk.lavs:
		
		if lav[1] == 'Yes':
			
			if canvas_type == 'dxf':
				if lopa_bk.aircraft_type in ['A320', 'A319']:
					if lav[0] in ['Lav A', 'Lav D']: 
						m_datum = [0, datum[3]]
					else:
						m_datum = [0, datum[1]]
			else:
				m_datum = [0,0]
			lav_draw.draw_lav_side(lopa_bk, lav, canvas, canvas_type, m_datum)

def draw_galleys_top_down(lopa_bk, canvas, canvas_type, datum,):

	for galley in lopa_bk.galleys:
	
		if galley[1] == 'Yes':
			
			galley_draw.draw_galley_top_down(lopa_bk, galley, canvas, canvas_type, datum)

def draw_galleys_side(lopa_bk, canvas, canvas_type, datum,):

	for galley in lopa_bk.galleys:
		
		if galley[1] == 'Yes':

			galley_draw.draw_galley_side(lopa_bk, galley, canvas, canvas_type, datum)
			
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
	#draw_aircraft(self.backend, ac_block, 'dxf', [0,0], dxf)
	#modelspace.add_blockref('aircaft model', (0, 0))
	modelspace.add_blockref('aircaft model', (0, 0))

	if self.backend.aircraft_type == 'A320':
		ac_model = Default_AC_Models.A320_Family_Model('A320', canvas_type, ac_block, ac_block, ac_block, dxf)

	ac_model.draw_all()	

	lopa_model = LOPA_Drawing(self.backend, 'dxf', modelspace, modelspace, modelspace, dxf)
	lopa_model.draw_all()
	# add_seats_to_dxf(self, dxf, modelspace, True, True)
	
	# # Add floor
	# draw_floor(self.backend, modelspace, 'dxf', [0,-180-0.12])
	# draw_floor(self.backend, modelspace, 'dxf', [0,130+0.12])
	
	# # Monuments
	# draw_windbreakers_top_down(self.backend, modelspace, 'dxf', [0,0])
	# draw_windbreakers_side(self.backend, [modelspace, modelspace], 'dxf', [0, 130+0.12, 0, -180-0.12])
	
	# draw_lavs_top_down(self.backend, modelspace, 'dxf', [0,0], dxf)
	# draw_lavs_side(self.backend, [modelspace, modelspace], 'dxf', [0, 130+0.12, 0, -180-0.12])

	# draw_galleys_top_down(self.backend, modelspace, 'dxf', [0,0])
	# draw_galleys_side(self.backend, [modelspace, modelspace], 'dxf', [0, 130+0.12, 0, -180-0.12])
		
	# Insert Stations for seats
	stations, pitches = lopa_bk.process_seat_stations_for_drawing(self.backend.seat_layout)
	
	if pitches['RHS'] != pitches['LHS']:
		sides = ['LHS', 'RHS']
	else:
		sides = ['LHS']
		
	for side in sides:

		if side == 'LHS':
			y = -210
		else:
			y = 100
		for s in stations[side]:
			modelspace.add_text(s, dxfattribs={'rotation': 90, 'height': 5.35}).set_pos((float(s), y),align='CENTER')
			
		for p in pitches[side]:

			dim = modelspace.add_linear_dim(base=(p[3], y+10), p1=(p[2], y), p2=(p[3], y), text=p[1])
					 #override={'dimtxt': p[1],})
			dim.render()
			#modelspace.add_text(p[1], dxfattribs={'height': 5.35}).set_pos((p[0], y),align='CENTER')
	dxf.saveas(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.19\lopa.dxf')
	
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
			
			y = lopa_frontend_tk.get_seat_y_datum(station, self.backend.aircraft_type, side)
			modelspace.add_blockref(row[1], (station, y))


class LOPA_Drawing():

	def __init__(self, lopa_backend, canvas_type, top_canvas=None, lhs_canvas=None, rhs_canvas=None, dxf=None):

		self.lopa_backend = lopa_backend
		self.seat_layout = lopa_backend.seat_layout
		self.mainapp = lopa_backend.mainapp

		self.canvas_type = canvas_type
		self.top_canvas = top_canvas
		self.lhs_canvas = lhs_canvas
		self.rhs_canvas = rhs_canvas

		self.seat_blocks = {}
		self.lav_blocks = {}
		self.galley_blocks = {}
		self.wb_blocks = {}

		self.dxf=dxf


		if self.canvas_type == 'dxf':
			self.floor_coords = [-180, 130] #lhs, rhs
		else:
			self.floor_coords = [0, 0]

	def draw_all(self, psu=False, eel=False):

		if not psu and not eel:
			self.draw_top_down_view()

		if not eel:
			self.draw_side_view()

		if not eel:
			self.draw_lavs_side()
			
		self.draw_lavs_top()
		self.draw_galleys_top()

		if not eel:
			self.draw_galleys_side()
			self.draw_wb_side()

		self.draw_wb_top()

		if self.canvas_type == 'dxf':
			self.add_seat_blocks()
			self.add_lav_blocks()
			self.add_galley_blocks()
			self.add_wb_blocks()

	def draw_top_down_view(self):

		if self.top_canvas != None:

			for side in ['LHS', 'RHS']:
				for row in self.seat_layout[side]:
					
					if self.lopa_backend.aircraft_type in ['A320', 'A319']:
						if side == 'LHS':
							y_datum = -30.12
						else:
							y_datum = 30.12
					#get the seat
					seat = self.mainapp.frames[row[1]].backend					

					#if canvas_type == 'matplotlib':
					#	canvas = self.ax2
					if '(' in str(row[3]):
						station = float(str(row[3]).split('(')[-1].replace(')', ''))
					else:
						station = float(row[3])

					if row[1] not in self.seat_blocks.keys() and self.canvas_type == 'dxf':

						canvas = self.seat_blocks[row[1]] = self.dxf.blocks.new(name=f'Seat_{row[1]}')

					if self.canvas_type == 'dxf':
						seats_draw.triple_economy_top_down(seat, self.seat_blocks[row[1]], self.canvas_type, [0, 0])

					elif self.canvas_type == 'matplotlib':

						seats_draw.triple_economy_top_down(seat, self.top_canvas, self.canvas_type, [station, y_datum])

	def draw_side_view(self):

			side_canvas_s = {'LHS': self.lhs_canvas, 'RHS': self.rhs_canvas}

			for side in ['LHS', 'RHS']:

				if side_canvas_s[side] != None:
					for row in self.seat_layout[side]:
						
						if self.lopa_backend.aircraft_type in ['A320', 'A319']:
							if self.lhs_canvas == self.rhs_canvas:
								if side == 'LHS':
									y_datum = -150
								else:
									y_datum = 100
							else:
								y_datum = 0

						#get the seat
						seat = self.mainapp.frames[row[1]].backend						

						#if canvas_type == 'matplotlib':
						#	canvas = self.ax2
						if '(' in str(row[3]):
							station = float(str(row[3]).split('(')[-1].replace(')', ''))
						else:
							station = float(row[3])
						side_datum = [station, y_datum]


					if row[1] not in self.seat_blocks.keys() and self.canvas_type == 'dxf':

						canvas = self.seat_blocks[row[1]] = self.dxf.blocks.new(name=f'Seat_{row[1]}')

					if self.canvas_type == 'dxf':
						seats_draw.economy_seat_generic_side_view(seat, self.seat_blocks[row[1]], self.canvas_type, [0, y_datum])

					elif self.canvas_type == 'matplotlib':

						seats_draw.economy_seat_generic_side_view(seat, canvas, self.canvas_type, side_datum)

	def add_seat_blocks(self):

		side_canvas_s = {'LHS': self.lhs_canvas, 'RHS': self.rhs_canvas}

		for side in ['LHS', 'RHS']:

			if self.lopa_backend.aircraft_type in ['A320', 'A319']:
				if side == 'LHS':
					y_datum = -30.12
				else:
					y_datum = 30.12

			if side_canvas_s[side] != None:
				for row in self.seat_layout[side]:
					station = float(row[3])

					side_canvas_s[side].add_blockref(f'Seat_{row[1]}', (station, y_datum))

	def draw_lavs_top(self):

		for lav in self.lopa_backend.lavs:
			if lav[1] == 'Yes':

				if lav[0] in ['Lav A', 'Lav D']:
					canvas = self.lhs_canvas
				else:
					canvas = self.rhs_canvas

				if canvas != None:
					if self.canvas_type == 'dxf':

						if lav[0] not in self.lav_blocks:
								canvas = self.lav_blocks[lav[0]] = self.dxf.blocks.new(name=lav[0])
						else:
								canvas = self.lav_blocks[lav[0]]

					if self.lopa_backend.aircraft_type in ['A320', 'A319']:
						if lav[0] in ['Lav A', 'Lav D']: 
							m_datum = [0, 0]
						else:
							m_datum = [0, 0]
					else:
						m_datum = [0,0]


					lav_draw.draw_lav_top_down(self.lopa_backend, lav, canvas, self.canvas_type, m_datum)

	def draw_lavs_side(self):

		for lav in self.lopa_backend.lavs:
			if lav[1] == 'Yes':

				if lav[0] in ['Lav A', 'Lav D']:
					canvas = self.lhs_canvas
				else:
					canvas = self.rhs_canvas

				if canvas != None:
					if self.canvas_type == 'dxf':

						if lav[0] not in self.lav_blocks:
								canvas = self.lav_blocks[lav[0]] = self.dxf.blocks.new(name=lav[0])
						else:
								canvas = self.lav_blocks[lav[0]]

					if self.lopa_backend.aircraft_type in ['A320', 'A319']:
						if lav[0] in ['Lav A', 'Lav D']: 
							m_datum = [0, self.floor_coords[0]]
						else:
							m_datum = [0, self.floor_coords[1]]
					else:
						m_datum = [0,0]


					lav_draw.draw_lav_side(self.lopa_backend, lav, canvas, self.canvas_type, m_datum)

	def add_lav_blocks(self):

		for lav in self.lopa_backend.lavs:

			if lav[0] in self.lav_blocks:
				sta = self.lopa_backend.lav_coords[self.lopa_backend.aircraft_type][lav[0]]

				self.top_canvas.add_blockref(lav[0], (sta, 0))

	def draw_galleys_top(self):
		for galley in self.lopa_backend.galleys:
			if galley[1] == 'Yes':

				if self.top_canvas != None:
					if self.canvas_type == 'dxf':

						if galley[0] not in self.galley_blocks:
								canvas = self.galley_blocks[galley[0]] = self.dxf.blocks.new(name=galley[0])
						else:
								canvas = self.galley_blocks[galley[0]]
					else:
						canvas = self.top_canvas

					m_datum = [0,0]

					galley_draw.draw_galley_top_down(self.lopa_backend, galley, canvas, self.canvas_type, m_datum)

	def draw_galleys_side(self):

		for galley in self.lopa_backend.galleys:
			if galley[1] == 'Yes':

				if galley[0] in ['Galley 1']:
					canvas = self.rhs_canvas
				else:
					canvas = self.lhs_canvas

				if canvas != None:
					if self.canvas_type == 'dxf':

						if galley[0] not in self.galley_blocks:
								canvas = self.galley_blocks[galley[0]] = self.dxf.blocks.new(name=galley[0])
						else:
								canvas = self.galley_blocks[galley[0]]

						if galley[0] in ['Galley 1']:
							m_datum = [0,self.floor_coords[1]]
						else:
							m_datum = [0, self.floor_coords[0]]
					else:
						m_datum = [0,0]

					galley_draw.draw_galley_side(self.lopa_backend, galley, canvas, self.canvas_type, m_datum)

					if galley[0] == 'Galley 5' and self.canvas_type == 'dxf':	
						galley_draw.draw_galley_side(self.lopa_backend, galley, canvas, self.canvas_type, [0, self.floor_coords[1]])

	def add_galley_blocks(self):

		for galley in self.lopa_backend.galleys:

			if galley[0] in self.galley_blocks:
				sta = self.lopa_backend.galley_coords[self.lopa_backend.aircraft_type][galley[0]]

				self.top_canvas.add_blockref(galley[0], (sta, 0))

	def draw_wb_side(self):

		for wb in self.lopa_backend.windbreakers:

			wb_bknd = self.mainapp.frames[wb[0]].backend
			side = wb_bknd.side

			if side == 'LHS':
				canvas = self.lhs_canvas
			else:
				canvas = self.rhs_canvas

			if canvas != None:
				if self.canvas_type == 'dxf':

					if wb[0] not in self.wb_blocks:
							canvas = self.wb_blocks[wb[0]] = self.dxf.blocks.new(name=wb[0])
					else:
							canvas = self.wb_blocks[wb[0]]

					if side == 'LHS':
						m_datum = [0,self.floor_coords[0]]
					else:
						m_datum = [0, self.floor_coords[1]]
				else:
					m_datum = [0,0]

				windbreaker_draw.windbreaker_side_view(canvas, self.canvas_type, m_datum, wb_bknd)

	def draw_wb_top(self):
		for wb in self.lopa_backend.windbreakers:
			wb_bknd = self.mainapp.frames[wb[0]].backend

			if self.top_canvas != None:
				if self.canvas_type == 'dxf':

					if wb[0] not in self.wb_blocks:
							canvas = self.wb_blocks[wb[0]] = self.dxf.blocks.new(name=wb[0])
					else:
							canvas = self.wb_blocks[wb[0]]
				else:
					canvas = self.top_canvas

				if wb_bknd.side == 'LHS':
					m_datum = [0,float(wb_bknd.dist_from_cl)*-1]
				else:
					m_datum = [0,float(wb_bknd.dist_from_cl)]

				windbreaker_draw.windbreaker_top_down_view(canvas, self.canvas_type, m_datum, wb_bknd)

	def add_wb_blocks(self):

		for wb in self.lopa_backend.windbreakers:

			if wb[0] in self.wb_blocks:
				sta = float(wb[1])

				self.top_canvas.add_blockref(wb[0], (sta, 0))