from machine import Pin, ADC, PWM, I2C
from time import sleep_ms
import time

sensors = None

# do we do a conversion
buffer = False
# number of boucle
ticks_boucle = 0
time_ns = time.time_ns() - time.ticks_ms()
ticks_max = 2**30

# import blinxC
# a = blinxC.Blinx(configs = {'A' : {'new_name' : 'B', 'is_input' : False, 'is_display' : False, 'channels' : [{'type':'Digital', 'pin':2}]}}, i2c = None)
# b = a.sensors['B']['sensor']
# c = b.channels[0]
# d = c.dic['1s']['buffer']

class Blinx():
    def __init__(self, configs, i2c):
        # list of all the sensor
        #self.sensors = {}
        # list of all the input sensor
        self.input_sensors = {}
        # list of all the output sensor
        self.output_sensors = {}
        # list of all the output sensor
        self.display_sensors = {}
        for sensor, config in configs.items():
            # get info for the sensors
            new_name = config['new_name']
            is_input = config['is_input']
            is_display = config['is_display']
            min = config['min']
            max = config['max']

            if new_name == '':
                new_name = sensor

            # create the sensor
            if is_display:
                config = config['config']
                temp = {'name' : sensor, 'sensor' : sensors.__list_sensors[sensor]['create'](i2c, *config)}
            else:
                channels = config['channels']
                temp = {'name' : sensor, 'sensor' : Sensor(sensor, channels,  input = is_input, i2c = i2c, min = min, max = max)}

            #self.sensors[new_name] = temp

            # stock the sensor
            if is_input :
                self.input_sensors[new_name] = temp
            elif is_display :
                self.display_sensors[new_name] = temp
            else:
                self.output_sensors[new_name] = temp

    def save(self, time, input_sensor = True):
        # save the reply of all the sensor
        dic = self.input_sensors
        for i in dic.values():
            i['sensor'].save(time)

    def get_index(self, time, index, translate = True):
        # get the data from a index for all the sensor
        result = []
        for i in self.input_sensors.values():
            result.append(i['sensor'].get_index(time, index, translate = translate))
        return result

    def get_time_buffer(self, time):
        # current time of the buffer
        temp = next(iter(self.input_sensors.keys()))
        return self.input_sensors[temp]['sensor'].get_time_buffer(time)

    def buffer_to_log(self):
        # move the buffer to the log
        for i in self.input_sensors.values():
            i['sensor'].buffer_to_log(time)


# Sensors
class Sensor():
    def __init__(self, sensor_type, channels, input = True, error = b'\xff\xfe', i2c = None, min=-1, max=-1):
        # the type of sensor
        self.sensor_type = sensor_type
        # the error code
        self.error = error
        # number of byte for each data
        self.size = 2
        # it is a input or output sensor
        self.input = input
        # the i2c bus
        self.i2c = i2c
        # the list of the channel of each pin for the sensor
        self.channels = []
        # the waiting time
        self.waiting = 0
        # all the pin of the sensor
        self.pin_sensor = []
        # the min max value to calcul the %
        self.min = min
        self.max = max
        # create all the channel
        self._create_channels(channels)

    def _create_channels(self, channels):
        """create all the channel"""
        for channel in channels:
            if channel['type'] == "I2C":
                waiting_time = sensors.__list_sensors[self.sensor_type]['byte'+str(channel['id'])]['waiting']
                if self.waiting < waiting_time:
                    self.waiting = waiting_time
            t = Channel._configure(channel, self.sensor_type, self.i2c, self.input)
            self.channels.append(t[0])
            self.pin_sensor.append(t[1])

    def read(self):
        temp = []
        for i in self.channels:
            temp.append(i.read())
        return temp

    def write(self, array_value):
        for i in range(len(self.channels)):
            self.channels[i].write(array_value[i])

    def save(self, time):
        # save the reply of the sensor
        # if we are converting the data, we record the new data in a buffer (only each 1s)
        # when we finish the convert we will move the data from the buffer to the log
        if buffer: # buffer is a global variable difine in the begin of the code
            for i in self.channels:
                i.buffer_save(time)
        else:
            for i in self.channels:
                i.save(time)

    def get_index(self, time, index, translate = True):
        # get the data from a index of all channel
        result = []
        for i in self.channels:
            data = i.get_index(time, index, translate = translate)
            if translate and (min > 0 and max > min):
                t = data[0]
                t = int.from_bytes(t, 'big')
                if t <= min:
                    result = 0
                elif t >= max:
                    result = 100
                else :
                    temp = t - min
                    diff = max - min
                    result = int(temp/diff * 100)
                data[0] = result.to_bytes(i.data_size, 'big')
            result.append(data)
        return result

    def get_time_buffer(self, time):
        # current time of the buffer
        return self.channels[0].get_time_buffer(time)


    def buffer_to_log(self):
        # move the buffer to log
        for i in self.channels:
            i.buffer_to_log(time)


# Channels
class Channel():
    def __init__(self, name, error = b'\xff\xfe', translation_byte_function = lambda x, y, z : x, translation_data_function = lambda x:x, id = '', input = True, data_size = 2):

        # the data for the last reply
        self.old_data = 0
        # the function to translate the byte
        self.translation_byte_function = translation_byte_function
        # the function to translate the data
        self.translation_data_function = translation_data_function
        # the error code
        self.error = error
        # id of the channel
        self.id = id
        # data size
        self.data_size = data_size

        # is it a channel of a input sensor
        self.input = input

        if self.input:
            # the dic of information of the channel + their buffer (if a input sensor)
            self.dic = {}
            # the buffer for when we convert the data
            self.buffer = Buffer(30)
            for key, config in sensors_create_dict().items():
                size = config['size']
                times = config['times']
                step = config['value']

                temp = {}
                temp['buffer'] = CircularBuffer(name, size, step, times, error = error, data_size=self.data_size)
                temp['before'] = config['before']
                temp['offset'] = config['offset']
                temp['times'] = times
                temp['next'] = step

                if key == '1s':
                    self.size = size

                self.dic[key] = temp

    def _configure(channel, sensor_type, i2c, input):
        if channel['type'] == "I2C":
            id = channel['id']
            function_byte = sensors.__list_sensors[sensor_type]['byte'+str(id)]['func']
            waiting_time = sensors.__list_sensors[sensor_type]['byte'+str(id)]['waiting']
            function_data = sensors.__list_sensors[sensor_type]['data'+str(id)]['func']

            # the address of the sensor I2C
            addr = sensors.__list_sensors[sensor_type]['args']['addr']
            # the number of byte to receive form the sensor
            number_byte_receive = sensors.__list_sensors[sensor_type]['args']['byteReceive']
            # the code to send to the sensor to tell him we want the data
            code_to_send = sensors.__list_sensors[sensor_type]['args']['codeSend']
            return I2CChannel(i2c, addr, number_byte_receive, code_to_send, waiting_time, name = sensor_type, translation_byte_function = function_byte, translation_data_function = function_data, id = id, input = input), {}
        elif channel['type'] == "Analog":
            id = channel['id']
            function_byte = sensors.__list_sensors[sensor_type]['byte'+str(id)]['func']
            function_data = sensors.__list_sensors[sensor_type]['data'+str(id)]['func']

            pin = channel['pin']
            p1 = channel['p1']
            p2 = channel['p2']
            p3 = channel['p3']
            freq = sensors.__list_sensors[sensor_type]['args']['freq']
            temp = {
                'pin' : pin, 
                'p1' : p1, 
                'p2' : p2, 
                'p3' : p3, 
            }
            return AnalogChannel(pin, p1, p2, p3, name = sensor_type, translation_byte_function = function_byte, translation_data_function = function_data, freq = freq, id = id, input = input), temp
        elif channel['type'] == "Digital":
            id = channel['id']
            pin = channel['pin']
            return DigitalChannel(pin, name = sensor_type, id = id, input = input), {'pin' : pin}

    def read(self):
        raise NotImplementedError
    def write(self, value):
        raise NotImplementedError

    def save(self, time):
        """
            save the reply of the sensor
        """
        self.save_value_in_log(time, self.read())

    def buffer_save(self, time):
        """
            we are converting the data, we record the new data in a buffer (only each 1s)
            when we finish the convert we will move the data from the buffer to the log
        """
        if self.buffer.time == -1:
            self.buffer.set_time(time)
        value = self.read()
        self.buffer.append(value, time)

    def buffer_to_log(self):
        """
            when we finish with tge buffer, 
            we have to transfert all data from the buffer
            to the log and do the mean for the different time
        """
        self.buffer.set_time(-1)
        lenArray = 30

        for index in range(lenArray):
                value_brut, time = self.buffer.get_index(index)
                self.save_value_in_log(time, value_brut)
        self.buffer.clear()

    def save_value_in_log(self, time, value_brut):
        for i in self.dic:
            temp = self.dic[i]
            before = temp['before']
            next = temp['next']
            print(0,before, next, temp['times'], temp['offset'], value_brut, time, temp['times'] + temp['offset'])
            if (temp['times'] + temp['offset']) <= time:
                print(1)
                # is it a mean of the reply of before ?
                if before == None :
                    print(2)
                    value = value_brut
                else:
                    print(3)
                    buffer_before = self.dic[before]['buffer']
                    last_time = temp['times'] - next
                    array = buffer_before.get_partial(last_time)
                    print(4, array)
                    s = self.sum_bytes(array[0], buffer_before.data_size)
                    value = int(s/array[1])
                    value = value.to_bytes(buffer_before.data_size, 'big')
                temp['buffer'].append(value, time)
                temp['times'] = time + next

    def sum_bytes(self, byte_array, bytes_amount):
        """ sum the data sensor in a bytearray """
        s = 0
        for i in range(0, len(byte_array), bytes_amount):
            y = i+bytes_amount
            sub = byte_array[i:y]
            if bytes_amount > 1:
                s += int.from_bytes(sub, 'big')
            else :
                s += int.from_bytes(sub, 'big')
        return s

    def get_time_buffer(self, time):
        """ current time of the buffer """
        temp = self.dic[time]['buffer']
        diffBoucle = ticks_boucle - temp.ticks_boucle
        return temp.time + time_ns - ticks_max * diffBoucle

    def get_index(self, time, index, translate = True):
        """ get the data for a index """
        temp = self.dic[time]['buffer']
        data, time = temp.get_index(index)
        if translate:
            return self.translation_data_function(data), time
        return data, time


class DigitalChannel(Channel):
    def __init__(self, pin, name, error = b'\xff\xfe', translation_byte_function = lambda x, y, z : b'\x01' if x else b'\x00', translation_data_function = lambda x:x, id = '', input = True):
        # a digital sensor will give us a boolean (true or false) when we read it
        # It is the fact that there is power or not
        # but the buffer use the byte array, so we will transform the boolean to byte
        # b'\x01' for True and b'\x00' for False
        # it is the role of the translation_byte_function

        # the pin for the sensor
        self.pin = Pin(pin, Pin.OUT)

        super().__init__(name = name, error = error, translation_byte_function = translation_byte_function, translation_data_function = translation_data_function, id = id, input = input, data_size = 1)

    def read(self):
        return self.translation_byte_function(self.pin(), self.error, self.old_data)
    def write(self, value):
        self.pin.value(value)

class AnalogChannel(Channel):
    def __init__(self, pin, p1, p2, p3, name, error = b'\xff\xfe', translation_byte_function = lambda x, y, z : x, translation_data_function = lambda x:x, freq = 1000, id = '', input = True):
        # here we don't have a specific transformation to do to the sensor data, so we will return the data
        # but, some sensors may have some transformations to do

        # the pin for the output
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(pin)
        self.pwm.freq(freq)

        # the pin for the input
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        super().__init__(name = name, error = error, translation_byte_function = translation_byte_function, translation_data_function = translation_data_function, id = id, input = input)
    def read(self):
        Pin(0, mode = Pin.OUT).value(self.p1)
        Pin(2, mode = Pin.OUT).value(self.p2)
        Pin(15, mode = Pin.OUT).value(self.p3)
        return self.translation_byte_function(ADC(0).read(), self.error, self.old_data)
    def write(self, value):
        self.pwm.duty(value)

class I2CChannel(Channel):
    def __init__(self, i2c, addr, byte_receive, code_send, wait, name, error = b'\xff\xfe', translation_byte_function = lambda x, y, z : x, translation_data_function = lambda x:x, id = '', input = True):
        # here we don't have a specific transformation to do to the sensor data, so we will return the data
        # but, some sensors may have some transformations to do

        # the i2c bus
        self.i2c = i2c
        # the i2c addr for the sensor
        self.addr = addr
        # the byte to receive from the sensor
        self.byte_receive = byte_receive
        # the code to send to the sensor
        self.code_send = code_send
        # the time to wait
        self.wait = wait

        super().__init__(name = name, error = error, translation_byte_function = translation_byte_function, translation_data_function = translation_data_function, id = id, input = input)
    def read(self):
        self.write(self.code_send)
        sleep_ms(self.wait)
        return self.read_i2c()
    def write(self, value):
        self.i2c.writeto(self.addr, value)
    def read_i2c(self):
        return self.translation_byte_function(self.i2c.readfrom(self.addr, self.byte_receive), self.error, self.old_data)

# Buffers
class Buffer():
    def __init__(self, size, step = 1, time = 0, null = b'\xff\xff', data_size = 2):
        # the real index in the byte array
        self.real_index = 0
        # the index for the each data, it is not equal to the realIndex, 
        # if the data is stock in multiple byte
        self.data_index = 0
        # value index is the value of one index
        # if the index is 2, and step = 1, then we are at 2s
        # if the index is 2, and step = 10, then we are at 20s ...
        self.step = step
        # it is the number of byte to stock the data
        self.data_size = data_size
        # it is the number of data stock
        self.size = size
        # the code for error
        self.null = null
        # number of boucle of the ticks
        self.ticks_boucle = ticks_boucle
        # the byte array for data
        #self._data = null*(size*data_size)   # each measure is stored in 2 bytes
        self._data = bytearray()
        for _ in range(size*data_size) :
            self._data += null
        # the timestamp in index 0
        self.time = time

    def append(self, value, time):
        """
        verify if we don't miss data and if we have to reset the index
        then add the 2 bytes of information
        """
        self.fix_missing_data(time)
        self.reset_index(time)
        for i in range(self.data_size):
            self._data[self.real_index] = value[i]
            self.real_index += 1
        self.data_index += 1

    def reset_index(self, time):
        """reset the index"""
        if self.data_index == self.size:
            self.real_index = 0
            self.data_index = 0
            self.time = time
            self.ticks_boucle = ticks_boucle

    def get_index(self, index):
        """get the data of a index (in accordance with the present data (index 0)) to the present data"""
        diff_boucle = ticks_boucle - self.ticks_boucle
        time_ns = time_ns - ticks_max * diff_boucle
        diff = self.data_index - index - 1
        if self.data_index == 0:
            time_data = self.size * self.step
        elif self.data_index > index:
            time_data = self.time + diff
        elif self.data_index <= index:
            time_data = self.time - (diff - self.data_index)
        index_data = diff*self.data_size
        return self._data[index_data], time_data + time_ns #  : index_data+self.data_size

    def last_time(self):
        """last time we stock a data"""
        return self.time + (self.data_index-1) * self.step

    def missing(self, time):
        """do we have missing data"""
        return diff_ticks(self.last_time() + self.step, time) > 0

    def fix_missing_data(self, time):
        """correct the missing data : put the 'null' bytes in missing data"""
        if self.missing(time):
            self.append(self.null, time - 1)

    def set_time(self, time):
        """change the time"""
        self.time = time

    def clear(self):
        """clear of the data (for the buffer)"""
        self.real_index = 0
        self.data_index = 0
        self._data = bytearray()
        for _ in range(self.size*self.data_size) :
            self._data += self.null
        self.time = -1

class CircularBuffer(Buffer):
    def __init__(self, name, size, step = 1, time = 0, null = b'\xff\xff', error = b'\xff\xfe', data_size = 2):
        # the code for error
        self.error = error
        # the nam of the sensor
        self.name = name
        super().__init__(size, step = step, time = time, null = null, data_size = data_size)

    def get_partial(self, time_stamp):
        """get partial data, with the timeStamp"""
        i = round((time_stamp - self.time) / self.step)
        l = self.get_data(time_stamp >= self.time, i)
        return self.get_list_modify(l)

    def get_all(self):
        """get all the data"""
        return self._data

    def get_list_modify(self, l):
        """remove the error and the missing data of the list"""
        array = bytearray()
        s = 0
        for i in range(0, len(l), self.data_size):
            y = i+self.data_size
            sub = l[i:y]
            if sub != self.null and sub != self.error:
                s += 1
                array += sub
        return array, s

    def save(self, nmb):
        """save a number of the data"""
        i = self.data_index - nmb
        l = self.get_data(self.data_index >= nmb, i)

        text = self.array_to_str(l)
        return text

    def array_to_str(array, separator = '\n'):
        """change array to string"""
        return separator.join(array) + separator

    def get_data(self, before_index, i):
        """
        beforeIndex : is the information we want begin
        before or after the current index
        """
        if before_index :
            l = self._data[i*self.data_size:self.real_index*self.data_size]
            l = self.reverse_bytearray(l)
        else:
            l1 = self._data[:self.real_index*self.data_size]
            l1 = self.reverse_bytearray(l1)
            l2 = self._data[i*self.data_size:]
            l2 = self.reverse_bytearray(l2)
            l = l1 + l2
        return l

    def reverse_bytearray(self, array):
        """reverse the data of a sensor in a bytearray"""
        l = len(array)
        temp = bytearray()
        for i in range(l, 0, -self.data_size):
            y = i-self.data_size
            sub = array[y:i]
            temp += sub
        return temp




def sensors_create_dict():
    """
    create the dic of the info for the buffer
    """
    array_time_value = [1, 10, 60, 600, 3600]
    array_time_name = ['1s', '10s', '1m', '10m', '1h']
    array_time_size = [300, 180, 120, 144, 168] # 5min, 30min, 2h, 24h, 7j
    array_time_offset = [0, 0, 1, 2, 3]
    array_next_time = next_time(array_time_value)
    before = None

    temp_dict = {}

    for i in range(len(array_time_value)):
        name_time = array_time_name[i]
        temp_dict[name_time] = {
            'size' : array_time_size[i], 
            'times' : array_next_time[i], 
            'value' : array_time_value[i], 
            'offset' : array_time_offset[i], 
            'before' : before, 
        }
        before = name_time
    return temp_dict


def next_time(arrayTime):
    """
    calculate the next we have each time, for example :
    if it is 12s, the next time we have 10s it is 20s
    if it is 96s, the next time we have 60s it is 120s
    """
    array_next_time = []
    present = time.time()
    for i in arrayTime:
        temp_time = present + (i - (present % i))
        array_next_time.append(temp_time)

    return array_next_time

def diff_ticks(before, after):
    """calcul the difference between to ticks"""
    diff = time.ticks_diff(after, before)
    if after >= before:
        return diff
    else :
        reset_ticks()
        return diff

def reset_ticks():
    """reset ticks"""
    global ticks_boucle, time_ns
    ticks_boucle += 1
    time_ns = time.time_ns() - time.ticks_ms()