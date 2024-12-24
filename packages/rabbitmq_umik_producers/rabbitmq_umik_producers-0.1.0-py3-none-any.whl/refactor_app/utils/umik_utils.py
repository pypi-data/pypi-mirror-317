"""Модуль для вспомогательного класса PyAudio для взаимодействия с микрофоном"""

from typing import Optional

import pyaudio

from refactor_app.core.logging_config import logger


class UmikAudioUtils:
    """
    Класс для взаимодейсвия с pyaudio

    create_stream - создание соединения

    get_umik_index -  поиск микрофона для записи звука

    """

    def __init__(self):
        self.format = pyaudio.paInt24
        self.channels = 1
        self.rate = 48000
        self.chunk = 48000
        self.device_index = None

    def create_stream(self) -> pyaudio.Stream:
        p = pyaudio.PyAudio()

        # Открываем стрим для записи с микрофона
        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.find_sensor(),
        )

        logger.info("Recording...")

        return stream

    @staticmethod
    def find_sensor() -> Optional[int]:
        """Метод для для поиска микрофона Umik"""
        p = pyaudio.PyAudio()
        name = [
            i
            for i in range(p.get_device_count())
            if p.get_device_info_by_index(i).get("name").startswith("Umik")
        ]
        if not name:
            return None
        return name[0]
