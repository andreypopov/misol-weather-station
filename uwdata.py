''' Map the weather data from the C structure into MicroPython '''
import uctypes
RawWeatherData = {
    "FC":       uctypes.BFUINT8  | 0  | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "SC":       uctypes.BFUINT8  | 1  | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "DIR":      uctypes.BFUINT8  | 2  | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "DIR8":     uctypes.BFUINT8  | 3  | 7  << uctypes.BF_POS | 1  << uctypes.BF_LEN,
    "FIX":      uctypes.BFUINT8  | 3  | 5  << uctypes.BF_POS | 2  << uctypes.BF_LEN,
    "WSP8":     uctypes.BFUINT8  | 3  | 4  << uctypes.BF_POS | 1  << uctypes.BF_LEN,
    "BAT":      uctypes.BFUINT8  | 3  | 5  << uctypes.BF_POS | 1  << uctypes.BF_LEN,
    "TMP":      uctypes.BFUINT16 | 3  | 0  << uctypes.BF_POS | 11 << uctypes.BF_LEN,
    "HM":       uctypes.BFUINT8  | 5  | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "WIND":     uctypes.BFUINT8  | 6  | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "GUST":     uctypes.BFUINT8  | 7  | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "RAIN":     uctypes.BFUINT16 | 8  | 0  << uctypes.BF_POS | 16 << uctypes.BF_LEN,
    "UVI":      uctypes.BFUINT16 | 10 | 0  << uctypes.BF_POS | 16 << uctypes.BF_LEN,
    "LIGHT":    uctypes.BFUINT32 | 12 | 8  << uctypes.BF_POS | 24 << uctypes.BF_LEN,
    "CRC":      uctypes.BFUINT8  | 15 | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "CHECKSUM": uctypes.BFUINT8  | 16 | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN,
    "BAR":      uctypes.BFUINT32 | 17 | 8  << uctypes.BF_POS | 24 << uctypes.BF_LEN,
    "CHECKSUM_BAR": uctypes.BFUINT8  | 20 | 0  << uctypes.BF_POS | 8  << uctypes.BF_LEN
}
