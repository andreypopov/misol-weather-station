# !/usr/bin/env python3
#
# disp.py - read from Fine Offset RS495 weather station.
# Take RS485 via USB message from a Fine Offset WH2950 and interpret.
# See https://wordpress.com/post/doughall.me/1683
#
# Copyright (C) 2018, Doug Hall
# Licensed under MIT license, see included file LICENSE or http://opensource.org/licenses/MIT

import logging
import time

from paho.mqtt.client import Client, MQTT_ERR_SUCCESS
from serial import Serial

from wdata import RawWeatherData, wdata


def publish(client: Client, topic: str, order: int):
    client.publish(f"{BASE}/{topic}/meta/type", "value", qos=0, retain=True)
    client.publish(f"{BASE}/{topic}/meta/readonly", 1, qos=0, retain=True)
    client.publish(f"{BASE}/{topic}/meta/order", order, qos=0, retain=True)


logging.basicConfig(
    level=logging.DEBUG, filename='/tmp/misol.log', filemode='w',
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
log = logging.getLogger(__name__)

BASE = '/devices/misol/controls'
TOPICS = ['temperature', 'humidity', 'light', 'wind_direction', 'wind_speed',
          'wind_gust', 'rain', 'uvi', 'bar', 'battery_low', 'last_update']
UVI = [432, 851, 1210, 1570, 2017, 2761, 3100, 3512, 3918, 4277, 4650, 5029,
       5230]


def main():
    try:
        client = Client("Misol")  # create new instance
        client.connect("192.168.1.3")  # connect to broker

        client.publish("/devices/misol/meta/name", "Misol Meteostation", qos=0,
                       retain=True)

        for order, topic in enumerate(TOPICS, 1):
            publish(client, topic, order)

        log.debug("Connected to MQTT")

        s = Serial('/dev/ttyUSB0', 9600, timeout=60)

        log.debug("Connected to serial")

        while True:
            log.debug("Start Read")

            raw = s.read(21)

            checksum = sum(i for i in raw[:16]) & 0xFF
            assert checksum == raw[16], "Wrong checksum"

            wd = wdata.from_buffer_copy(raw)
            rwd: RawWeatherData = wd.rawdata

            wind = ((wd.rawdata.WSP8 << 8) + wd.rawdata.WIND) / 8 * 1.12
            uvi = next((i for i, v in enumerate(UVI) if rwd.UVI <= v), 13)

            payload = {
                'wind_direction': (wd.rawdata.DIR8 << 8) + wd.rawdata.DIR,
                'battery_low': rwd.BAT,
                'temperature': (rwd.TMP - 400) / 10.0,
                'humidity': rwd.HM,
                'wind_speed': round(wind),
                'wind_gust': round(rwd.GUST * 1.12),
                'rain': rwd.RAIN,
                'uvi': uvi,
                'light': round(rwd.LIGHT / 10.0),
                'bar': round(rwd.BAR / 100.0, 2),
                'last_update': int(time.time())
            }

            for k, v in payload.items():
                info = client.publish(f"{BASE}/{k}", v, retain=True)
                assert info.rc == MQTT_ERR_SUCCESS, f"MQTT Error: {info.rc}"

            log.debug("Updated MQTT")

    except AssertionError as e:
        log.error(e)

    except:
        log.exception("Exception")


if __name__ == '__main__':
    main()