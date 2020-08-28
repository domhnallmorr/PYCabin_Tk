try:
	import tkinter as tk
	from tkinter import ttk
	from tkinter import *
except ImportError:
	import Tkinter as tk
	import ttk

class Double_ScrollableFrame:
	"""
	A vertically scrolled Frame that can be treated like any other Frame
	ie it needs a master and layout and it can be a master.
	keyword arguments are passed to the underlying Frame
	except the keyword arguments 'width' and 'height', which
	are passed to the underlying Canvas
	note that a widget layed out in this frame will have Canvas as self.master,
	if you subclass this there is no built in way for the children to access it.
	You need to provide the controller separately.
	"""
	def __init__(self, master, mainapp, **kwargs):
		width = kwargs.pop('width', None)
		height = kwargs.pop('height', None)
		self.outer = tk.Frame(master, **kwargs)

		self.vsb = ttk.Scrollbar(self.outer, orient=tk.VERTICAL)
		self.vsb.grid(row=0, column=1, sticky='ns')
		self.hsb = ttk.Scrollbar(self.outer, orient=tk.HORIZONTAL)
		self.hsb.grid(row=1, column=0, sticky='ew')
		self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height)
		self.canvas.grid(row=0, column=0, sticky='nsew')
		self.outer.rowconfigure(0, weight=1)
		self.outer.columnconfigure(0, weight=1)
		self.canvas['yscrollcommand'] = self.vsb.set
		self.canvas['xscrollcommand'] = self.hsb.set
		# mouse scroll does not seem to work with just "bind"; You have
		# to use "bind_all". Therefore to use multiple windows you have
		# to bind_all in the current widget
		self.canvas.bind("<Enter>", self._bind_mouse)
		self.canvas.bind("<Leave>", self._unbind_mouse)
		self.vsb['command'] = self.canvas.yview
		self.hsb['command'] = self.canvas.xview

		self.inner = tk.Frame(self.canvas)
		# pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
		self.canvas.create_window(4, 4, window=self.inner, anchor='nw', tags='frame')
		#self.inner.bind("<Configure>", self.FrameWidth)
		#self.inner.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(canvas))
		self.canvas.bind("<Configure>", self._on_frame_configure)

		self.outer_attr = set(dir(tk.Widget))
		
		self.inner_width_set = False
	def __getattr__(self, item):
		if item in self.outer_attr:
			# geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
			return getattr(self.outer, item)
		else:
			# all other attributes (_w, children, etc) are passed to self.inner
			return getattr(self.inner, item)

	def _on_frame_configure(self, event=None):

		x1, y1, x2, y2 = self.canvas.bbox("all")
		height = self.canvas.winfo_height()
		width = self.canvas.winfo_width()
		self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))
		self.canvas.itemconfig('frame', width = max(x2, width))


	def FrameWidth(self, event):
		canvas_width = event.width
		self.canvas.itemconfig('frame', width = canvas_width)
		
	def _bind_mouse(self, event=None):
		self.canvas.bind_all("<4>", self._on_mousewheel)
		self.canvas.bind_all("<5>", self._on_mousewheel)
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

	def _unbind_mouse(self, event=None):
		self.canvas.unbind_all("<4>")
		self.canvas.unbind_all("<5>")
		self.canvas.unbind_all("<MouseWheel>")
		
	def _on_mousewheel(self, event):
		"""Linux uses event.num; Windows / Mac uses event.delta"""
		func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll 
		if event.num == 4 or event.delta > 0:
			func(-1, "units" )
		elif event.num == 5 or event.delta < 0:
			func(1, "units" )

#  **** SCROLL BAR TEST *****
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
if __name__ == "__main__":
	root = tk.Tk()
	root.title("Scrollbar Test")
	root.geometry('400x500')
	lbl = tk.Label(root, text="Hold shift while using the scroll wheel to scroll horizontally")
	lbl.pack()
  
	note = ttk.Notebook(root)
	main_tab = Frame(note)
	
	note.add(main_tab, text = "Main")
	note.pack(fill=tk.BOTH, expand=True)
	# use the Scrolled Frame just like any other Frame
	frame = Double_ScrollableFrame(main_tab, None, width=300, borderwidth=2, relief=tk.SUNKEN, background="light gray")
	#frame.grid(column=0, row=0, sticky='nsew') # fixed size
	frame.pack(fill=tk.BOTH, expand=True) # fill window

	for i in range(30):
		for j in range(20):
			label = tk.Label(frame, text="{}{}".format(alphabet[j], i), relief='ridge')
			label.grid(column=j, row=i, sticky='ew', padx=2, pady=2)

	root.mainloop()