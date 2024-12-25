from refactor_app.core.logging_config import logger
from refactor_app.core.repositories.base_sensor_repository import BaseRepository
from refactor_app.schemas.audio_converter_schemas import NoiseRecordMessage


class NoiseRecordRepository(BaseRepository):
    def __init__(self, connection):
        self.connection = connection

    def create(self, noise_record_data: NoiseRecordMessage):
        cursor = self.connection.cursor()

        cursor.execute(
            """
                INSERT INTO noise_records(
                    event_id,
                    bucket_name,
                    object_name,
                    duration,
                    file_size_bytes,
                    message_type
                )
                VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                noise_record_data.event_id,
                noise_record_data.bucket_name,
                noise_record_data.object_name,
                noise_record_data.duration,
                noise_record_data.file_size_bytes,
                noise_record_data.message_type
            ),
        )

        self.connection.commit()
        cursor.close()
        logger.info("insert noise_record message")
        return {"message": "noise_record message created"}
