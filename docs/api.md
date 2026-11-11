# Ambient Light API

`from ambient_light import AmbientLight`

## `Reading`

A `TypedDict` describing one measurement:

| Key | Type | Description |
|-----|------|-------------|
| `lux` | `float` | Illuminance in lux, rounded to one decimal, never negative |
| `state` | `str` | `"dark"` when `lux` is below `threshold`, `"bright"` otherwise |
| `threshold` | `float` | Threshold in lux used for this reading |

## `AmbientLight`

A brick (`@brick`): the App Lab framework calls `start()`, then `loop()` repeatedly, then `stop()` when the app exits.

### `AmbientLight(read=None, on_reading=None, threshold=None, period_sec=None, mqtt_topic=None)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `read` | `Callable[[], float] \| None` | `None` | Function returning the illuminance in lux. When omitted, a slowly drifting simulated value between 0 and 2000 lux is used |
| `on_reading` | `Callable[[Reading], None] \| None` | `None` | Called with every reading taken by the loop |
| `threshold` | `float \| None` | `LIGHT_THRESHOLD_LUX` variable, `100` | Lux below which the environment is dark |
| `period_sec` | `float \| None` | `LIGHT_PERIOD_SEC` variable, `2` | Seconds between two readings of the loop |
| `mqtt_topic` | `str \| None` | `MQTT_TOPIC` variable, `ambient_light/readings` | Topic every reading is published to as JSON; `""` disables publishing |

Raises `ValueError` if `threshold` is negative or `period_sec` is not positive.

### Attributes

- `threshold: float`: the threshold in lux in use.
- `period_sec: float`: the interval between readings in seconds.
- `mqtt_topic: str`: the topic readings are published to, empty when publishing is disabled.

### Methods

- `read_once() -> Reading`: takes one reading with the `read` function, stores it as the last reading, publishes it to `mqtt_topic` when connected, and returns it. Negative values from `read` are clamped to 0. Exceptions raised by `read` propagate to the caller.
- `last_reading() -> Reading | None`: the most recent reading, or `None` before the first one. Thread-safe.
- `start() -> None`: lifecycle hook called by the framework; connects to the MQTT broker in the background when `mqtt_topic` is set.
- `stop() -> None`: lifecycle hook; disconnects from the broker.
- `loop() -> None`: called repeatedly by the framework: takes one reading with `read_once()`, passes it to `on_reading` when set, then sleeps `period_sec` seconds.
