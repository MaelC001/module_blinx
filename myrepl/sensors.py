# list of the different function for all the sensor
__list_sensors = {}

infoSensorI2C = {}

# register for function who calculate the brut donnee
def register(fn, name, etape, waiting = 0, args = {}):
  def wrapper(fn):

    if name in __list_sensors:
      __list_sensors[name][etape] = {'func' : fn, 'waiting' : waiting}
    else :
      __list_sensors[name] = {etape : {'func' : fn, 'waiting' : waiting}}

    if etape == 'immediate':
      __list_sensors[name]['args'] = args

    return fn
  return wrapper(fn)



def get_all_function_sensor():
  __list_sensors.clear()
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
