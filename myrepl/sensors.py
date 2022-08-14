# list of the different function for all the sensor
__listSensor = {}

infoSensorI2C = {}

# register for function who calculate the brut donnee
def register(fn, name, etape, waiting = 0, args = {}):
  def wrapper(fn):

    if name in __listSensor:
      __listSensor[name][etape] = {'func' : fn, 'waiting' : waiting}
    else :
      __listSensor[name] = {etape : {'func' : fn, 'waiting' : waiting}}

    if etape == 'immediate':
      __listSensor[name]['args'] = args

    return fn
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


def get_all_function_sensor():
  __listSensor.clear()
  try:
    import listSensorUser
  except:
    return
  list_sensors = listSensorUser.list_sensors
  for i in list_sensors:
    a = __import__(i)
    info = a.info
    names = info['name']
    for name in names:
      if name in list_sensors:
        infoSensor = info['info']
        functions = info['channels']
        for id, infoChannel in functions.items():
          waiting = infoChannel['waiting']
          dictFunctions = infoChannel['functionsId']
          for type, function in dictFunctions.items():
            register(function, name, type+id, waiting=waiting)

        dictFunctions = info['functions']
        for type, function in dictFunctions.items():
          register(function, name, type, waiting=waiting, args=infoSensor)
