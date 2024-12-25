"""
Модуль абстрактной реализации BaseNoiseSensorService

"""

from abc import ABC, abstractmethod

from refactor_app.core.services.base_sensor_service import SensorService


class NoiseSensorService(SensorService, ABC):
    """Базовый клас для реализации бизнес логики"""

    @abstractmethod
    def get_la_max(self) -> float:
        pass

    @abstractmethod
    def get_rta(self) -> str:
        pass

    @abstractmethod
    def get_dt(self) -> float:
        pass
