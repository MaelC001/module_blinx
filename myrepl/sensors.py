# list of the different function for all the sensor
__list_sensors = {}

infoSensorI2C = {}

# register for function who calculate the brut donnee
def register(fn, name, etape, waiting = 0, args = {}):
  def wrapper(fn):
    
    tempo = {'func' : fn, 'waiting' : waiting}
    if etape == 'create':
      tempo = fn

    if name in __list_sensors:
      __list_sensors[name][etape] = tempo
    else :
      __list_sensors[name] = {etape : tempo}

    if etape == 'immediate':
      __list_sensors[name]['args'] = args

    return fn
  return wrapper(fn)



def get_all_function_sensor():
  """
      Get all the info for each file for sensors
  """
  __list_sensors.clear()
  try:
    import listSensorUser
  except:
    return
  list_sensors = listSensorUser.list_sensors
  list_names = listSensorUser.list_names
  for i in list_sensors:
    # import the file
    a = __import__(i)
    # get the info
    info = a.info
    names = info['name']
    for name in names:
      if name in list_names:
        infoSensor = info['info']
        functions = info['channels']
        waiting = 0
        for id, infoChannel in functions.items():
          waiting = infoChannel['waiting']
          dictFunctions = infoChannel['functionsId']
          for type, function in dictFunctions.items():
            register(function, name, type+id, waiting=waiting)

        dictFunctions = info['functions']
        for type, function in dictFunctions.items():
          register(function, name, type, waiting=waiting, args=infoSensor)
