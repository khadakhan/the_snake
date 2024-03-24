from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов игры.

class GameObject:
    """Класс GameObject является родительским классом для всех элементов
    игры.
    """

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def __init__(self, position=position,
                 body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, предназначенный для переопределения в дочерних
        классах.
        """
        pass


class Apple(GameObject):
    """Класс Apple описывает яблоко и наследуется от класса
    GameObject.
    """

    body_color = (255, 0, 0)

    def __init__(self):
        super().__init__(GameObject.position, Apple.body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для установления случайного положения яблока."""
        return ((randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                 randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
                )

    def draw(self):
        """Метод отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake описывает змейку и наследуется от класса
    GameObject.
    """

    length = 1
    positions = [GameObject.position]  # Позиция головы на старте.
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self):
        super().__init__(GameObject.position, Snake.body_color)
        self.positions = Snake.positions
        self.length = Snake.length
        self.direction = Snake.direction
        self.next_direction = Snake.next_direction
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
        old_head_position = self.get_head_position()
        new_head_position = ((old_head_position[0] + self.direction[0]
                              * GRID_SIZE) % SCREEN_WIDTH,
                             (old_head_position[1] + self.direction[1]
                              * GRID_SIZE) % SCREEN_HEIGHT
                             )
        if len(self.positions) > 2 and new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop(-1)

    def draw(self):
        """Метод отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние после столкновения
        с собой.
        """
        self.length = 1
        self.positions = [GameObject.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill((0, 0, 0))


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной метод."""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
