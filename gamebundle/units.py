from .gametypes import Vector2
import pygame as pg


class Grid:
    """
    Class to represent Grid with
    definded grid size.

    Contains methods to take coordinates
    of ceils, to turn local coordinates
    to global and etc.
    """

    def __init__(self, screen, width, height, grid_size):
        self.screen = screen
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.width_in_cells = width // grid_size
        self.height_in_cells = height // grid_size

    def get_cell_size(self):
        """Returns weight and height
        of cell
        """
        return Vector2(self.width_in_cells, self.height_in_cells)

    def get_all_cells_coordinates(self):
        """Returns all coordinates of grid
        may be useful to fill all grid
        with some objects.
        """
        all_cells_coords = ((Vector2(x, y) for y in range(self.height_in_cells)
                            for x in range(self.width_in_cells)))
        return all_cells_coords

    def draw_on_grid(self, position, color=(255, 255, 255), margin=0):
        """Renders square by global coordinates
        of point in left top angle of
        grid cell.
        """
        global_position = position * self.grid_size
        x, y = global_position.x + margin / 2, global_position.y + margin / 2
        size = self.grid_size - margin
        pg.draw.rect(self.screen, color, (x, y, size, size))

    @staticmethod
    def get_coordinates_around(positions: list[Vector2]) -> list[Vector2]:
        """This method returns coordinates
        around square shaped area of cells
        described by coordinates.

        WARNING: Be carefull with non-square
        shaped areas, behaviour may be
        unpredictable
        """
        RIGHT = Vector2(1, 0)
        DOWN = Vector2(0, 1)
        LEFT = Vector2(-1, 0)
        UP = Vector2(0, -1)

        directions = [RIGHT, DOWN, LEFT, UP]

        left_corner = positions[0] + Vector2(-1, -1)
        new_positions = [left_corner]
        current_position = left_corner

        for i in range(len(directions)):
            view = directions[(i + 1) % len(directions)]
            current_position += directions[i]

            while (current_position + view) in positions:
                new_positions.append(current_position)
                current_position += directions[i]

            new_positions.append(current_position)

        return new_positions


class FrameCounter:
    """
    Cyclical counter to controll speed of updating
    game objects
    (for example some game objects must be update 1 time
    in 20 frames)
    """

    def __init__(self, max_frames):
        self.frame_counter = 0
        self.max_frames = max_frames

    def update(self):
        """Update counter from 1 to
        max_frames - 1
        """
        self.frame_counter = (self.frame_counter + 1) % self.max_frames

    def get_frame_number(self):
        """Return current frame number"""
        return self.frame_counter

    def get_fps(self):
        """Return current instance FPS"""
        return self.max_frames
