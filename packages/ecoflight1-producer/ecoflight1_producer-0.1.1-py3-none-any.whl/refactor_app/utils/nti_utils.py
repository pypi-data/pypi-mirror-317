"""
Модуль для инициализации класса SerialManager
который отвечает за считывание данных с nti устройства

"""

import glob
from typing import Optional

import serial

from refactor_app.core.logging_config import logger


class NtiAudioUtils:
    """
    start - запуск SerialManager

    get_rasberry_port - поиск порта для подключение к устройству


    """
    FIRST_STRING = b"*IDN?\n"
    EXPECTED_RESPONSE = "NTiAudio"

    def __init__(self):
        self._port: Optional[str] = self.find_sensor()
        self._connection: serial.Serial = serial.Serial(port=self._port, timeout=0.25)

    @property
    def connection(self):
        return self._connection

    @staticmethod
    def find_sensor() -> Optional[str]:
        """
        Определяет порт Raspberry, если он доступен, иначе возвращает None.
        """
        ports = glob.glob("/dev/ttyACM*")
        for port in ports:
            try:
                with serial.Serial(port, timeout=1) as ser:
                    ser.write(NtiAudioUtils.FIRST_STRING)
                    line = ser.readline()
                    response = str(line.decode("utf-8")).split(",")[0]
                    if response == NtiAudioUtils.EXPECTED_RESPONSE:
                        logger.info(f"Port is defined - {port}")
                        return port
            except (OSError, serial.SerialException) as e:
                logger.info(f"Error with port {port}: {e}")
                continue

        logger.info("No needed port found.")
        return None
