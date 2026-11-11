# Ambient Light MQTT monitor

App Lab app that receives the readings of the Ambient Light brick through the MQTT broker the brick starts (`ambient-light-broker`, eclipse-mosquitto) and prints them. It shows the brick container and the published JSON payload: `{"lux": 312.4, "state": "bright", "threshold": 100.0}`.
