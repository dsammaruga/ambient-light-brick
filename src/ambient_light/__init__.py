# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

"""Ambient Light brick: periodic illuminance readings with a dark/bright state.

Sample third-party brick for the App Bricks registry. Without a real sensor the
reading is simulated, so the brick runs on any board. Every reading is also
published as JSON to the MQTT broker bundled in brick_compose.yaml, unless the
MQTT_TOPIC variable is empty.
"""

from __future__ import annotations

import json
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
        mqtt_topic: Topic the readings are published to. Defaults to
            `MQTT_TOPIC`; an empty string disables publishing.
    """

    def __init__(
        self,
        read: Callable[[], float] | None = None,
        on_reading: Callable[[Reading], None] | None = None,
        threshold: float | None = None,
        period_sec: float | None = None,
        mqtt_topic: str | None = None,
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
        self.mqtt_topic = mqtt_topic if mqtt_topic is not None else os.getenv("MQTT_TOPIC", "ambient_light/readings")
        self._mqtt_host = os.getenv("MQTT_HOST", "ambient-light-broker")
        self._mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
        self._mqtt = None

    def start(self) -> None:
        logger.info(f"Starting AmbientLight (threshold={self.threshold} lux, period={self.period_sec}s)")
        if self.mqtt_topic:
            self._connect_mqtt()

    def stop(self) -> None:
        logger.info("Stopping AmbientLight")
        if self._mqtt is not None:
            self._mqtt.loop_stop()
            self._mqtt.disconnect()
            self._mqtt = None

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
        self._publish(reading)
        return reading

    def last_reading(self) -> Reading | None:
        """Returns the most recent reading, or None before the first one."""
        with self._lock:
            return self._last

    def _connect_mqtt(self) -> None:
        # Imported here so that apps that disable publishing do not pay for it.
        import paho.mqtt.client as mqtt

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ambient-light")
        try:
            # Asynchronous: the broker container may still be starting, paho retries in the background.
            client.connect_async(self._mqtt_host, self._mqtt_port)
            client.loop_start()
        except OSError as e:
            logger.warning(f"MQTT broker {self._mqtt_host}:{self._mqtt_port} unreachable, readings are not published: {e}")
            return
        self._mqtt = client

    def _publish(self, reading: Reading) -> None:
        if self._mqtt is None or not self.mqtt_topic:
            return
        result = self._mqtt.publish(self.mqtt_topic, json.dumps(reading))
        if result.rc != 0:
            logger.debug(f"MQTT publish not delivered (rc={result.rc})")

    def _simulated_read(self) -> float:
        self._simulated += random.uniform(-40.0, 40.0)
        self._simulated = max(0.0, min(2000.0, self._simulated))
        return self._simulated
