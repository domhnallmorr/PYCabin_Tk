import numpy as np
def convert_matplotlib_to_dxf(x, y):

	points = []
	for index, v in enumerate(x):
		points.append((v, y[index]))

	return points

def plot_x_y_coords(canvas, canvas_type, x, y, color=None):

	if canvas_type == 'matplotlib':
		if not color:
			canvas.plot(x,y)
		else:
			canvas.plot(x,y, color=color)
	elif canvas_type == 'dxf':
		canvas.add_lwpolyline(convert_matplotlib_to_dxf(x, y))

class A320_Family_Model():

	def __init__(self, aircraft_type, canvas_type, top_canvas=None, lhs_canvas=None, rhs_canvas=None):

		self.aircraft_type = aircraft_type
		self.offsets = {'A320': 0}

		self.offset = self.offsets[aircraft_type]
		self.top_canvas = top_canvas
		self.lhs_canvas = lhs_canvas
		self.rhs_canvas = rhs_canvas
		self.canvas_type = canvas_type
		
	def draw_all(self):

		if self.top_canvas != None:
			self.draw_outline()
			self.draw_windows()
			self.draw_centerline()

		if self.lhs_canvas != None:
			if self.lhs_canvas == self.top_canvas:
				y_datum = -180
			else:
				y_datum = 0

			self.draw_floor(self.lhs_canvas, y_datum)

		if self.rhs_canvas != None:
			if self.rhs_canvas == self.top_canvas:
				y_datum = 130
			else:
				y_datum = 0

			self.draw_floor(self.rhs_canvas, y_datum)

	def draw_outline(self):
		print('outline')
		x=[105.4137,105.9721,110.56,117.8845,125.2459,137.8717,169.2054,223.2479,244.57,279.0,285.7,
			314.0,320.0,320.0,1156.5+self.offset,1156.5+self.offset,1207.0+self.offset,1242.85+self.offset,1250.45+self.offset,1278.62+self.offset,1322.52+self.offset,1322.52+self.offset,1322.52+self.offset,
			1278.62+self.offset,1250.45+self.offset,1242.85+self.offset,1207.0+self.offset,1156.5+self.offset,320.0,314.0,285.7,279.0,244.57,223.2479,169.2054,
			137.8717,125.2459,117.8845,110.56,105.9721,105.4137]	

		y=[0.0,-4.969999999999999,-15.129999999999995,-23.539999999999992,-29.599999999999994,-37.55000000000001,-51.08000000000001,
			-64.77000000000001,-68.0,-71.69999999999999,-72.6,-73.44,-73.6,-73.6,-73.6,-73.6,-73.30000000000001,-70.94999999999999,
			-70.08000000000001,-65.6,-53.96000000000001,0.0,53.95999999999998,65.60000000000002,70.07999999999998,70.94999999999999,
			73.30000000000001,73.60000000000002,73.60000000000002,73.44,72.60000000000002,71.69999999999999,68.0,
			64.76999999999998,51.079999999999984,37.55000000000001,
			29.600000000000023,23.54000000000002,15.129999999999995,4.969999999999999,0.0]

		if self.canvas_type == 'matplotlib':
			coords = np.array([x, y])		
			self.top_canvas.plot(x,y, color='dimgrey')
		elif self.canvas_type == 'dxf':
			self.top_canvas.add_lwpolyline(convert_matplotlib_to_dxf(x, y))

	def draw_windows(self):

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
			if self.canvas_type == 'matplotlib':
				self.top_canvas.fill(x,y, color=color)
			elif self.canvas_type == 'dxf':
				self.top_canvas.add_lwpolyline(convert_matplotlib_to_dxf(x, y))

	def draw_centerline(self):

		#Centerline
		x = [105.4137,1322.52+self.offset]
		y = [0.0, 0.0]
		if self.canvas_type == 'matplotlib':
			line, = self.top_canvas.plot(x,y, color='black', linewidth=1)
			line.set_dashes([4, 4, 4, 4])
		elif self.canvas_type == 'dxf':
			self.top_canvas.add_line((x[0], y[0]), (x[1]+self.offset, y[1]), dxfattribs={'linetype': 'CENTER'})

	def draw_floor(self, canvas, y_datum):

		x = [105.4137,1322.52+self.offset]
		y = [y_datum, y_datum]

		plot_x_y_coords(canvas, self.canvas_type, x, y, 'black')