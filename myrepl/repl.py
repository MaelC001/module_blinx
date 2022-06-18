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
import ssd1306, saveSensor, sensors, bufferCircular

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

@register('digital', "")
def digital(pin, value = 0):
  """
  change value output for a digital sensor
  arg :
    - pin : int
    - value : int (0, 1)
  """
  verification(pin, int)
  verification(value, int, [0, 1])
  Pin(pin, mode=Pin.OUT).value(value)
  return ''

# the function led use the function digital
# so if a error occur in digital, led have to say it
@register('led', "digital")
def led(value = 0):
  """
  play with the led
  arg :
    - value : int (0, 1)
  """
  pin = 2 # the led have the pin 2
  return digital(pin, value, id=0)

@register('PWMSensor', "")
def PWMSensor(pin, value, freq = 50):
  """
  turn a servoMotor
  arg :
    - pin : int
    - value : int
    - freq : int (optional)
  """
  verification(pin, int)
  verification(value, int)
  verification(freq, int)
  servo = PWM(Pin(pin))
  servo.freq(freq)
  servo.duty(value)
  return servo

@register('sensors_stop', "")
def sensorStop(name, p1 = 0, p2 = 0, p3 = 0):
  """
  stop record a sensor
  arg :
    - name : str
        # if it is a analog sensor we need the pin
          - p1 : int
          - p2 : int (optional)
          - p3 : int (optional)
  """
  analog = ['analogique'] if saveSensor.donnee['analog']['function'] else []
  digital = ['digital'] if saveSensor.donnee['digital']['function'] else []
  verification(name, str, saveSensor.donnee['i2c']['name'] + analog + digital)

  if name == 'analogique':
    # the name of the analog sensor is : 'analog' + pin 1 + pin 2 + pin 3
    name = nameAnalog(p1, p2, p3)
    saveSensor.donnee['analog']['function'].pop(i)
  elif name == 'digital':
    # the name of the analog sensor is : 'analog' + pin 1 + pin 2 + pin 3
    verification(p1, int)
    name = name+str(p1)
    saveSensor.donnee['digital']['function'].pop(name)
  else:
    i = saveSensor.donnee['i2c']['name'].index(name)
    saveSensor.donnee['i2c']['name'].pop(i)
    saveSensor.donnee['i2c']['function'].pop(name)
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
    verification(sensor, str, saveSensor.listSensorModify)
    newName = config['new']
    if sensor == 'analogique':
      p1 = config['p1']
      p2 = config['p2']
      p3 = config['p3']
      newNameAnalog = nameAnalog(p1 = p1, p2 = p2, p3 = p3)
      saveSensor.listSensorModify[newName] = {'name' : newNameAnalog, 'p1': p1, 'p2': p2, 'p3': p3}
      analogCreate(p1 = p1, p2 = p2, p3 = p3, created = True)
    elif sensor == 'digital':
      pin = config['pin']
      saveSensor.listSensorModify[newName] = {'name' : sensor+str(pin), 'pin': pin}
      digitalCreate(pin = pin, created = True)
    else:
      saveSensor.listSensorModify[newName] = {'name' : sensor}
      sensorsI2CCreate(sensor, created = True)

def sensorsCreate(digital =  False):
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
        text += ';' + str(sensorsI2CCreate(sensor, times))
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
          dataSensor, timeDataSensor = sensorsI2CCreate(sensor, times, index = indexData)
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
    nameSensors.append(saveSensor.listSensorModify[sensor])
  return text, nameSensors

def sensorsI2CCreate(sensor, index = 0, times = '1s', created = False):
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
      sensors.__listSensor[sensor]['immediate'](i2c = i2c)
    else:
      raise Exception("le sensor n'existe pas")
  elif created:
    tempoDict = sensorsCreate()
    function = bufferCircular.baseFunction
    if 'byte' in sensors.__listSensor[sensor]:
      function = sensors.__listSensor[sensor]['byte']
    waitingTime = sensors.__listSensor[sensor]['waiting']

    sensorI2C = bufferCircular.i2cSensor(sensor, tempoDict, i2c, None, waitingTime, function)
    saveSensor.donnee['i2c']['function'][sensor] = sensorI2C
    saveSensor.donnee['i2c']['name'].append(sensor)
  elif sensor in saveSensor.donnee['i2c']['function']:
    return saveSensor.donnee['i2c']['function'][sensor].getIndex(times, index)
  else :
    raise Exception("Sensor inconnu")

def analogCreate(times = '1s', p1 = 0, p2 = 0, p3 = 0, index = 0, created = False):
  """
  if created is True we begin to record the sensor
  else we return the bytearray of the data record it,
  with the time and index of the present record
  arg :
    - temps : str
    - p1 : int
    - p2 : int (optional)
    - p3 : int (optional)
    - index : int
    - created : boolean
  """
  name = nameAnalog(p1, p2, p3)
  if times == '0s':
    pinDic = {'p1' : p1, 'p2': p2, 'p3': p3}
    sensors.__listSensor['analogique']['immediate'](pinDic = pinDic)
  elif created:
    tempoDict = sensorsCreate()
    tempoDict['p1'] = p1
    tempoDict['p2'] = p2
    tempoDict['p3'] = p3

    analog = bufferCircular.AnalogSensor(name, tempoDict, None, 0)
    saveSensor.donnee['Analog']['function'][name] = analog
  elif name in saveSensor.donnee['Analog']['function']:
    return saveSensor.donnee['Analog']['function'][name].getIndex(times, index)
  else :
    raise Exception("Sensor inconnu")


def digitalCreate(pin, times = '1s', index = 0, created = False):
  """
  if created is True we begin to record the sensor
  else we return the bytearray of the data record it,
  with the time and index of the present record
  arg :
    - temps : str
    - pin : int
    - index : int
    - created : boolean
  """
  name = nameAnalog(p1, p2, p3)
  if times == '0s':
    sensors.__listSensor['digital']['immediate'](pin = pin)
  elif created:
    tempoDict = sensorsCreate(digital = True)

    digital = bufferCircular.DigitalSensor(name, tempoDict, None, 0, pin)
    saveSensor.donnee['digital']['function'][name] = digital
  elif name in saveSensor.donnee['digital']['function']:
    return saveSensor.donnee['digital']['function'][name].getIndex(times, index)
  else :
    raise Exception("Sensor inconnu")

def nextTime(arrayTime):
  """
  calculate the next we have each time, for example :
  if it is 12s, the next time we have 10s it is 20s
  if it is 96s, the next time we have 60s it is 120s
  """
  arrayNextTime = []
  present = time.time()
  for i in arrayTime:
    tempoTime = present + (i - (present % i))
    arrayNextTime.append(tempoTime)

  return arrayNextTime

def nameAnalog(p1, p2 = 0, p3 = 0):
  """
  the name of the analog sensors and verify the pin
  if (with p2=0 and p3 =0)
      p1 = 0 then analog is in pin 12
      p1 = 1 then analog is in pin 13
  """
  verification(p1, int, [0, 1])
  verification(p2, int, [0, 1])
  verification(p3, int, [0, 1])
  name = 'analogique'+str(p1)+str(p2)+str(p3)
  return name



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
