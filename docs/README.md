# Ambient Light Brick

This Brick reads an ambient light sensor periodically and reports the illuminance in lux with a dark/bright state. It is a sample third-party brick: without a real sensor it produces a simulated, slowly drifting reading.

## Overview

The Ambient Light Brick allows you to:

- Take illuminance readings at a fixed interval in the background.
- Receive every reading through a callback.
- Classify the environment as dark or bright against a configurable threshold.

## Features

- Pluggable `read` function: pass your own sensor reader, or use the simulated one
- Readings delivered to an `on_reading` callback and kept as `last_reading()`
- Threshold and period configurable from **Brick Configuration** or the constructor
- No dependencies and no hardware required to run

## Prerequisites

- **Supported boards**: Arduino® UNO™ Q and Arduino VENTUNO™ Q.
- **Sensor**: optional. Any function returning lux can act as the sensor.

## Code example and usage

### Simulated readings

```python
from arduino.app_utils import App
from ambient_light import AmbientLight

def on_reading(reading):
    print(f"{reading['lux']} lux -> {reading['state']}")

light = AmbientLight(on_reading=on_reading)

App.run()
```

### Your own sensor

```python
from arduino.app_utils import App
from ambient_light import AmbientLight

def read_lux():
    raw = 700  # replace with the value read from the sensor
    return raw * 0.25

light = AmbientLight(read=read_lux, threshold=50)

App.run()
```

## Configuration

Set these variables in **Brick Configuration** in App Lab:

| Variable | Description | Default |
|----------|-------------|---------|
| `LIGHT_THRESHOLD_LUX` | Illuminance below which the environment is reported as dark | `100` |
| `LIGHT_PERIOD_SEC` | Seconds between two readings | `2` |
| `MQTT_TOPIC` | Topic the readings are published to as JSON; empty to disable publishing | `ambient_light/readings` |
| `MQTT_HOST` | Host of the MQTT broker (hidden) | `ambient-light-broker` |
| `MQTT_PORT` | Port of the MQTT broker (hidden) | `1883` |

Threshold, period and topic can also be passed to the constructor: `AmbientLight(threshold=50, period_sec=5, mqtt_topic="")`.

## MQTT broker

The brick starts an MQTT broker next to the app: the `ambient-light-broker` container ([eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto) 2.0.22, pinned by digest in `brick_compose.yaml`), listening on port 1883 without authentication and bound to the board's localhost. Every reading is published as JSON (`{"lux": ..., "state": ..., "threshold": ...}`) to `MQTT_TOPIC`. Publishing is best effort: if the broker is not reachable the brick keeps reading and logs a warning. The `paho-mqtt` client is installed from the brick's `requirements.txt`.

## Methods

- **`read_once()`**: Takes a single reading and returns a dictionary with `lux`, `state` and `threshold`.
- **`last_reading()`**: Returns the most recent reading, or `None` before the first one.

## Errors

- The constructor raises `ValueError` if the threshold is negative or the period is not positive.
- A `read` function that raises stops the loop with the original exception, visible in the app logs.

## License

MPL-2.0. See the `LICENSE` file at the repository root and the SPDX headers in the source files.
