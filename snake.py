"""
    Скрипт с описанием класса для змейки.
"""
from collections import Counter
from abc import ABC, abstractmethod

from body import Body, BodyList


class Snake(ABC):

    def __init__(self, max_x: int, max_y: int, symbol: str = "▪", preset_count: int = 3):
        """ Метод инициализации змейки

        :param max_x: максимальное значение по оси X,
        :param max_y: максимальное значение по оси Y,
        :param symbol: символ для отрисовки звейки,
        :param preset_count: кол-во начальных точек в змейке.
        """
        self._max_x = max_x
        self._max_y = max_y
        self._symbol = symbol

        self._body = self._set_body()
        # наполнение тела змейки
        self._preset_body(preset_count)
        # было ли столкновение
        self._incident = False

    @abstractmethod
    def _set_body(self) -> Body:
        """ Метод для получения элемента для тела змейки """
        pass

    @property
    def incident(self) -> bool:
        """ Свойство для получения, было ли столкновение """
        return self._incident

    @property
    def symbol(self) -> str:
        """ Свойство для получения символа для отрисовки змейки """
        return self._symbol

    def get_body(self) -> list:
        """ Метод для получения списка координат тела змейки """
        return self._body.to_list()

    def get_head(self) -> tuple:
        """ Метод для получения первого элемента """
        return self._body.get_first()

    def _preset_body(self, preset_count: int):
        """ Метод для получения начальных звеньев в змейке

        :param preset_count: кол-во начальных точек в змейке.
        """
        preset_count = 1 if preset_count < 1 else preset_count
        x = self._max_x // 2 - preset_count // 2
        y = self._max_y // 2

        for i in range(preset_count):
            self._body.add_tail((x, y))
            x += 1

    def move(self, direction: int, grow: bool = False):
        """ Метод для движения змейки в заданном направлении

        :param direction: напрвление змейки (0 - направо,
                                             1 - вверх,
                                             2 - навлево,
                                             3 - вниз).
        :param grow: требуется ли увелисть длину змейки.
        """
        if not grow:
            self._body.pop()
        first = self._body.get_first()
        if direction == 0:
            first = (first[0] + 1, first[1])
        elif direction == 1:
            first = (first[0], first[1] - 1)
        elif direction == 2:
            first = (first[0] - 1, first[1])
        else:
            first = (first[0], first[1] + 1)

        self._body.add_head(first)

        if not all(0 < coord[0] < self._max_x - 1 for coord in self._body.to_list()):
            # Если вышли за границы поля по X
            self._incident = True

        if not all(0 < coord[1] < self._max_y - 1 for coord in self._body.to_list()):
            # Если вышли за границы поля по Y
            self._incident = True

        if any(value > 1 for value in Counter(self._body.to_list()).values()):
            # Если пересекли саму себя
            self._incident = True


class SnakeList(Snake):
    def _set_body(self) -> Body:
        """ Метод для получения элемента для тела змейки """
        return BodyList()
