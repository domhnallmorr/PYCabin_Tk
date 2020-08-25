import time
import main_tkinter
import tkinter as tk

import components_tk

def run_test():
	root = tk.Tk()
	root.resizable(width=tk.TRUE, height=tk.TRUE)
	#MainApplication(root).pack(side="top", fill="both", expand=True)
	MA = main_tkinter.MainApplication(root)
	MA.grid(row=1, columnspan=4, sticky='nsew')
	#root.bind('<Control-z>', MA.states.undo)
	#root.bind('<Control-y>', MA.states.redo)
	
	root.geometry('{}x{}'.format(1600, 800))    
	
	root.bind('<Control-n>', lambda event, MA=MA: fm.new_project(event, MA))
	root.bind('<Control-o>', lambda event, MA=MA: fm.load(event, MA))
	root.bind('<Control-s>', lambda event, MA=MA: fm.save(event, MA))
	root.bind('<Control-z>', lambda event, MA=MA: MA.states.undo())
	root.bind('<Control-y>', lambda event, MA=MA: MA.states.redo())
	#loop = root.mainloop()

	add_seat(MA)
def add_seat(mainapp):
	
	components_tk.new_component(mainapp, 'Seat')

	mainapp.w.cancel_button.invoke()
	#root.update()
run_test()