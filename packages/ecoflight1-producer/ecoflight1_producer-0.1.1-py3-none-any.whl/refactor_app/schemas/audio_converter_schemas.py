from typing import Optional

from pydantic import BaseModel


class RawNoiseAudioMessage(BaseModel):
    id: int = None
    event_id: str
    bytestring: bytes
    time_stamp: str


class NoiseRecordMessage(BaseModel):
    event_id: str
    bucket_name: str
    object_name: str
    duration: int
    file_size_bytes: int
    message_type: str = "noise_record"
