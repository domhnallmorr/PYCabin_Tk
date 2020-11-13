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