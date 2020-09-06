

def windbreaker_top_down_view(canvas, canvas_type, datum, wb):
	
	wb_color = 'orange'
	if wb.joggle == 'No':
		thickness = float(wb.thickness)
	else:
		thickness = float(wb.joggle_width)
	
	width = float(wb.width)
	if wb.side == 'LHS':
		x = datum[0]
		y = datum[1]
		
		x_coords = [x, x, x-thickness, x-thickness, x] 
		y_coords = [y, y-width, y-width, y, y] 
		
		canvas.plot(x_coords,y_coords, color = wb_color)

	if wb.side == 'RHS':
		x = datum[0]
		y = datum[1]
		
		x_coords = [x, x, x-thickness, x-thickness, x] 
		y_coords = [y, y+width, y+width, y, y] 
		
		canvas.plot(x_coords,y_coords, color = wb_color)

def windbreaker_side_view(canvas, canvas_type, datum, wb):
	
	wb_color = 'orange'
	x = datum[0]
	y = datum[1]
	
	height = float(wb.height)
	thickness = float(wb.thickness)
	
	if wb.joggle == 'No':
		
		x_coords = [x, x, x-thickness, x-thickness, x] 
		y_coords = [y, y+height, y+height, y, y]
		
		canvas.plot(x_coords,y_coords, color = wb_color)
		
	elif wb.joggle == 'Yes':
		
		joggle_width = float(wb.joggle_width)
		joggle_lower = float(wb.joggle_lower)
		joggle_upper= float(wb.joggle_upper)
		
		#start at bottom right corner, go anti clockwise
		x_coords = [x, x, x + joggle_width, x + joggle_width,
					x + joggle_width - thickness, x + joggle_width - thickness,
					x - thickness, x-thickness, x]
					
		y_coords = [y, joggle_lower, joggle_upper, height, height, joggle_upper,
					joggle_lower, y, y]
					
		canvas.plot(x_coords,y_coords, color = wb_color)