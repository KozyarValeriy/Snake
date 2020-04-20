import subprocess
import sys
import time
import random
import copy

from pynput.keyboard import Key, Listener


from snake import Snake, SnakeList


# Константа с классом для змейки
SNAKE_CLASS = SnakeList

# определние функции для расчета времени на основе операционной системы
time_func = time.perf_counter if sys.platform.startswith('win') else time.time

# начальные значения переменных
_direction = 2

# Определение функции очистки экрана в зависимости от операционной системы
if sys.platform.startswith('win'):
    def screen_clear():
        subprocess.call(['cmd.exe', '/C', 'cls'])
else:
    def screen_clear():
        subprocess.call(['clear'])


def print_field(grid: list, snake_body: list, eat: tuple, symbol_snake: str, score: int, symbol_eat: str = '*'):
    """ Функция для отрисовки игрового поля

    :param grid: текущее игровое поле,
    :param snake_body: координаты тела змейки,
    :param eat: координаты еды,
    :param symbol_snake: символ для отрисовки змейки,
    :param score: кол-во очков,
    :param symbol_eat: символ для отрисовки еды.
    """
    # s = '\tYour score: {0}'.format(_score)
    plot = copy.deepcopy(grid)
    plot[0].append('    Your score: {0}'.format(score))
    # добавляем еду на поле
    plot[eat[1]][eat[0]] = symbol_eat
    # добавляем тело змейки
    for x, y in snake_body:
        if plot[y][x] in (" ", "*"):
            plot[y][x] = symbol_snake
        else:
            # если было пересечение, то отмечаем 'x'
            plot[y][x] = 'x'
    screen_clear()
    print()
    for row in range(len(plot)):
        print(''.join(plot[row]))


def get_grid(size: tuple) -> list:
    """ Функция для получения чистого игрового поля

    :param size: размеры игрового поля,
    :return: игровое поле в формате двумерного массива
    """
    grid = []
    for row in range(size[1]):
        if row == 0:
            line = ['╔'] + ['═'] * (size[1] - 2) + ['╗']
        elif row == size[1] - 1:
            line = ['╚'] + ['═'] * (size[1] - 2) + ['╝']
        else:
            line = ['║'] + [' '] * (size[1] - 2) + ['║']
        grid.append(line)
    return grid


def timer(delay=0.15) -> bool:
    """ Функция для счетчика времени

    :param delay: задержка в секундах.
    """
    try:
        # пробуем получить атрибут функции
        getattr(timer, 'time')
    except AttributeError:
        # если его нет, то добавляем атрибут и записываем в него время
        timer.time = time_func()
    if time_func() - timer.time > delay:
        timer.time = time_func()
        return True
    return False


def on_press(key):
    """ Функция обработчик нажатий

    :param key: кнопка, которая нажата в текущий момент.
    """
    global _direction
    if key == Key.right:
        # нажатие кнопки направо
        if _direction != 2:
            # если до этого змейка ползла не влево
            _direction = 0
    elif key == Key.left:
        # нажатие кнопки налево
        if _direction != 0:
            # если до этого змейка ползла не вправо
            _direction = 2
    elif key == Key.up:
        # нажатие кнопки вверх
        if _direction != 3:
            # если до этого змейка ползла не вниз
            _direction = 1
    elif key == Key.down:
        # нажатие кнопки вниз
        if _direction != 1:
            # если до этого змейка ползла не ввехр
            _direction = 3


def generate_eat(size: tuple, snake_head: tuple) -> tuple:
    """ Метод для генерации еды на поле

    :param size: размеры игрового поля,
    :param snake_head: координаты головы змейки,
    :return: координаты еды на поле.
    """
    eat = (random.randint(1, size[0] - 2), random.randint(1, size[1] - 2))
    while eat == snake_head:
        eat = (random.randint(1, size[0] - 2), random.randint(1, size[1] - 2))
    return eat


def main(size: tuple, snake_class: type(Snake)):
    snake = snake_class(max_x=size[0], max_y=size[1])
    score = 0
    grid = get_grid(size=size)
    eat = generate_eat(size=size, snake_head=snake.get_head())
    delay = 0.2
    with Listener(on_press=on_press):
        while not snake.incident:
            if timer(delay=delay):
                if eat == snake.get_head():
                    snake.move(_direction, grow=True)
                    eat = generate_eat(size=size, snake_head=snake.get_head())
                    score += 1
                    if score % 3 == 0 and delay > 0.05:
                        delay = round(delay - 0.02, 2)
                else:
                    snake.move(_direction, grow=False)
                print_field(grid, snake.get_body(), eat, snake.symbol, score)
                print(delay)
        print('You lose!!!')


if __name__ == "__main__":
    main((20, 20), SNAKE_CLASS)
