import time
import blinxSensor
# https://raw.githubusercontent.com/MaelC001/sensor_blinx/main/
# 
# def function(value, error):
#    return




def function(arg, error):
    return arg

def next_time(arrayTime):
    arrayNextTime = []
    present = time.time()
    for i in arrayTime:
        tempoTime = present + (i - (present % i))
        arrayNextTime.append(tempoTime)

    return arrayNextTime

a = blinxSensor.BufferCircular('Aaaa', 5)
bytearrayTempo = bytearray()
for _ in range(10):
    bytearrayTempo += bytearray(b'\xff\xff')
assert a._data == bytearrayTempo
assert a._data == a.getAll()
a.append(bytearray(b'\x00\x00'), 0)
assert (a._data, a.realIndex, a.dataIndex, a.time) == (bytearray(b'\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'), 2, 1, 0)
assert a._data == a.getAll()
a.append(bytearray(b'\x00\x01'), 1)
assert (a.getAll(), a.realIndex, a.dataIndex, a.time) == (bytearray(b'\x00\x00\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'), 4, 2, 0)
a.append(bytearray(b'\x00\x03'), 3)
assert (a.getAll(), a.realIndex, a.dataIndex, a.time) == (bytearray(b'\x00\x00\x00\x01\xff\xff\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'), 8, 4, 0)
assert a.lastTime() == 3
assert a.missing(4) == False
assert a.missing(5) == True
a.fix_missing_data(5)
assert a.getAll() == bytearray(b'\x00\x00\x00\x01\xff\xff\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
assert a.getListModify(a._data) == (bytearray(b'\x00\x00\x00\x01\x00\x03'), 3)
assert a.getPartial(-2) == (bytearray(b'\x00\x03\x00\x01\x00\x00'), 3)
assert a.getPartial(0) == (bytearray(b'\x00\x03\x00\x01\x00\x00'), 3)
assert a.getPartial(1) == (bytearray(b'\x00\x03\x00\x01'), 2)
assert a.getPartial(2) == (bytearray(b'\x00\x03'), 1)
assert a.getPartial(3) == (bytearray(b'\x00\x03'), 1)
assert a.getIndex(0) == (bytearray(b'\xff\xff'), 4)
assert a.getIndex(1) == (bytearray(b'\x00\x03'), 3)
assert a.getIndex(2) == (bytearray(b'\xff\xff'), 2)
assert a.getIndex(3) == (bytearray(b'\x00\x01'), 1)
assert a.getIndex(4) == (bytearray(b'\x00\x00'), 0)


array = next_time([1, 10, 60, 600, 3600])
t = array[0]
dic = {'1s': {'size': 300, 'times': array[0], 'value': 1, 'offset': 0, 'before': None}, '10s': {'size': 300, 'times': array[1], 'value': 10, 'offset': 0, 'before': '1s'}, '1m': {'size': 300, 'times': array[2], 'value': 60, 'offset': 1, 'before': '10s'}, '10m': {'size': 300, 'times': array[3], 'value': 600, 'offset': 2, 'before': '1m'}, '1h': {'size': 300, 'times': array[4], 'value': 3600, 'offset': 3, 'before': '10m'}}
a = blinxSensor.Sensor('aaaa', dic, '10s', 10)
assert a.time2write(0) == False
assert a.time2write(16551389670) == True
assert a.wait() == 10
assert a.sum(bytearray([10, 11, 12, 20]), 1) == 53
assert a.sum(bytearray([10, 11, 12, 20]), 2) == 5663
a.save(t+1, function, bytearray(b'\x00\x00'))
a.save(t+2, function, bytearray(b'\x00\x01'))
a.save(t+4, function, bytearray(b'\x00\x03'))
assert a.getIndex('1s', 0) == (bytearray(b'\x00\x03'), t+4)
assert a.getIndex('1s', 1) == (bytearray(b'\xff\xff'), t+3)
assert a.getIndex('1s', 2) == (bytearray(b'\x00\x01'), t+2)
assert a.getIndex('1s', 3) == (bytearray(b'\x00\x00'), t+1)
assert a.getTimeBuffer('1s') == t
# assert a.tampon2log()


# a = blinxSensor.i2cSensor
# assert a.send()
# assert a.save(time)


# a = blinxSensor.AnalogSensor
# assert a.save(time)

