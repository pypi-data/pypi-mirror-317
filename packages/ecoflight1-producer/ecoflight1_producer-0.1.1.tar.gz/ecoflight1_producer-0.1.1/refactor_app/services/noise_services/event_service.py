"""
Модуль реализации сервиса обработки шумового события

"""

import sqlite3
from collections import deque
from uuid import uuid4
from datetime import datetime
from typing import Deque

from refactor_app.core.services.noise_event import NoiseEvent
from refactor_app.schemas.noise_schemas import EventMessage, NotificationMessage
from refactor_app.repositories.noise.notification_repository import NotificationRepository
from refactor_app.repositories.noise.event_repository import EventRepository
from refactor_app.repositories.noise.audio_converter_repository import RawNoiseAudioRepository
from refactor_app.schemas.audio_converter_schemas import RawNoiseAudioMessage
from refactor_app.core.logging_config import logger


class EventService:
    """
    Класс для обработки шумового события. Регистрируем threshold, начинаем обработку события

    noise_event_process - main метод обработки события в котором проверяются необходимые переменные
                          в зависимости от проверки, изменяются состояния события

    noise_event_start - фиксация старта шумового события
        1) проверка что это начало шумового события if not self.noise_event.is_event:
        2) отправляем уведомление о начале события в БД

    noise_event_close - завершение шумового события if self.noise_event.waiting == 5, то есть прошло пять секунд с последнего превышения
        1) формируем EventMessage
        2) отправляем в БД
        3) сбрасываем waiting, is_event

    """
    WINDOW_SIZE = 5

    def __init__(
        self, db: sqlite3.Connection, sensor_name: str, to_record: bool = False
    ) -> None:
        self.noise_event = NoiseEvent()
        self.sensor_name = sensor_name
        self.to_record = to_record
        self.notification_repository: NotificationRepository = NotificationRepository(db=db)
        self.event_repository: EventRepository = EventRepository(db=db)
        self.raw_records_repository: RawNoiseAudioRepository = RawNoiseAudioRepository(connection=db)
        self.threshold: float = 0.0

        self.noise_buffer: Deque = deque(maxlen=5)
        self.event_audio_buffer: Deque = deque()  

    def process(self, la_max: float, time_stamp: str, data: bytes):
        """
        Обработка шумового события

        1) Обновляем threshold
        2) проверяем что это конец шумового события self.noise_event.waiting
        3) проверяем больше ли la_max threshold
            если да:
                фиксируем начало события
        4) если это шумовое событие, но нет превышения звука:
            увеличиваем NoiseEvent.event_counter_below_threshold на 1

        """
        self.noise_buffer.append(data)

        # опеределяем сейчас день или ночь по time_stamp
        self.threshold = self.get_correct_noise_threshold(time_stamp)

        if self.noise_event.event_counter_below_threshold == self.WINDOW_SIZE:
            # self.noise_record_queue.extend(self.noise_buffer)
            self.close()

        if self.noise_event.is_event and len(self.event_audio_buffer) <= 60:
            logger.debug(len(self.event_audio_buffer))
            self.event_audio_buffer.append(data)

        # Начало шумового события
        if la_max > self.threshold:
            self.noise_event.time_stamp_end = time_stamp
            self.start(time_stamp=time_stamp, la_max=la_max)
            self.noise_event.event_counter_below_threshold = 0

        elif self.noise_event.is_event:
            self.noise_event.event_counter_below_threshold += 1

    def start(self, time_stamp: str, la_max: float) -> None:
        """
        Обработка начала шумового события
        Если is_event == False:
            устанавливаем True
            добавляем event_id
            фиксируем время начала шумового события

        При каждом превышении проверяем больше ли текущее максимальное значение поступившего
        если да:
            Обновляем его и фиксируем время

        """
        if not self.noise_event.is_event:
            self.noise_event.uuid = str(uuid4())
            self.noise_event.is_event = True
            self.noise_event.time_stamp_start = time_stamp
            self.noise_event.event_la_max = la_max
            self.noise_event.time_stamp_max = time_stamp
            self.event_audio_buffer.extend(self.noise_buffer)

            notification_message: NotificationMessage = NotificationMessage(
                notification_id=self.noise_event.uuid,
                sensor_name=self.sensor_name,
                notification_ts=str(self.noise_event.time_stamp_start),
                threshold=self.threshold,
            )
            # добавляем сообщение в таблицу notifications о начале шумового события
            self.notification_repository.create(notification_message=notification_message)

        # Обновление максимального значения la_max
        if self.noise_event.event_la_max < la_max:
            self.noise_event.event_la_max = la_max
            self.noise_event.time_stamp_max = time_stamp

    def close(self) -> None:
        """
        Обработка окончания шумового события
        Если waiting == 5:
            Значит шумовое событие закончилось
            Обнуляем is_evet, event_la_max, waiting

            Отправляем данные о ивенте в БД

        """
        # self.noise_record_queue.extend(self.noise_buffer)

        event_message = EventMessage(
            event_id=self.noise_event.uuid,
            sensor_name=self.sensor_name,
            event_la_max=self.noise_event.event_la_max,
            time_stamp_start=str(self.noise_event.time_stamp_start),
            time_stamp_max=str(self.noise_event.time_stamp_max),
            time_stamp_end=str(self.noise_event.time_stamp_end),
            threshold=self.threshold,
        )
        # Записываем в таблицу events, данные шумового события
        self.event_repository.create(event_message=event_message)

        if self.to_record:
            raw_audio = b"".join(self.event_audio_buffer)
            raw_noise_audio_message = RawNoiseAudioMessage(
                event_id=self.noise_event.uuid,
                bytestring=raw_audio,
                time_stamp=self.noise_event.time_stamp_start
            )
            self.raw_records_repository.create(
                raw_data=raw_noise_audio_message
            )
            self.event_audio_buffer.clear()
        
        # Сбрасываем значения NoiseEvent до дефолтных
        self.noise_event.reset_to_default()

    @staticmethod
    def get_correct_noise_threshold(time_stamp: str):
        """
        Метод для расчета threshold

        в промежуток с 7 утра до 23 - это день threshold = 70
        ночью 60

        """
        current_hour = datetime.fromtimestamp(float(time_stamp)).hour
        return 70 if 7 <= current_hour < 23 else 60
