
def draw_galley_top_down(lopa_bk, galley, canvas, canvas_type, top_down_datum):
	
	galley_color = 'red'


	if lopa_bk.aircraft_type in ['A320', 'A319']:

		offset = 0
		
		if galley[0] == 'Galley 1':
			
			b = 38 # breath (longitudinal direction)
			s = 278.6 #station
			cl = 3.14 #dist from C/L
			w = 62.6 #width (spanwise direction)
			
			x = [s, s-b, s-b, s, s]
			y = [cl, cl, cl + w, cl+w, cl]
			
			if canvas_type == 'matplotlib':
				canvas.plot(x, y, color = galley_color)
				
				canvas.text(s - (b/2), cl+(w/2), 'G1', ha='center', va='center')
		
		if galley[0] == 'Galley 5':

			if canvas_type == 'matplotlib':
				canvas.plot([1280, 1280, 1285, 1285, 1280, 1280], [65, 45, 45, -45, -45, -65], color = galley_color)
				canvas.plot([1285, 1320], [45, 45], color = galley_color)
				canvas.plot([1285, 1320], [-45, -45], color = galley_color)
				
				canvas.text(1300, 0, 'G5', ha='center', va='bottom')
				
			
				
def draw_galley_side(lopa_bk, galley, canvas, canvas_type, side_datum):

	galley_color = 'red'
	
	if lopa_bk.aircraft_type in ['A320', 'A319']:
	
		offset = 0	

		if galley[0] == 'Galley 1':
		
			b = 38 # breath (longitudinal direction)
			s = 278.6 #station
			cl = 3.14 #dist from C/L
			w = 62.6 #width (spanwise direction)
			
			x = [s-b, s-b, s, s]
			y = [0, 82.12, 82.12, 0]
			
			if canvas_type == 'matplotlib':
				canvas[0].plot(x, y, color = galley_color)	
	
		if galley[0] == 'Galley 5':
		
			if canvas_type == 'matplotlib':
				canvas[0].plot([1280, 1280, 1320, 1320], [0, 82, 67, 0], color = galley_color)			
				canvas[1].plot([1280, 1280, 1320, 1320], [0, 82, 67, 0], color = galley_color)			