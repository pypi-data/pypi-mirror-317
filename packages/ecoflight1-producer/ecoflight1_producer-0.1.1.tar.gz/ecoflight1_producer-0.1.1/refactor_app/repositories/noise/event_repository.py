from refactor_app.core.repositories.base_sensor_repository import BaseRepository
from refactor_app.core.logging_config import logger
from refactor_app.schemas.noise_schemas import EventMessage


class EventRepository(BaseRepository):
    def __init__(self, db):
        self.db = db

    def create(self, event_message: EventMessage):
        cursor = self.db.cursor()

        cursor.execute(
            """
                INSERT INTO events (
                    event_id,
                    sensor_name,
                    message_type,
                    event_type,
                    threshold,
                    time_stamp_start,
                    event_la_max,
                    time_stamp_max,
                    time_stamp_end
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                event_message.event_id,
                event_message.sensor_name,
                event_message.message_type,
                event_message.event_type,
                event_message.threshold,
                event_message.time_stamp_start,
                event_message.event_la_max,
                event_message.time_stamp_max,
                event_message.time_stamp_end,
            ),
        )

        self.db.commit()
        cursor.close()
        logger.info("insert event message")
        return {"message": "event message created"}

    def delete(self, id: int) -> None:
        pass
