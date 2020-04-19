"""
    Скрипт с классом тела змейки
"""
from abc import ABC, abstractmethod


class Body(ABC):
    """ Абстрактный класс для тела змейки """

    @abstractmethod
    def add_head(self, value: tuple):
        """ Метод для добавления в начало

        :param value: координаты в виде кортежа для добавления в начало.
        """
        pass

    @abstractmethod
    def add_tail(self, value: tuple):
        """ Метод для добавления в конец

        :param value: координаты в виде кортежа для добавления в конец.
        """
        pass

    @abstractmethod
    def get_first(self) -> tuple:
        """ Метод для получения первого элемента

        :return: первый элемент тела
        """
        pass

    @abstractmethod
    def pop(self) -> tuple:
        """ Метод для удаления с конца тела

        :return: кортеж последних координат в виде (x, y)
        """
        pass

    @abstractmethod
    def to_list(self) -> list:
        """ Метод для получения списка из тела змейки

        :return: список координат тела змейки
        """
        pass


class BodyList(Body):
    """ Класс для хранения тела змейки из списка """

    def __init__(self):
        """ Метод инициализации тела змейки """
        self._body = []

    def add_head(self, value: tuple):
        """ Метод для добавления в начало """
        self._body.insert(0, value)

    def add_tail(self, value: tuple):
        """ Метод для добавления в конец """
        self._body.append(value)

    def get_first(self) -> tuple:
        """ Метод для получения первого элемента """
        return self._body[0]

    def pop(self) -> tuple:
        """ Метод для удаления с конца тела """
        return self._body.pop()

    def to_list(self) -> list:
        """ Метод для получения списка из тела змейки """
        return self._body
