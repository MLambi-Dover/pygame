import tkinter as tk

window = tk.Tk()


exitButton = tk.Button(text="Exit", command=window.destroy)
exitButton.pack()

mainloop()