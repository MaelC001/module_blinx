from machine import Pin, ADC, PWM, I2C
from time import sleep_ms

class Channel():
    def __init__(self):
        pass
    def read(self):
        raise Exception('not configure')
    def write(self, value):
        raise Exception('not configure')

class ChannelDigital(Channel):
    def __init__(self, pin, error, translateFunction = lambda x,y : b'\x01' if x else b'\x00'):
        self.pin = Pin(pin, Pin.OUT)

        self.oldData = 0
        self.translateFunction = translateFunction
        self.error = error
    def read(self):
        return self.translateFunction(self.pin(), self.error, self.oldData)
    def write(self, value):
        self.pin.value(value)

class ChannelAnalog(Channel):
    def __init__(self, pin, p1, p2, p3, translateFunction, error, freq = 1000):
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(pin)
        self.pwm.freq(freq)

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.oldData = 0
        self.translateFunction = translateFunction
        self.error = error
    def read(self):
        Pin(0, mode=Pin.OUT).value(self.p1)
        Pin(2, mode=Pin.OUT).value(self.p2)
        Pin(15, mode=Pin.OUT).value(self.p3)
        return self.translateFunction(ADC(0).read(), self.error, self.oldData)
    def write(self, value):
        self.pwm.duty(value)

class ChannelI2C(Channel):
    def __init__(self, i2c, addr, byteReceive, codeSend, wait, translateFunction, error):
        self.i2c = i2c
        self.addr = addr
        self.byteReceive = byteReceive
        self.codeSend = codeSend
        self.wait = wait

        self.oldData = 0
        self.translateFunction = translateFunction
        self.error = error
    def read(self):
        self.write(self.codeSend)
        sleep_ms(self.wait)
        return self.read_i2c()
    def write(self, value):
        self.i2c.writeto(self.addr, value)
    def read_i2c(self):
        return self.translateFunction(self.i2c.readfrom(self.addr, self.byteReceive), self.error, self.oldData)