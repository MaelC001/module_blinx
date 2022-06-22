try:
    import uos as os
except:
    import os
try:
    import uasyncio as asyncio
except:
    import asyncio
try:
    import utime as time
except:
    import time

from machine import I2C, UART, PIN
import saveSensor, replClass


class Blinx():
    def __init__(self):
        # connection to i2c
        self.i2c = I2C(sda=Pin(4),scl=Pin(5))
        # serial port
        self.uart = UART(0, 115200)

        self.repl = replClass.Repl(self.i2c, self.uart, self.changeBlinxSensor)

    async def saveAllSensor(self):
        while True:
            # we will wait a minimum of 1 secondes before we recommence
            timeBefore = time.ticks_ms()

            self.repl.BlinxSensor.save()

            present= time.ticks_ms()
            diffTime = 1000 - self.diffTicks(timeBefore, present)
            if diffTime > 0:
                await asyncio.sleep_ms(diffTime)

    def changeBlinxSensor(self, arraySensor = [], arrayName = []):
        self.BlinxSensor = saveSensor.BlinxSensor(arraySensor, arrayName)


def launch(b):
    os.dupterm(b.uart, 1)
    os.dupterm(None, 1)
    loop = asyncio.get_event_loop()
    loop.create_task(b.repl.receiver())
    loop.create_task(b.saveAllSensor())
    loop.run_forever()
