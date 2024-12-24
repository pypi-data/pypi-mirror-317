from refactor_app.core.repositories.base_sensor_repository import BaseRepository
from refactor_app.core.logging_config import logger
from refactor_app.schemas.noise_schemas import NoiseMessage


class NoiseRepository(BaseRepository):
    def __init__(self, db):
        self.db = db

    def create(self, noise_message: NoiseMessage) -> dict:
        cursor = self.db.cursor()

        if not noise_message.la_max:
            raise ValueError("Invalid value la_max")

        cursor.execute(
            """INSERT INTO noise (
                la_max,
                la_eq,
                la_eq_hour,
                rta,
                dt,
                time_stamp,
                sensor_name,
                message_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                noise_message.la_max,
                noise_message.la_eq,
                noise_message.la_eq_hour,
                noise_message.rta,
                noise_message.dt,
                noise_message.time_stamp,
                noise_message.sensor_name,
                noise_message.message_type,
            ),
        )

        self.db.commit()
        cursor.close()
        logger.info("insert noise message")
        return {"message": "noise message created"}

    def delete(self, noise_id: int) -> None:
        pass
