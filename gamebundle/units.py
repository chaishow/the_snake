from random import randint

import pygame as pg

from gamebundle.gametypes import Vector2


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
        return ((Vector2(x, y) for y in range(self.height_in_cells)
                 for x in range(self.width_in_cells)))

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


class ColorManager:
    """Class represent set of colors constants
    and methods to work with colors, dont need
    to be initializated
    """

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Secondary Colors
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    # Grayscale Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)

    # Additional Colors
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    BEIGE = (245, 245, 220)
    MAROON = (128, 0, 0)
    OLIVE = (128, 128, 0)
    TEAL = (0, 128, 128)
    NAVY = (0, 0, 128)
    DARK_PURPLE = (15, 8, 17)
    EXTRA_LIGHT_BLUE = (130, 255, 255)

    @staticmethod
    def _get_delta(first_color, second_color):
        """Returns delta of two colors
        in RGB color format
        """
        return (tuple(i - j
                      for i, j in zip(first_color, second_color)))

    @staticmethod
    def get_gradient(first_color, second_color, detailing=5):
        """Returns list of colors thats represents
        discrete linear gradiaent
        """
        gradient = [first_color]

        delta = ColorManager._get_delta(first_color, second_color)

        current_color = first_color
        for _ in range(detailing - 2):
            new_color = []

            for clr, dlt in zip(current_color, delta):
                new_color.append(clr
                                 - int(dlt / detailing))

            gradient.append(tuple(new_color))
            current_color = new_color

        gradient.append(second_color)

        return gradient

    @staticmethod
    def get_random_color(min_saturation=0, max_color_saturation=255):
        """Return random color from
        min_saturation arg, to
        max_saturation arg.
        """
        return tuple(randint(min_saturation, max_color_saturation)
                     for _ in range(3))
