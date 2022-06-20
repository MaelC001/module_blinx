# list of the different function for all the sensor
__listSensor = {}

# register for function who calculate the brut donnee
def register(fn, name, etape, waiting = 0, channel = []):
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
      __listSensor[name]['channel'] = channel

    return func
  return wrapper(fn)

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

def clearDict():
  global __listSensor
  __listSensor= {}

def getAllFunctionSensor():
  clearDict()
  try:
    import listSensorUser
  except:
    return
  for i in listSensorUser.array:
    a = __import__(i)
    info = a.info
    name = info['name']
    waiting = info['waiting']
    channel = info['channel']
    register(a.functionByte, name, "byte")
    register(a.functionTranslate, name, "readable")
    register(a.functionImmediate, name, "immediate", waiting, channel)