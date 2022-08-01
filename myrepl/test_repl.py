import time, os

# https://raw.githubusercontent.com/MaelC001/sensor_blinx/main/
# 
# def function(value, error):
#    return

import repl






repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'remove', 'id' : 1}\n")
array_file = os.listdir()

assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 1}\n") == {'result': array_file, 'id': 1}

assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'create', 'id' : None}\n") == {'result': '', 'id': None}
assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'create', 'id' : 0}\n") == {'id': 0, 'error': {'code': -32000, 'message': 'a.txt don\'t have a correct value'}}
assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 0}\n") == {'result': ['a.txt'] + array_file, 'id': 0}
assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'read', 'id' : 1}\n") == {'result': '', 'id': 1}

assert repl.decode_input(b"{'params': {'name': 'a.txt', 'text': 'bonjour'}, 'method': 'write', 'id' : 1}\n") == {'result': '', 'id': 1}
assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 1}\n") == {'result': ['a.txt'] + array_file, 'id': 1}
assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'read', 'id' : 1}\n") == {'result': 'bonjour', 'id': 1}

assert repl.decode_input(b"{'params': {'name': 'a.txt', 'text': ' m', 'format': 'a'}, 'method': 'write', 'id' : 1}\n") == {'result': '', 'id': 1}
assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 1}\n") == {'result': ['a.txt'] + array_file, 'id': 1}
assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'read', 'id' : 1}\n") == {'result': 'bonjour m', 'id': 1}

assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'remove', 'id' : 1}\n") == {'result': '', 'id': 1}
assert repl.decode_input(b"{'params': {'name': 'a.txt'}, 'method': 'remove', 'id' : 1}\n") == {'id': 1, 'error': {'code': -32000, 'message': 'a.txt don\'t have a correct value'}}
assert repl.decode_input(b"{'params': {'name': 10}, 'method': 'read', 'id' : 1}\n") == {'id': 1, 'error': {'code': -32000, 'message': 'the type of 10 isn\'t < class \'str\' > '}}
assert repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 1}\n") == {'result': array_file, 'id': 1}

assert repl.decode_input(b"{'params': {'value': 0}, 'method': 'led', 'id' : 1}\n") == {'result': '', 'id': 1}
assert repl.decode_input(b"{'params': {'value': 1}, 'method': 'led', 'id' : 1}\n") == {'result': '', 'id': 1}
assert repl.decode_input(b"{'params': {'value': 2}, 'method': 'led', 'id' : 1}\n") == {'id': 1, 'error': {'code': -32000, 'message': '2 don\'t have a correct value'}}






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