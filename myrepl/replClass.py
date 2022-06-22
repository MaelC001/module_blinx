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
import saveSensor, sensors, bufferCircular, channelClass

#import sh1107, mpu9250
#import dps310_simple as dps310


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


# display info, can only connect to 1 display
display=None
displayType = None

class Repl():
    def __init__(self, i2c, uart):
        # connection to i2c
        self.i2c = i2c

        # serial port
        self.uart = uart

        self.display = None

        # function register

        self.dicOutputSensors = {}

    __register = {}
    def register(name, subFunction = "", register = __register):
        def decorator(fn):
            def inner_wrapper(self, *args, id, **kwargs):
                error = ""
                output = ""
                message = ""
                #returnResult = {}
                # execute the function and capture the error
                try:
                    output = fn(self, *args, **kwargs)
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
            register[name] = inner_wrapper
            return inner_wrapper
        return decorator

    # send message to serial port in json
    def sender(self, j):
        self.uart.write(json.dumps(j))

    # receive information by the serial port in json
    # and execute the function with the given argument
    async def receiver(self):
        sreader = asyncio.StreamReader(self.uart)
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
                self.sender(j)
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
                    self.sender(j)

                # method exist ?
                if cmd in self.__register:
                    # type of the parameter
                    if isinstance(args, list):
                        reply = self.__register[cmd](*args, id = id)
                        self.sender(reply)
                    elif isinstance(args, dict):
                        reply = self.__register[cmd](id = id, **args)
                        self.sender(reply)
                    else :
                        j={}
                        j['error'] = {"code": -32602, "message": "Invalid params"}
                        j['id'] = id
                        self.sender(j)
                else :
                    j={}
                    j['error'] = {"code": -32601, "message": "Method not found"}
                    j['id'] = id
                    self.sender(j)
            except Exception as e:
                #error = str(e)
                if id:
                    errorId = id
                else:
                    errorId = None
                j={}
                j['error'] = {"code": -32600, "message": "Invalid Request"}#error}
                j['id'] = errorId
                self.sender(j)

    @register('write', subFunction = "")
    def writeFile(self, name, text, format = 'w', doVerification=True):
        """
        write in a file
        arg :
            - name : str
            - text : str
            - format : str (optional)
        """
        if doVerification:
            self.verification(name, str)
            self.verification(text, str)
            self.verification(format, str, ['w','w+','a','a+'])
        f = open(name, format)
        f.write(text)
        f.close()
        return ''

    @register('read', subFunction = "")
    def readFile(self, name):
        """
        read a file
        arg :
            - name : str
        """
        self.verification(name, str, os.listdir(), True)
        f = open(name, 'r')
        r = f.read()
        f.close()
        return r

    @register('create', subFunction = "")
    def createFile(self, name):
        """
        create a file
        arg :
            - name : str
        """
        self.verification(name, str, os.listdir(), False)
        f = open(name, 'x')
        f.close()
        return ''

    @register('remove', subFunction = "")
    def removeFile(self, name):
        """
        remove a file
        arg :
            - name : str
        """
        self.verification(name, str, os.listdir(), True)
        os.remove(name)
        return ''

    @register('liste', subFunction = "")
    def listFile(self):
        """
        do the list of the file
        arg : none
        """
        return os.listdir()

    @register('exec', subFunction = "")
    def execute(self, cmd):
        """
        execute a command python of the user
        arg :
            - cmd : str
        """
        self.verification(cmd, str)

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


    """
    @register('digital', subFunction = "")
    def digital(pin, value = 0):
    ""
    change value output for a digital sensor
    arg :
        - pin : int
        - value : int (0, 1)
    ""
    self.verification(pin, int)
    self.verification(value, int, [0, 1])
    Pin(pin, mode=Pin.OUT).value(value)
    return ''
    """

    # the function led use the function digital
    # so if a error occur in digital, led have to say it
    """
    @register('led', subFunction = "digital")
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
    @register('PWMSensor', subFunction = "")
    def PWMSensor(pin, value, freq = 50):
    ""
    turn a servoMotor
    arg :
        - pin : int
        - value : int
        - freq : int (optional)
    ""
    self.verification(pin, int)
    self.verification(value, int)
    self.verification(freq, int)
    servo = PWM(Pin(pin))
    servo.freq(freq)
    servo.duty(value)
    return servo
    """

    @register('sensors_stop', subFunction = "")
    def sensorStop(self, newName):
        ...
        ...
        """
        stop record a sensor
        arg :
            - name : str
                # if it is a analog sensor we need the pin
                - p1 : int
                - p2 : int (optional)
                - p3 : int (optional)
        """
        self.verification(newName, str, saveSensor.listSensorModify)

        name = saveSensor.listSensorModify[newName]['name']

        saveSensor.listSensorModify.pop(newName)
        if name in saveSensor.donnee['name']:
            i = saveSensor.donnee['name'].index(name)
            saveSensor.donnee['name'].pop(i)
            saveSensor.donnee['function'].pop(name)
        elif name in self.dicOutputSensors:
            self.dicOutputSensors['function'].pop(name)
        else:
            raise Exception('sensor not find')
        return ''

    @register('configSensor', subFunction = "")
    def configSensor(self, dictConfig):
        """
        for config the sensors with custom names
        arg :
            - dictConfig : dict
        """
        self.verification(dictConfig, dict)

        for sensor, config in dictConfig.items():
            self.verification(sensor, str)#, saveSensor.listSensorModify)
            newName = config['new']
            input = config['input']
            saveSensor.listSensorModify[newName] = {'name' : sensor, 'channel': {}, "config": {}, "input" : input}
            self.sensorsCreate(sensor, created = True, input = input)

    def sensorsCreateDict(self, digital =  False):
        """
        create the dictionary with the information for each time
        """
        arrayTimeValue = [1, 10, 60, 600, 3600]
        arrayTimeName = ['1s', '10s', '1m', '10m', '1h']
        arrayTimeSize = [300] * 5
        arrayTimeOffset = [0, 0, 1, 2, 3]
        arrayNextTime = self.nextTime(arrayTimeValue)
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



    @register('get_sensors', subFunction = "")
    def getSensors(self, listSensors, times = '1s'):
        """
        get the data form the sensors
        if the time is 0s, we want the data form now
        """
        bufferCircular.tampon = True
        timeBefore = time.time()

        text, nameSensors = self.verificationListSensor(listSensors)
        # immedate data of the sensor
        if times == '0s':
            text += '\n' + str(time.time())
            for sensor in nameSensors:
                timeBefore = self.saveSensorWhileRequest(timeBefore)

                if sensor[:-3] == 'annalogique':
                    p1 = int(sensor[-3])
                    p2 = int(sensor[-2])
                    p3 = int(sensor[-1])
                    text += ';' + str(analogCreate(times = times, p1 = p1, p2 = p2, p3 = p3))
                elif sensor[:7] == 'digital':
                    pin = int(sensor[7:])
                    text += ';' + str(digitalCreate(times = times, pin = pin))
                else:
                    text += ';' + str(self.sensorsCreate(sensor, times))
            return text
        else :
            # capture each sensor the user want the data
            dataAllSensor = ''
            indexData = 0
            sizeBuffer = 300
            while indexData < sizeBuffer:
                textTimeStamp = ''
                for sensor in nameSensors:
                    timeBefore = self.saveSensorWhileRequest(timeBefore)

                    if sensor[:-3] == 'annalogique':
                        p1 = int(sensor[-3])
                        p2 = int(sensor[-2])
                        p3 = int(sensor[-1])
                        dataSensor, timeDataSensor = analogCreate(times = times, p1 = p1, p2 = p2, p3 = p3, index = indexData)
                    elif sensor[:7] == 'digital':
                        pin = int(sensor[7:])
                        dataSensor, timeDataSensor = digitalCreate(times = times, pin = pin, index = indexData)
                    else:
                        dataSensor, timeDataSensor = self.sensorsCreate(sensor, times, index = indexData)
                    textTimeStamp += ';' + dataSensor

                dataAllSensor = timeDataSensor + ';' + textTimeStamp + dataAllSensor

                indexData += 1
            text += '\n' + dataAllSensor

        bufferCircular.tampon = False
        return text

    def saveSensorWhileRequest(self, timeBefore):
        if timeBefore < time.time()+1:
            timeBefore = time.time()+1
            timeWait, finishWait, finishDonnee, l_donneeAnalog, indexAnalog = saveSensor.recordDataPart1()
            if not finishWait:
                time.sleep_ms(timeWait - time.time())

            saveSensor.recordDataPart2(finishDonnee, l_donneeAnalog, indexAnalog)
        return timeBefore

    def verificationListSensor(self, listSensors):
        """
        verification of the sensors : exist or not
        and capture the information
        """
        text = 'Time'
        nameSensors = []
        for sensor in listSensors:
            self.verification(sensor, str, saveSensor.listSensorModify)
            text += ';' + sensor
            nameSensors.append(saveSensor.listSensorModify[sensor]['name'])
        return text, nameSensors

    def sensorsCreate(self, sensor, index = 0, times = '1s', created = False, channels = [], info = None, input= True):
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
            tempoDict = self.sensorsCreateDict()
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
                    arrayChannel.append(channelClass.ChannelI2C(self.i2c, addr, byteReceive, codeSend, waitingTime, function))
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
                self.dicOutputSensors[sensor] = arrayChannel
        elif sensor in saveSensor.donnee['function']:
            return saveSensor.donnee['function'][sensor].getIndex(times, index)
        else :
            raise Exception("Sensor inconnu")

    def nextTime(self, arrayTime):
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


    def verification(self, value, type_value, possible = [], inPossible = True):
        """
        verify the value the user give us is correct
        """
        if not isinstance(value, type_value):
            message = f"the type of {value} isn't {type_value}"
            raise TypeError(message)
        if possible != [] and not ( (value not in possible) ^ inPossible ):
            message = f"{value} don't have a correct value"
            raise TypeError(message)

    def debug(self, json):
        """
        for the debugging, we will simulate the serial port
        """
        cmd = json['method']
        args = json['params']
        id = json['id']
        return self.__register[cmd](**args, id = id)







    # https://github.com/rdehuyss/micropython-ota-updater
    @register('updateFirmware', subFunction = "")
    def otaUpdate(self):
        from .ota_updater import OTAUpdater
        otaUpdater = OTAUpdater('https://github.com/MaelC001/micropython', github_src_dir='src', main_dir='app', secrets_file="secrets.py")
        otaUpdater.install_update_if_available()
        del(otaUpdater)
