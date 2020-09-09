

def draw_lav_top_down(lopa, canvas, canvas_type, top_down_datum):
	
	lav_color = 'green'
	reference_side = lav.reference_side
	breadth = float(lav.breadth)
	
	if reference_side == 'LHS':
		breadth = breadth*-1
	width = float(lav.width)
	
	x = top_down_datum[0]
	y = top_down_datum[1]
	
	if lav.side == 'LHS':
		#x = datum[0]
		#y = datum[1]
		
		x_coords = [x, x, x-breadth, x-breadth, x] 
		y_coords = [y, y-width, y-width, y, y] 
		
		canvas.plot(x_coords,y_coords, color = lav_color)

	if lav.side == 'RHS':
		#x = datum[0]
		#y = datum[1]
		
		x_coords = [x, x, x-breadth, x-breadth, x] 
		y_coords = [y, y+width, y+width, y, y] 
		
		canvas.plot(x_coords,y_coords, color = lav_color)
		
def draw_lav_side(lav, canvas, canvas_type, side_datum):

	lav_color = 'green'
	reference_side = lav.reference_side
	breadth = float(lav.breadth)
	height = float(lav.height)
	
	if reference_side == 'LHS':
		breadth = breadth*-1
	width = float(lav.width)
	
	x = side_datum[0]
	y = side_datum[1]
	
	x_coords = [x, x, x-breadth, x-breadth, x] 
	y_coords = [y, y+height, y+height, y, y] 
	
	canvas.plot(x_coords,y_coords, color = lav_color)