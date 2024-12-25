from dataclasses import dataclass
from pathlib import Path


@dataclass
class RawRecordData:
    event_id: str
    bytestring: bytes
    time_stamp: str
    duration: int
    object_name: str = None
    size: int = None
    path_to_file_wav: Path = None
    path_to_file_mp3: Path = None