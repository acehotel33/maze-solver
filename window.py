from tkinter import Tk, BOTH, Canvas
import time

def main():
    print("running...")
    window = Window(500, 500)

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
    window.draw_cell(cell1, cell_fill_color)

    cell2 = Cell(190, 15, 360, 185)
    cell2.set_walls(False, True, True, False)
    window.draw_cell(cell2, cell_fill_color)

    cell3 = Cell(190, 190, 360, 360)
    cell3.set_walls(True, False, False, True)
    window.draw_cell(cell3, cell_fill_color)

    cell4 = Cell(365, 190, 535, 360)
    cell4.set_walls(False, True, False, True)
    window.draw_cell(cell4, cell_fill_color)

    cell5 = Cell(365, 15, 535, 185)
    cell5.set_walls(True, True, True, False)
    window.draw_cell(cell5, cell_fill_color)
    
    window.draw_cell_move(cell1, cell2)
    window.draw_cell_move(cell2, cell3)
    window.draw_cell_move(cell3, cell4)
    window.draw_cell_move(cell4, cell5)
    window.draw_cell_move(cell4, cell5, True)

    # window.wait_for_close()

    window2 = Window(500,500)
    maze = Maze(15, 15, 5, 5, 100, 100, window2)
    window2.draw_maze(maze, "white")
    window2.draw_maze(maze, "white")
    window2.wait_for_close()


cell_fill_color = "white"

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Root")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack(fill=BOTH, expand=True)
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

    def draw_cell_move(self, from_cell, to_cell, undo=False):
        from_cell.draw_move(self.__canvas, to_cell, undo)

    def draw_maze(self, maze, fill_color):
        maze.draw(self.__canvas, fill_color)

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
        if x1 > x2 or y1 > y2:
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

    def get_top_left_point(self):
        return Point(self.__x1, self.__y1)
    
    def get_top_right_point(self):
        return Point(self.__x2, self.__y1)

    def get_bottom_left_point(self):
        return Point(self.__x1, self.__y2)

    def get_bottom_right_point(self):
        return Point(self.__x2, self.__y2)

    def draw(self, canvas, fill_color):
        top_left_point = self.get_top_left_point()
        bottom_left_point = self.get_bottom_left_point()
        top_right_point = self.get_top_right_point()
        bottom_right_point = self.get_bottom_right_point()

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

    def get_cell_center(self):
        x_center = self.__x1 + ((self.__x2 - self.__x1) // 2)
        y_center = self.__y1 + ((self.__y2 - self.__y1) // 2)
        return Point(x_center, y_center)

    def draw_move(self, canvas, to_cell, undo=False):
        fill_color = "red"        
        if undo:
            fill_color = "gray"
        self_center = self.get_cell_center()
        to_cell_center = to_cell.get_cell_center()
        move_line = Line(self_center, to_cell_center)
        move_line.draw(canvas, fill_color)


class Maze:
    def __init__(
        self, x1, y1,
        num_rows, num_cols,
        cell_size_x, cell_size_y,
        win
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = None
        self.__initiated = False

        self._initiate()

    def _create_cells(self):
        self.__cells = [[None for row in range(self.__num_rows)] for col in range(self.__num_cols)]

    def _position_cells(self):
        starting_x = self.__x1
        starting_y = self.__y1

        for i in range(len(self.__cells)):
            for j in range(len(self.__cells[i])):
                self.__cells[i][j] = Cell(starting_x, starting_y, starting_x+ self.__cell_size_x, starting_y + self.__cell_size_y)
                starting_y += self.__cell_size_y + 5
            starting_y = self.__y1
            starting_x += self.__cell_size_x + 5

    def _initiate(self):
        if self.__initiated == False:
            self._create_cells()
            self._position_cells()
            self.__initiated = True
            return
        return

    def _animate(self):
        self.__win.redraw()
        time.sleep(0.1)
    
    def draw(self, canvas, fill_color):
        self._initiate()
        for column in self.__cells:
            for row in column:
                row.draw(canvas, fill_color)
                self._animate()

    
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