import numpy as np
import ezdxf

def gen_aircraft_offsets():

	return {'A320': 0, 'A319': -147,
			'B737-800': 0}


def draw_a320_family_model(self, canvas, canvas_type, datum):

	if self.aircraft_type == 'A320':
		offset = 0
	elif self.aircraft_type == 'A319':
		offset = -147
		
	if self.aircraft_type == 'A320' or self.aircraft_type == 'A319':
		x=[105.4137,105.9721,110.56,117.8845,125.2459,137.8717,169.2054,223.2479,244.57,279.0,285.7,
			314.0,320.0,320.0,1156.5+offset,1156.5+offset,1207.0+offset,1242.85+offset,1250.45+offset,1278.62+offset,1322.52+offset,1322.52+offset,1322.52+offset,
			1278.62+offset,1250.45+offset,1242.85+offset,1207.0+offset,1156.5+offset,320.0,314.0,285.7,279.0,244.57,223.2479,169.2054,
			137.8717,125.2459,117.8845,110.56,105.9721,105.4137]		
		y=[0.0,-4.969999999999999,-15.129999999999995,-23.539999999999992,-29.599999999999994,-37.55000000000001,-51.08000000000001,
			-64.77000000000001,-68.0,-71.69999999999999,-72.6,-73.44,-73.6,-73.6,-73.6,-73.6,-73.30000000000001,-70.94999999999999,
			-70.08000000000001,-65.6,-53.96000000000001,0.0,53.95999999999998,65.60000000000002,70.07999999999998,70.94999999999999,
			73.30000000000001,73.60000000000002,73.60000000000002,73.44,72.60000000000002,71.69999999999999,68.0,
			64.76999999999998,51.079999999999984,37.55000000000001,
			29.600000000000023,23.54000000000002,15.129999999999995,4.969999999999999,0.0]
		
		if canvas_type == 'matplotlib':
			coords = np.array([x, y])		
			canvas.plot(x,y, color='dimgrey')
		elif canvas_type == 'dxf':
			points = []
			for index, v in enumerate(x):
				points.append((v, y[index]))
			canvas.add_lwpolyline(points)
	

					
		#Centerline
		x = [105.4137,1322.52+offset]
		y = [0.0, 0.0]
		if canvas_type == 'matplotlib':
			line, = canvas.plot(x,y, color='black', linewidth=1)
			line.set_dashes([4, 4, 4, 4])
		elif canvas_type == 'dxf':
			canvas.add_line((x[0], y[0]), (x[1]+offset, y[1]), dxfattribs={'linetype': 'CENTER'})
			
		#if canvas_type == 'matplotlib':				
	if self.aircraft_type == 'A320' or self.aircraft_type == 'A319':
		#cockpit windows
		color = 'darkcyan'
		
		x_s = [[231.6159, 208.8165, 208.4993, 231.6156, 231.6159],
				[206.6681, 176.5639, 192.2056, 206.0361, 206.6681],
				[231.6159, 208.8165, 208.4993, 231.6156, 231.6159,],
				[206.6681, 176.5639, 192.2056, 206.0361, 206.6681,],
				[175.33, 154.69, 175.33, 191, 175.33],
				[175.33, 154.69, 175.33, 191, 175.33]]
				
		y_s = [[186.75-250, 194.62-250,208.46-250,200.12-250,186.75-250],
				[195.37-250, 212.61-250, 216.94-250, 209.44-250,195.37-250],
				[313.25-250, 305.38-250, 291.54-250, 299.88-250, 313.25-250],
				[304.63-250, 287.39-250, 283.06-250, 290.56-250, 304.63-250],
				[214.55-250, 248.75-250, 248.75-250, 218.82-250, 214.55-250],
				[285.45-250, 251.25-250, 251.25-250, 281.18-250, 285.45-250]]

		for index, x in enumerate(x_s):
			y = y_s[index]
			if canvas_type == 'matplotlib':
				canvas.fill(x,y, color=color)
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
	
def draw_b737_family_model(self, canvas, canvas_type, datum):

	offset = 0
	
	#a/c outline
	list_of_points = [(130.0+offset,0),( 146.0+offset,0-16.0),( 196.17+offset,0-38.9),
				(220.2+offset,0-46.02),( 269.56+offset, 0 - 58.36),( 292.9+offset, 0 - 62.36),
				(312+offset, 0 - 65.22),( 323.92+offset,0 - 66.5),( 335.9+offset,0 - 67.54),
				(349.93+offset, 0 - 68.45),( 361.27+offset,0 - 69.48),( 1124.65 +232+offset,0 - 69.48),
				(1124.65 +232+offset,0 + 69.48),
				(1124.65 +232+offset,0 + 69.48),(361.27+offset,0 + 69.48),(349.93+offset, 0 + 68.45),
				(335.9+offset, 0 + 67.54),(323.92+offset,0 + 66.5),(312+offset, 0 + 65.22),
				(292.9+offset, 0 + 62.36),( 269.56+offset,0 + 58.36),(220.2+offset,0+46.02),
				(196.17+offset,0+38.9),( 146.0+offset,0+16.0),(130.0+offset,0),]
				
	x = []
	y = []
	
	for p in list_of_points:
		x.append(p[0])
		y.append(p[1])
		
	if canvas_type == 'matplotlib':
		coords = np.array([x, y])		
		canvas.plot(x,y, color='dimgrey')
		
	elif canvas_type == 'dxf':
		#points = []
		#for index, v in enumerate(x):
			#points.append((v, y[index]))
		canvas.add_lwpolyline(list_of_points)		
		