import time, os

# https://raw.githubusercontent.com/MaelC001/sensor_blinx/main/
# 
# def function(value, error):
#    return

import repl


try:
    os.remove('a.txt')
except Exception:
    pass
array_file = os.listdir()
__register = repl.__register

# test function verification
assert repl.verification('a', str)
assert repl.verification('a', int) == TypeError
assert repl.verification(0, str) == TypeError
assert repl.verification(0, int)
assert repl.verification('a', str, ['a'])
assert repl.verification('a', str, ['b']) == TypeError
assert repl.verification(0, int, [0])
assert repl.verification(0, int, [1]) == TypeError
assert repl.verification('a', str, ['b'], False)
assert repl.verification('a', str, ['a'], False) == TypeError
assert repl.verification(0, int, [1], False)
assert repl.verification(0, int, [0], False) == TypeError

# test the register
@repl.__register('test1', False)
def test1(a):
    return a
@repl.__register('test2', False)
def test2(a):
    raise TypeError(a)

@repl.__register('test3', True)
def test3(a):
    return test1(a)
@repl.__register('test4', True)
def test4(a):
    return test2(a)

assert 'test1' in repl.__register
assert 'test2' in repl.__register
assert 'test3' in repl.__register
assert 'test4' in repl.__register
assert repl.__register['test1']('a', id = 0) == {"result":'a', 'id': 0}
assert repl.__register['test2']('a', id = 0) == {"error":{"code": -32000, "message": 'error'}, 'id': 0}
assert repl.__register['test3']('a', id = 0) == {"result":'a', 'id': 0}
assert repl.__register['test4']('a', id = 0) == {"error":{"code": -32000, "message": 'error'}, 'id': 0}

repl.__register = __register


# test read_input function
assert repl.read_input({'method':'liste', 'params':{}, 'id' : 1}, how_send = 'return') == {'result': array_file, 'id': 1}
assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'create', 'id' : None}, how_send = 'return') == {'result': '', 'id': None}
assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'create', 'id' : 0}, how_send = 'return') == {'id': 0, 'error': {'code': -32000, 'message': 'a.txt don\'t have a correct value'}}
assert repl.read_input({'method':'liste', 'params':{}, 'id' : 0}, how_send = 'return') == {'result': ['a.txt'] + array_file, 'id': 0}
assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'read', 'id' : 1}, how_send = 'return') == {'result': '', 'id': 1}

assert repl.read_input({'params': {'name': 'a.txt', 'text': 'bonjour'}, 'method': 'write', 'id' : 1}, how_send = 'return') == {'result': '', 'id': 1}
assert repl.read_input({'method':'liste', 'params':{}, 'id' : 1}, how_send = 'return') == {'result': ['a.txt'] + array_file, 'id': 1}
assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'read', 'id' : 1}, how_send = 'return') == {'result': 'bonjour', 'id': 1}

assert repl.read_input({'params': {'name': 'a.txt', 'text': ' m', 'format': 'a'}, 'method': 'write', 'id' : 1}, how_send = 'return') == {'result': '', 'id': 1}
assert repl.read_input({'method':'liste', 'params':{}, 'id' : 1}, how_send = 'return') == {'result': ['a.txt'] + array_file, 'id': 1}
assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'read', 'id' : 1}, how_send = 'return') == {'result': 'bonjour m', 'id': 1}

assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'remove', 'id' : 1}, how_send = 'return') == {'result': '', 'id': 1}
assert repl.read_input({'params': {'name': 'a.txt'}, 'method': 'remove', 'id' : 1}, how_send = 'return') == {'id': 1, 'error': {'code': -32000, 'message': 'a.txt don\'t have a correct value'}}
assert repl.read_input({'params': {'name': 10}, 'method': 'read', 'id' : 1}, how_send = 'return') == {'id': 1, 'error': {'code': -32000, 'message': 'the type of 10 isn\'t < class \'str\' > '}}
assert repl.read_input({'method':'liste', 'params':{}, 'id' : 1}, how_send = 'return') == {'result': array_file, 'id': 1}

assert repl.read_input({'params': {'value': 0}, 'method': 'led', 'id' : 1}, how_send = 'return') == {'result': '', 'id': 1}
assert repl.read_input({'params': {'value': 1}, 'method': 'led', 'id' : 1}, how_send = 'return') == {'result': '', 'id': 1}
assert repl.read_input({'params': {'value': 2}, 'method': 'led', 'id' : 1}, how_send = 'return') == {'id': 1, 'error': {'code': -32000, 'message': '2 don\'t have a correct value'}}


# test function rpc :
assert repl.list_file() == array_file
assert repl.create_file(name = 'a.txt') == ''
assert repl.create_file(name = 'a.txt') == Exception
assert repl.list_file() == ['a.txt'] + array_file
assert repl.read_file(name = 'a.txt') == ''
assert repl.write_file(name = 'a.txt', text = 'bonjour') == ''
assert repl.read_file(name = 'a.txt') == 'bonjour'
assert repl.write_file(name = 'a.txt', text = ' m', format = 'a') == ''
assert repl.read_file(name = 'a.txt') == 'bonjour m'
assert repl.write_file(name = 'a.txt', text = ' m', format = 'w') == ''
assert repl.remove_file(name = 'a.txt') == ''
assert repl.remove_file(name = 'a.txt') == Exception
assert repl.write_file(name = 'a.txt', text = 'bonjour') == Exception
assert repl.read_file(name = 'a.txt') == Exception
assert repl.list_file() == array_file


# test read_input function
assert repl.read_input({'method':'liste', 'params':{}, 'id' : 1}, how_send = 'return') == {'result': array_file, 'id': 1}
assert repl.read_input({'method':'liste', 'params':[], 'id' : '1'}, how_send = 'return') == {'result': array_file, 'id': '1'}
assert repl.read_input({'method':'liste', 'params':{}, 'id' : None}, how_send = 'return') == {'result': array_file, 'id': None}

assert repl.read_input({'method':'liste', 'params':{}}, how_send = 'return') == {'result': {"code": -32600, "message": "Invalid Request"}, 'id': None}
assert repl.read_input({'method':'liste', 'params':{}, 'id' : [1]}, how_send = 'return') == {'result': {"code": -32600, "message": "Invalid Request"}, 'id': None}
assert repl.read_input({'method':0, 'params':{}, 'id' : 1}, how_send = 'return') == {'result': {"code": -32600, "message": "Invalid Request"}, 'id': None}

assert repl.read_input({'method':'aaasssafddsgdf', 'params':{}, 'id' : 1}, how_send = 'return') == {'result': {"code": -32601, "message": "Method not found"}, 'id': None}
assert repl.read_input({'method':'liste', 'params':'sdfds', 'id' : 1}, how_send = 'return') == {'result': {"code": -32602, "message": "Invalid params"}, 'id': None}
assert repl.read_input({'method':'liste', 'params':12.34, 'id' : 1}, how_send = 'return') == {'result': {"code": -32602, "message": "Invalid params"}, 'id': None}

# test decode_input function
assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 1}\n", how_send = 'return') == {'result': array_file, 'id': 1}
assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' 1}\n", how_send = 'return') == {'error': {"code": -32700, "message": "Parse error"}, 'id': 1}






# TODO
# register
# verification

# decode_input
# read_input

# write_file
# read_file
# create_file
# remove_file
# list_file

    # wifi
    # wifi_active
    # wifi_connect
    # wifi_server

    # remove_all_function_sensor
    # sensor_stop
    # config_sensor
    # get_sensors
    # display_sensors
    # output_sensors
    # scan_i2c
    # save_sensor_while_request
    # verification_list_sensor

    # ota_update