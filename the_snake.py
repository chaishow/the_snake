from random import choice, randint

import pygame as pg

from gamebundle import ColorManager, FrameCounter, Grid, Vector2

# System constants.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Direction constants.
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
ZERO_VECTOR = Vector2(0, 0)

# Color constants
BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (252, 245, 141)
SNAKE_COLOR = (35, 185, 182)
WAVE_COLOR = (60, 32, 68)
FLOOR_COLOR = (10, 10, 10)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Snake')
clock = pg.time.Clock()


class GameObject:
    """
    class to represent any
    game object.
    """

    def __init__(self, position=ZERO_VECTOR, color=None):
        self.position = Vector2(position)
        self.body_color = color

    def get_position(self):
        """Returns GameObject position."""
        return self.position

    def _set_position(self, position):
        """Change positon of GameObject."""
        self.position = Vector2(position)

    def draw(self, grid):
        """Draw GameObject on grid."""
        raise NotImplementedError('Method should be overridden')


class Snake(GameObject):
    """Class to represent snake in a game."""

    MAX_SPEED = FPS - 1

    def __init__(self, position=ZERO_VECTOR, color=SNAKE_COLOR,
                 start_speed=5, speed_delta=1):

        super().__init__(position, color)

        self.head_color = (254, 252, 221)
        self.direction = Vector2(1, 0)
        self.is_eating = False
        self.start_speed = start_speed
        self.speed_delta = speed_delta
        self.directions_queue = [self.direction]

        self._reset()

    def get_head_position(self):
        """Returns snake head position as Vector2."""
        return self.positions[0]

    def get_all_positions(self):
        """Returns all snake positions
        as Vector2 set.
        """
        return set(self.positions)

    def __update_direction(self):
        """Method to process direction queue."""
        if len(self.directions_queue) > 0:
            new_direction = self.directions_queue.pop(0)
            if new_direction != -self.direction:
                self.direction = new_direction

    def _add_to_directions_queue(self, direction):
        """Method to add new direction in
        directions queue if that dont
        overflow.
        """
        if len(self.directions_queue) < 3:
            self.directions_queue.append(direction)

    def __change_speed(self, delta):
        """Method to safety change
        snake speed (cant be <0 and >MAX_SPEED).
        """
        if self.speed + delta < self.MAX_SPEED:
            self.speed += delta
        elif self.speed + delta < 0:
            self.speed = 0
        else:
            self.speed = self.MAX_SPEED

    def _increace_level(self):
        """Method to increace snale level
        on every 3 levels snake will be
        accelerate.
        """
        self.level += 1
        if self.level % 3 == 0:
            self.__change_speed(self.speed_delta)

    def _move(self, grid, frame_counter):
        """Update positions of snake.
        Create new block in
        """
        # Snake move once at self.speed frames.
        if (
            frame_counter.get_frame_number() %
            (frame_counter.get_fps() // self.speed) == 0
        ):
            # Process new direction from queue.
            self.__update_direction()

            # Make new segment of snake.
            new_head_position = ((self.get_head_position() + self.direction)
                                 % grid.get_cell_size())

            # Check collision between snake positions and new segment.
            if new_head_position in self.positions:
                self.die()

            # Add new segment to list
            self.positions.insert(0, new_head_position)

            # If snake not eating last segment will be deleted.
            if not self.is_eating:
                self.positions.pop(-1)
            else:
                self.is_eating = False

    def grow(self):
        """Method to turn on snake grow state. Make
        values to not delete last position in move()
        method and increace snake level.
        """
        self._increace_level()
        self.is_eating = True

    def die(self):
        """Method to stop snake processing
        to next reset.
        """
        self.dead = True

    def _reset(self):
        """Return snake to origin state."""
        self.positions = [Vector2(0, 0)]
        self.dead = False
        self.level = 1
        self.speed = self.start_speed

    def handle_keys(self, event):
        """Event handler method."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self._add_to_directions_queue(UP)
            if event.key == pg.K_a:
                self._add_to_directions_queue(LEFT)
            if event.key == pg.K_d:
                self._add_to_directions_queue(RIGHT)
            if event.key == pg.K_s:
                self._add_to_directions_queue(DOWN)

    def update(self, grid_map, frame_counter):
        """Method to update snake state."""
        if not self.dead:
            self._move(grid_map, frame_counter)
        else:
            self._reset()

    def draw(self, grid):
        """Draw all of snake positions on grid."""
        for position in self.positions:
            grid.draw_on_grid(position, self.body_color, 2)


class Apple(GameObject):
    """Class to represent apple in game."""

    def __init__(self, availeble_positions=None,
                 position=ZERO_VECTOR, color=APPLE_COLOR):

        super().__init__(position, color)

        if availeble_positions:
            self._randomize_position(availeble_positions)

    def _randomize_position(self, availeble_positions):
        """Change apple position to random
        from available
        """
        self._set_position(choice(availeble_positions))

    def draw(self, grid):
        """Draw Apple on grid"""
        grid.draw_on_grid(self.position, self.body_color, 4)


class Wave(GameObject):
    """Visual instance for create
    effect of wave on new apple
    place.
    """

    def __init__(self, position=ZERO_VECTOR, color=None, deep=7):
        super().__init__(position, color)
        self.positions = [self.position]
        self.period = 30
        self.level = 1
        self.deep = deep

    def is_ended(self):
        """Return True if instance deep equal max deep
        else return False.
        """
        return self.level == self.deep

    def update(self, grid, frame_counter):
        """Update positions of Wave.
        Check is wave ended.
        """
        if self.level < self.deep:
            if (
                frame_counter.get_frame_number()
                % self.period == self.period - 1
            ):
                self.positions = grid.get_coordinates_around(self.positions)
                self.level += 1

    def draw(self, grid):
        """Draw all of Wave positions on grid."""
        colors = ColorManager.get_gradient(self.body_color,
                                           ColorManager.BLACK,
                                           self.deep)
        for position in self.positions:
            grid.draw_on_grid(position, colors[self.level - 1], 1)


class DicscoCell(GameObject):
    """Colorswapping ellement of background."""

    def __init__(self, position=ZERO_VECTOR, color=FLOOR_COLOR):
        self.position = Vector2(position)

        # Use lists to change colors in dynamic
        self.origin_color = list(color)
        self.current_color = list(color)

        self.is_color_changed = False

    def _return_to_own_color(self):
        """Return cell to origin color."""
        delta_r = self.current_color[0] - self.origin_color[0]
        delta_g = self.current_color[1] - self.origin_color[1]
        delta_b = self.current_color[2] - self.origin_color[2]
        delts = [delta_r, delta_g, delta_b]

        count = 0
        step = randint(5, 60)
        for i in range(len(delts)):
            delta = delts[i]
            if abs(delta) < 0.1:
                self.current_color[i] = self.origin_color[i]
                count += 1

            else:
                self.current_color[i] -= delta / step
        if count == 3:
            self.is_color_changed = False

    def _change_color(self, color):
        """Safety changing color of cell."""
        for i in range(3):
            if color[i] > 255:
                self.current_color[i] = 255
            elif color[i] < 0:
                self.current_color[i] = 0
            else:
                self.current_color[i] = color[i]
        self.is_color_changed = True

    def update(self):
        """Updating of cell state."""
        if self.is_color_changed:
            self._return_to_own_color()
        else:
            self._change_color(list(get_random_color(max_color_saturation=40)))

    def draw(self, grid):
        """Draw DiscoCell on grid."""
        grid.draw_on_grid(self.position,
                          tuple(self.current_color),
                          margin=0)


def get_random_color(min_saturation=0, max_color_saturation=255):
    """Return random color from
    min_saturation arg, to
    max_saturation arg.
    """
    return tuple(randint(min_saturation, max_color_saturation)
                 for _ in range(3))


def get_availeble_positions(grid, snake):
    """Returns free positions on grid."""
    avalieble_positions = (set(grid.get_all_cells_coordinates())
                           - set(snake.get_all_positions()))
    return list(avalieble_positions)


def handle_keys(handlers):
    """Function to handle player events
    and send it to local GameObjects
    handlers.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        else:
            for handler in handlers:
                handler.handle_keys(event)


def main():
    """Main function to run game.
    Initialiaze game components, create and
    process game loop.
    """
    pg.init()

    # Initialize of units.
    grid = Grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)
    frame_counter = FrameCounter(FPS)

    # Initialize of GameObjects
    snake = Snake((0, 0), SNAKE_COLOR)
    current_apple = Apple()
    current_apple._randomize_position(get_availeble_positions(grid, snake))
    waves = []

    DiscoFloor = [DicscoCell(position)
                  for position in grid.get_all_cells_coordinates()]
    for cell in DiscoFloor:
        cell._change_color(get_random_color(max_color_saturation=40))

    # Make list of objects who handle user events
    # Now it's just snake, but maybe in future there will be more of them
    handlers = [snake]

    while True:
        clock.tick(FPS)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Update and draw background
        for cell in DiscoFloor:
            cell.update()
            cell.draw(grid)

        # Update and draw waves from apples
        for wave in waves:
            if wave.is_ended():
                waves.remove(wave)
            wave.update(grid, frame_counter)
            wave.draw(grid)

        # Update and draw snake
        snake.update(grid, frame_counter)
        snake.draw(grid)

        # Draw apple
        current_apple.draw(grid)

        # Check collision between snake head and apple
        if snake.get_head_position() == current_apple.get_position():

            snake.grow()

            del current_apple
            current_apple = Apple(get_availeble_positions(grid, snake))

            waves.append(Wave(current_apple.get_position(), WAVE_COLOR))

        # All events handlers handle events
        handle_keys(handlers)

        pg.display.update()
        frame_counter.update()


if __name__ == '__main__':
    main()
