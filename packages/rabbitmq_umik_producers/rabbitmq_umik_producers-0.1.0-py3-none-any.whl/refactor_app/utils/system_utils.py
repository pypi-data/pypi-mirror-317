"""
Модуль для вспомогательного класса SystemUtils для взаимодействия с ОС

"""

import os
import sys

from refactor_app.core.logging_config import logger


class SystemUtils:
    @staticmethod
    def get_sensor_name(prefix: str = "") -> str:
        """Метод для получения имени датчика"""
        return prefix + os.uname().nodename

    @staticmethod
    def get_correction_param() -> float:
        param, correction = sys.argv[1:]

        correct: float = float(correction)

        if param != "-c":
            logger.exception(f"Неизвестный параметр запуска: {param}")
            raise KeyError("Неизвестный параметр запуска")
        elif correct < 0 or correct > 100:
            logger.exception(f"Неверное значение корректировочной константы: {correction}")
            raise ValueError("Неверное значение корректировочной константы")
        else:
            return correct
