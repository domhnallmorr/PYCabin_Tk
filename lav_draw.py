import matplotlib.patches as patches

def draw_lav_top_down(lopa_bk, lav, canvas, canvas_type, top_down_datum):
	
	lav_color = 'green'
	# reference_side = lav.reference_side
	# breadth = float(lav.breadth)
	
	# if reference_side == 'LHS':
		# breadth = breadth*-1
	# width = float(lav.width)
	
	# x = top_down_datum[0]
	# y = top_down_datum[1]
	
	# if lav.side == 'LHS':
		# #x = datum[0]
		# #y = datum[1]
		
		# x_coords = [x, x, x-breadth, x-breadth, x] 
		# y_coords = [y, y-width, y-width, y, y] 
		
		# canvas.plot(x_coords,y_coords, color = lav_color)

	# if lav.side == 'RHS':
		# #x = datum[0]
		# #y = datum[1]
		
		# x_coords = [x, x, x-breadth, x-breadth, x] 
		# y_coords = [y, y+width, y+width, y, y] 
		
		# canvas.plot(x_coords,y_coords, color = lav_color)

	if lopa_bk.aircraft_type in ['A320', 'A319']:
	
		offset = 0

		if lav[0] == 'Lav A':
			
			if canvas_type == 'matplotlib':
				s = 278.6
			elif canvas_type == 'dxf':
				s=0
			b = 36.6
			cl = 19.685
			w = 46.51
			
			x = [s, s-b, s-b, s, s]
			y = [-cl-w, -cl-w, -cl, -cl, -cl-w]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)

			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
			x = [s-b+7, s-b+7]
			y = [-cl-w, -cl]
				
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				canvas.text(s - (b/2), -cl-w/2, 'La', ha='center', va='bottom')
				
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
			# if canvas_type == 'matplotlib':
				# canvas.plot(x, y, color = lav_color)

				
		if lav[0] == 'Lav D':
			
			if canvas_type == 'matplotlib':
				s = 1207 #station
			elif canvas_type == 'dxf':
				s = 0 #station is handled when block is inserted
			cl = -19.68
			b = 36.81
			w = 51.51
			
			x = [s, s, s+36.81, s+36.81]
			y = [-19.68-51.51, -19.68, -19.68, -19.68-46.51]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
			
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
			x = [s, s + 36.81]
			y = [-19.68-40, -19.68-40]
		
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
			
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
			x = [s+7, s+7]
			y = [-19.68-40, -19.68]

			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				canvas.text(s + (b/2), cl-w/2, 'Ld', ha='center', va='center')
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
			if lav[4] == 'Yes': #draw doghouse
							
				rect = patches.Rectangle((s-8,cl - 5),8,-45,linewidth=1,edgecolor='grey',facecolor='grey')
				canvas.add_patch(rect)
				
		if lav[0] == 'Lav E':
			
			if canvas_type == 'matplotlib':
				s = 1207
			elif canvas_type == 'dxf':
				s = 0
			cl = 19.68
			b = 36.61
			w = 51.51
			
			x = [s, s, s+36.81, s+36.81]
			y = [19.68+51.51, 19.68, 19.68, 19.68+46.51]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)

			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
			x = [s, s + 36.81]
			y = [19.68+40, +19.68+40]
		
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)

			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
		
			x = [s+7, s+7]
			y = [+19.68+40, +19.68]

			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				canvas.text(s + (b/2), cl+w/2, 'Le', ha='center', va='center')

			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
			if lav[4] == 'Yes': #draw doghouse
				
				if canvas_type == 'matplotlib':
					rect = patches.Rectangle((s-8,cl + 5),8,45,linewidth=1,edgecolor='grey',facecolor='grey')
					canvas.add_patch(rect)
				elif canvas_type == 'dxf':
					x = [s, s, s-8, s-8, s]
					y = [cl+5+45, cl+5, cl+5, cl+5+45, cl+5+45]
					points = []
					for index, v in enumerate(x):
						points.append((v, y[index]))
					canvas.add_lwpolyline(points)					
def draw_lav_side(lopa_bk, lav, canvas, canvas_type, side_datum):

	lav_color = 'green'
	# reference_side = lav.reference_side
	# breadth = float(lav.breadth)
	# height = float(lav.height)
	
	# if reference_side == 'LHS':
		# breadth = breadth*-1
	# width = float(lav.width)
	
	# x = side_datum[0]
	# y = side_datum[1]
	
	# x_coords = [x, x, x-breadth, x-breadth, x] 
	# y_coords = [y, y+height, y+height, y, y] 
	
	# canvas.plot(x_coords,y_coords, color = lav_color)

	if lopa_bk.aircraft_type in ['A320', 'A319']:
	
		offset = 0	
		y_datum = side_datum[1]
		
		if lav[0] == 'Lav A':

			if canvas_type == 'matplotlib':
				s=278.6
			elif canvas_type == 'dxf':
				s=0
			b = 36.6
			
			
			x = [s, s, s-36.6, s-36.6]
			y = [0+y_datum, 82.12+y_datum, 82.12+y_datum, 0+y_datum]
			
			if canvas_type == 'matplotlib':
				canvas[1].plot(x, y, color = lav_color)	
				canvas[1].text(s - (b/2), 40, 'La', ha='center', va='bottom')
			
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
		if lav[0] == 'Lav E':
			
			if canvas_type == 'matplotlib':
				s = 1207
			elif canvas_type == 'dxf':
				s = 0

			b= 36.6
			
			x = [s, s, s+36.81, s+36.81]
			y = [0+y_datum, 84.6+y_datum, 84.6+y_datum, 0+y_datum]
			
			if canvas_type == 'matplotlib':
				canvas[0].plot(x, y, color = lav_color)	
				canvas[0].text(s + (b/2), 40, 'Le', ha='center', va='bottom')
			
			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
		if lav[0] == 'Lav D':
			
			if canvas_type == 'matplotlib':
				s = 1207
			elif canvas_type == 'dxf':
				s=0

			b = 36.81
			
			x = [s, s, s+36.81, s+36.81]
			y = [0+y_datum, 84.6+y_datum, 84.6+y_datum, 0+y_datum]
			
			if canvas_type == 'matplotlib':
				canvas[1].plot(x, y, color = lav_color)	
				canvas[1].text(s + (b/2), 40, 'Ld', ha='center', va='bottom')

			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
		if lav[4] == 'Yes': #doghouse
			
			if canvas_type == 'matplotlib':
				rect = patches.Rectangle((s-8, 0),8,24,linewidth=1,edgecolor='grey',facecolor='grey')
				if lav[0] == 'Lav D':
					canvas[0].add_patch(rect)
				elif lav[0] == 'Lav E':
					canvas[1].add_patch(rect)
			
			elif canvas_type == 'dxf':
				points = []
				x = [s, s, s-8, s-8, s]
				y = [y_datum, y_datum+24, y_datum+24, y_datum, y_datum]
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)			