import components_tk

def check_data_input(data, mainapp):

	data_good = True
	msg = None
	
	for widget in data:
		if data[widget][0] == 'entry':
			data_good, msg = check_entry_input(data[widget])
			
		elif data[widget][0] == 'combo':
			data_good, msg = check_combo_input(data[widget])
			
		elif data[widget][0] == 'title':
			data_good, msg = check_title_input(data[widget], mainapp)
			
		if not data_good:
			msg = f'{widget} {msg}'
				
			break
	
	return data_good, msg

def check_combo_input(combo_data):

	''' Possible Checks
			in values 
	'''
	
	combo_good = True
	combo_msg = None
	
	user_input = combo_data[1].get()
	
	if 'in values' in combo_data[2]:
		values = combo_data[1].config()['values'][-1]

		if user_input not in values:
			combo_good = False
			combo_msg = 'Selection Not Available'
	
	elif 'int greater than' in combo_data[2]:
		
		if user_input.strip() == '':
			combo_good = False
			combo_msg = 'Must be Entered'
		
		if combo_good:
			if 'equal' in combo_data[2]: #handle equal greater than or equal to
				
				if int(user_input) < int(combo_data[2].split()[-1]):
					combo_good = False
					combo_msg = f'Should be an Integer Greater than or Equal to {int(combo_data[2].split()[-1])}'
			else:		
				if int(user_input) <= int(combo_data[2].split()[-1]):
					combo_good = False
					combo_msg = f'Should be an Integer Greater than {int(combo_data[2].split()[-1])}'
			
	return combo_good, combo_msg
def check_entry_input(entry_data):
	
	''' Possible Checks
			float positive
	'''
	
	entry_good = True
	entry_msg = None
	
	user_input = entry_data[1].get()

	# If it should be a float, check first it can converted to a float
	if 'float' in entry_data[2]:
		if user_input.strip() != '':
			try:
				user_input = float(user_input)
			except:
				entry_good = False
		else:
			entry_good = False

	# If data good to this point, check if it is the right range
	if entry_good:
	
		if 'float positive' in entry_data[2]:
		
			if user_input <= 0:
				
				entry_good = False
				
			
	
	if not entry_good:
		
		if 'float positive' in entry_data[2]:
		
			entry_msg = 'Should be Numeric and Greater Than 0'
			
	return entry_good, entry_msg
	
def check_title_input(entry_data, mainapp):
	
	title_good = True
	title_msg = None
	
	user_input = entry_data[1].get().strip()
	
	#Check title is not blank
	
	if user_input.strip() == '':
		
		title_good = False
		title_msg = 'Must be Entered'
	
	if title_good:
		# Check if title in reserved ids
		
		if user_input in mainapp.ids_not_allowed:
			
			title_good = False
			title_msg = 'is Reserved, Choose Another'
	
	# Illegal characters
	if title_good:
		
		for c in [',', ':']:
			if c in user_input:
				title_good = False
				title_msg = 'Title must not contain any of the following characters:\n      ,:'
	if title_good:
		if user_input != entry_data[2]: # entry_data[2] is the original title, before user editted it
			# Check Component Does not exits already
			components = components_tk.get_all_components(mainapp, 'all')
			
			for component in components['All']:
				component_title = mainapp.frames[component].backend.title
		
				if component_title == user_input:
					title_good = False
					title_msg = 'Already Exists, Choose Another'
					break
	return title_good, title_msg
	
def check_title_clash(user_input, original_title, mainapp, type = 'Title'):
	
	title_good = True
	title_msg = None
	
	# Check if title is blank
	if user_input.strip() == '':
		title_good = False
		title_msg = f'Blank {type} Not Allowed'

	if title_good:
		# Check if title in reserved ids
		
		if user_input in mainapp.ids_not_allowed:
			
			title_good = False
			title_msg = '{user_input} is Reserved, Choose Another'

	if title_good:
		if user_input != original_title: # the original title, before user editted it
			# Check Component Does not exits already
			components = components_tk.get_all_components(mainapp, 'all')
			
			for component in components['All']:
				component_title = mainapp.frames[component].backend.title
		
				if component_title == user_input:
					title_good = False
					title_msg = f'{user_input} Already Exists, Choose Another Title'
					break
	return title_good, title_msg