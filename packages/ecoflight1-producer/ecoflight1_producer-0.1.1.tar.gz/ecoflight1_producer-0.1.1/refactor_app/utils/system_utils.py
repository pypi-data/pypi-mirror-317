"""
Модуль для вспомогательного класса SystemUtils для взаимодействия с ОС

"""

import os
import subprocess
import sys
import time
import traceback
import wave
from pathlib import Path

from refactor_app.core.logging_config import logger
from refactor_app.core.config import settings
from refactor_app.core.services.raw_record_data import RawRecordData


class SystemUtils:
    LAUNCH_PARAMETER = "-c"

    @staticmethod
    def get_sensor_name(prefix: str = "") -> str:
        """Метод для получения имени датчика"""
        return prefix + os.uname().nodename

    @staticmethod
    def get_correction_constant() -> float:
        parameter_to_launch = sys.argv[1]
        correction_constant = float(sys.argv[2])

        if parameter_to_launch != SystemUtils.LAUNCH_PARAMETER:
            logger.exception(f"Неизвестный параметр запуска: {parameter_to_launch}")
            raise KeyError("Неизвестный параметр запуска")
        elif correction_constant < 0 or correction_constant > 100:
            logger.exception(f"Неверное значение корректировочной константы: {correction_constant}")
            raise ValueError("Неверное значение корректировочной константы")
        else:
            return correction_constant

    @staticmethod
    def create_audio_records_dir(path_to_dir: Path):
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
        logger.info("Noise records directory exists")

    @staticmethod
    def save_wav_record(record: RawRecordData) -> bool:
        """
            Сохранение записи в формате wav

            Args:
                raw_record_data: данные о записи
            Returns:
                bool: статус сохранения, `True` - успешно, `False` - неуспешно
        """

        if os.path.exists(record.path_to_file_wav):
            return True

        try:
            path_to_file = str(record.path_to_file_wav)

            wf = wave.open(path_to_file, "wb")
            wf.setnchannels(1)  # Всё вынести в конфиг для PyAudio или сделать Audio config
            wf.setsampwidth(3)
            wf.setframerate(48000)
            wf.writeframes(record.bytestring)
            wf.close()

            logger.info("Noise record was written successfully!")

            return True

        except Exception:
            logger.exception(f"Error while saving noise record:\n{traceback.format_exc()}")
            return False

    @staticmethod
    def convert_to_mp3(raw_record_data: RawRecordData) -> bool:
        """
            Конвертация аудизаписи в формате wav в формат mp3

            Args:
                raw_record_data: данные о записи
            Returns:
                bool: статус конвертации, `True` - успешно, `False` - неуспешно

        """
        if os.path.exists(raw_record_data.path_to_file_mp3):
            return True

        command = (f"ffmpeg -i {raw_record_data.path_to_file_wav} " 
                   f"-vn -ar {48000} -ac {1} -b:a 32k {raw_record_data.path_to_file_mp3}") #config

        try:
            start_converting = time.time()
            subprocess.run(command.split(" "))

            while start_converting + settings.audio_converter_settings.time_to_convert > time.time():
                if os.path.exists(raw_record_data.path_to_file_mp3):
                    os.remove(raw_record_data.path_to_file_wav)
                    return True
                time.sleep(1)

            # Если не успели за назначенное время, то в файле wav ошибка
            os.remove(raw_record_data.path_to_file_wav)
            raise Exception(f"File {raw_record_data.path_to_file_wav.name} wasn't converted to mp3 format")

        except Exception as e:
            logger.exception(str(e))
            return False