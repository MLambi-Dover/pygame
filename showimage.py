import tkinter as tk
from PIL import ImageTk, Image

win = tk.Tk()


# I would like to figure out ways to keep the same window/size
# and change the image or background and resize it to the 
# existing window.


# I would like to figure out ways to keep the same window/size
# and change the image or background and resize it to the 
# existing window.

win.geometry("800x600")

frame = tk.Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = ImageTk.PhotoImage(Image.open("assets/background-black.png"))

label = tk.Label(frame, image = img)
label.pack()

win.mainloop()
