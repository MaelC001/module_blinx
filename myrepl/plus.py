
from machine import Pin, I2C, SoftI2C, ADC, PWM, UART
import network, os, webrepl, time
wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_sta.connect('wifi','wifiwifi')
time.sleep(0.2)
webrepl.start(password='blinx')


try:
  import uasyncio as asyncio
except:
  import asyncio

import sys


async def r1(uart):
  sreader = asyncio.StreamReader(uart)
  while True:
    data = await sreader.read(1)
    print('a1-',type(data))



async def r2():
  sreader = asyncio.StreamReader(sys.stdin)
  while True:
    data = await sreader.read(1)
    print('a2-',type(data))



def f():
	baud_rate = 9600
	uart = UART(0, baudrate=baud_rate) # , tx=17, rx=16)  # UART(0, baud_rate)
	uart.init(baudrate = baud_rate)#, rxbuf = 200)
	#os.dupterm(uart, 0)
	#os.dupterm(None, 0)
	#uart.write('aa')
	#print(uart.read())
	#return uart
	loop = asyncio.get_event_loop()
	loop.create_task(r1(uart))
	loop.create_task(r2())
	loop.run_forever()

