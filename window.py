from tkinter import Tk, BOTH, Canvas
import time

def main():
    print("running...")
    window = Window(200, 200)

    # point_a = Point(15, 15)
    # point_b = Point(185, 185)
    # line_a_b = Line(point_a, point_b)
    # fill_color_red = "red"
    # window.draw_line(line_a_b, fill_color_red)

    # point_c = Point(185, 15)
    # point_d = Point(15, 185)
    # line_c_d = Line(point_c, point_d)
    # fill_color_black = "black"
    # window.draw_line(line_c_d, fill_color_black)

    cell1 = Cell(15, 15, 185, 185)
    cell1.set_walls(True, False, True, True)
    cell1.set_walls(False, False, False, True)
    window.draw_cell(cell1, cell_fill_color)

    window.wait_for_close()
    
cell_fill_color = "white"

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

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point_a.x,
            self.point_a.y,
            self.point_b.x,
            self.point_b.y,
            fill=fill_color,
            width=2
        )

class Cell:
    def __init__(self, x1, y1, x2, y2):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if x1 > x2 or y1 < y2:
            self.__x1, self.__x2 = self.__x2, self.__x1
            self.__y1, self.__y2 = self.__y2, self.__y1
        
        self.top_left_corner = Point(x1, y1)
        self.bottom_right_corner = Point(x2, y2)

        self.__win = False

    def set_walls(self, left, right, top, bottom):
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom

    def draw(self, canvas, fill_color):
        top_left_point = self.top_left_corner
        top_right_point = Point(self.bottom_right_corner.x, self.top_left_corner.y)
        bottom_left_point = Point(self.top_left_corner.x, self.bottom_right_corner.y)
        bottom_right_point = self.bottom_right_corner

        if self.has_left_wall:
            left_wall = Line(top_left_point, bottom_left_point)
            left_wall.draw(canvas, fill_color)

        if self.has_right_wall:
            right_wall = Line(top_right_point, bottom_right_point)
            right_wall.draw(canvas, fill_color)

        if self.has_top_wall:
            top_wall = Line(top_left_point, top_right_point)
            top_wall.draw(canvas, fill_color)

        if self.has_bottom_wall:
            bottom_wall = Line(bottom_left_point, bottom_right_point)
            bottom_wall.draw(canvas, fill_color)



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