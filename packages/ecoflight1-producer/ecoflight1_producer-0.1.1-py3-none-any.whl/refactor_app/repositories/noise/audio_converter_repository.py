import sqlite3
from typing import List

from refactor_app.core.repositories.base_sensor_repository import BaseRepository
from refactor_app.core.logging_config import logger
from refactor_app.schemas.audio_converter_schemas import RawNoiseAudioMessage


class RawNoiseAudioRepository(BaseRepository):
    def __init__(self, connection):
        self.connection = connection

    def create(self, raw_data: RawNoiseAudioMessage):
        cursor = self.connection.cursor()

        cursor.execute(
            """
                INSERT INTO raw_noise_audio (
                    event_id,
                    data,
                    time_stamp_start
                )
                VALUES (?, ?, ?);
            """,
            (
                raw_data.event_id,
                raw_data.bytestring,
                raw_data.time_stamp,
            ),
        )

        self.connection.commit()
        cursor.close()
        logger.debug("insert raw_noise_audio message")
        return {"message": "raw_noise_audio message created"}

    def get(self):
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()

        cursor.execute(
            """
                SELECT id, event_id, data, time_stamp_start
                FROM raw_noise_audio
                LIMIT 10
            """
        )

        rows = cursor.fetchall()

        raw_audio_messages = []
        for row in rows:
            message = RawNoiseAudioMessage(
                        id=row["id"],
                        event_id=row["event_id"],
                        bytestring=row["data"],
                        time_stamp=row["time_stamp_start"]
                    )
            raw_audio_messages.append(message)

        return raw_audio_messages


    def delete(self, ids):
        cursor = self.connection.cursor()

        ids = tuple(ids)

        if len(ids) == 1:
            where = f"WHERE id = {ids[0]}"
        else:
            where = f"WHERE id IN {ids}"

        cursor.execute(
            f"""
                DELETE 
                FROM raw_noise_audio
                {where}
            """
        )

        self.connection.commit()
        cursor.close()
        logger.debug("delete raw_noise_audio message")
        return {"message": "raw_noise_audio message was deleted"}