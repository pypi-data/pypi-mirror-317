"""
Модуль для реализации основной логики

"""

import time
from collections import deque
from typing import Deque, Optional

import numpy as np
from acoustics.signal import third_octaves

from refactor_app.core.services.base_noise_equivalent import Equivalent
from refactor_app.core.services.base_noise_sensor_service import NoiseSensorService
from refactor_app.core.database.sqlite import get_connection_sqlite
from refactor_app.core.logging_config import logger
from refactor_app.utils.umik_utils import UmikAudioUtils
from refactor_app.utils.calculate_utils import Calculator
from refactor_app.utils.system_utils import SystemUtils
from refactor_app.repositories.noise.noise_repository import NoiseRepository
from refactor_app.schemas.noise_schemas import NoiseMessage
from refactor_app.services.noise_services.event_service import EventService


class UmikService(NoiseSensorService):
    """
    UmikSerivce - класс в котором реализованна логика считывания и записи звука

    create - метод для считывания расчета значений и записи звука в базу

    get_la_max - получение текущего уровня шума в дБА

    get_rta - получение тртеьоктавного спектра

    get_dt - получение временной разницы между измерениями

    """
    MAX_LEN = 11

    def __init__(self) -> None:
        self.prefix = "NOISE_"

        # классы репозиториев для запросов в Sqlite
        self.noise_repository: NoiseRepository = NoiseRepository(db=get_connection_sqlite())

        # Вспомогательные классы
        self.calculator: Calculator = Calculator()
        self.system: SystemUtils = SystemUtils()
        self.umik_audio_utils: UmikAudioUtils = UmikAudioUtils()

        # Обьекты необходимые для создания NoiseMessage
        self.la_eq: Equivalent = Equivalent()
        self.la_eq_hour: Equivalent = Equivalent()

        # Буфер для вычисления la_max
        self.buffer_pressures: Deque = deque(maxlen=self.MAX_LEN)

        self.current_time: float = 0.0
        self.old_time: Optional[float] = None
        self.filter_params = self.calculator.get_filter()

        # Получаем коректировочную константу с команды запуска скрипта
        self.correction_constant = self.system.get_correction_constant()

        self.stream = self.umik_audio_utils.create_stream()
        self.sensor_name = self.system.get_sensor_name(prefix=self.prefix)

        # обьект для фиксации шумового события
        self.event_service: EventService = EventService(
            db=get_connection_sqlite(), sensor_name=self.sensor_name, to_record=True
        )

    def run(self):
        """
        1) Получаем данные с микрофона
        2) Обрабатываем данные вычисляем необходимые значения
        3) формируем запрос к бд
        4) выполняем запрос

        """
        start_time = time.time()

        try:
            if not self.correction_constant:
                raise ValueError("Корректировочная константа задана неверно")

            while True:
                logger.info("Start noise data proccessing...")
                try:
                    # получаем значения с микрофона
                    data = self.stream.read(self.umik_audio_utils.chunk)

                    # Получаем актуальное время
                    self.current_time = time.time()
                    # self.noise_buffer.append(data)

                    # Формируем сообщение
                    noise_message: NoiseMessage = self.get_message(
                        data=data, time_stamp=self.current_time
                    )
                    logger.debug(f"noise_data: {noise_message}")

                    # Создаем запись в базе sqlite
                    self.noise_repository.create(noise_message=noise_message)

                    # Регистрация шумового события
                    self.event_service.process(
                        la_max=noise_message.la_max, time_stamp=noise_message.time_stamp, data=data
                    )

                    time.sleep(1.0 - ((time.time() - start_time) % 1.0))

                except Exception:
                    logger.exception("Ошибка при которой скрипт должен упасть и перезагрузиться")
                    break
        except ValueError as e:
            logger.exception(e)

    def get_message(self, data: np.ndarray, time_stamp: float) -> NoiseMessage:
        """
        Вычисление необходимых метрик и формирование noise-сообщения

            la_max: float - текущий уровня шума в дБА
            la_eq: float - эквивалентный уровня шума в дБА за день/ночь
            la_eq_hour: float - эквивалентный уровня шума в дБА за час
            rta: str - третьоктавный спектр
            dt: float - временная разница между измерениями
            time_stamp: str - время измерения
            serial_number: str - имя датчика
            message_type: str - тип сообщения

        """

        # Формирование массива значений для окна сглаживания
        data_in_24_bit = self.calculator.convert_signal_in_24_bit(data)

        # Применение частотной корректировки
        weighted_data = self.calculator.frequency_weighting(
            signal=data_in_24_bit, B=self.filter_params[0], A=self.filter_params[1]
        )

        self.buffer_pressures.append(self.calculator.ac_rms(weighted_data))

        pressures = np.array(self.buffer_pressures)
        logger.debug(f"pressures {pressures}")

        la_max = self.get_la_max(pressures=pressures)  # уровень шума

        # dt - разница во времени между двума операциями
        dt = self.get_dt()
        # tz_seconds = int(tz) * 60 * 60 # корректировка по таймзоне

        noise_message = NoiseMessage(
            la_max=la_max,
            la_eq=self.calculator.equivalent_la(la_max=la_max, la_eq=self.la_eq),
            la_eq_hour=self.calculator.equivalent_la(
                la_max=la_max, la_eq=self.la_eq_hour, per_hour=True
            ),
            rta=self.get_rta(data=data_in_24_bit),  # третьоктавный спектр
            dt=dt,
            time_stamp=str(time_stamp),
            sensor_name=self.sensor_name,
        )

        return noise_message

    def get_la_max(self, pressures: np.ndarray) -> float:
        """
        Получение текущего уровня шума в дБА

        Args:
            pressures: массив давлений за прошедшие 11 секунд

        Returns:
            float: текущий уровень шума в дБ
        """
        la_max = round(
            self.calculator.time_weighting(p_series=pressures) - self.correction_constant + 94,
            1,
        )
        return la_max

    def get_rta(self, data: list, fs: float = 48000) -> str:
        """Метод для расчёта третьоктавного спектра

        Args:
            data: сигнал с микрофона
            fs: частота дискретизация(размер массива data)

        Returns:
            str: значения уровня шума на каждый частоте третьоктавного спектра

        """

        rta = third_octaves(p=data, fs=fs)[1]
        rta_rounded = [str(np.round(rta[i], 1)) for i in range(len(rta))]
        return ", ".join(rta_rounded)

    def get_dt(self) -> float:
        """
        Получение временной разницы между измерениями

        Returns:
            float: временная разница между измерениями
        """
        if self.old_time is None:
            self.old_time = self.current_time
            return 1.0
        else:
            dt = self.old_time - self.current_time
            self.old_time = self.current_time

            return dt
