import json
import tkinter.messagebox


def new_project(event=None, mainapp=None):

	msg = tkinter.messagebox.askokcancel(title='Create New Project', message='Any Unsaved Data Will Be Lost, This Cannot Be Undone, Do You Want To Continue?')
	
	if msg:
		mainapp.frames['Project'].clear_project_data()
	
def save(event=None, mainapp=None):

	if not mainapp.save_file:
		save_as(mainapp)
	else:
		write_save_file(mainapp)

def save_as(mainapp):

	mainapp.save_file = r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.01\Pycabin_Frontend_Tk\test.json'
	write_save_file(mainapp)
	
def write_save_file(mainapp):


	save_dict = {'Project': mainapp.frames['Project'].gen_save_dict()}
	
	print(save_dict)
	
	with open(mainapp.save_file, 'w') as outfile:
		json.dump(save_dict, outfile, indent=4)
		
		
def load(event=None, mainapp=None):

	with open(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.01\Pycabin_Frontend_Tk\test.json') as f:
		data = json.load(f)
		
	# ______ Project _________________
	if 'Project' in data.keys():
	
		mainapp.frames['Project'].load_project_data(data['Project'])