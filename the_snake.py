from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GAME_OBJECT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
STONE_COLOR = (224, 224, 224)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Игра Змейка. Для выхода-нажмите ESC. Для увел/уменьш '
                       'скорости-нажмите s/d.')

# Настройка времени:
clock = pg.time.Clock()

# Настройка словаря направлений
NEXT_DIR_DIC = {(LEFT, pg.K_UP): UP,
                (RIGHT, pg.K_UP): UP,
                (LEFT, pg.K_DOWN): DOWN,
                (RIGHT, pg.K_DOWN): DOWN,
                (UP, pg.K_LEFT): LEFT,
                (DOWN, pg.K_LEFT): LEFT,
                (UP, pg.K_RIGHT): RIGHT,
                (DOWN, pg.K_RIGHT): RIGHT}


class GameObject:
    """Класс GameObject является родительским классом для всех элементов
    игры.
    """

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.position = GAME_OBJECT_POSITION
        self.body_color = body_color
        self.speed = 10

    def draw(self):
        """Абстрактный метод, предназначенный для переопределения
        в дочерних классах.
        """
        raise NotImplementedError(f'В классе {self.__class__.__name__} не'
                                  'переопределен абстрактный метод базового'
                                  'класса')

    def draw_rect(self, position, body_color):
        """Метод отрисовывает квадратик"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс Stone описывает камень и наследуется от класса
    GameObject.
    """

    def __init__(self, snake_positions, apple_position):
        super().__init__(body_color=STONE_COLOR)
        self.randomize_position(snake_positions or [], apple_position or None)

    def randomize_position(self, snake_positions, apple_position):
        """Метод для установления случайного положения яблока
        с учетом положения змейки.
        """
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if ((self.position not in snake_positions)
                    and (self.position != apple_position)):
                break

    def draw(self):
        """Метод отрисовывает камень на игровой поверхности."""
        self.draw_rect(self.position, self.body_color)


class Apple(GameObject):
    """Класс Apple описывает яблоко и наследуется от класса
    GameObject.
    """

    def __init__(self, snake_positions):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(snake_positions or [])

    def randomize_position(self, snake_positions, stone_position=None):
        """Метод для установления случайного положения яблока
        с учетом положения змейки.
        """
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if ((self.position not in snake_positions)
                    and (self.position != stone_position)):
                break

    def draw(self):
        """Метод отрисовывает яблоко на игровой поверхности."""
        self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    """Класс Snake описывает змейку и наследуется от класса
    GameObject.
    """

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.next_direction = None
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляет позицию змейки (координаты каждой секции)
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась (не съела яблоко).
        """
        old_head_position_w, old_head_position_h = self.get_head_position()
        direction_w, direction_h = self.direction
        new_head_position = ((old_head_position_w + direction_w
                              * GRID_SIZE) % SCREEN_WIDTH,
                             (old_head_position_h + direction_h
                              * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)
        else:
            self.last = None

    def draw(self):
        """Метод отрисовывает змейку на экране, затирая след."""
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        # Отрисовка головы змейки
        self.draw_rect(self.get_head_position(), self.body_color)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние после столкновения
        с собой.
        """
        self.length = 1
        self.positions = [GAME_OBJECT_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif event.key == pg.K_s:
                if 1 <= game_object.speed <= 19:
                    game_object.speed += 1
            elif event.key == pg.K_d:
                if 2 <= game_object.speed <= 20:
                    game_object.speed -= 1
            game_object.next_direction = NEXT_DIR_DIC.get((game_object
                                                           .direction,
                                                           event.key))


def main():
    """Основной метод."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)
    stone = Stone(snake.positions, apple.position)
    while True:
        clock.tick(snake.speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions, stone.position)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions, stone.position)
        if snake.get_head_position() == stone.position:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            stone.randomize_position(snake.positions, stone.position)
        apple.draw()
        snake.draw()
        stone.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
