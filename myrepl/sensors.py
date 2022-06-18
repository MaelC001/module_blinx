try:
  import uos as os
except:
  import os

import time
from machine import Pin, ADC, PWM

#import sh1107, mpu9250
#import dps310_simple as dps310


# list of the different function for all the sensor
__listSensor = {}


# register for function who calculate the brut donnee
def register(name, etape, waiting = 0):
  def wrapper(fn):
    def innerWrapper(*args, **kwargs):
      if 'i2c' in __listSensor[name]:
        return fn(*args, addr = __listSensor[name]['i2c']['addr'], code = __listSensor[name]['i2c']['code'], nmbBytes = __listSensor[name]['i2c']['nmbBytes'], **kwargs)
      return fn(*args, **kwargs)

    func = fn
    if etape == 'immediate':
      func = innerWrapper

    if name in __listSensor:
      __listSensor[name][etape] = func
    else :
      __listSensor[name] = {etape : func}

    if etape == 'immediate':
      __listSensor[name]['waiting'] = waiting

    return func
  return wrapper

@register('temperature', 'byte')
def temp_receive(bytes, error):
  result = bytes[0:2]
  if crc8_sht3(result) != bytes[2]:
    return error
    raise Exception('Checksum temperature error')
  return result

@register('humidity', 'byte')
def hum_receive(bytes, error):
  result = bytes[3:5]
  if crc8_sht3(result) != bytes[5]:
    return error
    raise Exception('Checksum humidity error')
  return result

@register('temperature', 'readable')
def byte2temperature(bytes, celsus=True):
  #databytes = temp_hum_receive(i2c, 0x3c)
  temperature_raw = bytes[0] << 8 | bytes[1]
  if celsus:
    temperature = (175.0 * float(temperature_raw) / 65535.0) - 45
  else: # fahreheit
    temperature = (315.0 * float(temperature_raw) / 65535.0) - 49
  return temperature

@register('humidity', 'readable')
def byte2humidity(bytes):
  """  if immediate :
      temp_hum_send(i2c, addr)
      time.sleep_ms(sleep)
      bytes = hum_receive(i2c, error)
      if bytes == error:
        raise Exception('Checksum humidity error')"""
  #databytes = temp_hum_receive(i2c, 0x3c)
  humidity_raw = bytes[0] << 8  | bytes[1]
  humidity = (100.0 * float(humidity_raw) / 65535.0)
  return humidity

@register('temperature', 'immediate', waiting = 15)
def immediateTemperature(i2c, addr, code, nmbBytes, error = bytearray(b'\xff\xfe'), celsus=True, sleep = 15):
  bytes = __listSensor['temperature']['byte'](i2cSendReceive(i2c, addr, code, nmbBytes, sleep), error = error)
  if bytes == error:
    raise Exception('Checksum temperature error')
  return __listSensor['temperature']['readable'](bytes, celsus=celsus)

@register('humidity', 'immediate', waiting = 15)
def immediateHumidity(i2c, addr, code, nmbBytes, error = bytearray(b'\xff\xfe'), sleep = 15):
  bytes = __listSensor['humidity']['byte'](i2cSendReceive(i2c, addr, code, nmbBytes, sleep), error = error)
  if bytes == error:
    raise Exception('Checksum humidity error')
  return __listSensor['humidity']['readable'](bytes)

@register('analogique', 'immediate')
def analog(pinDic):
  p1 = pinDic['p1']
  p2 = pinDic['p2']
  p3 = pinDic['p3']
  Pin(0, mode=Pin.OUT).value(p1)
  Pin(2, mode=Pin.OUT).value(p2)
  Pin(15, mode=Pin.OUT).value(p3)
  adc = ADC(0)
  return adc.read()

@register('digital', 'immediate')
def digital(pin):
  pin = Pin(pin, Pin.IN)
  return pin()

# https://github.com/ralf1070/Adafruit_Python_SHT31/
def crc8_sht3(buffer):
	""" Polynomial 0x31 (x8 + x5 +x4 +1) """
	polynomial = 0x31
	crc = 0xFF
	index = 0
	for index in range(0, len(buffer)):
		crc ^= buffer[index]
		for i in range(8, 0, -1):
			if crc & 0x80:
				crc = (crc << 1) ^ polynomial
			else:
				crc = (crc << 1)
	return crc & 0xFF



def i2cSendReceive(i2c, addr, code, nmbBytes, sleep):
  i2c.writeto(addr, code)
  time.sleep_ms(sleep)
  return i2c.readfrom(addr, nmbBytes)


dicSHT3x = {
  'addr':0x70,
  'code':b'\x24\x00',
  'nmbBytes':6,
}

__listSensor['temperature']['i2c'] = dicSHT3x
__listSensor['humidity']['i2c'] = dicSHT3x