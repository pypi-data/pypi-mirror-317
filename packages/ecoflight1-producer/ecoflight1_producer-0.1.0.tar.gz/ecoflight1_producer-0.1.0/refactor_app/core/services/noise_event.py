from dataclasses import dataclass
from typing import Optional


@dataclass
class NoiseEvent:
    uuid: Optional[str] = None
    is_event: bool = False
    waiting_for_noise_end: int = 0
    time_stamp_start: Optional[str] = None
    event_la_max: float = 0.0
    time_stamp_max: Optional[str] = None
    time_stamp_end: Optional[str] = None


    def to_default(self) -> None:
        self.is_event = False
        self.waiting_for_noise_end = 0
        self.event_la_max = 0.0

