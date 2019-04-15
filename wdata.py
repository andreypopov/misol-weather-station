''' Map the weather data from the C structure into Python '''
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, BigEndianStructure, Union

class RawWeatherData(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FC", c_uint8, 8),
        ("SC", c_uint8, 8),
        ("DIR", c_uint8, 8),
        ("DIR8", c_uint8, 1),
        ("FIX", c_uint8, 2),
        ("WSP8", c_uint8, 1),
        ("BAT", c_uint8, 1),
        ("TMP", c_uint16, 11),
        ("HM", c_uint8, 8),
        ("WIND", c_uint8, 8),
        ("GUST", c_uint8, 8),
        ("RAIN", c_uint16, 16),
        ("UVI", c_uint16, 16),
        ("LIGHT", c_uint32, 24),
        ("CRC", c_uint8, 8),
        ("CHECKSUM", c_uint8, 8),
        ("BAR", c_uint32, 24),
        ("CHECKSUM_BAR", c_uint8, 8)
    ]

class wdata(Union):
    _pack_ = 1
    _fields_ = [
        ("rawdata", RawWeatherData),
        ("ulData", c_uint64)
    ]
