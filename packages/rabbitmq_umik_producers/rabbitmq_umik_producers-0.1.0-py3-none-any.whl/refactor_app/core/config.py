"""
Файл конфигураций проекта

"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RabbitSettings(BaseModel):
    """Конфиг RabbitMQ"""

    RABBIT_HOST: str = "mq.noise.aero"
    RABBIT_PORT: int = 6672
    RABBIT_LOGIN: str = "eco"
    RABBIT_PASSWORD: str = "eco"
    RABBIT_EXCHENGES: str = "NoiseExchange"


class PyAudioSettings(BaseModel):
    """Конфиг для PyAudio"""

    pass


class LoggingSettings(BaseModel):
    """Конфиг для логирнования"""

    log_level: str = "DEBUG"  # в prod нужно изменить уровень на INFO


class NtiSettings(BaseModel):
    input_range: str = "L"
    time_weighting: str = "S"
    frequency_weighthing: str = "A"
    mask: str = "/dev/ttyACM*"


class Settings(BaseSettings):
    """Общий класс в котором инициализированны все классы конфигураций"""

    rabbit: RabbitSettings = RabbitSettings()
    logger_settings: LoggingSettings = LoggingSettings()
    nti_setting: NtiSettings = NtiSettings()

    sensor_type: str = "Noise"


settings: Settings = Settings()
