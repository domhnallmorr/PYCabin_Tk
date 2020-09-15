

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
			
			s = 278.6
			b = 36.6
			cl = 19.685
			w = 46.51
			
			x = [s, s-b, s-b, s, s]
			y = [-cl-w, -cl-w, -cl, -cl, -cl-w]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				
			x = [s-b+7, s-b+7]
			y = [-cl-w, -cl]
		
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
		
			# x = [1207+7, 1207+7]
			# y = [-19.68-40, -19.68]

			# if canvas_type == 'matplotlib':
				# canvas.plot(x, y, color = lav_color)

				
		if lav[0] == 'Lav D':
		
			x = [1207, 1207, 1207+36.81, 1207+36.81]
			y = [-19.68-51.51, -19.68, -19.68, -19.68-46.51]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				
			x = [1207, 1207 + 36.81]
			y = [-19.68-40, -19.68-40]
		
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
		
			x = [1207+7, 1207+7]
			y = [-19.68-40, -19.68]

			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)

		if lav[0] == 'Lav E':
		
			x = [1207, 1207, 1207+36.81, 1207+36.81]
			y = [19.68+51.51, 19.68, 19.68, 19.68+46.51]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				
			x = [1207, 1207 + 36.81]
			y = [19.68+40, +19.68+40]
		
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
		
			x = [1207+7, 1207+7]
			y = [+19.68+40, +19.68]

			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = lav_color)
				
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

		if lav[0] == 'Lav A':
		
			x = [278.6, 278.6, 278.6-36.6, 278.6-36.6]
			y = [0, 82.12, 82.12, 0]
			
			if canvas_type == 'matplotlib':
				canvas[1].plot(x, y, color = lav_color)	
				
		if lav[0] == 'Lav E':
		
			x = [1207, 1207, 1207+36.81, 1207+36.81]
			y = [0, 84.6, 84.6, 0]
			
			if canvas_type == 'matplotlib':
				canvas[1].plot(x, y, color = lav_color)	
				
		if lav[0] == 'Lav D':
		
			x = [1207, 1207, 1207+36.81, 1207+36.81]
			y = [0, 84.6, 84.6, 0]
			
			if canvas_type == 'matplotlib':
				canvas[0].plot(x, y, color = lav_color)	