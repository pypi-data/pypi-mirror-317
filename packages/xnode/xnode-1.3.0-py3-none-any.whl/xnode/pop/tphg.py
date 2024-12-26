import time
import ustruct
import machine 
from micropython import const


class Tphg:
    __BME680_ADDR = const(0x77)
    
    def __set_power_mode(self, value):
            tmp = self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x74, 1)[0]
            
            tmp &= ~0x03
            tmp |= value
            self.__i2c.writeto_mem(self.__BME680_ADDR, 0x74, bytes([tmp]))
            time.sleep(0.01)

    def __perform_reading(self):
        ctrl = self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x74, 1)[0]
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x74, bytes([(ctrl & 0xFC) | 0x01]))
        
        new_data = 0
        while not new_data:
            data = self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x1D, 17)
            new_data = data[0] & 0x80 != 0
            time.sleep(0.01)
        
        self._adc_pres = ((data[2] * 4096) + (data[3] * 16) + (data[4] / 16))
        self._adc_temp = ((data[5] * 4096) + (data[6] * 16) + (data[7] / 16))
        self._adc_hum = ustruct.unpack(">H", bytes(data[8:10]))[0]
        self._adc_gas = int(ustruct.unpack(">H", bytes(data[13:15]))[0] / 64)
        self._gas_range = data[14] & 0x0F
            
        var1 = (self._adc_temp / 8) - (self._temp_calibration[0] * 2)
        var2 = (var1 * self._temp_calibration[1]) / 2048
        var3 = ((var1 / 2) * (var1 / 2)) / 4096
        var3 = (var3 * self._temp_calibration[2] * 16) / 16384
        self._t_fine = int(var2 + var3)

    def __temperature(self):
        return ((((self._t_fine * 5) + 128) / 256) / 100) + self._temperature_correction
            
    def __pressure(self):
        var1 = (self._t_fine / 2) - 64000
        var2 = ((var1 / 4) * (var1 / 4)) / 2048
        var2 = (var2 * self._pressure_calibration[5]) / 4
        var2 = var2 + (var1 * self._pressure_calibration[4] * 2)
        var2 = (var2 / 4) + (self._pressure_calibration[3] * 65536)
        var1 = ((((var1 / 4) * (var1 / 4)) / 8192) * (self._pressure_calibration[2] * 32) / 8) + ((self._pressure_calibration[1] * var1) / 2)
        var1 = var1 / 262144
        var1 = ((32768 + var1) * self._pressure_calibration[0]) / 32768
        calc_pres = 1048576 - self._adc_pres
        calc_pres = (calc_pres - (var2 / 4096)) * 3125
        calc_pres = (calc_pres / var1) * 2
        var1 = (self._pressure_calibration[8] * (((calc_pres / 8) * (calc_pres / 8)) / 8192)) / 4096
        var2 = ((calc_pres / 4) * self._pressure_calibration[7]) / 8192
        var3 = (((calc_pres / 256) ** 3) * self._pressure_calibration[9]) / 131072
        calc_pres += (var1 + var2 + var3 + (self._pressure_calibration[6] * 128)) / 16
        return calc_pres / 100

    def __humidity(self):
        temp_scaled = ((self._t_fine * 5) + 128) / 256
        var1 = (self._adc_hum - (self._humidity_calibration[0] * 16)) - ((temp_scaled * self._humidity_calibration[2]) / 200)
        var2 = (self._humidity_calibration[1] * (((temp_scaled * self._humidity_calibration[3]) / 100) + 
                (((temp_scaled * ((temp_scaled * self._humidity_calibration[4]) / 100)) / 64) / 100) + 16384)) / 1024
        var3 = var1 * var2
        var4 = self._humidity_calibration[5] * 128
        var4 = (var4 + ((temp_scaled * self._humidity_calibration[6]) / 100)) / 16
        var5 = ((var3 / 16384) * (var3 / 16384)) / 1024
        var6 = (var4 * var5) / 2
        calc_hum = ((((var3 + var6) / 1024) * 1000) / 4096) / 1000
        return 100 if calc_hum > 100 else 0 if calc_hum < 0 else calc_hum
    
    def __gas(self):
        LOOKUP_TABLE_1 = (2147483647.0, 2147483647.0, 2147483647.0, 2147483647.0, 2147483647.0, 2126008810.0, 2147483647.0, 2130303777.0, 
                        2147483647.0, 2147483647.0, 2143188679.0, 2136746228.0, 2147483647.0, 2126008810.0, 2147483647.0, 2147483647.0)

        LOOKUP_TABLE_2 = (4096000000.0, 2048000000.0, 1024000000.0, 512000000.0, 255744255.0, 127110228.0, 64000000.0, 32258064.0,
                        16016016.0, 8000000.0, 4000000.0, 2000000.0, 1000000.0, 500000.0, 250000.0, 125000.0)
        
        var1 = ((1340 + (5 * self._sw_err)) * (LOOKUP_TABLE_1[self._gas_range])) / 65536
        var2 = ((self._adc_gas * 32768) - 16777216) + var1
        var3 = (LOOKUP_TABLE_2[self._gas_range] * var1) / 512
        return ((var3 + (var2 / 2)) / var2) / 1000

    def __init__(self):
        self.__i2c = machine.I2C(1)

        self.__i2c.writeto_mem(self.__BME680_ADDR, 0xE0, bytes([0xB6]))
        time.sleep(0.01)        
        
        self.__set_power_mode(0)
        t_calibration = self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x89, 25)
        t_calibration += self.__i2c.readfrom_mem(self.__BME680_ADDR, 0xE1, 16)
        self._heat_range = (self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x02, 1)[0] & 0x30) / 16
        self._heat_val = self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x00, 1)[0]
        self._sw_err = (self.__i2c.readfrom_mem(self.__BME680_ADDR, 0x04, 1)[0] & 0xF0) / 16

        calibration = [float(i) for i in list(ustruct.unpack("<hbBHhbBhhbbHhhBBBHbbbBbHhbb", bytes(t_calibration[1:39])))]
        self._temp_calibration = [calibration[x] for x in [23, 0, 1]]
        self._pressure_calibration = [calibration[x] for x in [3, 4, 5, 7, 8, 10, 9, 12, 13, 14]]
        self._humidity_calibration = [calibration[x] for x in [17, 16, 18, 19, 20, 21, 22]]
        self._gas_calibration = [calibration[x] for x in [25, 24, 26]]
        
        self._humidity_calibration[1] *= 16
        self._humidity_calibration[1] += self._humidity_calibration[0] % 16
        self._humidity_calibration[0] /= 16

        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x72, bytes([0b010]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x74, bytes([(0b100 << 5) | (0b011 << 2)]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x75, bytes([0b010 << 2]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x70, bytes([0b001 << 3]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x5A, bytes([0x74]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x64, bytes([0x65]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x70, bytes([0x00]))
        self.__i2c.writeto_mem(self.__BME680_ADDR, 0x71, bytes([0x10]))       
        self.__set_power_mode(1)
        self.__perform_reading(); self.__perform_reading(); self.__perform_reading()

        self._temperature_correction = -2 + -5
        self._t_fine = None
        self._adc_pres = None
        self._adc_temp = None
        self._adc_hum = None
        self._adc_gas = None
        self._gas_range = None

    def scan(self):
        return self.__BME680_ADDR in self.__i2c.scan()

    def set_temperature_correction(self, value):
        self._temperature_correction += value

    def read(self, gas=False):
        self.__perform_reading()
        if not gas:
            return self.__temperature(), self.__pressure(), self.__humidity(), None
        else:
            time.sleep(0.5)
            return self.__temperature(), self.__pressure(), self.__humidity(), self.__gas()
    
    def sealevel(self, altitude):
        press = self.__pressure()
        return press / pow((1-altitude/44330), 5.255), press
    
    def altitude(self, sealevel): 
        press = self.__pressure()
        return 44330 * (1.0-pow(press/sealevel,0.1903)), press
