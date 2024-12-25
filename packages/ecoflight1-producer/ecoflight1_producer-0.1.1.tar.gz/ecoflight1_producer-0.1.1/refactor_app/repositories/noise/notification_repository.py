from refactor_app.core.repositories.base_sensor_repository import BaseRepository
from refactor_app.core.logging_config import logger
from refactor_app.schemas.noise_schemas import NotificationMessage


class NotificationRepository(BaseRepository):
    def __init__(self, db):
        self.db = db

    def create(self, notification_message: NotificationMessage):
        cursor = self.db.cursor()

        cursor.execute(
            """
                INSERT INTO notifications (
                    notification_id,
                    sensor_name,
                    message_type,
                    threshold,
                    notification_ts,
                    notification_type
                )
                VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                notification_message.notification_id,
                notification_message.sensor_name,
                notification_message.message_type,
                notification_message.threshold,
                notification_message.notification_ts,
                notification_message.notification_type,
            ),
        )

        self.db.commit()
        cursor.close()
        logger.info("insert notification message")
        return {"message": "notification message created"}

    def delete(self, id: int) -> None:
        pass
