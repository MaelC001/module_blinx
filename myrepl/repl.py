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
import ssd1306, saveSensor, sensors, bufferCircular, channelClass

#import sh1107, mpu9250
#import dps310_simple as dps310

# connection to i2c
i2c=I2C(sda=Pin(4),scl=Pin(5))

# serial port
uart = UART(0, 115200)

loop = None

# display info, can only connect to 1 display
display=None
displayType = None

# function register
__register = {}

# output message
outputMessages = []
functionNameOutput = 'output'

dicOutputSensors = {}

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

def register(name, subFunction=""):
  def wrapper(fn):
    def inner_wrapper(*args, id, **kwargs):
      error = ""
      output = ""
      message = ""
      j = {}
      #returnResult = {}
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

# send message to serial port in json
def sender(j):
  uart.write(json.dumps(j))

# receive information by the serial port in json
# and execute the function with the given argument
async def receiver():
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

@register('display_create', "")
def displayCreate(typeDisplay, x, y):
  """
  connect to a display
  arg :
    - typeDisplay : str # sh1107 (grand, 128, 64) or ssd1306 (petit, 128, 32)
    - x : int
    - y : int
  """
  global display, displayType
  verification(typeDisplay, str, ['sh1107', 'ssd1306'])
  verification(x, int)
  verification(y, int)
  if display:
    clear()
  if typeDisplay != displayType or not display:
    displayType = typeDisplay
    if typeDisplay == 'sh1107':
      display = sh1107.SH1107_I2C(x, y, i2c)
    elif typeDisplay == 'sh1107':
      display = ssd1306.SSD1306_I2C(x,y,i2c)
  return ''

@register('display_text', "displayCreate")
def displayText(typeDisplay, x, y, show):
  """
  show text in the display
  arg :
    - typeDisplay : str #  sh1107 (grand, 128, 64) or ssd1306 (petit, 128, 32)
    - x : int
    - y : int
    - show :
        - text : str
        - x : int
        - y : int
        - taille : int
  """
  verification(typeDisplay, str, ['sh1107', 'ssd1306'])
  verification(show, dict)
  if typeDisplay != displayType or not display:
    displayCreate(typeDisplay, x, y)
  for i in show :
    text = i['text']
    x = i['x']
    y = i['y']
    t = i['taille']
    verification(text, str)
    verification(x, int)
    verification(y, int)
    verification(t, int)
    display.text(text, x, y, t)
  display.show()
  return ''

@register('display_clear', "displayCreate")
def displayClear(typeDisplay, y, x):
  """
  clear display
  arg :
    - typeDisplay : str # sh1107 (grand, 128, 64) or ssd1306 (petit, 128, 32)
    - x : int
    - y : int
  """
  verification(typeDisplay, str, ['sh1107', 'ssd1306'])
  if typeDisplay != displayType or not display:
    displayCreate(typeDisplay, y, x)
  clear()
  return ''

def clear():
  """
  clear display
  """
  display.fill(0)
  display.show()


@register(functionNameOutput, "")
def getOutput():
  """
  return all the message output
  and remove it all
  """
  out = outputMessages
  outputMessages.clear()
  return out

"""
@register('digital', "")
def digital(pin, value = 0):
  ""
  change value output for a digital sensor
  arg :
    - pin : int
    - value : int (0, 1)
  ""
  verification(pin, int)
  verification(value, int, [0, 1])
  Pin(pin, mode=Pin.OUT).value(value)
  return ''
"""

# the function led use the function digital
# so if a error occur in digital, led have to say it
"""
@register('led', "digital")
def led(value = 0):
  ""
  play with the led
  arg :
    - value : int (0, 1)
  ""
  pin = 2 # the led have the pin 2
  return digital(pin, value, id=0)
"""
"""
@register('PWMSensor', "")
def PWMSensor(pin, value, freq = 50):
  ""
  turn a servoMotor
  arg :
    - pin : int
    - value : int
    - freq : int (optional)
  ""
  verification(pin, int)
  verification(value, int)
  verification(freq, int)
  servo = PWM(Pin(pin))
  servo.freq(freq)
  servo.duty(value)
  return servo
"""

@register('sensors_stop', "")
def sensorStop(newName):
  ... ..
  """
  stop record a sensor
  arg :
    - name : str
        # if it is a analog sensor we need the pin
          - p1 : int
          - p2 : int (optional)
          - p3 : int (optional)
  """
  verification(newName, str, saveSensor.listSensorModify)

  name = saveSensor.listSensorModify[newName]['name']

  saveSensor.listSensorModify.pop(newName)
  if name in saveSensor.donnee['name']:
    i = saveSensor.donnee['name'].index(name)
    saveSensor.donnee['name'].pop(i)
    saveSensor.donnee['function'].pop(name)
  elif name in dicOutputSensors:
    dicOutputSensors['function'].pop(name)
  else:
    raise Exception('sensor not find')
  return ''

@register('configSensor', "")
def configSensor(dictConfig):
  """
  for config the sensors with custom names
  arg :
    - dictConfig : dict
  """
  verification(dictConfig, dict)

  for sensor, config in dictConfig.items():
    verification(sensor, str)#, saveSensor.listSensorModify)
    newName = config['new']
    input = config['input']
    saveSensor.listSensorModify[newName] = {'name' : sensor, 'channel': {}, "config": {}, "input" : input}
    sensorsCreate(sensor, created = True, input = input)

def sensorsCreateDict(digital =  False):
  """
  create the dictionary with the information for each time
  """
  arrayTimeValue = [1, 10, 60, 600, 3600]
  arrayTimeName = ['1s', '10s', '1m', '10m', '1h']
  arrayTimeSize = [300] * 5
  arrayTimeOffset = [0, 0, 1, 2, 3]
  arrayNextTime = nextTime(arrayTimeValue)
  before = None

  tempoDict = {}

  for i in range(len(arrayTimeValue)):
    nameTime = arrayTimeName[i]
    tempoDict[nameTime] = {
        'size' : arrayTimeSize[i],
        'times' : arrayNextTime[i],
        'value' : arrayTimeValue[i],
        'offset' : arrayTimeOffset[i],
        'before' : before,
      }
    if digital:
      tempoDict[nameTime]['dataSize'] = 1
    before = nameTime
  return tempoDict



@register('get_sensors', "")
def getSensors(listSensors, times = '1s'):
  """
  get the data form the sensors
  if the time is 0s, we want the data form now
  """
  bufferCircular.tampon = True
  timeBefore = time.time()

  text, nameSensors = verificationListSensor(listSensors)
  # immedate data of the sensor
  if times == '0s':
    text += '\n' + str(time.time())
    for sensor in nameSensors:
      timeBefore = saveSensorWhileRequest(timeBefore)

      if sensor[:-3] == 'annalogique':
        p1 = int(sensor[-3])
        p2 = int(sensor[-2])
        p3 = int(sensor[-1])
        text += ';' + str(analogCreate(times = times, p1 = p1, p2 = p2, p3 = p3))
      elif sensor[:7] == 'digital':
        pin = int(sensor[7:])
        text += ';' + str(digitalCreate(times = times, pin = pin))
      else:
        text += ';' + str(sensorsCreate(sensor, times))
    return text
  else :
    # capture each sensor the user want the data
    dataAllSensor = ''
    indexData = 0
    sizeBuffer = 300
    while indexData < sizeBuffer:
      textTimeStamp = ''
      for sensor in nameSensors:
        timeBefore = saveSensorWhileRequest(timeBefore)

        if sensor[:-3] == 'annalogique':
          p1 = int(sensor[-3])
          p2 = int(sensor[-2])
          p3 = int(sensor[-1])
          dataSensor, timeDataSensor = analogCreate(times = times, p1 = p1, p2 = p2, p3 = p3, index = indexData)
        elif sensor[:7] == 'digital':
          pin = int(sensor[7:])
          dataSensor, timeDataSensor = digitalCreate(times = times, pin = pin, index = indexData)
        else:
          dataSensor, timeDataSensor = sensorsCreate(sensor, times, index = indexData)
        textTimeStamp += ';' + dataSensor

      dataAllSensor = timeDataSensor + ';' + textTimeStamp + dataAllSensor

      indexData += 1
    text += '\n' + dataAllSensor

  bufferCircular.tampon = False
  return text

def saveSensorWhileRequest(timeBefore):
  if timeBefore < time.time()+1:
    timeBefore = time.time()+1
    timeWait, finishWait, finishDonnee, l_donneeAnalog, indexAnalog = saveSensor.recordDataPart1()
    if not finishWait:
      time.sleep_ms(timeWait - time.time())

    saveSensor.recordDataPart2(finishDonnee, l_donneeAnalog, indexAnalog)
  return timeBefore

def verificationListSensor(listSensors):
  """
  verification of the sensors : exist or not
  and capture the information
  """
  text = 'Time'
  nameSensors = []
  for sensor in listSensors:
    verification(sensor, str, saveSensor.listSensorModify)
    text += ';' + sensor
    nameSensors.append(saveSensor.listSensorModify[sensor]['name'])
  return text, nameSensors

def sensorsCreate(sensor, index = 0, times = '1s', created = False, channels = [], info = None, input= True):
  """
  if created is True we begin to record the sensor
  else we return the bytearray of the data record it,
  with the time and index of the present record
  arg :
    - sensor : str
    - temps : str
    - created : boolean
  """
  if times == '0s':
    if sensor in sensors.__listSensor:
      sensors.__listSensor[sensor]['immediate']['func'](info = info) # i2c or array of pin
    else:
      raise Exception("le sensor n'existe pas")
  elif created:
    tempoDict = sensorsCreateDict()
    # create the channel
    arrayChannel = []
    for channel in channels:
      if channel['type'] == "I2C":
        id = channel['id']
        function = sensors.__listSensor[sensor]['byte'+id]['func']
        waitingTime = sensors.__listSensor[sensor]['byte'+id]['waiting']

        addr = sensors.infoSensorI2C[sensor]['addr']
        byteReceive = sensors.infoSensorI2C[sensor]['byteReceive']
        codeSend = sensors.infoSensorI2C[sensor]['codeSend']
        arrayChannel.append(channelClass.ChannelI2C(i2c, addr, byteReceive, codeSend, waitingTime, function))
      elif channel['type'] == "Analog":
        id = channel['id']
        function = sensors.__listSensor[sensor]['byte'+id]['func']

        pin = channel['pin']
        p1 = channel['p1']
        p2 = channel['p2']
        p3 = channel['p3']
        freq = channel['freq']
        arrayChannel.append(channelClass.ChannelAnalog(pin, p1, p2, p3, function, freq = freq))
      elif channel['type'] == "Digital":
        pin = channel['pin']
        arrayChannel.append(channelClass.ChannelDigital(pin))

    if input:
      sensorBuffer = bufferCircular.Sensor(sensor, arrayChannel, tempoDict, waitingTime)
      saveSensor.donnee['function'][sensor] = sensorBuffer
      saveSensor.donnee['name'].append(sensor)
    else :
      dicOutputSensors[sensor] = arrayChannel
  elif sensor in saveSensor.donnee['function']:
    return saveSensor.donnee['function'][sensor].getIndex(times, index)
  else :
    raise Exception("Sensor inconnu")



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


def launch():
  os.dupterm(uart, 1)
  os.dupterm(None, 1)
  set_loop()
  loop.run_forever()

def set_loop():
  loop = asyncio.get_event_loop()
  loop.create_task(receiver())
  loop.create_task(saveSensor.saveAllSensor())

@register('loop', "")
def stop_loop():
  loop.stop()
  loop.close()


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
