import pandas as pd
import tkinter as tk

def get_columns_values(treeview, column):
	values = []
	
	children = treeview.get_children()

	for child in children:
		if column == 0:
			values.append(treeview.item(child, 'text'))
		else:
			values.append((treeview.item(child, 'values'))[column-1])
	return values
	
	
def get_all_treeview_items(treeview):

	treeview_data = []
	
	children = treeview.get_children()

	for child in children:
		treeview_data.append([treeview.item(child, 'text')])
		values = treeview.item(child, 'values')
		for x in values:
			treeview_data[-1].append(x)
	return treeview_data	
	
def write_data_to_treeview(treeview, mode, data):

	if mode == 'replace':
	
		treeview.delete(*treeview.get_children())
		
	for d in data:
		if len(d) > 1:
			treeview.insert('', 'end', text=d[0], values=tuple(d[1:]))
		else:
			treeview.insert('', 'end', text=d[0])

def get_treeview_headers(treeview):
	
	columns = list(treeview['columns'])
	columns.insert(0, '#0')
	
	return [treeview.heading(x)['text'] for x in columns]
	
def treeview_to_df(treeview):
	treeview_data = {}
	
	#Columns
	headers = get_treeview_headers(treeview)

	for column, h in enumerate(headers):
		treeview_data[h] = get_columns_values(treeview, column)
		
	df = pd.DataFrame.from_dict(treeview_data)
	
	return df
	
def del_selected_items(treeview, msg = False):
	selected_item = treeview.selection()
	if selected_item:

		if msg: #if we require a messagebox
			MsgBox = tk.messagebox.askquestion ('Delete Selected Item??','This Cannont Be Undone!',icon = 'warning')
			if MsgBox == 'yes':
				treeview.delete(selected_item)
		else:
			treeview.delete(selected_item)
			
	return MsgBox



def get_current_selection(treeview):

	item = treeview.selection()[0]
	index = treeview.index(item)
	
	data = list(treeview.item(item,"values"))
	data.insert(0, treeview.item(item,"text"))


	return index, data