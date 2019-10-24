
#!/usr/bin/env python3
#
# disp.py - read from Fine Offset RS495 weather station.
# Take RS485 via USB message from a Fine Offset WH2950 and interpret.
# See https://wordpress.com/post/doughall.me/1683
#
# Copyright (C) 2018, Doug Hall
# Licensed under MIT license, see included file LICENSE or http://opensource.org/licenses/MIT
#
import serial
import binascii
from wdata import RawWeatherData, wdata

import paho.mqtt.client as mqtt

client = mqtt.Client("Misol") #create new instance
client.connect("127.0.0.1") #connect to broker

client.publish("/devices/misol/meta/name","Misol Meteostation",qos=0,retain=True)

client.publish("/devices/misol/controls/temperature/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/temperature/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/temperature/meta/order",1,qos=0,retain=True)

client.publish("/devices/misol/controls/humidity/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/humidity/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/humidity/meta/order",2,qos=0,retain=True)

client.publish("/devices/misol/controls/light/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/light/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/light/meta/order",3,qos=0,retain=True)

client.publish("/devices/misol/controls/wind_direction/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/wind_direction/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/wind_direction/meta/order",4,qos=0,retain=True)

client.publish("/devices/misol/controls/wind_speed/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/wind_speed/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/wind_speed/meta/order",5,qos=0,retain=True)

client.publish("/devices/misol/controls/wind_gust/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/wind_gust/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/wind_gust/meta/order",6,qos=0,retain=True)

client.publish("/devices/misol/controls/rain/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/rain/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/rain/meta/order",7,qos=0,retain=True)

client.publish("/devices/misol/controls/uvi/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/uvi/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/uvi/meta/order",8,qos=0,retain=True)

client.publish("/devices/misol/controls/bar/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/bar/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/bar/meta/order",9,qos=0,retain=True)

client.publish("/devices/misol/controls/battery_low/meta/type","value",qos=0,retain=True)
client.publish("/devices/misol/controls/battery_low/meta/readonly",1,qos=0,retain=True)
client.publish("/devices/misol/controls/battery_low/meta/order",10,qos=0,retain=True)


def main():
    s = serial.Serial('/dev/tty.SLAB_USBtoUART', 9600)

    wd = wdata()
    while True:
        b = s.read(21)
        wd = wdata.from_buffer_copy(b)
        print(binascii.hexlify(bytearray(b)))
        print("dir: {}".format((wd.rawdata.DIR8<<8)+wd.rawdata.DIR))
        client.publish("/devices/misol/controls/wind_direction",wd.rawdata.DIR)
        print("bat: {}".format(wd.rawdata.BAT))
        client.publish("/devices/misol/controls/battery_low",wd.rawdata.BAT)

        print("tmp: {}".format((wd.rawdata.TMP-400)))
        client.publish("/devices/misol/controls/temperature",wd.rawdata.TMP-400)

        print("hm: {}".format(wd.rawdata.HM))
        client.publish("/devices/misol/controls/humidity",wd.rawdata.HM)
        print("wind: {}".format((wd.rawdata.WSP8<<8)+wd.rawdata.WIND))
        client.publish("/devices/misol/controls/wind_speed",wd.rawdata.WIND)
        print("gust: {}".format(wd.rawdata.GUST))
        client.publish("/devices/misol/controls/wind_gust",wd.rawdata.GUST)
        print("rain: {}".format(wd.rawdata.RAIN))
        client.publish("/devices/misol/controls/rain",wd.rawdata.RAIN)
        print("uvi: {}".format(wd.rawdata.UVI))
        client.publish("/devices/misol/controls/uvi",wd.rawdata.UVI)
        print("light: {}".format(wd.rawdata.LIGHT))
        byteArray = bytes(wd.rawdata.LIGHT)
        client.publish("/devices/misol/controls/light",byteArray,0)

        print("bar: {}".format(wd.rawdata.BAR))
        byteArray2 = bytes(wd.rawdata.BAR)
        client.publish("/devices/misol/controls/bar",byteArray2,0)

        print("================================")
    ser.close()

if __name__ == '__main__':
    main()



