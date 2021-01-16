import aircraft_data

def draw_ohsc_layout(self, canvas, canvas_type, datum, side):

	for bin in self.layout[side]:
	
		frames, frame_stations = aircraft_data.get_frame_stations(self.aircraft_type)
		
		start = frame_stations[frames.index(bin[2])]
		end = frame_stations[frames.index(bin[3])]
		
		#start rectangle from top left, go clockwise
		x = [start, end, end, start, start]
		if side == 'LHS':
			y = [-25, -25, -65, -65, -25] 
		else:
			y = [65, 65, 25, 25, 65] 
		line, = canvas.plot(x,y, color='black', linewidth=1)

class OHSC_Drawing():

	def __init__(self, ohsc_backend, canvas_type, top_canvas=None, lhs_canvas=None, rhs_canvas=None, dxf=None):

		self.ohsc_backend = ohsc_backend
		self.mainapp = ohsc_backend.mainapp

		self.canvas_type = canvas_type
		self.top_canvas = top_canvas
		self.lhs_canvas = lhs_canvas
		self.rhs_canvas = rhs_canvas

		self.dxf=dxf

		self.frames, self.frame_stations = aircraft_data.get_frame_stations(self.ohsc_backend.aircraft_type)

		self.draw_bins()

	def draw_bins(self):


		if self.dxf:
			for side in ['LHS', 'RHS']:
				for bin in self.ohsc_backend.layout[side]:
					start = self.frame_stations[self.frames.index(bin[2])]
					end = self.frame_stations[self.frames.index(bin[3])]
					
					#start rectangle from top left, go clockwise
					x = [start, end, end, start, start]
					if side == 'LHS':

						if bin[2] == '20' and bin[3] == '21':
							y = [-25, -25, -65, -50, -25]
						else:
							y = [-25, -25, -65, -65, -25] 
					else:

						if bin[2] == '20' and bin[3] == '21':
							y = [50, 65, 25, 25, 50] 
						else:
							y = [65, 65, 25, 25, 65] 

					points = []
					for index, v in enumerate(x):
						points.append((v, y[index]))
					self.top_canvas.add_lwpolyline(points)

					#line, = canvas.plot(x,y, color='black', linewidth=1)