import os
from datetime import datetime
from typing import Optional

from core.config import settings
from core.database.minio import get_minio_client
from core.logging_config import logger
from core.services.raw_record_data import RawRecordData
from utils.system_utils import SystemUtils


class MinioRepository:
    def __init__(self):
        self.minio_client = get_minio_client()

    def create(self, record: RawRecordData) -> Optional[RawRecordData]:
        """
            Загрузка аудиозаписи в хранилище Minio

            Args:
                record: данные о аудиозаписи
            Returns:
                Возвращает объект RawRecordData в случае успешной загрузки,
                или None в случае неуспешной загрузки.
        """
        try:
            record.object_name = self._get_object_name(raw_record_data=record)
            record.size = os.stat(record.path_to_file_mp3).st_size
            bucket_name = settings.minio.BUCKET_NAME

            with open(record.path_to_file_mp3, "rb") as audiofile:
                is_uploaded = self.minio_client.put_object(
                    bucket_name=bucket_name,
                    object_name=record.object_name,
                    data=audiofile,
                    length=record.size
                )

            if is_uploaded:
                os.remove(record.path_to_file_mp3)
                return record
        except Exception as e:
            logger.exception(str(e))
        return None

    def _get_object_name(self, raw_record_data: RawRecordData) -> str:
        """
            Получение пути до аудиозаписи в Minio

            Args:
                 raw_record_data: данные о записи
            Returns:
                str: пути до аудиозаписи в Minio
        """
        date = datetime.fromtimestamp(float(raw_record_data.time_stamp)).strftime("%Y/%m/%d")
        serial_number = SystemUtils.get_sensor_name(prefix="")
        return f"{date}/{serial_number}/{raw_record_data.path_to_file_mp3.name}"