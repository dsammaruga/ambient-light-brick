# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

"""Ambient Light brick: periodic illuminance readings with a dark/bright state.

Sample third-party brick for the App Bricks registry. Without a real sensor the
reading is simulated, so the brick runs on any board.
"""

from __future__ import annotations

import os
import random
import threading
import time
from collections.abc import Callable
from typing import TypedDict

from arduino.app_utils import Logger, brick

logger = Logger("AmbientLight")


class Reading(TypedDict):
    lux: float
    state: str
    threshold: float


@brick
class AmbientLight:
    """Reads ambient light periodically and reports it in lux.

    Args:
        read: Optional function returning the illuminance in lux. When omitted,
            a slowly drifting simulated value is used.
        on_reading: Optional callback invoked with every `Reading`.
        threshold: Lux below which the environment is dark. Defaults to the
            `LIGHT_THRESHOLD_LUX` variable.
        period_sec: Seconds between readings. Defaults to `LIGHT_PERIOD_SEC`.
    """

    def __init__(
        self,
        read: Callable[[], float] | None = None,
        on_reading: Callable[[Reading], None] | None = None,
        threshold: float | None = None,
        period_sec: float | None = None,
    ) -> None:
        self._read = read or self._simulated_read
        self._on_reading = on_reading
        self.threshold = float(threshold if threshold is not None else os.getenv("LIGHT_THRESHOLD_LUX", "100"))
        self.period_sec = float(period_sec if period_sec is not None else os.getenv("LIGHT_PERIOD_SEC", "2"))
        if self.threshold < 0:
            raise ValueError("threshold must not be negative")
        if self.period_sec <= 0:
            raise ValueError("period_sec must be positive")
        self._lock = threading.Lock()
        self._last: Reading | None = None
        self._simulated = 250.0

    def start(self) -> None:
        logger.info(f"Starting AmbientLight (threshold={self.threshold} lux, period={self.period_sec}s)")

    def stop(self) -> None:
        logger.info("Stopping AmbientLight")

    def loop(self) -> None:
        """Takes one reading, stores it and notifies the callback. Called repeatedly by the framework."""
        reading = self.read_once()
        if self._on_reading is not None:
            self._on_reading(reading)
        time.sleep(self.period_sec)

    def read_once(self) -> Reading:
        """Takes a single reading and returns it."""
        lux = max(0.0, float(self._read()))
        reading: Reading = {
            "lux": round(lux, 1),
            "state": "dark" if lux < self.threshold else "bright",
            "threshold": self.threshold,
        }
        with self._lock:
            self._last = reading
        logger.info(f"{reading['lux']} lux -> {reading['state']}")
        return reading

    def last_reading(self) -> Reading | None:
        """Returns the most recent reading, or None before the first one."""
        with self._lock:
            return self._last

    def _simulated_read(self) -> float:
        self._simulated += random.uniform(-40.0, 40.0)
        self._simulated = max(0.0, min(2000.0, self._simulated))
        return self._simulated
