from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .const import CCT_TEMPERATURE_MAX, CCT_TEMPERATURE_MIN, CCT_TEMPERATURE_REAL_MAX, CCT_TEMPERATURE_REAL_MIN


@dataclass(frozen=True)
class LexmanCCTSmartBulbState:

    power: Optional[bool] = None
    brightness: Optional[int] = None
    temperature: Optional[int] = None

    @property
    def temperature_kelvin(self) -> Optional[int]:
        if self.temperature is None:
            return None
        return round(
            (self.temperature - CCT_TEMPERATURE_MIN) * (CCT_TEMPERATURE_REAL_MAX - CCT_TEMPERATURE_REAL_MIN) / (CCT_TEMPERATURE_MAX - CCT_TEMPERATURE_MIN) + CCT_TEMPERATURE_REAL_MIN
        )
