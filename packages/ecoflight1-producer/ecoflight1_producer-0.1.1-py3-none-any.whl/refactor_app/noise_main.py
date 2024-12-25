"""
Main файл для управления запуском устройств

"""

from typing import Optional

from refactor_app.core.database.sqlite import create_database
from refactor_app.core.logging_config import logger
from refactor_app.core.services.base_noise_sensor_service import NoiseSensorService
from refactor_app.core.services.base_sensor_service import SensorService
from refactor_app.services.noise_services.umik_service import UmikService
from refactor_app.services.noise_services.nti_service import NtiService
from refactor_app.utils.umik_utils import UmikAudioUtils
from refactor_app.utils.nti_utils import NtiAudioUtils


# TODO Нужно реализовать кастомные ошибки
class NoiseSensorManager:
    """
    Класс для управления запуском шумомеров

    check_sensors - идентификация шумомеров

    run - запуск одного из сервисов, проверка количества подключенных устройств

    """

    def __init__(self) -> None:
        self.noise_service: Optional[NoiseSensorService] = self.define_noise_service()

    def define_noise_service(self) -> Optional[SensorService]:
        """Определение типа шумомера и поиск подключенного устройства"""
        if UmikAudioUtils.find_sensor():
            return UmikService()
        elif NtiAudioUtils.find_sensor():
            return NtiService()
        return None

    def run(self) -> None:
        """Запуск шумомера"""

        try:
            if not self.noise_service:
                raise KeyError("Устройства не обнаружены")

            self.noise_service.run()
        except ValueError as e:
            logger.exception(f"Ошибка {e}")
        except KeyError as e:
            logger.exception(f"Ни одного устройство не подключено {e}")


noise_sensor_manager = NoiseSensorManager()


def main():
    try:
        create_database()
        noise_sensor_manager.run()
    except KeyboardInterrupt:
        logger.exception('Остановка программы')


if __name__ == "__main__":
    main()
