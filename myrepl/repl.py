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
import blinxSensor, sensors, display, network

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

wlan_sta=network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_ap=network.WLAN(network.AP_IF)
wlan_ap.active(False)

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
def register(name, sub_function=""):
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
        elif sub_function and type(output) == dict:
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
      error_id = None
      j={}
      j['error'] = {"code": -32700, "message": "Parse error"}#error}
      j['id'] = error_id
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
        error_id = id
      else:
        error_id = None
      j={}
      j['error'] = {"code": -32600, "message": "Invalid Request"}#error}
      j['id'] = error_id
      sender(j)

@register('write', "")
def write_file(name, text, format = 'w', do_verification=True):
  """
  write in a file
  arg :
    - name : str
    - text : str
    - format : str (optional)
  """
  if do_verification:
    verification(name, str)
    verification(text, str)
    verification(format, str, ['w','w+','a','a+'])
  f = open(name, format)
  f.write(text)
  f.close()
  return ''

@register('read', "")
def read_file(name):
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
def create_file(name):
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
def remove_file(name):
  """
  remove a file
  arg :
    - name : str
  """
  verification(name, str, os.listdir(), True)
  os.remove(name)
  return ''

@register('liste', "")
def list_file():
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

@register('wifi', "")
def wifi():
  return {
    'wlan_sta' : {
      'active' : wlan_sta.active(),
      'isconnected' : wlan_sta.isconnected(),
      'scan' : wlan_sta.scan() if wlan_sta.active() else [],
      'config' : {
        "ifcongif" : wlan_sta.ifconfig(),
        "mac" : wlan_sta.config('mac'),
        "ssid" : wlan_sta.config('essid'),
        "dhcp_hostname" : wlan_sta.config('dhcp_hostname'),
      },
    },
    'wlan_ap' : {
      'active' : wlan_ap.active(),
      'isconnected' : wlan_ap.isconnected(),
      'config' : {
        "ifcongif" : wlan_ap.ifconfig(),
        "mac" : wlan_ap.config('mac'),
        "ssid" : wlan_ap.config('essid'),
        "channel" : wlan_ap.config('channel'),
        "hidden" : wlan_ap.config('hidden'),
        "authmode" : wlan_ap.config('authmode'),
      },
    },
  }

@register('wifi_connect', "")
def wifi_connect(ssid = '', password = '', active = True):
  wlan_sta.active(active)
  if active:
    if not wlan_sta.isconnected():
      wlan_sta.connect(ssid, password)

      status = wlan_sta.status()
      if status == network.STAT_NO_AP_FOUND:
        return "no AP found"
      elif status == network.STAT_WRONG_PASSWORD:
        return "wrong password"
      elif status == network.STAT_CONNECT_FAIL:
        return "connection fail"

      time.sleep(0.1)
      return wlan_sta.isconnected()
  else :
    wlan_sta.disconnect()

@register('wifi_server', "")
def wifi_server(ssid = '', password = '', auth = 3, active = True):
  wlan_ap.active(False)
  if active:
    wlan_ap.config(essid=ssid, password=password, authmode=auth)
    wlan_ap.active(True)

@register('sensors_stop', "")
def sensor_stop():
  """
  stop all sensor
  arg : none
  """
  global Blinx
  Blinx = blinxSensor.Blinx()
  #sensors.__listSensor.clear()


@register('configSensor', "")
def config_sensor(dictConfig):
  """
  for config the sensors with custom names
  arg :
    - dictConfig : dict
  """
  global Blinx
  verification(dictConfig, dict)
  Blinx = blinxSensor.Blinx(dictConfig, i2c)
  sensors.get_all_function_sensor()

@register('remove_config', "remove_file")
def remove_all_function_sensor():
  sensors.__listSensor.clear()
  try:
    import listSensorUser
  except:
    return
  for i in listSensorUser.array:
    remove_file(i+'.py')
  remove_file("listSensorUser.py")
  del sys.modules['listSensorUser']

@register('get_sensors', "")
def get_sensors(list_sensors, times = '1s'):
  """
  get the data form the sensors in the list
  if the time is 0s, we want the data form now
  """
  blinxSensor.tampon = True
  time_before = time.time()

  text, name_sensors, function_sensors = verification_list_sensor(list_sensors)
  # immedate data of the sensor
  if times == '0s':
    text += '\n' + str(time.time())
    for sensor in name_sensors:
      time_before = save_sensor_while_request(time_before)
      sensor_info = sensors.__listSensor[sensor]['immediate']
      text += ';' + str(sensor_info['func'](i2c, **sensor_info['args']))
    return text
  else :
    # capture all the data from each sensor the user want the data
    data_all_sensor = ''
    index_data = 0
    size_buffer = 300
    while index_data < size_buffer:
      text_time_stamp = ''
      for i in range(len(function_sensors)):
        func = function_sensors[i]
        sensor = name_sensors[i]
        time_before = save_sensor_while_request(time_before)
        data_sensor, time_data_sensor = func.getIndex(times, index_data)
        text_time_stamp += ';' + data_sensor

      data_all_sensor = time_data_sensor + ';' + text_time_stamp + data_all_sensor

      index_data += 1
    text += '\n' + data_all_sensor

  blinxSensor.tampon = False
  return text

def save_sensor_while_request(time_before):
  """
  when we get the data form the sensors for the user,
  we have to continue to capture the data
  """
  if time_before < time.time()+1:
    time_before = time.time()+1
    Blinx.save()
  return time_before

def verification_list_sensor(list_sensors):
  """
  verification of the sensors : exist or not
  and capture the information
  """
  text = 'Time'
  name_sensors = []
  function_sensors = []
  for sensor in list_sensors:
    verification(sensor, str, Blinx.sensors_input)
    text += ';' + sensor
    name_sensors.append(Blinx.sensors_input[sensor]['name'])
    function_sensors.append(Blinx.sensors_input[sensor]['sensor'])
  return text, name_sensors, function_sensors



def verification(value, type_value, possible = [], in_possible = True):
  """
  verify the value the user give us is correct
  """
  if not isinstance(value, type_value):
    message = f"the type of {value} isn't {type_value}"
    raise TypeError(message)
  if possible != [] and not ( (value not in possible) ^ in_possible ):
    message = f"{value} don't have a correct value"
    raise TypeError(message)


async def save_all_sensor():
  while True:
    # we will wait a minimum of 1 secondes before we recommence
    time_before = time.ticks_ms()

    Blinx.save()

    present= time.ticks_ms()
    diffTime = 1000 - blinxSensor.diffTicks(time_before, present)
    if diffTime > 0:
      await asyncio.sleep_ms(diffTime)

def launch():
  os.dupterm(uart, 1)
  os.dupterm(None, 1)
  loop = asyncio.get_event_loop()
  loop.create_task(receiver())
  loop.create_task(save_all_sensor())
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
