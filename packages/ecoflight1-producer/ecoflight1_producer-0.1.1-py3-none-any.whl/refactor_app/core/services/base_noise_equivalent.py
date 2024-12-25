from dataclasses import dataclass


@dataclass
class Equivalent:
    end_hour: int = 0
    la_eq_temp: float = 0
    iters: int = 0
