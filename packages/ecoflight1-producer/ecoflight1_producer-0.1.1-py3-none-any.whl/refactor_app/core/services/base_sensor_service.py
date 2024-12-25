"""
Модуль абстрактной реализации SensorService

"""

from abc import ABC, abstractmethod

from refactor_app.schemas.noise_schemas import NoiseMessage


class SensorService(ABC):
    """Базовый клас для реализации бизнес логики"""

    @abstractmethod
    def run(self) -> None: ...

    @abstractmethod
    def get_message(self) -> NoiseMessage: ...
