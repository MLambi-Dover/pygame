import tkinter as tk
from PIL import ImageTk, Image

win = tk.Tk()

win.geometry("700x500")

frame = tk.Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = ImageTk.PhotoImage(Image.open("spaceinvaders/assets/background-black.png"))

label = tk.Label(frame, image = img)
label.pack()

win.mainloop()
