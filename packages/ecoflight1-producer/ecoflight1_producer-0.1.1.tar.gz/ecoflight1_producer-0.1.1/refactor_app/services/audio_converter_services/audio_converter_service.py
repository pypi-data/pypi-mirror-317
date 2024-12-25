"""
Модуль для отправки аудиозаписей в Minio
"""

import time
from pathlib import Path
from typing import Optional

from refactor_app.repositories.noise.audio_converter_repository import RawNoiseAudioRepository
from refactor_app.repositories.noise.minio_repository import MinioRepository

from refactor_app.repositories.noise.noise_record_repository import NoiseRecordRepository
from refactor_app.core.database.sqlite import get_connection_sqlite
from refactor_app.core.config import settings
from refactor_app.core.logging_config import logger
from refactor_app.core.services.raw_record_data import RawRecordData
from refactor_app.schemas.audio_converter_schemas import NoiseRecordMessage, RawNoiseAudioMessage
from refactor_app.utils.system_utils import SystemUtils


#TODO: Изменить путь до папки records, убрать параметры записи в конфиг
class AudioConverterService:
    """
    run - метод для получения записей из таблицы и их дальнейшей обработки

    process_single_message - метод для обработки одной записи

    create_mp3_records - метод для cохранения аудиозаписи в формате mp3

    upload_to_minio - метод для загрузки аудиозаписи в хранилище Minio

    save_wav_record - метод для сохранения записи в формате wav

    convert_to_mp3 - метод для конвертации аудизаписи в формате wav в формат mp3

    get_duration - метод для получения длительности аудиозаписи

    get_object_name - метод для получение пути до аудиозаписи в Minio
    """
    MAX_RETRIES = 3

    def __init__(self):
        self.raw_noise_audio_repository: RawNoiseAudioRepository = RawNoiseAudioRepository(connection=get_connection_sqlite())
        self.noise_records_repository: NoiseRecordRepository = NoiseRecordRepository(connection=get_connection_sqlite())
        self.minio_repository: MinioRepository = MinioRepository()
        self.system_utils: SystemUtils = SystemUtils()
        self.serial_number = self.system_utils.get_sensor_name() # Без префикса получаем хостнейм

        # Стоит вынести в конфиги, сделать конфиг для PyAudio
        self.duration_limit = 60
        self.bytes_per_second = 3 * 48000
        self.time_to_converting = 120

        self.bytestring_max_length: int = self.bytes_per_second * self.duration_limit

    def run(self) -> None:
        """
            1) Получение записи из таблицы raw_noise_audio
            2) Дальнейшая обработка: отправка в Minio аудиозаписи, сохранение сообщения в таблицу noise_records
            3) Удаление записей об обработанных аудиозаписях из таблицы raw_noise_audio
        """
        while True:
            try:
                raw_audio_messages = self.raw_noise_audio_repository.get()

                if raw_audio_messages:
                    ids = []

                    for message in raw_audio_messages:
                        id = self.process_single_message(message=message)

                        if id:
                            ids.append(id)

                    self.raw_noise_audio_repository.delete(ids=ids)
                else:
                    time.sleep(5) # время сна можно тоже в конфиг

            except Exception as e:
                logger.exception(e)


    def process_single_message(self, message: RawNoiseAudioMessage) -> Optional[str]:
        """
            1) Cохраняем аудиозапись в виде файла с расширением mp3
            2) Загрузка файла в Minio
            3) Запись сообщения об отправленной аудиозаписи в таблицу noise_records

            Args:
                message: запись из таблицы raw_noise_audio с аудиозаписью в виде байт строки,
        """
        converted_record = self.create_mp3_records(message=message)

        if not converted_record:
            return None

        uploaded_record = self.minio_repository.create(record=converted_record)

        noise_record_message = NoiseRecordMessage(
            event_id=uploaded_record.event_id,
            bucket_name=settings.minio.BUCKET_NAME,
            object_name=uploaded_record.object_name,
            duration=uploaded_record.duration,
            file_size_bytes=uploaded_record.size
        )

        logger.debug(noise_record_message)

        self.noise_records_repository.create(noise_record_message)

        return message.id


    def create_mp3_records(self, message: RawNoiseAudioMessage) -> Optional[RawRecordData]:
        """
            Cохранение аудиозаписи в формате mp3

            Args:
                message: запись из БД с аудиозаписью в виде байт строки,
            Returns:
                Возвращает объект RawRecordData в случае успешной загрузки,
                или None в случае неуспешной загрузки.
        """

        duration = self.get_duration(bytestring=message.bytestring)
        path_to_file_wav = settings.audio_converter_settings.path_to_records_dir.joinpath(f"{message.event_id}.wav")
        path_to_file_mp3 = settings.audio_converter_settings.path_to_records_dir.joinpath(f"{message.event_id}.mp3")

        raw_record_data = RawRecordData(
            event_id=message.event_id,
            bytestring=message.bytestring,
            time_stamp=message.time_stamp,
            duration=duration,
            path_to_file_wav=path_to_file_wav,
            path_to_file_mp3=path_to_file_mp3
        )

        is_wav_saved = self.system_utils.save_wav_record(record=raw_record_data)

        if not is_wav_saved:
            return None

        is_mp3_converted = self.system_utils.convert_to_mp3(raw_record_data=raw_record_data)

        if is_mp3_converted:
            return raw_record_data

        return None

    def get_duration(self, bytestring: bytes) -> int:
        """
            Получение длительности записи

             Args:
                 bytestring: аудиозапись в формате строки байтов
             Returns:
                 int: длительность аудиозаписи в секундах

        """
        return int(len(bytestring) // ( 3 * 48000)) #config














