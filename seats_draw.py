import numpy as np


def triple_economy_top_down(seat, canvas, canvas_type, top_down_datum):

	width = float(seat.width)
	width_inbd = float(seat.width_inbd)
	length_fwd = float(seat.length_fwd)
	length_aft = float(seat.length_aft)
	armrest_width = float(seat.armrest_width)
		
	x = float(top_down_datum[0])
	y = float(top_down_datum[1])
	
	
	x_coords = [x - length_fwd, x + length_aft, x + length_aft, x - length_fwd, x - length_fwd]
	
	if seat.side == 'LHS':
		y_top = y - width + width_inbd + armrest_width
		y_btm = y_top + width - (armrest_width*2)
	elif seat.side == 'RHS':
		y_top = y + width - width_inbd - armrest_width
		y_btm = y_top - width + (armrest_width*2)
		
	y_coords = [y_top, y_top, y_btm, y_btm, y_top]
	
	if canvas_type == 'matplotlib':
		canvas.fill(x_coords, y_coords, color=seat.color, linewidth=1)
		canvas.plot(x_coords, y_coords, color='black', linewidth=1)	
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x_coords):
			points.append((v, y_coords[index]))
			canvas.add_lwpolyline(points)
		
def economy_seat_generic_side_view(seat, canvas, canvas_type, side_datum):
	
	l_fwd = float(seat.length_fwd)
	l_aft = float(seat.length_aft)
	h = float(seat.height)
	h_c = float(seat.cushion_height)
	iat = seat.iat
	#cushion spline

	x = [0.3105,0.1646,0.0918,0.0376,0.0165,0.0513,0.1646,0.3761,0.7587,
	1.2838,2.2703,4.1792,6.827,7.8093,9.3321,10.4131,11.3353,11.9465,
	13.7156,14.3089,15.2895,15.6938,15.8456,15.901,15.997,16.2367,16.63,
	17.6547,17.9929,18.3544,18.6885,18.8811,18.9394,19.0881,19.3643,19.5465,
	19.5857,19.5527,19.4336,19.1924,18.7481,18.2596,17.4452,16.124,15.1028,
	12.644,10.4276,7.7231,4.0594,1.7564,0.3105]

	for idx, v in enumerate(x):
		x[idx] = x[idx] + float(side_datum[0])
		
	y =[-257.4384,-256.9364,-256.4653,-255.8622,-255.2334,-254.9287,-254.7198,-254.6045,
	-254.5077,-254.4387,-254.4042,-254.4419,-254.4937,-254.4714,-254.3457,-254.1187,
	-253.8092,-253.5532,-252.5206,-251.9765,-250.7059,-249.775,-248.6926,-248.1472,
	-247.8443,-247.6246,-247.582,-247.6768,-247.642,-247.525,-247.3178,-247.0478,
	-246.6841,-246.4616,-246.5047,-246.7129,-247.1318,-248.3734,-249.7119,-250.8166,
	-252.1001,-253.2385,-254.6233,-256.2434,-257.1219,-258.4113,-258.8075,-258.5307,
	-257.9964,-257.6613,-257.4384,]
	
	for index, i in enumerate(y):
		y[index] = y[index] + 269.88 + side_datum[1] 
	
	if canvas_type == 'matplotlib':
		coords = np.array([x, y])		
		canvas.plot(x,y, color='black', linewidth=1)
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x):
			points.append((v, y[index]))
			canvas.add_lwpolyline(points)

			
	#front leg
	x = [side_datum[0]- 0.5, side_datum[0] + 0.31, side_datum[0]+2.85, side_datum[0]+ 0.5, side_datum[0]- 0.5]
	y = [side_datum[1], side_datum[1]+12.45,  side_datum[1]+12.06, side_datum[1], side_datum[1]]
	
	if canvas_type == 'matplotlib':
		coords = np.array([x, y])		
		canvas.plot(x,y, color='black', linewidth=1)
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x):
			points.append((v, y[index]))
			canvas.add_lwpolyline(points)
			
		
	#rear leg
						  
	x = [3.0677,3.6612,4.8953,6.764,8.1522,8.6781,10.5561,12.6487,14.1511,16.0023,
		17.0486,17.4602,17.4602,22.0651,22.0651,20.8993,18.9065,18.7581,18.2764,
		16.8437,14.8267,13.0859,12.0239,11.5949,11.5043,]				  
	y = [-257.8292,-258.1007, -258.8246,-260.2469,-261.1563,-261.7199,-264.1862,-266.17
		,-267.2692,-268.3415,-268.9045,-269.0944,-269.88,-269.88,-269.08,-268.3466,-268.3466,
		-268.2967,-267.9846,-266.976,-265.1723,-262.7725,-260.5154,-259.1652,-258.6868]

	for idx, v in enumerate(x):
		x[idx] = x[idx] + side_datum[0]		
	for idx, v in enumerate(y):
		y[idx] = y[idx] + side_datum[1]	+ 269.88
		
	if canvas_type == 'matplotlib':
		coords = np.array([x, y])		
		canvas.plot(x,y, color='black', linewidth=1)
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x):
			points.append((v, y[index]))
			canvas.add_lwpolyline(points)

	
	# backrest
	x = [side_datum[0]+ 18.2995, side_datum[0]+ 18.838, side_datum[0]+ 21.5257, side_datum[0]+ l_aft,
		side_datum[0]+ l_aft, side_datum[0]+ l_aft-2.73, side_datum[0]+ l_aft-2.73,
		side_datum[0]+16.7735]
	
	y= [side_datum[1]+ 269.88 -245.2909, side_datum[1]+ 269.88 -243.573, side_datum[1]+ 269.88-241.36,
		side_datum[1]+ 269.88-233.7, side_datum[1]+ h, side_datum[1]+ h, side_datum[1]+ h-6.86,
		side_datum[1]+269.88-244.6323]

	if canvas_type == 'matplotlib':		
		coords = np.array([x, y])		
		canvas.plot(x,y, color='black', linewidth=1)
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x):
			points.append((v, y[index]))
			canvas.add_lwpolyline(points)
					
	#armrest
								  
	x = [16.1367,15.1433, 13.7092, 12.8578,11.4878,10.0629,7.3485,5.6107,4.3358,3.2913,
			2.9024, 2.6271, 2.2814, 2.0893, 1.9357, 1.654, 1.4748, 1.5, 1.6668, 2.0125, 2.6463,
			4.5332, 6.3149, 7.7075, 9.1103, 10.5234, 12.9234, 14.3744, 15.6881, 16.7735, 17.6848,
			18.2275, 18.8624, 19.0496,]
	for idx, v in enumerate(x):
		x[idx] = x[idx] + side_datum[0]

	y = [-247.677, -247.4666,  -247.2235, -247.0763, -246.9228, -246.82,
			-246.788, -246.7699,-246.8211, -246.9083, -246.9864, -247.0568,
			-247.0248, -246.8201, -246.5194, -245.8605, -245.4127, -245.081,
			-244.8605, -244.6707, -244.4916, -244.3156, -244.2542, -244.1826,
			-244.1416, -244.1416, -244.131, -244.264, -244.4686, -244.6323,
			-244.9495, -245.2462, -245.8397, -246.4771]		
	for idx, v in enumerate(y):
		y[idx] = y[idx] + side_datum[1]	+ 269.88
		
	if canvas_type == 'matplotlib':			
		coords = np.array([x, y])		
		canvas.plot(x,y, color='black', linewidth=1)
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x):
			points.append((v, y[index]))
			canvas.add_lwpolyline(points)
	
	# top of cushion
	
	x = [-0.0165, -l_fwd, -l_fwd, 12.8]
	for idx, v in enumerate(x):
		x[idx] = x[idx] + side_datum[0]
		
	y = [14.64, 14.64, h_c, 16.76] 

	for idx, v in enumerate(y):
		y[idx] = y[idx] + side_datum[1]
		
	if canvas_type == 'matplotlib':			
		coords = np.array([x, y])		
		canvas.plot(x,y, color='black', linewidth=1)
	elif canvas_type == 'dxf':
		points = []
		for index, v in enumerate(x):
			points.append((v, y[index]))
			canvas.add_lwpolyline(points)	