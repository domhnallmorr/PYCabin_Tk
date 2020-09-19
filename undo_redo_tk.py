
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import components_tk

class Undo_Redo():
	def __init__(self, mainapp):
		
		self.mainapp = mainapp
			
		self.undo_stack = []
		self.redo_stack = []
	
	def reset(self, undo = True, redo = True):
	
		if undo:
			self.undo_stack = []
		
		if redo:
			self.redo_stack = []
			
	def undo(self, event=None):
	
		if len(self.undo_stack) > 0:
			action = self.undo_stack[-1]
			
			component_backend = action['component']
			
			if action['type'] != 'comment':
				old_title = component_backend.title

			if action['type'] == 'new':
				#delete created component
				
				name = action['component'].title
				index = self.mainapp.main_treeview.index(component_backend.parent_page.treeview_iid)
				
				components_tk.delete_item_from_main_treeview(self.mainapp, name, component_backend)
				
				self.redo_stack.insert(0, {'type': 'deleted component', 'component': action['component'],
												'new_class': component_backend.save_class(component_backend), 'index': index})
					
			elif action['type'] == 'edit':
				
				name = action['component'].title
				save_class = action['new_class']

				self.redo_stack.insert(0, {'type': 'edit', 'component': action['component'],
												'new_class': component_backend.save_class(component_backend)})
				component_backend.parent_page.update_component(save_class, 'undo_redo')
				
				components_tk.show_frame(self.mainapp, component_backend.title)
			elif action['type'] == 'deleted component':
				
				if 'index' in action.keys():
					index = action['index']
				else:
					index = 0
				
				self.mainapp.main_treeview.move(component_backend.parent_page.treeview_iid, component_backend.treeview_node, index)
				components_tk.show_frame(self.mainapp, component_backend.title)
				
				self.redo_stack.append({'type': 'new', 'component': component_backend,
														'new_class': component_backend.save_class(component_backend)})		

			elif action['type'] == 'comment':
				#component_backend is actually the frontend for comment undo/redo (sorry :( )
				
				current_text = component_backend.comment_text.get("1.0","end")
				component_backend.comment_text.config(state='normal')
				component_backend.comment_text.delete('1.0', END)
				component_backend.comment_text.insert('1.0', action['new_class'])
				component_backend.comment_text.config(state='disabled')
			
				components_tk.show_frame(self.mainapp, component_backend.backend.title)
				component_backend.note.select(len(component_backend.note.tabs())-1) #select comments tab (makes obvious what is undone)
				self.redo_stack.append({'type': 'comment', 'component': component_backend,
														'new_class': current_text})
			self.undo_stack.pop(-1)

	def redo(self):

		if len(self.redo_stack) > 0:
			
			action = self.redo_stack[0]
			
			component = action['component']
			
			if action['type'] != 'comment':
				old_title = component.title
			
			if action['type'] == 'deleted component':
				
				if 'index' in action.keys():
					index = action['index']
				else:
					index = 0
					
				self.mainapp.main_treeview.move(component.parent_page.treeview_iid, component.treeview_node, index)
				self.undo_stack.append({'type': 'new', 'component': action['component'],
												'new_class': component.save_class(component)})
				components_tk.show_frame(self.mainapp, component.title)
			
			if action['type'] == 'new':
				''' If a component was inserted and we want to remove it '''
				
				index = self.mainapp.main_treeview.index(component.parent_page.treeview_iid)
				
				name = action['component'].title
				components_tk.delete_item_from_main_treeview(self.mainapp, name, component)
				
				self.undo_stack.append({'type': 'deleted component', 'component': action['component'],
												'new_class': component.save_class(component), 'index': index})				
			# if action['type'] != 'deleted component':
				# self.undo_stack.append({'type': 'edit', 'component': action['component'],
												# 'new_class': component.save_class(component)})
				
			if action['type'] == 'edit':
				component_backend = action['component']
				name = action['component'].title
				save_class = action['new_class']

				self.undo_stack.append({'type': 'edit', 'component': action['component'],
												'new_class': component_backend.save_class(component_backend)})			
				
				components_tk.show_frame(self.mainapp, component_backend.title)
				
			if action['type'] == 'comment':
				#component_backend is actually the frontend for comment undo/redo (sorry :( )
				component_backend = action['component']
				current_text = component_backend.comment_text.get("1.0","end")
				component_backend.comment_text.config(state='normal')
				component_backend.comment_text.delete('1.0', END)
				component_backend.comment_text.insert('1.0', action['new_class'])
				component_backend.comment_text.config(state='disabled')
				
				components_tk.show_frame(self.mainapp, component_backend.backend.title)
				component_backend.note.select(len(component_backend.note.tabs())-1)
				self.undo_stack.append({'type': 'comment', 'component': component_backend,
														'new_class': current_text})
			
			if action['type'] != 'comment':
				self.mainapp.frames[component.title].update_component(action['new_class'], 'undo_redo')
			
			
			self.redo_stack.pop(0)
			
		
	def component_updated(self, update_type, component, save_class):
		
		if update_type != 'comment':
			self.undo_stack.append({'type': update_type, 'component': component,
															'new_class': save_class(component)})
		else:
			self.undo_stack.append({'type': update_type, 'component': component,
															'new_class': save_class})			
														
		self.reset(undo=False, redo=True)