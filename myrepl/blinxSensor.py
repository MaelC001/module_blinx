from machine import Pin, ADC, PWM, I2C
from time import sleep_ms
import sensors, time

# do we do a conversion
tampon = False
# number of boucle
ticks_boucle = 0
time_ns = time.time_ns() - time.ticks_ms()
ticks_max = 2**30


class Blinx():
    def __init__(self, configs = {}, i2c = None):
        # list of all the sensor
        self.sensors = {}
        # list of all the input sensor
        self.sensors_input = {}
        # list of all the output sensor
        self.sensors_output = {}
        for sensor, config in configs.items():
            newName = config['new']
            input = config['input']
            channels = config['channels']
            temp = {'name' : sensor, 'sensor' : Sensor(sensor, channels,  input, i2c)}
            self.sensors[newName] = temp
            if input :
                self.sensors_input[newName] = temp
            else:
                self.sensors_output[newName] = temp

    def save(self, time):
        # save the reply of all the sensor
        for i in self.sensors.values():
            i['sensor'].save(time)

    def getIndex(self, time, index):
        # get the data from a index for all the sensor
        result = []
        for i in self.sensors.values():
            result.append(i['sensor'].getIndex(time, index))
        return result

    def getTimeBuffer(self, time):
        # current time of the buffer
        tempo = next(iter(a.keys()))
        return self.sensors[tempo]['sensor'].getTimeBuffer(time)

    def tampon2log(self):
        # move the tampon to the log
        for i in self.sensors.values():
            i['sensor'].tampon2log(time)


# Sensors
class Sensor():
    def __init__(self, sensorType, channels = [], input= True, error = bytearray(b'\xff\xfe'), i2c = None):
        # the type of sensor
        self.sensorType = sensorType
        # the error code
        self.error = error
        # number of byte for each data
        self.size = 2
        # it is a input or output sensor
        self.input = input
        # the i2c bus
        self.i2c = i2c
        # the list of the channel of each pin for the sensor
        self.arrayChannel = []
        # the number of channel
        self.numberChannel = len(channels)
        # the waiting time
        self.waiting = 0
        # create all the channel
        self._createChannel(sensorType, channels, input)

    def _createChannel(self, sensor, channels = [], input= True):
        """create all the channel"""
        for channel in channels:
            if channel['type'] == "I2C":
                id = channel['id']
                function = sensors.__listSensor[sensor]['byte'+id]['func']
                waitingTime = sensors.__listSensor[sensor]['byte'+id]['waiting']
                if self.waiting < waitingTime:
                    self.waiting = waitingTime

                addr = sensors.infoSensorI2C[sensor]['addr']
                byteReceive = sensors.infoSensorI2C[sensor]['byteReceive']
                codeSend = sensors.infoSensorI2C[sensor]['codeSend']
                self.arrayChannel.append(ChannelI2C(self.i2c, addr, byteReceive, codeSend, waitingTime, function))
            elif channel['type'] == "Analog":
                id = channel['id']
                function = sensors.__listSensor[sensor]['byte'+id]['func']

                pin = channel['pin']
                p1 = channel['p1']
                p2 = channel['p2']
                p3 = channel['p3']
                freq = channel['freq']
                self.arrayChannel.append(ChannelAnalog(pin, p1, p2, p3, function, freq = freq))
            elif channel['type'] == "Digital":
                pin = channel['pin']
                self.arrayChannel.append(ChannelDigital(pin))

    def save(self, time):
        # save the reply of the sensor
        # if we are converting the data, we record the new data in a tampon (only each 1s)
        # when we finish the convert we will move the data from the tampon to the log
        if tampon:
            for i in self.arrayChannel:
                i.tamponSave(time)
        else:
            for i in self.arrayChannel:
                i.save(time)

    def wait(self):
        # the time to wait before retrieve the reply
        return self.waiting

    def getIndex(self, time, index):
        # get the data from a index of all channel
        result = []
        for i in self.arrayChannel:
            result.append(i.getIndex(time, index))
        return result

    def getTimeBuffer(self, time):
        # current time of the buffer
        return self.arrayChannel[0].getTimeBuffer(time)


    def tampon2log(self):
        # move the tampon to log
        for i in self.arrayChannel:
            i.tampon2log(time)


# Channels
class Channel():
    def __init__(self, translateFunction, error = bytearray(b'\xff\xfe')):

        # the tampon for when we convert the data
        self.tampon = Buffer(30)

        # the data for the last reply
        self.oldData = 0
        # the function to translate the byte
        self.translateFunction = translateFunction
        # the error code
        self.error = error

        # the dic of information of the channel + their buffer
        self.dic = {}
        for key, config in sensorsCreateDict().items():
            size = config['size']
            times = config['times']
            step = config['value']
            name = config['name']

            tempo = {}
            self.buffer = self.createBuffer(name, size, step, times, error)
            tempo['before'] = config['before']
            tempo['offset'] = config['offset']
            tempo['times'] = times
            tempo['next'] = step

            if key == '1s':
                self.size = size

            self.dic[key] = tempo
    def createBuffer(self, name, size, step, times, error):
        return BufferCircular(name, size, step, times, error = error)

    def read(self):
        pass
    def write(self, value):
        pass

    def save(self, time):
        """
            save the reply of the sensor
        """
        for i in self.dic:
            tempo = self.dic[i]
            before = tempo['before']
            next = tempo['next']
            if (tempo['times'] + tempo['offset']) <= time:
                # is it a mean of the reply of before ?
                if before == None :
                    value = self.read()
                else:
                    bufferBefore = self.dic[before]['buffer']
                    lastTime = tempo['times'] - next
                    array = bufferBefore.getPartial(lastTime)
                    s = self.sumByte(array[0], bufferBefore.dataSize)
                    value = int(s/array[1])
                    value = value.to_bytes(2, 'big')
                tempo['buffer'].append(value, time)
                tempo['times'] += next
    def tamponSave(self, time):
        """
            we are converting the data, we record the new data in a tampon (only each 1s)
            when we finish the convert we will move the data from the tampon to the log
        """
        if self.tampon.time == -1:
            self.tampon.setTime(time)
        value = self.read()
        self.tampon.append(value, time)

    def tampon2log(self):
        """
            when we finish with tge tampon,
            we have to transfert all data from the tampon
            to the log and do the mean for the different time
        """
        self.tampon.setTime(-1)
        lenArray = 30

        for index in range(lenArray):
                valueBrut, time = self.tampon.getIndex(index)
                for i in self.dic:
                    tempo = self.dic[i]
                    before = tempo['before']
                    next = tempo['next']
                    if (tempo['times'] + tempo['offset']) <= time:
                        if before == None :
                            value = valueBrut
                        else:
                            bufferBefore = self.dic[before]['buffer']
                            lastTime = tempo['times'] - next
                            array = bufferBefore.getPartial(lastTime)
                            s = sum(array[0], bufferBefore.dataSize)
                            value = int(s/array[1])
                            value = value.to_bytes(2, 'big')
                        tempo['buffer'].append(value, time)
                        tempo['times'] += next
        self.tampon.clear()

    def sumByte(self, byteArray, nmbByte):
        """ sum the data sensor in a bytearray """
        s = 0
        for i in range(0, len(byteArray), nmbByte):
            y = i+nmbByte
            sub = byteArray[i:y]
            if nmbByte > 1:
                s += int.from_bytes(sub, 'big')
            else :
                s += int.from_bytes(sub, 'big')
        return s

    def getTimeBuffer(self, time):
        """ current time of the buffer """
        tempo = self.dic[time]['buffer']
        diffBoucle = ticks_boucle - tempo.ticks_boucle
        return tempo.time + time_ns - ticks_max * diffBoucle

    def getIndex(self, time, index):
        """ get the data for a index """
        tempo = self.dic[time]['buffer']
        return tempo.getIndex(index)


class ChannelDigital(Channel):
    def __init__(self, pin, error = bytearray(b'\xff\xfe'), translateFunction = lambda x,y,z : b'\x01' if x else b'\x00'):
        # the pin for the sensor
        self.pin = Pin(pin, Pin.OUT)

        super().__init__(translateFunction, error)

    def createBuffer(self, name, size, step, times, error):
        return BufferCircular(name, size, step, times, error = error, dataSize = 1)

    def read(self):
        return self.translateFunction(self.pin(), self.error, self.oldData)
    def write(self, value):
        self.pin.value(value)

class ChannelAnalog(Channel):
    def __init__(self, pin, p1, p2, p3, error = bytearray(b'\xff\xfe'), translateFunction = lambda x,y,z : x, freq = 1000):
        # the pin for the output
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(pin)
        self.pwm.freq(freq)

        # the pin for the input
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        super().__init__(translateFunction, error)
    def read(self):
        Pin(0, mode=Pin.OUT).value(self.p1)
        Pin(2, mode=Pin.OUT).value(self.p2)
        Pin(15, mode=Pin.OUT).value(self.p3)
        return self.translateFunction(ADC(0).read(), self.error, self.oldData)
    def write(self, value):
        self.pwm.duty(value)

class ChannelI2C(Channel):
    def __init__(self, i2c, addr, byteReceive, codeSend, wait, error = bytearray(b'\xff\xfe'), translateFunction = lambda x,y,z : x):
        # the i2c bus
        self.i2c = i2c
        # the i2c addr for the sensor
        self.addr = addr
        # the byte to receive from the sensor
        self.byteReceive = byteReceive
        # the code to send to the sensor
        self.codeSend = codeSend
        # the time to wait
        self.wait = wait

        super().__init__(translateFunction, error)
    def read(self):
        self.write(self.codeSend)
        sleep_ms(self.wait)
        return self.read_i2c()
    def write(self, value):
        self.i2c.writeto(self.addr, value)
    def read_i2c(self):
        return self.translateFunction(self.i2c.readfrom(self.addr, self.byteReceive), self.error, self.oldData)

# Buffers
class Buffer():
    def __init__(self, size, step = 1, time = 0, null = bytearray(b'\xff\xff'), dataSize = 2):
        # the real index in the byte array
        self.realIndex = 0
        # the index for the each data, it is not equal to the realIndex,
        # if the data is stock in multiple byte
        self.dataIndex = 0
        # value index is the value of one index
        # if the index is 2, and step=1, then we are at 2s
        # if the index is 2, and step=10, then we are at 20s ...
        self.step = step
        # it is the number of byte to stock the data
        self.dataSize = dataSize
        # it is the number of data stock
        self.size = size
        # the code for error
        self.null = null
        # number of boucle of the ticks
        self.ticks_boucle = ticks_boucle
        # the byte array for data
        #self._data = null*(size*dataSize)   # each measure is stored in 2 bytes
        self._data = bytearray()
        for _ in range(size*dataSize) :
            self._data += null
        # the timestamp in index 0
        self.time = time

    def append(self, value, time):
        """
        verify if we don't miss data and if we have to reset the index
        then add the 2 bytes of information
        """
        self.fix_missing_data(time)
        self.resetIndex(time)
        for i in range(self.dataSize):
            self._data[self.realIndex] = value[i]
            self.realIndex += 1
        self.dataIndex += 1

    def resetIndex(self, time):
        """reset the index"""
        if self.dataIndex == self.size:
            self.realIndex = 0
            self.dataIndex = 0
            self.time = time
            self.ticks_boucle = ticks_boucle

    def getIndex(self, index):
        """get all the data of a index (in accordance with the present data (index 0)) to the present data"""
        diffBoucle = ticks_boucle - self.ticks_boucle
        time_ns = time_ns - ticks_max * diffBoucle
        diff = self.dataIndex - index - 1
        if self.dataIndex == 0:
            timeData = self.size * self.step
        elif self.dataIndex > index:
            timeData = self.time + diff
        elif self.dataIndex <= index:
            timeData = self.time - (diff - self.dataIndex)
        indexData = diff*self.dataSize
        return self._data[indexData : indexData+self.dataSize], timeData + time_ns

    def lastTime(self):
        """last time we stock a data"""
        return self.time + (self.dataIndex-1) * self.step

    def missing(self, time):
        """do we have missing data"""
        return int(diffTicks(self.lastTime() + self.step, time)/1000) > 0

    def fix_missing_data(self, time):
        """correct the missing data : put the 'null' bytes in missing data"""
        if self.missing(time):
            self.append(self.null, time - 1)

    def setTime(self, time):
        """change the time"""
        self.time = time

    def clear(self):
        """clear of the data (for the tampon)"""
        self.realIndex = 0
        self.dataIndex = 0
        self._data = bytearray()
        for _ in range(self.size*self.dataSize) :
            self._data += self.null
        self.time = -1

class BufferCircular(Buffer):
    def __init__(self, name, size, step = 1, time = 0, null = bytearray(b'\xff\xff'), error = bytearray(b'\xff\xfe'), dataSize = 2):
        # the code for error
        self.error = error
        # the nam of the sensor
        self.name = name
        super().__init__(size, step, time, null, dataSize)

    def getPartial(self, timeStamp):
        """get partial data, with the timeStamp"""
        i = round((timeStamp - self.time) / self.step)
        l = self.getData(timeStamp >= self.time, i)
        return self.getListModify(l)

    def getAll(self):
        """get all the data"""
        return self._data

    def getListModify(self, l):
        """remove the error and the missing data of the list"""
        array = bytearray()
        s = 0
        for i in range(0, len(l), self.dataSize):
            y = i+self.dataSize
            sub = l[i:y]
            if sub != self.null and sub != self.error:
                s += 1
                array += sub
        return array, s

    def save(self, nmb):
        """save a number of the data"""
        i = self.dataIndex - nmb
        l = self.getData(self.dataIndex >= nmb, i)

        text = self.array2str(l)
        return text

    def array2str(array, separator = '\n'):
        """change array to string"""
        return separator.join(array) + separator

    def getData(self, beforeIndex, i):
        """
        beforeIndex : is the information we want begin
        before or after the current index
        """
        if beforeIndex :
            l = self._data[i*self.dataSize:self.realIndex*self.dataSize]
            l = self.reverseBytearray(l)
        else:
            l1 = self._data[:self.realIndex*self.dataSize]
            l1 = self.reverseBytearray(l1)
            l2 = self._data[i*self.dataSize:]
            l2 = self.reverseBytearray(l2)
            l = l1 + l2
        return l

    def reverseBytearray(self, array):
        """reverse the data of a sensor in a bytearray"""
        l = len(array)
        tempo = bytearray()
        for i in range(l, 0, -self.dataSize):
            y = i-self.dataSize
            sub = array[y:i]
            tempo += sub
        return tempo




def sensorsCreateDict():
    """
    create the dic of the info for the buffer
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
        before = nameTime
    return tempoDict


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

def diffTicks(self, before, after, diffMax = 2000):
    """calcul the difference between to ticks"""
    diff = time.ticks_diff(after, before)
    if after >= before:
        return diff
    else :
        resetTicks()
        return diff

def resetTicks():
    """reset ticks"""
    global ticks_boucle, time_ns
    ticks_boucle += 1
    time_ns = time.time_ns() - time.ticks_ms()