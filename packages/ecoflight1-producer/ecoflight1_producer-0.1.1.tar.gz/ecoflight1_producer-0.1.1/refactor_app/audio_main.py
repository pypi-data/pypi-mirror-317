from refactor_app.core.logging_config import logger
from refactor_app.services.audio_converter_services.audio_converter_service import AudioConverterService
from refactor_app.utils.system_utils import SystemUtils
from refactor_app.core.config import settings
from refactor_app.core.database.sqlite import create_database


class AudioConverterManager:
    def __init__(self):
        path_to_dir = settings.audio_converter_settings.path_to_records_dir
        SystemUtils.create_audio_records_dir(path_to_dir=path_to_dir)

        self.service = AudioConverterService()

    def run(self):
        try:
            self.service.run()
        except Exception as e:
            logger.exception("Exception while audio converter service running:", str(e))

audio_converter_manager = AudioConverterManager()

def main():
    try:
        audio_converter_manager.run()
    except KeyboardInterrupt:
        logger.info('Виключай я сказал')

if __name__ == "__main__":
    main()