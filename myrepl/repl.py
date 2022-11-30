try:
  import utime as time
except:
  import time



# librairy from micropython :
try:
  import uos as os
except:
  import os
try:
  import uasyncio as asyncio
except:
  import asyncio

import sys, json, io
import network, binascii
from machine import Pin, I2C, SoftI2C, ADC, PWM, UART

# my librairy form the rpc :
import blinxSensor, sensors
# librairy form the ota updater
from ota_updater import OTAUpdater
# librairy for the web server/rpc wifi
import webServer


blinxSensor.sensors = sensors

# the class with all the sensor
Blinx = blinxSensor.Blinx({}, None)

# connection to i2c
#i2c = I2C(sda = Pin(4), scl = Pin(5))
#i2c = I2C(sda = Pin(5), scl = Pin(6))
i2c = SoftI2C(freq=400000, scl=Pin(19, pull=Pin.PULL_UP), sda=Pin(18, pull=Pin.PULL_UP)) # SoftI2C(sda = Pin(5), scl = Pin(6))


# the loop async
loop = None

# function register
__register = {}

# the connection wifi
wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)

# the ota updater
otaUpdater = OTAUpdater('https://github.com/MaelC001/micropython', github_src_dir = 'src', main_dir = 'main', secrets_file = '__config.json')

# connection with the UART
baud_rate = 9600
uart = UART(0, baudrate=baud_rate, tx=10, rx=9)  # UART(0, baud_rate)
uart.init(baudrate = baud_rate, rxbuf = 200)

# class for capture the stdout when `exec`
class DUP(io.IOBase):
  def __init__(self):
    self.s = bytearray()
  def write(self, data):
    self.s += data
    return len(data)
  def readinto(self, data):
    return 0
  def read_all(self):
    return str(self.s)

# the register for the user function
def register(name, sub_function = False):
  def wrapper(fn):
    def inner_wrapper(*args, id, **kwargs):
      output = ""
      # execute the function and capture the error
      try:
        # the output of the function
        output = fn(*args, **kwargs)
        # if the function use a user function, then we have to check the other function as well
        if sub_function and type(output) == dict:
          if 'error' in output:
            return {'error' : output['error'], 'id': id}
          elif 'result' in output:
            return {'result' : output['result'], 'id': id}
        return {'result' : output, 'id': id}
      except Exception as e:
        # the error of the function
        return {'error' : {"code": -32000, "message": str(e)}, 'id': id}

    __register[name] = inner_wrapper
    return inner_wrapper
  return wrapper

def sender(text):
  """send message to serial port in json"""
  if isinstance(text, dict) or isinstance(text, list):
    #sys.stdout.write(json.dumps(text))
    uart.write(json.dumps(text))
    uart.write('\n')
    return
  uart.write(text)
  uart.write('\n')

def senderDonneeSensor(donne):
  """send message to serial port in json"""
  if isinstance(donne, dict) or isinstance(donne, list):
    uart.write(json.dumps(donne))
    return
  uart.write(donne)

async def receiver():
  """
    receive information by the serial port in json
    and execute the function with the given argument
  """
  sreader = asyncio.StreamReader(uart) # sys.stdin)
  while True:
    # wait for the input
    data = await sreader.readline()
    # read the input
    decode_input(data, send = True, how_send_data = None, debug = True)

def decode_input(input, send = True, how_send = sender, how_send_data = senderDonneeSensor, printMessage = False, debug = False):
  """we will read the input and try to decode it, then we will try to execute it.

  Args:
      input (bytes): the input of the user
      send (bool, optional): do we send the info on the serial port?. Defaults to True.
      debug (bool, optional): do we send info by print?. Defaults to False.
  """
  try:
    # try to transform bytes to str
    line = input.decode('utf-8').rstrip()
    if debug:
      #print(0, line)
      pass
    # try to parse the json
    j = json.loads(line)
    if debug:
      #print(1, j)
      pass
  except Exception as e:
    # if an error appear, we send the error message and we stop the function
    #error = str(e)
    j = {
      'error' : {"code": -32700, "message": "Parse error"},
      'id' : None,
    }
    if debug:
      #print(2, j, str(e), line)
      pass
    elif printMessage:
      #print(j)
      pass
    if send:
      how_send(j)
    return

  read_input(j, send, how_send, how_send_data, printMessage, debug)

def read_input(j, send = True, how_send = sender, how_send_data = senderDonneeSensor, printMessage = False, debug = False):
  """we will read the input and try to decode it, then we will try to execute it.

  Args:
      input (bytes): the input of the user
      send (bool, optional): do we send the info on the serial port?. Defaults to True.
      debug (bool, optional): do we send info by print?. Defaults to False.
  """
  # try to read the parameter of the json
  # then the parameter of the method
  # to execute the method with the parameter
  try:
    id = j['id']
    cmd = j['method']
    args = j['params']

    # is the id correct ? and the command ?
    test_id_1 = isinstance(id, str)
    test_id_2 = isinstance(id, int)
    test_id_3 = id is None
    test_cmd = isinstance(cmd, str)
    if not(test_id_1 or test_id_2 or test_id_3) or not(test_cmd):
      j = {
        'error' : {"code": -32600, "message": "Invalid Request"},
        'id' : None,
      }
      if debug:
        #print(3, j, test_id_1, test_id_2, test_id_3, test_cmd)
        pass
      elif printMessage:
        #print(j)
        pass
      if send:
        how_send(j)
      return

    # method exist ?
    if cmd in __register:
      # type of the parameter
      if isinstance(args, list):
        reply = __register[cmd](*args, id = id)
        if debug:
          #print(4, reply)
          pass
        elif printMessage:
          #print(reply)
          pass
        if send:
          # if we don't want to get the data form the sensor then we send the reply normally
          # else we will send the data piece by piece in the function, so we have nothing to send
          # except if the request come from the rpc wifi, then we have to send it all the reply at once
          if cmd != 'get_sensors':
            how_send(reply)
          elif how_send_data != None:
            how_send_data(reply)
      elif isinstance(args, dict):
        reply = __register[cmd](id = id, **args)
        if debug:
          #print(5, reply)
          pass
        elif printMessage:
          #print(reply)
          pass
        if send:
          # if we don't want to get the data form the sensor then we send the reply normally
          # else we will send the data piece by piece in the function, so we have nothing to send
          # except if the request come from the rpc wifi, then we have to send it all the reply at once
          if cmd != 'get_sensors':
            how_send(reply)
          elif how_send_data != None:
            how_send_data(reply)
      else :
        # if the args is not a list or a dict we have a error
        j = {
          'error' : {"code": -32602, "message": "Invalid params"},
          'id' : id,
        }
        if debug:
          #print(6, j, type(args))
          pass
        elif printMessage:
          #print(j)
          pass
        if send:
          how_send(j)
    else :
      # if the command don't exist we have a error :
      j = {
        'error' : {"code": -32601, "message": "Method not found"},
        'id' : id,
      }
      if debug:
        #print(7, j, cmd, __register.keys)
        pass
      elif printMessage:
        #print(j)
        pass
      if send:
        how_send(j)
  except Exception as e:
    # if an error appear, we send the error message
    #error = str(e)
    #if id:
    #  error_id = id
    #else:
    j = {
      'error' : {"code": -32600, "message": "Invalid Request"},
      'id' : None,
    }
    if debug:
      #print(8, j, str(e))
      pass
    elif printMessage:
      #print(j)
      pass
    if send:
      how_send(j)


@register('write', False)
def write_file(name, text, format = 'w', do_verification = True):
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
    verification(format, str, ['w', 'w+', 'a', 'a+'])
  f = open(name, format)
  f.write(text)
  f.close()
  return ''

@register('read', False)
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

@register('create', False)
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

@register('remove', False)
def remove_file(name):
  """
  remove a file
  arg :
    - name : str
  """
  verification(name, str, os.listdir(), True)
  os.remove(name)
  return ''

@register('liste', False)
def list_file():
  """
  do the list of the file
  arg : none
  """
  return os.listdir()

@register('wifi', False)
def wifi():
  """
    we return all the wifi information
  """
  return {
    'wlan_sta' : {
      'active' : wlan_sta.active(), 
      'isconnected' : wlan_sta.isconnected(), 
#      'scan' : wlan_sta.scan() if wlan_sta.active() else [], # all the wifi the microcontroller scan
      'config' : {
        "ifcongif" : wlan_sta.ifconfig(), # the ip, netmask ...
        "mac" : wlan_sta.config('mac'), # the mac address
        "ssid" : wlan_sta.config('essid'), # the ssid of the wifi connected
        "dhcp_hostname" : wlan_sta.config('dhcp_hostname'), # the hostname of the microcontroller (for the mdns)
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

@register('wifi_active', False)
def wifi_active(active = True):
  """active the wifi

  Args:
      active (bool, optional): actived the wifi or desactived. Defaults to True.
  """
  wlan_sta.active(active)
  if not active:
    wlan_sta.disconnect()
  return ''

@register('wifi_connect', False)
def wifi_connect(ssid = '', password = ''):
  """connect the microcontroller to wifi

  Args:
      ssid (str, optional): the ssid to connect. Defaults to ''.
      password (str, optional): the password of the ssid. Defaults to ''.
  """
  # try to connect to wifi
  wlan_sta.connect(ssid, password)

  # get the status, to know if a error appear
  status = wlan_sta.status()
  if status == network.STAT_NO_AP_FOUND:
    return "no AP found"
  elif status == network.STAT_WRONG_PASSWORD:
    return "wrong password"
  elif status == network.STAT_CONNECT_FAIL:
    return "connection fail"

  time.sleep(0.1)
  return wlan_sta.isconnected()

@register('wifi_server', False)
def wifi_server(ssid = '', password = '', auth = 3, active = True):
  """create a wifi server

  Args:
      ssid (str, optional): the name of the wifi server. Defaults to ''.
      password (str, optional): the password of the wifi server. Defaults to ''.
      auth (int, optional): the mode of authentication of the wifi server. Defaults to 3.
      active (bool, optional): actived the wifi server?. Defaults to True.
  """
  wlan_ap.active(False)
  if active:
    wlan_ap.config(essid = ssid, password = password, authmode = auth)
    wlan_ap.active(True)
  return ''

@register('sensors_stop', False)
def sensor_stop():
  """
  stop all sensor
  arg : none
  """
  global Blinx
  Blinx = blinxSensor.Blinx({}, None)
  #sensors.__list_sensors.clear()
  return 'sensor stopped'

@register('configSensor', False)
def config_sensor(dictConfig):
  """
  for config the sensors with custom names
  arg :
    - dictConfig : dict
  """
  global Blinx
  verification(dictConfig, dict)
  sensors.get_all_function_sensor()
  Blinx = blinxSensor.Blinx(dictConfig, i2c)
  return 'change config success'

@register('remove_config', True)
def remove_all_function_sensor():
  """
    remove the last config for the sensor (remove the python file of the function)
  """
  sensors.__list_sensors.clear()
  try:
    import listSensorUser
  except:
    return 'no config'
  for i in listSensorUser.list_sensors:
    try:
      remove_file(i+'.py', id = 0)
      del sys.modules[i]
    except:
      continue
  remove_file("listSensorUser.py", id = 0)
  del sys.modules['listSensorUser']
  return 'success'

@register('sensors_output', False)
def output_sensors(sensor_name, array_value):
  """
    give a command to the ouput sensor

  Args:
      sensor_name (str): the name of the output sensor we want to change
      array_value (list): the data to write for each channel
  """
  verification(sensor_name, str, Blinx.output_sensors)
  array_value_format = []
  for i in array_value:
    if isinstance(i, str):
        try:
          t = int(i)
        except ValueError as e:
          t = i
        array_value_format.append(t)
    else:
      array_value_format.append(i)
  Blinx.output_sensors[sensor_name]['sensor'].write(array_value_format)
  return 'Done'

@register('display', False)
def display_sensors(sensor_name, func_name, array_value): #*array_value):
  """
    give a command to a display sensor

  Args:
      sensor_name (str): the name of the display sensor
      func_name (str): the function we want to use for the command
  """
  verification(sensor_name, str, Blinx.display_sensors)
  return Blinx.display_sensors[sensor_name]['sensor'].function(func_name, *array_value)

@register('get_sensors', False)
def get_sensors(list_sensors, times = '1s', notAll = True):
  """
  get the data form the sensors in the list
  if the time is 0s, we want the data form now
  """
  crc = 0

  if notAll:
    senderDonneeSensor("{'id':0,'result':[")
  else :
    j = {'id':0, 'result':[]}

  present_ticks = time.ticks_ms()
  time_before = present_ticks - present_ticks % 100

  text, name_sensors, function_sensors = verification_list_sensor(list_sensors)

  if notAll:
    senderDonneeSensor(name_sensors)
    senderDonneeSensor(",['")
    senderDonneeSensor(text)
  else :
    j['result'].append(name_sensors)
    j['result'].append([])
    textAll = text

  blinxSensor.buffer = True

  # immedate data of the sensor
  if times == '0s':
    text += '\n' + str(time.time())
    for i in range(len(name_sensors)):
      time_before = save_sensor_while_request(time_before)
      sensor_info = sensors.__list_sensors[name_sensors[i]]['immediate'](i2c, function_sensors[name_sensors[i]].pin_sensor)
      text += ';' + str(sensor_info)

    if notAll:
      senderDonneeSensor("','")
      senderDonneeSensor(text)
    else :
      j['result'][1].append(text)

    crc = binascii.crc32(bytes(text,'utf-8'))
  else :
    # capture all the data from each sensor the user want the data
    index_data = 0
    size_buffer_max = 300

    while index_data < size_buffer_max:
      #print(index_data)

      #text_time_stamp = ''
      #time_data_sensor = 0
      dateShow = True
      if notAll:
        senderDonneeSensor("','")
      else :
        j['result'][1].append(textAll)
        textAll = ""

      for i in range(len(function_sensors)):
        func = function_sensors[i]
        time_before = save_sensor_while_request(time_before)

        for y in func.get_index(times, index_data, True):
          #print(y)
          if y[0] == b'\xff\xff':
            break
          elif y[0] == b'\xff\xfe':
            data_sensor, time_data_sensor = 'error', y[1]
            #text_time_stamp += ';' + str(data_sensor)
          else:
            data_sensor, time_data_sensor = y
            #text_time_stamp += ';' + str(data_sensor)
          if dateShow:
            if notAll:
              senderDonneeSensor(time_data_sensor)
            else :
              textAll += time_data_sensor
            crc = binascii.crc32(bytes(str(time_data_sensor),'utf-8'), crc)
            dateShow = False
          
          if notAll:
            senderDonneeSensor(';')
          else :
            textAll += ';'
          
          crc = binascii.crc32(bytes(';','utf-8'), crc)
          
          if notAll:
            senderDonneeSensor(data_sensor)
          else :
            textAll += data_sensor
          
          crc = binascii.crc32(data_sensor, crc)
        else:
          continue
        break
      else:
        index_data += 1
        continue
      break
  blinxSensor.buffer = False
  Blinx.buffer_to_log()
  if notAll:
    senderDonneeSensor("'],[")
    senderDonneeSensor(crc)
    senderDonneeSensor("]}\n")
    return ""
  else :
    if textAll != "":
      j['result'][1].append(textAll)
    j['result'].append(crc)
    return j

@register('scan_i2c', False)
def scan_i2c(addr = None):
  """scan the i2c bus and look if a address is in the

  Args:
      addr (hex, optional): the hexadecimal address of the i2c sensor we are looking at. Defaults to None.

  Returns:
      list or bool: all the i2c address connected (list) or is the address given in the i2c bus (bool)
  """
  if addr == None:
    return i2c.scan()
  return addr in i2c.scan()

def save_sensor_while_request(time_before):
  """
  when we get the data form the sensors for the user, 
  we have to continue to capture the data
  """
  present = time.ticks_ms()
  diffTime = 1000 - blinxSensor.diff_ticks(time_before, present)

  if diffTime <= 0:
    time_before = time_before + 1000
    Blinx.save(present)
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
    verification(sensor, str, Blinx.input_sensors)
    text += ';' + sensor
    name = Blinx.input_sensors[sensor]['name']
    for i in Blinx.input_sensors[sensor]['sensor'].channels:
      name_sensors.append(name+'-'+str(i.id))
    function_sensors.append(Blinx.input_sensors[sensor]['sensor'])
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

    Blinx.save(time.ticks_ms())

    present = time.ticks_ms()
    diffTime = 1000 - blinxSensor.diff_ticks(time_before, present)
    if diffTime > 0:
      await asyncio.sleep_ms(diffTime)

def launch(site = False):
  if site:
    webServer.websocket_helper.decode_input = decode_input
    webServer.start()
  os.dupterm(uart, 0)
  os.dupterm(None, 0)
  loop = asyncio.get_event_loop()
  loop.create_task(receiver())
  loop.create_task(save_all_sensor())
  loop.run_forever()

"""
for the debugging, we will simulate the serial port
"""
# data = b'{"method":"liste","params":[],"id":0}'
# read_input(data, send = False, debug = True)







# https://github.com/rdehuyss/micropython-ota-updater
@register('updateFirmware', False)
def ota_update():
  """
    update the firmware of the microcontroller
  """
  otaUpdater.install_update_if_available()
