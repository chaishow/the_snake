from random import choice, randint
import pygame as pg
from gamebundle import Vector2, Grid, FrameCounter

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (252, 245, 141)

# Цвет змейки
SNAKE_COLOR = (35, 185, 182)

# Цвет визуального эффекта "волна"
WAVE_COLOR = (59, 32, 68)

# Начальный цвет фоновых ячеек
FLOOR_COLOR = (10, 10, 10)

# Скорость движения змейки:
FPS = 60

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    class to represent any
    game object
    """

    def __init__(self, position=Vector2(0, 0), color=None):
        self.position = Vector2(position)
        self.body_color = color

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = Vector2(position)

    def draw(self, grid):
        pass


class Snake(GameObject):
    MAX_SPEED = FPS - 1

    def __init__(self, position=Vector2(0, 0), color=SNAKE_COLOR, speed=5):
        super().__init__(position, color)
        self.head_color = (254, 252, 221)
        self.positions = [Vector2(position)]
        self.direction = Vector2(1, 0)
        self.is_eating = False
        self.dead = False
        self.speed = speed
        self.start_speed = speed
        self.level = 1
        self.directions_queue = [self.direction]

    def get_head_position(self):
        return self.positions[0]

    def get_all_positions(self):
        return set(self.positions)

    def update_direction(self):
        if len(self.directions_queue) > 0:
            new_direction = self.directions_queue.pop(0)
            if new_direction != -self.direction:
                self.direction = new_direction

    def add_to_directions_queue(self, direction):
        if len(self.directions_queue) < 3:
            self.directions_queue.append(direction)

    def change_speed(self, delta):
        if self.speed + delta < self.MAX_SPEED:
            self.speed += delta
        elif self.speed + delta < 0:
            self.speed = 0
        else:
            self.speed = self.MAX_SPEED

    def increace_level(self):
        self.level += 1
        if self.level % 3 == 0:
            self.change_speed(1)

    def move(self, grid, frame_counter):
        if (
            frame_counter.get_frame_number() %
            (frame_counter.get_fps() // self.speed) == 0
        ):
            self.update_direction()

            new_head_x = ((self.positions[0].x + self.direction.x) %
                          grid.get_cell_size().x)
            new_head_y = ((self.positions[0].y + self.direction.y) %
                          grid.get_cell_size().y)
            new_head_position = Vector2(new_head_x, new_head_y)

            if new_head_position in self.positions:
                self.die()

            self.positions.insert(0, new_head_position)

            if not self.is_eating:
                self.positions.pop(-1)
            else:
                self.is_eating = False

    def grow(self):
        self.increace_level()
        self.is_eating = True

    def die(self):
        self.dead = True

    def reset(self):
        self.positions = [Vector2(0, 0)]
        self.dead = False
        self.level = 1
        self.speed = self.start_speed

    def handle_keys(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.add_to_directions_queue(UP)
            if event.key == pg.K_a:
                self.add_to_directions_queue(LEFT)
            if event.key == pg.K_d:
                self.add_to_directions_queue(RIGHT)
            if event.key == pg.K_s:
                self.add_to_directions_queue(DOWN)

    def update(self, grid_map, frame_counter):
        if not self.dead:
            self.move(grid_map, frame_counter)
        else:
            self.reset()

    def draw(self, grid):
        for position in self.positions:
            grid.draw_on_grid(position, self.body_color, 2)


class Apple(GameObject):

    margin = 4

    def __init__(self, position=Vector2(0, 0), color=APPLE_COLOR):
        super().__init__(position, color)

    def randomize_position(self, avalieble_positions):
        self.set_position(choice(avalieble_positions))

    def draw(self, grid):
        grid.draw_on_grid(self.position, self.body_color, self.margin)


class Wave(GameObject):
    def __init__(self, position, color, deep=15, margin=1):
        super().__init__(position, color)
        self.positions = [self.position]
        self.period = 30
        self.level = 1
        self.deep = deep
        self.margin = margin

    def is_ended(self):
        return self.level == self.deep

    def update(self, grid, frame_counter):
        if self.level < self.deep:
            if (
                frame_counter.get_frame_number()
                % self.period == self.period - 1
            ):
                self.positions = grid.get_coordinates_around(self.positions)
                self.level += 1

    def draw(self, grid):
        for position in self.positions:
            grid.draw_on_grid(position, self.body_color, self.margin)


class DicscoCell(GameObject):
    """Element of disco floor"""

    def __init__(self, position, color=FLOOR_COLOR, margin=0):
        self.position = Vector2(position)
        self.margin = margin

        # Use lists to change colors in dynamic
        self.origin_color = list(color)
        self.current_color = list(color)

        self.is_color_changed = False

    def return_to_own_color(self):
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

    def change_color(self, color):
        for i in range(3):
            if color[i] > 255:
                self.current_color[i] = 255
            else:
                self.current_color[i] = color[i]
        self.is_color_changed = True

    def update(self):
        if self.is_color_changed:
            self.return_to_own_color()
        else:
            self.change_color(list(get_random_color(40)))

    def draw(self, grid):
        grid.draw_on_grid(self.position,
                          tuple(self.current_color),
                          self.margin)


def get_random_color(max_color_saturation=255):
    return tuple(randint(0, max_color_saturation) for _ in range(3))


def get_avalieble_positions(grid, snake):
    avalieble_positions = (set(grid.get_all_cells_coordinates())
                           - set(snake.get_all_positions()))
    return list(avalieble_positions)


def handle_keys(handlers):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        else:
            for handler in handlers:
                handler.handle_keys(event)


def main():

    pg.init()

    # Initialize of units.
    grid = Grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)
    frame_counter = FrameCounter(FPS)

    # Initialize of GameObjects
    snake = Snake((0, 0), SNAKE_COLOR)
    current_apple = Apple()
    current_apple.randomize_position(get_avalieble_positions(grid, snake))
    waves = []

    DiscoFlor = [DicscoCell(position)
                 for position in grid.get_all_cells_coordinates()]
    for cell in DiscoFlor:
        cell.change_color(get_random_color(max_color_saturation=40))

    # Make list of objects who handle user events
    # Now it's just snake, but maybe in future there will be more of them
    handlers = [snake]

    while True:
        clock.tick(FPS)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Update and draw background
        for cell in DiscoFlor:
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
            current_apple = Apple()
            current_apple.randomize_position(get_avalieble_positions(grid,
                                                                     snake))

            waves.append(Wave(current_apple.get_position(), WAVE_COLOR))

        # All events handlers handle events
        handle_keys(handlers)

        pg.display.update()
        frame_counter.update()


if __name__ == '__main__':
    main()
