from tkinter import Tk, BOTH, Canvas
import random
import time

def main():
    print("running...")
    # window = Window(500, 500)

    # cell1 = Cell(15, 15, 185, 185)
    # cell1.set_walls(True, False, True, True)
    # window.draw_cell(cell1, cell_fill_color)

    # cell2 = Cell(190, 15, 360, 185)
    # cell2.set_walls(False, True, True, False)
    # window.draw_cell(cell2, cell_fill_color)

    # cell3 = Cell(190, 190, 360, 360)
    # cell3.set_walls(True, False, False, True)
    # window.draw_cell(cell3, cell_fill_color)

    # cell4 = Cell(365, 190, 535, 360)
    # cell4.set_walls(False, True, False, True)
    # window.draw_cell(cell4, cell_fill_color)

    # cell5 = Cell(365, 15, 535, 185)
    # cell5.set_walls(True, True, True, False)
    # window.draw_cell(cell5, cell_fill_color)
    
    # window.draw_cell_move(cell1, cell2)
    # window.draw_cell_move(cell2, cell3)
    # window.draw_cell_move(cell3, cell4)
    # window.draw_cell_move(cell4, cell5)
    # window.draw_cell_move(cell4, cell5, True)

    # window.wait_for_close()

    window2 = Window(700,700)
    maze = Maze(15, 15, 20, 20, 25, 25, window2)
    maze.draw()
    # maze._break_entrance_and_exit()
    ex_i = 0
    ex_j = 0
    example_cell = maze._cells[ex_i][ex_j]
    neighbor_cell = maze._cells[ex_i+1][ex_j]
    # maze._get_adjacent_cells_indices(example_cell)
    # print(maze._get_adjacent_cells_indices(example_cell))
    # print(maze._get_adjacent_cells(example_cell))

    
    # example_cell_indices = maze._get_cell_indices(example_cell)
    # neighbor_cell_indices = maze._get_cell_indices(neighbor_cell)
    # print(example_cell_indices)
    # print(neighbor_cell_indices)
    # maze._break_walls_between(example_cell, neighbor_cell)
    # window2.redraw()
    window2.wait_for_close()


cell_fill_color = "white"

class Window:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._root = Tk()
        self._root.title("Root")
        self._root.geometry(f"{width}x{height}")
        self._canvas = Canvas(self._root)
        self._canvas.pack(fill=BOTH, expand=True)
        self._window_running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def get_default_background_color(self):
        try:
            default_bg_color = self._root.cget('background')
            if default_bg_color:
                return default_bg_color
        except Exception as e:
            print(f"Error retrieving default background color: {e}")
        return "#ffffff"

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._window_running = True
        while self._window_running:
            self.redraw()

    def close(self):
        self._window_running = False

    def draw_line(self, line, fill_color):
        line.draw(self._canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self._canvas, fill_color)

    def draw_cell_move(self, from_cell, to_cell, undo=False):
        from_cell.draw_move(self._canvas, to_cell, undo)

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
    def __init__(self, x1, y1, x2, y2, win=None, visited=False):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if x1 > x2 or y1 > y2:
            self._x1, self._x2 = self._x2, self._x1
            self._y1, self._y2 = self._y2, self._y1
        
        self.top_left_corner = Point(x1, y1)
        self.bottom_right_corner = Point(x2, y2)

        self._win = win
        self._visited = visited

    def set_walls(self, left, right, top, bottom):
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom

    def delete_walls(self, left, right, top, bottom):
        if left == True:
            self.has_left_wall = False
        if right == True:
            self.has_right_wall = False
        if top == True:
            self.has_top_wall = False
        if bottom == True:
            self.has_bottom_wall = False

    def get_top_left_point(self):
        return Point(self._x1, self._y1)
    
    def get_top_right_point(self):
        return Point(self._x2, self._y1)

    def get_bottom_left_point(self):
        return Point(self._x1, self._y2)

    def get_bottom_right_point(self):
        return Point(self._x2, self._y2)

    def draw(self, canvas, fill_color):
        top_left_point = self.get_top_left_point()
        bottom_left_point = self.get_bottom_left_point()
        top_right_point = self.get_top_right_point()
        bottom_right_point = self.get_bottom_right_point()

        background_color = self._win.get_default_background_color()

        left_wall = Line(top_left_point, bottom_left_point)
        if self.has_left_wall:
            left_wall.draw(canvas, fill_color)
        else:
            left_wall.draw(canvas, background_color)


        right_wall = Line(top_right_point, bottom_right_point)
        if self.has_right_wall:
            right_wall.draw(canvas, fill_color)
        else:
            right_wall.draw(canvas, background_color)

        top_wall = Line(top_left_point, top_right_point)
        if self.has_top_wall:
            top_wall.draw(canvas, fill_color)
        else:
            top_wall.draw(canvas, background_color)

        bottom_wall = Line(bottom_left_point, bottom_right_point)
        if self.has_bottom_wall:
            bottom_wall.draw(canvas, fill_color)
        else:
            bottom_wall.draw(canvas, background_color)

    def get_cell_center(self):
        x_center = self._x1 + ((self._x2 - self._x1) // 2)
        y_center = self._y1 + ((self._y2 - self._y1) // 2)
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
        win=None, seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = None
        self._initiated = False
        self._seed = seed
        if seed:
            random.seed(seed)

        # self._initiate()

    def _create_cells(self):
        self._cells = [[None for row in range(self._num_rows)] for col in range(self._num_cols)]

    def _position_cells(self):
        starting_x = self._x1
        starting_y = self._y1

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j] = Cell(starting_x, starting_y, starting_x + self._cell_size_x, starting_y + self._cell_size_y, self._win)
                starting_y += self._cell_size_y
            starting_y = self._y1
            starting_x += self._cell_size_x

    def _initiate(self):
        if self._initiated == False:
            self._create_cells()
            self._position_cells()
            self._initiated = True
            return
        return

    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].set_walls(True, True, False, True)
        self._cells[-1][-1].set_walls(True, True, True, False)
        # self.draw()
        # left rgiht top bottom

    def _break_walls_r(self, i, j):
        # print(f"\nCurrently on cell {(i, j)}")
        current_cell = self._cells[i][j]
        current_cell._visited = True
        while True:
            possible_directions = []
            adjacent_cells = self._get_adjacent_cells(current_cell)
            for cell in adjacent_cells:
                if cell != None:
                    if cell._visited == False:
                        possible_directions.append(cell)
            if possible_directions == []:
                # print(f"\nNo more possible directions!")
                current_cell.draw(self._win._canvas, cell_fill_color)
                return
            else:
                random_cell = possible_directions[random.randrange(0, len(possible_directions))]

                direction_indices = []
                for direction in possible_directions:
                    direction_indices.append(self._get_cell_indices(direction))

                # print(f"\nPossible directions: {direction_indices}")

                random_cell_indices = self._get_cell_indices(random_cell)

                # print(f"\nPicked random direction of {random_cell_indices}")

                rand_cell_i = random_cell_indices[0]
                rand_cell_j = random_cell_indices[1]

                self._break_walls_between(current_cell, random_cell)
                self._win.draw_cell_move(current_cell, random_cell)
                self._animate()
                self._break_walls_r(rand_cell_i, rand_cell_j)
                self._win.draw_cell_move(current_cell, random_cell, undo=True)
                
        for col in self._cells:
            for cell in col:
                cell._visited = False

                # print(f"\nPossible directions: \n{direction_indices} \n{possible_directions}")
                # print(f'\nRandom direction: {self._get_cell_indices(random_cell)} of cell {random_cell}')
                
    def _break_walls_between(self, cell_one, cell_two):
        cell_one_indices = self._get_cell_indices(cell_one)
        cell_two_indices = self._get_cell_indices(cell_two)

        if cell_two_indices[0] < cell_one_indices[0]:
            # break left wall of cell one
            cell_one.delete_walls(True, False, False, False)
            # break right wall of cell two
            cell_two.delete_walls(False, True, False, False)

        if cell_two_indices[0] > cell_one_indices[0]:
            # break right wall of cell one
            cell_one.delete_walls(False, True, False, False)
            # break left wall of cell two
            cell_two.delete_walls(True, False, False, False)

        if cell_two_indices[1] < cell_one_indices[1]:
            # break top wall of cell one
            cell_one.delete_walls(False, False, True, False)
            # break bottom wall of cell two
            cell_two.delete_walls(False, False, False, True)

        if cell_two_indices[1] > cell_one_indices[1]:
            # break bottom wall of cell one
            cell_one.delete_walls(False, False, False, True)
            # break top wall of cell two
            cell_two.delete_walls(False, False, True, False)

        self._animate()

    def _get_adjacent_cells(self, cell):
        adjacent_indices = self._get_adjacent_cells_indices(cell)
        
        left_indices = adjacent_indices[0]
        right_indices = adjacent_indices[1]
        top_indices = adjacent_indices[2]
        bottom_indices = adjacent_indices[3]

        left_cell = None
        right_cell = None
        top_cell = None
        bottom_cell = None

        if left_indices != None:
            left_cell = self._cells[left_indices[0]][left_indices[1]]
        if right_indices != None:
            right_cell = self._cells[right_indices[0]][right_indices[1]]
        if top_indices != None:
            top_cell = self._cells[top_indices[0]][top_indices[1]]
        if bottom_indices != None:
            bottom_cell = self._cells[bottom_indices[0]][bottom_indices[1]]

        return [left_cell, right_cell, top_cell, bottom_cell]


    def _get_adjacent_cells_indices(self, cell):
        adjacents = []
        cell_indices = self._get_cell_indices(cell)
        cell_i = cell_indices[0]
        cell_j = cell_indices[1]

        top_cell_indices = None
        bottom_cell_indices = None
        left_cell_indices = None
        right_cell_indices = None

        if cell_j > 0:
            top_cell_indices = (cell_i, cell_j-1)

        if cell_j < self._num_rows-1:
            bottom_cell_indices = (cell_i, cell_j+1)
            
        if cell_i > 0:
            left_cell_indices = (cell_i-1, cell_j)

        if cell_i < self._num_cols-1:
            right_cell_indices = (cell_i+1, cell_j)
        
        # print(f"\nWorking on {cell}\n")
        # print(f"(i, j) = {self._get_cell_indices(cell)}\n")
        # print(f"checking i and j: ({cell_i}, {cell_j})\n")

        # print(f"top cell: {top_cell_indices}")
        # print(f"bottom cell: {bottom_cell_indices}")
        # print(f"left cell: {left_cell_indices}")
        # print(f"right cell: {right_cell_indices}")

        # top_cell = self._cells[top_cell_indices[0]][top_cell_indices[1]]
        # bottom_cell = self._cells[bottom_cell_indices[0]][bottom_cell_indices[1]]
        # left_cell = self._cells[left_cell_indices[0]][left_cell_indices[1]]
        # right_cell = self._cells[right_cell_indices[0]][right_cell_indices[1]]

        return [left_cell_indices, right_cell_indices, top_cell_indices, bottom_cell_indices]

    def _get_cell_indices(self, cell):
        maze_nested_list = self._cells
        cell_coordinates = (cell._x1, cell._y1)
        for i, sublist in enumerate(maze_nested_list):
            for j, item in enumerate(sublist):
                if (item._x1, item._y1) == cell_coordinates:
                    return (i, j)
        return None
    
    def draw(self, fill_color="white"):
        self._initiate()
        for column in self._cells:
            for row in column:
                self._win.draw_cell(row, fill_color)
                # self.enumerate_cell(row)
                # self._get_adjacent_cells_indices(row)
                self._animate()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def enumerate_cell(self, cell):
        center_point_of_cell = cell.get_cell_center()
        cell_indices = self._get_cell_indices(cell)
        self._win._canvas.create_text(
            center_point_of_cell.x,
            center_point_of_cell.y,
            text=f"{cell_indices}",
            fill="white"
        )

if __name__ == "__main__":
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