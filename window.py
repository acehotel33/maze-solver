from tkinter import Tk, BOTH, Canvas
import time

def main():
    print("running...")
    testWindow = Window(200, 200)
    testWindow.wait_for_close()
    

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Root")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack()
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()

    def close(self):
        self.__window_running = False


main()

# from tkinter import *
# from tkinter import ttk

# # print(ttk.Frame().configure().keys())

# root = Tk()
# frame = ttk.Frame(root, padding=10)
# frame.grid()
# ttk.Label(frame, text="Hi Vakho!").grid(column=0, row=0)
# ttk.Button(frame, text="Quit", command=root.destroy).grid(column=0, row=1)
# root.mainloop()