"""
Файл конфигураций проекта

"""
from pathlib import Path

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


class MinioSettings(BaseModel):
    """Конфиг Minio"""

    BUCKET_NAME: str = "test-bucket"
    ENDPOINT: str = "s3.corp.ecoflight.ru:9002"
    ACCESS_KEY: str = "5zIdXsLEuOyJ6L24FUP2"
    SECRET_KEY: str = "5ythQgzkJvfWChnZK3OLRtD1zBVaY1kBp4bWj0nZ"


class AudioConverterSettings(BaseSettings):
    path_to_records_dir: Path = Path(__file__).parent.resolve().parent.parent.joinpath("./records")
    time_to_convert: int = 300

class Settings(BaseSettings):
    """Общий класс в котором инициализированны все классы конфигураций"""

    rabbit: RabbitSettings = RabbitSettings()
    logger_settings: LoggingSettings = LoggingSettings()
    nti_setting: NtiSettings = NtiSettings()
    minio: MinioSettings = MinioSettings()
    audio_converter_settings: AudioConverterSettings = AudioConverterSettings()


    sensor_type: str = "Noise"


settings: Settings = Settings()
