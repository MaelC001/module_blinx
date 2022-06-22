try:
  import utime as time
except:
  import time



try:
  import uos as os
except:
  import os
try:
  import uasyncio as asyncio
except:
  import asyncio

import sys, json, io

from machine import Pin, I2C, ADC, PWM, UART
import blinxSensor, sensors, display

#import sh1107, mpu9250
#import dps310_simple as dps310

# the class with all the sensor
Blinx = blinxSensor.Blinx()

# connection to i2c
i2c=I2C(sda=Pin(4),scl=Pin(5))

# serial port
uart = UART(0, 115200)


loop = None

# display in the micro controller
display = display.DisplayBlinx()

# function register
__register = {}

# class for capture the stdout when `exec`
class DUP(io.IOBase):
  def __init__(self):
    self.s = bytearray()
  def write(self, data):
    self.s += data
    return len(data)
  def readinto(self, data):
    return 0
  def readAll(self):
    return str(self.s)

# the register for the user function
def register(name, subFunction=""):
  def wrapper(fn):
    def inner_wrapper(*args, id, **kwargs):
      error = ""
      output = ""
      message = ""
      # execute the function and capture the error
      try:
        output = fn(*args, **kwargs)
      except Exception as e:
        error = str(e)
      finally:
        message = "result"
        if error :
          message = "error"
          output = {"code": -32000, "message": error}

        # if the function use a user function, then we have to check the other function as well
        elif subFunction and type(output) == dict:
          if 'error' in output:
            message = 'error'
            output = output['error']
          elif 'result' in output:
            output = output['result']

        return {message : output, 'id': id}
    __register[name] = inner_wrapper
    return inner_wrapper
  return wrapper

def sender(j):
  """send message to serial port in json"""
  uart.write(json.dumps(j))


async def receiver():
  """
    receive information by the serial port in json
    and execute the function with the given argument
  """
  sreader = asyncio.StreamReader(uart)
  while True:
    data=await sreader.readline()

    # try to parse the json
    try:
      line = data.decode('utf-8').rstrip()
      #sender(line)
      j=json.loads(line)
    except Exception as e:
      #error = str(e)
      errorId = None
      j={}
      j['error'] = {"code": -32700, "message": "Parse error"}#error}
      j['id'] = errorId
      sender(j)
      continue

    # try to read the parameter of the json
    # then the parameter of the method
    # to execute the method with the parameter
    try:
      id = j['id']
      cmd = j['method']
      args = j['params']

      # is the id correct ?
      if not(isinstance(id, str) or isinstance(id, int) or id is None) or not(isinstance(cmd, str)):
        j={}
        j['error'] = {"code": -32600, "message": "Invalid Request"}
        j['id'] = None
        sender(j)

      # method exist ?
      if cmd in __register:
        # type of the parameter
        if isinstance(args, list):
          reply = __register[cmd](*args, id = id)
          sender(reply)
        elif isinstance(args, dict):
          reply = __register[cmd](id = id, **args)
          sender(reply)
        else :
          j={}
          j['error'] = {"code": -32602, "message": "Invalid params"}
          j['id'] = id
          sender(j)
      else :
        j={}
        j['error'] = {"code": -32601, "message": "Method not found"}
        j['id'] = id
        sender(j)
    except Exception as e:
      #error = str(e)
      if id:
        errorId = id
      else:
        errorId = None
      j={}
      j['error'] = {"code": -32600, "message": "Invalid Request"}#error}
      j['id'] = errorId
      sender(j)

@register('write', "")
def writeFile(name, text, format = 'w', doVerification=True):
  """
  write in a file
  arg :
    - name : str
    - text : str
    - format : str (optional)
  """
  if doVerification:
    verification(name, str)
    verification(text, str)
    verification(format, str, ['w','w+','a','a+'])
  f = open(name, format)
  f.write(text)
  f.close()
  return ''

@register('read', "")
def readFile(name):
  """
  read a file
  arg :
    - name : str
  """
  verification(name, str, os.listdir(), True)
  f = open(name, 'r')
  r = f.read()
  f.close()
  return r

@register('create', "")
def createFile(name):
  """
  create a file
  arg :
    - name : str
  """
  verification(name, str, os.listdir(), False)
  f = open(name, 'x')
  f.close()
  return ''

@register('remove', "")
def removeFile(name):
  """
  remove a file
  arg :
    - name : str
  """
  verification(name, str, os.listdir(), True)
  os.remove(name)
  return ''

@register('liste', "")
def listFile():
  """
  do the list of the file
  arg : none
  """
  return os.listdir()

@register('exec', "")
def execute(cmd):
  """
  execute a command python of the user
  arg :
    - cmd : str
  """
  verification(cmd, str)

  #result_exec = ""
  #def write(*args, sep=' ', end='\n'):
  #  global result
  #  result += sep.join(str(a) for a in args) + end

  # capture the stdout
  dupTempo = DUP()
  os.dupterm(dupTempo)
  exec(cmd)#, {"print":write})
  os.dupterm(None)
  return dupTempo.readAll()

@register('sensors_stop', "")
def sensorStop():
  """
  stop all sensor
  arg : none
  """
  global Blinx
  Blinx = blinxSensor.Blinx()
  sensors.__listSensor.clear()


@register('configSensor', "")
def configSensor(dictConfig):
  """
  for config the sensors with custom names
  arg :
    - dictConfig : dict
  """
  global Blinx
  verification(dictConfig, dict)
  Blinx = blinxSensor.Blinx(dictConfig, i2c)
  sensors.getAllFunctionSensor()


@register('get_sensors', "")
def getSensors(listSensors, times = '1s'):
  """
  get the data form the sensors in the list
  if the time is 0s, we want the data form now
  """
  blinxSensor.tampon = True
  timeBefore = time.time()

  text, nameSensors, functionSensors = verificationListSensor(listSensors)
  # immedate data of the sensor
  if times == '0s':
    text += '\n' + str(time.time())
    for sensor in nameSensors:
      timeBefore = saveSensorWhileRequest(timeBefore)
      sensorInfo = sensors.__listSensor[sensor]['immediate']
      text += ';' + str(sensorInfo['func'](i2c, **sensorInfo['args']))
    return text
  else :
    # capture all the data from each sensor the user want the data
    dataAllSensor = ''
    indexData = 0
    sizeBuffer = 300
    while indexData < sizeBuffer:
      textTimeStamp = ''
      for func in functionSensors:
        timeBefore = saveSensorWhileRequest(timeBefore)
        dataSensor, timeDataSensor = func.getIndex(times, indexData)
        textTimeStamp += ';' + dataSensor

      dataAllSensor = timeDataSensor + ';' + textTimeStamp + dataAllSensor

      indexData += 1
    text += '\n' + dataAllSensor

  blinxSensor.tampon = False
  return text

def saveSensorWhileRequest(timeBefore):
  """
  when we get the data form the sensors for the user,
  we have to continue to capture the data
  """
  if timeBefore < time.time()+1:
    timeBefore = time.time()+1
    Blinx.save()
  return timeBefore

def verificationListSensor(listSensors):
  """
  verification of the sensors : exist or not
  and capture the information
  """
  text = 'Time'
  nameSensors = []
  functionSensors = []
  for sensor in listSensors:
    verification(sensor, str, Blinx.sensors_input)
    text += ';' + sensor
    nameSensors.append(Blinx.sensors_input[sensor]['name'])
    functionSensors.append(Blinx.sensors_input[sensor]['sensor'])
  return text, nameSensors, functionSensors



def verification(value, type_value, possible = [], inPossible = True):
  """
  verify the value the user give us is correct
  """
  if not isinstance(value, type_value):
    message = f"the type of {value} isn't {type_value}"
    raise TypeError(message)
  if possible != [] and not ( (value not in possible) ^ inPossible ):
    message = f"{value} don't have a correct value"
    raise TypeError(message)


async def saveAllSensor():
  while True:
    # we will wait a minimum of 1 secondes before we recommence
    timeBefore = time.ticks_ms()

    Blinx.save()

    present= time.ticks_ms()
    diffTime = 1000 - blinxSensor.diff_ticks(timeBefore, present)
    if diffTime > 0:
      await asyncio.sleep_ms(diffTime)

def launch():
  os.dupterm(uart, 1)
  os.dupterm(None, 1)
  loop = asyncio.get_event_loop()
  loop.create_task(receiver())
  loop.create_task(saveAllSensor())
  loop.run_forever()

def debug(json):
  """
  for the debugging, we will simulate the serial port
  """
  cmd = json['method']
  args = json['params']
  id = json['id']
  return __register[cmd](**args, id = id)







# https://github.com/rdehuyss/micropython-ota-updater
@register('updateFirmware', "")
def otaUpdate():
    from .ota_updater import OTAUpdater
    otaUpdater = OTAUpdater('https://github.com/MaelC001/micropython', github_src_dir='src', main_dir='app', secrets_file="secrets.py")
    otaUpdater.install_update_if_available()
    del(otaUpdater)
