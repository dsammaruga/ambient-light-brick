# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import App
from ambient_light import AmbientLight


def on_reading(reading):
    print(f"{reading['lux']} lux -> {reading['state']}")


light = AmbientLight(on_reading=on_reading)

App.run()
