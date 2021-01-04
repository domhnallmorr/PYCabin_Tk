import matplotlib.patches as patches
from math import pi

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

				#add seat
				x = -7-29.6
				canvas.add_ellipse((22+x, -49.6), major_axis=(0, 8), start_param=1.2*pi, end_param=0.8*pi,ratio=0.8)
				points = []
				points.append((18.24+x, -56.07))
				points.append((25.76+x, -56.07))
				canvas.add_lwpolyline(points)

				points = [(7+x, -44), (17.43+x,-44)]
				canvas.add_lwpolyline(points)

				points = [(26.57+x, -44), (36.81+x,-44)]
				canvas.add_lwpolyline(points)

				#sink
				canvas.add_ellipse((-36.6+3.5, -66.2+30), major_axis=(0, 3), ratio=0.5)

				if lav[3] == 'Yes':#cas
					points = [(0, -cl), (7,-cl), (7,-cl-(w*0.7)), (0,-cl-(w*0.7))]
					canvas.add_lwpolyline(points)

					canvas.add_line((0, -cl-(w*0.35)), (7, -cl-(w*0.35)))

					canvas.add_text("F/A",
						             dxfattribs={
						                 'rotation': 270,}
						                 #'height': 0.35}
						             ).set_pos((3.5, -cl-(w*0.18)), align='MIDDLE_CENTER')

					canvas.add_text("F/A",
						             dxfattribs={
						                 'rotation': 270,}
						                 #'height': 0.35}
						             ).set_pos((3.5, -cl-(w*0.53)), align='MIDDLE_CENTER')

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

				#add seat
				canvas.add_ellipse((22, -49.6), major_axis=(0, 8), start_param=1.2*pi, end_param=0.8*pi,ratio=0.8)
				points = []
				points.append((18.24, -56.07))
				points.append((25.76, -56.07))
				canvas.add_lwpolyline(points)

				points = [(7, -44), (17.43,-44)]
				canvas.add_lwpolyline(points)

				points = [(26.57, -44), (36.81,-44)]
				canvas.add_lwpolyline(points)

				#sink
				canvas.add_ellipse((3.5, -59.68+30), major_axis=(0, 3), ratio=0.5)

				if lav[3] == 'Yes':#cas
					points = [(b, cl), (b+7,cl), (b+7,cl-(w*0.35)), (b,cl-(w*0.35))]
					canvas.add_lwpolyline(points)

					canvas.add_text("F/A",
						             dxfattribs={
						                 'rotation': 270,}
						                 #'height': 0.35}
						             ).set_pos((b+3.5, cl-(w*0.18)), align='MIDDLE_CENTER')



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

				#add seat
				canvas.add_ellipse((22, 59.68-10.08), major_axis=(0, 8), start_param=0.2*pi, end_param=1.8*pi,ratio=0.8)
				points = []
				points.append((18.24, 59.68-3.61))
				points.append((25.76, 59.68-3.61))
				canvas.add_lwpolyline(points)

				points = [(7, 59.68-15.68), (17.43,59.68-15.68)]
				canvas.add_lwpolyline(points)

				points = [(26.57, 59.68-15.68), (36.81,59.68-15.68)]
				canvas.add_lwpolyline(points)

				#sink
				canvas.add_ellipse((3.5, 59.68-30), major_axis=(0, 3), ratio=0.5)

				if lav[3] == 'Yes':#cas
					points = [(b, cl), (b+7,cl), (b+7,cl+(w*0.7)), (b,cl+(w*0.7))]
					canvas.add_lwpolyline(points)

					canvas.add_line((b, cl+(w*0.35)), (b+7, cl+(w*0.35)))

					points = [(b, cl), (b,cl-7), (b-(w*0.35),cl-7), (b-(w*0.35),cl)]
					canvas.add_lwpolyline(points)

					canvas.add_text("F/A",
						             dxfattribs={
						                 'rotation': 270,}
						                 #'height': 0.35}
						             ).set_pos((b+3.5, cl+(w*0.18)), align='MIDDLE_CENTER')

					canvas.add_text("F/A",
						             dxfattribs={
						                 'rotation': 270,}
						                 #'height': 0.35}
						             ).set_pos((b+3.5, cl+(w*0.53)), align='MIDDLE_CENTER')

					canvas.add_text("F/A").set_pos((b-(w*0.18), cl-3.5), align='MIDDLE_CENTER')

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
					canvas.add_patch(rect)
			
			elif canvas_type == 'dxf':
				points = []
				x = [s, s, s-8, s-8, s]
				y = [y_datum, y_datum+24, y_datum+24, y_datum, y_datum]
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)			