"""
Базовый класс для реализации SensorReposiotiry, классов для взаимодейсвия с базой данных

"""

from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """Абстрактный класс для репозиториев всех сенсоров"""

    @abstractmethod
    def create(self): ...
