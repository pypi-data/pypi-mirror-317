from pydantic import BaseModel


class NoiseMessage(BaseModel):
    la_max: float
    la_eq: float
    la_eq_hour: float
    rta: str
    dt: float
    time_stamp: str
    sensor_name: str
    message_type: str = "noise_message"


class EventMessage(BaseModel):
    event_id: str
    sensor_name: str
    event_type: str = "La"
    time_stamp_start: str
    time_stamp_end: str
    event_la_max: float
    time_stamp_max: str
    threshold: int
    message_type: str = "noise_event"


class NotificationMessage(BaseModel):
    notification_id: str
    sensor_name: str
    notification_type: str = "La"
    notification_ts: str
    threshold: int
    message_type: str = "notification_event"
