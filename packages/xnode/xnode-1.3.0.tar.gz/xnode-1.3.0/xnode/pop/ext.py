import time
import ustruct
import machine
from micropython import const

class Pir:
    NONE = 0
    DETECT = 1
    ENTER = 2
    LEAVE = 3
    
    def __init__(self):
        self.__pin = machine.Pin('P2', machine.Pin.IN)
        self.__t0 = 0
        
    def read(self):
        return self.__pin.value()    

    def state(self, timeout=1):
        old_state = self.read()
        time.sleep_ms(timeout)
        curr_state = self.read()
        if old_state != curr_state:
            return self.ENTER if curr_state else self.LEAVE
        else:
            return curr_state
    
    def detect(self, timeout=1500):
        n = self.read()
        if n == self.DETECT and not self.__t0:
            self.__t0 = time.ticks_ms()
        elif self.__t0:
            if time.ticks_ms() - self.__t0 >= timeout:
                self.__t0 = 0
            n = not self.DETECT
        return n == self.DETECT

class IRThermometer:
    __MLX90614_ADDR = const(0x5A)

    EEPROM_PWMCTRL = const(0x02)
    EEPROM_CONFIG_REGISTER1 = const(0x05)
    RAM_Ta = const(0x06)
    RAM_Tobj1 = const(0x07)

    def __init__(self):
        self.__i2c = machine.I2C(1, freq=50000) #The maximum frequency of the MLX90614 is 100 KHz and the minimum is 10 KHz. 

    def scan(self):
        return self.__MLX90614_ADDR in self.__i2c.scan()

    def read(self, reg, eeprom=False):
        if eeprom:
            reg = 0x20 | reg
        data = self.__i2c.readfrom_mem(self.__MLX90614_ADDR, reg, 2)
        return ustruct.unpack('<H', data)[0]

    def ambient(self):
        data = self.read(self.RAM_Ta)
        return round(data * 0.02 - 273.15, 1)

    def object(self):
        data = self.read(self.RAM_Tobj1)
        return round(data * 0.02 - 273.15, 1)


class IMU:
    __BNO055_ADDR = const(0x28)

    ACCELERATION = const(0x08)
    MAGNETIC = const(0x0E)
    GYROSCOPE = const(0x14)
    EULER = const(0x1A)
    QUATERNION = const(0x20)
    ACCEL_LINEAR = const(0x28)
    ACCEL_GRAVITY = const(0x2E)
    TEMPERATURE = const(0x34)
    
    def __init__(self):
        self.__i2c = machine.I2C(1)
        self.__scale = {self.ACCELERATION:1/100, self.MAGNETIC:1/16, self.GYROSCOPE:0.001090830782496456, self.EULER:1/16,  self.QUATERNION:1/(1<<14), self.ACCEL_LINEAR:1/100, self.ACCEL_GRAVITY:1/100}
        self.__call = {self.ACCELERATION:self.__read_other, self.MAGNETIC:self.__read_other, self.GYROSCOPE:self.__read_other, self.EULER:self.__read_other,  self.QUATERNION:self.__read_quaternion, self.ACCEL_LINEAR:self.__read_other, self.ACCEL_GRAVITY:self.__read_other, self.TEMPERATURE:self.__read_temperature}
        
    def scan(self):
        return self.__BNO055_ADDR in self.__i2c.scan()

    def init(self):
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0X3D, bytes([0x00])) #Mode Register, Enter configuration.
        time.sleep_ms(20)
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0x3F, bytes([0x20])) #Trigger Register, Reset
        time.sleep_ms(650)
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0X3E, bytes([0x00])) #Power Register, Set to normal power. cf) low power is 0x01
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0X07, bytes([0x00])) #Page Register, Make sure we're in config mode and on page0(param, data), page1(conf)
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0X3F, bytes([0x80])) #Trigger Register, External oscillator
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0X3F, bytes([0x00])) #Trigger Register,
        time.sleep_ms(10)
        self.__i2c.writeto_mem(self.__BNO055_ADDR, 0X3D, bytes([0x0C])) #Mode Register, Enter normal operation (NDOF)
        time.sleep_ms(200)

    def __read_temperature(self, addr):
        t = self.__i2c.readfrom_mem(self.__BNO055_ADDR, addr, 1)[0]
        return t - 256 if t > 127 else t

    def __read_quaternion(self, addr):
        t = self.__i2c.readfrom_mem(self.__BNO055_ADDR, addr, 8)  
        return tuple(v * self.__scale[self.QUATERNION] for v in ustruct.unpack('hhhh', t))

    def __read_other(self, addr):
        if addr not in self.__scale:
            raise ValueError(f"Address {addr} not in scale mapping")
        t = self.__i2c.readfrom_mem(self.__BNO055_ADDR, addr, 6)
        return tuple(v * self.__scale[addr] for v in ustruct.unpack('hhh', t))

    def calibration(self):
        data = self.__i2c.readfrom_mem(self.__BNO055_ADDR, 0x35, 1)[0] #Calibration Resiger, Read        
        return (data >> 6) & 0x03, (data >> 4) & 0x03, (data >> 2) & 0x03, data & 0x03  #Sys, Gyro, Accel, Mag

    def read(self, addr):
        return self.__call[addr](addr)