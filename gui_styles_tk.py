from tkinter import font  as tkfont
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from PIL import Image, ImageTk
import base64
import io

def create_label(frame, var):
	
	if type(var) == str:
		l = tk.Label(frame, text=var,relief="solid", width = 40,anchor='w', bg = 'white',borderwidth=1, height = 2)	
	else:
		l = tk.Label(frame, textvariable=var,relief="solid", width = 40,anchor='w', bg = 'white',borderwidth=1, height = 2)	
		
	return l
	
def create_multiple_labels(frame,  labels, row, column, width = 20, padx = 2, pady = 2):
	
	for l in labels:
		tk.Label(frame,width = width, text=l, anchor="e").grid(row=row,column=column,padx=padx, pady=pady,sticky = 'NW')
		row +=1

def create_entry_style():

	style = ttk.Style()
	style.layout("Custom.Entry", style.layout('TEntry'))
	style.configure("Custom.Entry", **style.configure('TEntry'))
	style.map("Custom.Entry", **style.map('TEntry'))
	style.map("Custom.Entry",
		fieldbackground=[(['invalid','!disabled'], '#ff4040'),
						(['invalid','disabled'], '#ffc0c0')])
					
	return style
	
	
def setup_fonts(mainapp):

	mainapp.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
	mainapp.title_font.configure(underline=True)
	
def setup_icons(mainapp):

	size = 18,18
	# mainapp.folder_icon1 = Image.open(f'{mainapp.icons_folder}\\folder.png')
	# mainapp.folder_icon1.thumbnail(size, Image.ANTIALIAS)
	# mainapp.folder_icon2 = ImageTk.PhotoImage(mainapp.folder_icon1)
	
	data = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAABfklEQVRoge2XPUvDUBSG39h84CyU1ioOMXToIDWCf8Ctf8DBTfE3ODYogoOIg4MOgoi/xN3FRRARdNChflBQ8tHkOhVyAzVgjmkTzgMZTnJ5733uPQkEYBiGYTKgxIuXS3QU4FQAjT/mCQD3ULBf38BF9uWlIwk8neMZwBxFsBBwFjbRpcj6DUng4QyCOP/A3MYOcaaEJHB3Qi4AARxFBvZaW3inzgYSArfH9AJV00bVXAEUJX1wCgP3O+z3Hp2Ztevd4T0p9eaQVqBu2ahZNmUkAvcr1NtX6rBWpYcB3USN5jJqi21ARHShADRjuhKvZYFB9glU3cB8cwmzVgtAmD0wbb54sdpZh6obNMnEOz8KSUDVtNwmpkKVy2ItHkgKFGz3AT6B8VMyAW6h/CmZQNFbSPAJ5E/J3oHCC3AL5U9C4P//oKjhFho3JRPgFsqfcp2A73qhbmiVUYMnAd8NpG/9VLz4eO07vuuFEBEm8fJdL+y9fXZz3TGGYZhy8wPLqL/TAN/hMAAAAABJRU5ErkJggg=='
	mainapp.folder_icon2 = ImageTk.PhotoImage(decode_base64_image(size, data))

	data = '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'
	mainapp.airbus_icon2 = ImageTk.PhotoImage(decode_base64_image(size, data))

	data = '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'
	mainapp.boeing_icon2 = ImageTk.PhotoImage(decode_base64_image(size, data))	

	data = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAACn0lEQVRoge2Xz0sUYRjHP+/srv0AZ9e0k662xhpInixzO6R20UsgdYmKjBK89Hf0LwQdrKBDCcVIRJK0UUgIHuvk2LLhRbD8CWuy7r5dXJ1sZnbV3Zm32C/M5eF5Xz6f54GBF6qpppp/OsJvgL2ZvnKnW2iMCVgRQW3w/MvRlFu/UgLTg0OdQopJoG67NB8Qsu+c8fSb0xnNG7TiSafTicjIrQcIUWcpR3NSJGeu3W11OqfEBkzTTGiaNgHo2bn0x9WHzy4hpZXNcRO+b8A0zYQQYkJKqUspCZ5u6dFHbnxC/DHbaE6KV3bnfRUowAO6tR6Kx3rC94c+75EI293hm4BpmglgZ/J7v0BL40WLxJrMc93unoCn1NtZTNIZ+jX1aPP41VoQx5z6RLg2GjrV9G5z5uu97tdPpm17Kodpn8UknRpMAnVboY7UysmxCEI74dC+qmnaQDwet4UHjwWs8IWai0RRePBQwA6+kK1QR2q54YVVYi2fz/e3t7e7woNHAm7whWyFOlJL9c8jCC0opSwJHjz4C/38QLcGSVzgAYLZL62RpZvfITtQKjxUeAOlTN6SNQT99X2UDA8VFPACHiok4BU8VEDAS3gos4DX8FBGAT/goUwCfsFDGQT8hIdDCvgND4cQUAEeDiigCjwcQEAleNingGrwsA8BFeGhRAFV4aEEAZXhoYiA6vDg8iLL/Jhv1Gqa3qMwPLgIZEP65UDb2zA1zcXu8A0eXASklL3URAm0vcFFwld4cH/U9wG4SPgODw4ChmFcME0ztlP4W0IJeHAQyGQyw4ZhMDs7u1vclVhWBR4cBNbX13tzuRzj4+MFiRQwKo403z56ZuqsKvAAQbvixsZGQywWm9N1PbmwsPC4q6tLGeBqqqnmP8tvXSoro8f3eSgAAAAASUVORK5CYII='
	mainapp.edit_icon2 = ImageTk.PhotoImage(decode_base64_image(size, data))	

def decode_base64_image(size, data):

	msg = base64.b64decode(data)
	buf = io.BytesIO(msg)
	
	i = Image.open(buf)
	i.thumbnail(size, Image.ANTIALIAS)
	return i
	