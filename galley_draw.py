
def draw_galley_top_down(lopa_bk, galley, canvas, canvas_type, top_down_datum):
	
	galley_color = 'red'

	if lopa_bk.aircraft_type in ['A320', 'A319']:

		offset = 0
		
		if galley[0] == 'Galley 1':
			
			b = 38 # breath (longitudinal direction)
			s = 278.6 #station
			cl = 3.14 #dist from C/L
			w = 62.6 #width (spanwise direction)
			
			if canvas_type == 'matplotlib':
				x = [s, s-b, s-b, s, s]
			elif canvas_type == 'dxf':
				x = [s-s, s-b-s, s-b-s, s-s, s-s]
			y = [cl, cl, cl + w, cl+w, cl]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = galley_color)
				
				canvas.text(s - (b/2), cl+(w/2), 'G1', ha='center', va='center')

			elif canvas_type == 'dxf':
				
				y = [cl, cl, cl + (w*0.8), cl+(w*0.8), cl]
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
				canvas.add_line((-b*0.25, cl + (w*0.8)), (-b*0.25, w*1.1))
				canvas.add_line((-b, cl + (w*0.8)), (-b, w*1.08))

		if galley[0] == 'Galley 5':

			s = 1280
			if canvas_type == 'matplotlib':
				canvas.plot([1280, 1280, 1285, 1285, 1280, 1280], [65, 45, 45, -45, -45, -65], color = galley_color)
				canvas.plot([1285, 1320], [45, 45], color = galley_color)
				canvas.plot([1285, 1320], [-45, -45], color = galley_color)
				
				canvas.text(1300, 0, 'G5', ha='center', va='bottom')
				
			elif canvas_type == 'dxf':
				for idx, x in enumerate([[1280-s, 1280-s, 1285-s, 1285-s, 1280-s, 1280-s], [1285-s, 1320-s], [1285-s, 1320-s]]):
					y = [[65, 45, 45, -45, -45, -65], [45, 45], [-45, -45]][idx]
					points = []
					for index, v in enumerate(x):
						points.append((v, y[index]))
					canvas.add_lwpolyline(points)		
					
def draw_galley_side(lopa_bk, galley, canvas, canvas_type, side_datum):

	galley_color = 'red'
	
	if lopa_bk.aircraft_type in ['A320', 'A319']:
	
		offset = 0	
		
		if galley[0] == 'Galley 1':
			y_datum = side_datum[1]
			b = 38 # breath (longitudinal direction)
			s = 278.6 #station
			cl = 3.14 #dist from C/L
			w = 62.6 #width (spanwise direction)
			
			if canvas_type == 'matplotlib':
				x = [s-b, s-b, s, s]
			elif canvas_type == 'dxf':
				x = [s-b-s, s-b-s, s-s, s-s]
				
			y = [0+y_datum, 82.12+y_datum, 82.12+y_datum, 0+y_datum]
			
			if canvas_type == 'matplotlib':
				canvas[0].plot(x, y, color = galley_color)	
				canvas[0].text(s - (b/2), 40, 'G1', ha='center', va='bottom')

			elif canvas_type == 'dxf':
				points = []
				for index, v in enumerate(x):
					points.append((v, y[index]))
				canvas.add_lwpolyline(points)
				
		if galley[0] == 'Galley 5':
			s = 1280
			y_datum = side_datum[1]
			if canvas_type == 'matplotlib':
				canvas[0].plot([1280, 1280, 1320, 1320], [0, 82, 67, 0], color = galley_color)			
				canvas[1].plot([1280, 1280, 1320, 1320], [0, 82, 67, 0], color = galley_color)
				
				canvas[0].text(1300, 40, 'G5', ha='center', va='bottom')
				canvas[1].text(1300, 40, 'G5', ha='center', va='bottom')
				
			elif canvas_type == 'dxf':
				for idx, x in enumerate([[1280-s, 1280-s, 1320-s, 1320-s], [1280-s, 1280-s, 1320-s, 1320-s]]):
					#y_datum = side_datum[1+(idx*2)]
					#y = [0+y_datum, 82+y_datum, 67+y_datum, 0+y_datum]
					y = [0+y_datum, 82+y_datum, 67+y_datum, 0+y_datum]
					points = []
					for index, v in enumerate(x):
						points.append((v, y[index]))
					canvas.add_lwpolyline(points)					
			