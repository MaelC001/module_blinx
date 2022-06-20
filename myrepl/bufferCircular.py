from machine import Pin, ADC
import saveSensor

tampon = False



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
        self.ticks_boucle = saveSensor.ticks_boucle
        # the byte array for data
        #self._data = null*(size*dataSize)   # each measure is stored in 2 bytes
        self._data = bytearray()
        for _ in range(size*dataSize) :
            self._data += null
        # the timestamp in index 0
        self.time = time

    def append(self, value, time):
        # verify if we don't miss data and if we have to reset the index
        # ten add the 2 bytes of information
        self.fix_missing_data(time)
        self.resetIndex(time)
        for i in range(self.dataSize):
            self._data[self.realIndex] = value[i]
            self.realIndex += 1
        self.dataIndex += 1

    def resetIndex(self, time):
        # reset the index
        if self.dataIndex == self.size:
            self.realIndex = 0
            self.dataIndex = 0
            self.time = time
            self.ticks_boucle = saveSensor.ticks_boucle

    def getIndex(self, index):
        # get all the data of a index (in accordance with the present data (index 0)) to the present data
        diffBoucle = saveSensor.ticks_boucle - self.ticks_boucle
        time_ns = saveSensor.time_ns - saveSensor.ticks_max * diffBoucle
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
        # last time we stock a data
        return self.time + (self.dataIndex-1) * self.step

    def missing(self, time):
        # do we have missing data
        return int(saveSensor.diffTicks(self.lastTime() + self.step, time)/1000) > 0

    def fix_missing_data(self, time):
        # correct the missing data : put the 'null' bytes in missing data
        if self.missing(time):
            self.append(self.null, time - 1)

    def setTime(self, time):
        # change the time
        self.time = time

    def clear(self):
        # clear of the data (for the tampon)
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
        # get partial data, with the timeStamp
        i = round((timeStamp - self.time) / self.step)
        l = self.getData(timeStamp >= self.time, i)
        return self.getListModify(l)

    def getAll(self):
        # get all the data
        return self._data

    def getListModify(self, l):
        # remove the error and the missing data of the list
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
        # save a number of the data
        i = self.dataIndex - nmb
        l = self.getData(self.dataIndex >= nmb, i)

        text = self.array2str(l)
        return text

    def array2str(array, separator = '\n'):
        # change array to string
        return separator.join(array) + separator

    def getData(self, beforeIndex, i):
        # beforeIndex : is the information we want begin
        # before or after the current index
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
        # reverse the data of a sensor in a bytearray
        l = len(array)
        tempo = bytearray()
        for i in range(l, 0, -self.dataSize):
            y = i-self.dataSize
            sub = array[y:i]
            tempo += sub
        return tempo


class Sensor():
    def __init__(self, sensorType, listChannel, dic, save, waiting, error = bytearray(b'\xff\xfe')):
        # the type of sensor
        self.sensorType = sensorType
        # when do we have to save in a file
        self.whenSave = save
        # the waiting time between the request and the reply of the sensor
        self.waiting = waiting
        # the waiting time between the request and the reply of the sensor
        self.tamponArray.setTime(-1)
        # the error code
        self.error = error
        # number of byte for each data
        self.size = 1
        # the dictionary of information of each time (plus their circular buffer)
        self.listChannel = listChannel
        self.numberChannel = len(listChannel)
        self.array = []
        self.tamponArray = []
        for i in range(self.numberChannel):
            self.array.append(self.to_dict(listChannel[i],dic, error))
            self.tamponArray.append(Buffer(30))

    def to_dict(self, dic, error):
        # create the dic with different information for each time to save
        tempoDictonary = {}
        for key, element in dic.items():
            size = element['size']
            times = element['times']
            valueIndex = element['value']
            name = self.sensorType + '_' + key + '.csv'

            tempo = {}
            if 'dataSize' in element:
                tempo['buffer'] = BufferCircular(name, size, valueIndex, times, error = error, dataSize = element['dataSize'])
            else:
                tempo['buffer'] = BufferCircular(name, size, valueIndex, times, error = error)
            tempo['before'] = element['before']
            tempo['offset'] = element['offset']
            tempo['times'] = times
            tempo['next'] = valueIndex

            if key == '1s':
                self.size = size

            tempoDictonary[key] = tempo
        return tempoDictonary

    def save(self, time):
        # save the reply of the sensor

        # is it time to save in a file ?
        #writable = self.time2write(time)

        # if we are converting the data, we record the new data in a tampon (only each 1s)
        # when we finish the convert we will move the data from the tampon to the log
        if tampon:
            if self.tamponArray[0].time == -1:
                for i in range(self.numberChannel):
                    self.tamponArray.setTime(time)
            for i in range(self.numberChannel):
                value = self.listChannel[i].read()
                self.tamponArray[i].append(value, time)
        else:
            # if we write in the log, we will see each time (not only 1s)
            # if it is 1s (no data before), we will record the data
            # else we will do a mean form the data from before
            for index in range(self.numberChannel):
                for i in self.array[index]:
                    tempo = self.array[i]
                    before = tempo['before']
                    next = tempo['next']
                    if (tempo['times'] + tempo['offset']) <= time:
                        #if writable:
                        #    tempo['buffer'].save()

                        # is it a mean of the reply of before ?
                        if before == None :
                            value = self.listChannel[index].read()
                        else:
                            bufferBefore = self.array[index][before]['buffer']
                            lastTime = tempo['times'] - next
                            array = bufferBefore.getPartial(lastTime)
                            s = sum(array[0], bufferBefore.dataSize)
                            value = int(s/array[1])
                            value = value.to_bytes(2, 'big')
                        tempo['buffer'].append(value, time)
                        tempo['times'] += next

    def time2write(self, time, index):
        # is it time to write the data in the flash
        return self.array[index][self.whenSave]['times'] <= time

    def wait(self):
        # the time to wait before retrieve the reply
        return self.waiting

    def getIndex(self, time, index):
        # get all data to a index
        result = []
        for i in self.array:
            tempo = i[time]['buffer']
            result.append(tempo.getIndex(index))
        return result

    def getTimeBuffer(self, time):
        # current time of the index 0  of the buffer
        tempo = self.array[0][time]['buffer']
        diffBoucle = saveSensor.ticks_boucle - tempo.ticks_boucle
        return tempo.time + saveSensor.time_ns - saveSensor.ticks_max * diffBoucle

    def sum(self, byteArray, nmbByte):
        # sum the data sensor in a bytearray
        s = 0
        for i in range(0, len(byteArray), nmbByte):
            y = i+nmbByte
            sub = byteArray[i:y]
            if nmbByte > 1:
                s += int.from_bytes(sub, 'big')
            else :
                s += int.from_bytes(sub, 'big')
        return s

    def tampon2log(self):
        # when we finish with tge tampon,
        # we have to transfert all data from the tampon
        # to the log and do the mean for the different time
        for i in self.tamponArray:
            i.setTime(-1)
        lenArray = 30

        for index in range(lenArray):
            for iIndex in range(self.numberChannel):
                valueBrut, time = self.tamponArray[iIndex].getIndex(index)
                for i in self.array[iIndex]:
                    tempo = self.array[i]
                    before = tempo['before']
                    next = tempo['next']
                    if (tempo['times'] + tempo['offset']) <= time:
                        if before == None :
                            value = valueBrut
                        else:
                            bufferBefore = self.array[iIndex][before]['buffer']
                            lastTime = tempo['times'] - next
                            array = bufferBefore.getPartial(lastTime)
                            s = sum(array[0], bufferBefore.dataSize)
                            value = int(s/array[1])
                            value = value.to_bytes(2, 'big')
                        tempo['buffer'].append(value, time)
                        tempo['times'] += next
        self.tamponArray.clear()

