# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import json

import paho.mqtt.client as mqtt
from arduino.app_utils import App
from ambient_light import AmbientLight

TOPIC = "ambient_light/readings"

light = AmbientLight(mqtt_topic=TOPIC)


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(TOPIC)


def on_message(client, userdata, message):
    reading = json.loads(message.payload)
    print(f"[mqtt] {reading['lux']} lux -> {reading['state']}")


monitor = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ambient-light-monitor")
monitor.on_connect = on_connect
monitor.on_message = on_message
monitor.connect_async("ambient-light-broker", 1883)
monitor.loop_start()

App.run()
