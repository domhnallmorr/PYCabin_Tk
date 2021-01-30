from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import ImageGrab
from PIL import Image

img = ImageGrab.grab()
name = asksaveasfilename()
img = img.crop((0, 0, 1920, 1010)) 
img.save(name)