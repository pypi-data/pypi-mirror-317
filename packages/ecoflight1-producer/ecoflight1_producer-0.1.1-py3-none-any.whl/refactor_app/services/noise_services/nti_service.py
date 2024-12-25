"""
Реализация логики для шумомера с nti

"""

import time

import serial

from refactor_app.core.services.base_noise_sensor_service import NoiseSensorService
from refactor_app.repositories.noise.noise_repository import NoiseRepository
from refactor_app.core.database.sqlite import get_connection_sqlite
from refactor_app.utils.nti_utils import NtiAudioUtils
from refactor_app.core.services.base_noise_equivalent import Equivalent
from refactor_app.schemas.noise_schemas import NoiseMessage
from refactor_app.utils.calculate_utils import Calculator
from refactor_app.core.config import settings
from refactor_app.utils.system_utils import SystemUtils
from refactor_app.core.logging_config import logger
from refactor_app.services.noise_services.event_service import EventService


class NtiService(NoiseSensorService):
    """
    create - метод для считывания значений и записи в БД

    get_message - получение значений шумовых данных необходимых для добавления в БД

    get_la_max - получение текущего уровня шума в дБА

    get_rta - получение тртеьоктавного спектра

    get_dt - получение временной разницы между измерениями

    """
    FIRST_STRING = b"*RST\n"
    SECOND_STRING = f"INPUT:RANGE {settings.nti_setting.input_range}\n".encode()
    THIRD_STRING = b"INIT START\n"

    def __init__(self):
        self.prefix = "NOISE_"

        # классы репозиториев для запросов в Sqlite
        self.noise_repository: NoiseRepository = NoiseRepository(db=get_connection_sqlite())

        # Вспомогательные классы
        self.calculator: Calculator = Calculator()
        self.nti_audio_utils: NtiAudioUtils = NtiAudioUtils()
        self.la_eq: Equivalent = Equivalent()
        self.la_eq_hour: Equivalent = Equivalent()
        self.system: SystemUtils = SystemUtils()
        self.sensor_name = self.system.get_sensor_name(prefix=self.prefix)

        # Сервис обработки шумового события
        self.event_service = EventService(
            db=get_connection_sqlite(), sensor_name=self.sensor_name
        )

    def run(self) -> None:
        """
        1) Считываем данные с NTi
        2) Формируем сообщения, валидируем
        3) Формируем запрос к БД
        4) Выполняем запрос

        """
        start_time = time.time()

        with self.nti_audio_utils.connection as ser:
            ser.write(self.FIRST_STRING)
            ser.write(self.SECOND_STRING)
            ser.write(self.THIRD_STRING)
            logger.info("Start noise data proccessing...")

            while True:
                noise_message: NoiseMessage = self.get_message(ser=ser)
                logger.debug(f"noise_data: {noise_message}")

                self.noise_repository.create(noise_message=noise_message)

                self.event_service.process(
                    la_max=noise_message.la_max, time_stamp=noise_message.time_stamp
                )

                time.sleep(1.0 - ((time.time() - start_time) % 1.0))

    def get_message(self, ser: serial.Serial) -> NoiseMessage:
        """
        Cоздание сообщения шумовой метрики

            la_max: float - текущий уровня шума в дБА
            la_eq: float - эквивалентный уровня шума в дБА за день/ночь
            la_eq_hour: float - эквивалентный уровня шума в дБА за час
            rta: str - третьоктавный спектр
            dt: float - временная разница между измерениями
            time_stamp: str - время измерения
            serial_number: str - имя датчика
            message_type: str - тип сообщения

        """

        la_max = self.get_la_max(ser=ser)

        rta = self.get_rta(ser=ser)

        dt = self.get_dt(ser=ser)

        la_eq = self.calculator.equivalent_la(la_max=la_max, la_eq=self.la_eq)
        la_eq_hour = self.calculator.equivalent_la(
            la_max=la_max, la_eq=self.la_eq_hour, per_hour=True
        )

        noise_message = NoiseMessage(
            la_max=la_max,
            la_eq=la_eq,
            la_eq_hour=la_eq_hour,
            rta=rta,
            dt=dt,
            time_stamp=str(time.time()),
            sensor_name=self.system.get_sensor_name(prefix=self.prefix),
        )

        return noise_message

    def get_la_max(self, ser: serial.Serial) -> float:
        """
        Получение текущего уровня шума в дБА

         Args:
            ser: порт подключения к NTi

        Returns:
            float: текущий уровень шума в дБ
        """

        ser.write(b"MEAS:INIT\n")
        ser.write(b"MEAS:SLM:123? LAS\n")
        line = ser.readline()
        return float(str(line.decode("utf-8"))[0:4])

    def get_rta(self, ser: serial.Serial) -> str:
        """
        Получение третьоктавного спектра

        Args:
            ser: порт подключения к NTi

        Returns:
            str: третьоктавный спектр
        """
        ser.write(b"MEAS:SLM:RTA? LIVE\n")
        line = ser.readline()
        return str(line.decode("utf-8")).split(" ")[0]

    def get_dt(self, ser: serial.Serial) -> float:
        """
        Получение временной разницы между измерениями

        Args:
            ser: порт подключения к NTi

        Returns:
            float: временная разница между измерениями
        """
        ser.write(b"MEAS:DTTIme?\n")
        line = ser.readline()
        return float(str(line.decode("utf-8"))[0:4])
