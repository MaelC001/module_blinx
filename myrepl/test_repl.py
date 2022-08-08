import time, os
import unittest
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

class TestStringMethods(unittest.TestCase):
    def test_verification(self):
        # test function verification
        self.assertTrue(repl.verification('a', str))
        self.assertTrue(repl.verification(0, int))
        with self.assertRaises(TypeError):
            repl.verification('a', int)
        with self.assertRaises(TypeError):
            repl.verification(0, str)

        self.assertTrue(repl.verification('a', str, ['a']))
        with self.assertRaises(TypeError):
            repl.verification('a', str, ['b'])

        self.assertTrue(repl.verification('a', str, ['b'], False))
        with self.assertRaises(TypeError):
            repl.verification('a', str, ['a'], False)

        self.assertTrue(repl.verification(0, int, [0]))
        with self.assertRaises(TypeError):
            repl.verification(0, int, [1])

        self.assertTrue(repl.verification(0, int, [1], False))
        with self.assertRaises(TypeError):
            repl.verification(0, int, [0], False)

    def test_register(self):
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

        self.assertTrue('test1' in repl.__register)
        self.assertTrue('test2' in repl.__register)
        self.assertTrue('test3' in repl.__register)
        self.assertTrue('test4' in repl.__register)

        self.assertDictEqual(repl.__register['test1']('a', id = 0), {"result":'a', 'id': 0})
        self.assertDictEqual(repl.__register['test2']('a', id = 0), {"error":{"code": -32000, "message": 'error'}, 'id': 0})
        self.assertDictEqual(repl.__register['test3']('a', id = 0), {"result":'a', 'id': 0})
        self.assertDictEqual(repl.__register['test4']('a', id = 0), {"error":{"code": -32000, "message": 'error'}, 'id': 0})

        repl.__register = __register

    def test_file_func(self):
        # test function rpc :
        self.assertListEqual(repl.list_file(), array_file)
        self.assertMultiLineEqual(repl.create_file(name = 'a.txt'), '')
        with self.assertRaises(FileExistsError):
            repl.create_file(name = 'a.txt')
        self.assertListEqual(repl.list_file(), ['a.txt'] + array_file)
        self.assertMultiLineEqual(repl.read_file(name = 'a.txt'), '')
        self.assertMultiLineEqual(repl.write_file(name = 'a.txt', text = 'bonjour'), '')
        self.assertMultiLineEqual(repl.read_file(name = 'a.txt'), 'bonjour')
        self.assertMultiLineEqual(repl.write_file(name = 'a.txt', text = ' m', format = 'a'), '')
        self.assertMultiLineEqual(repl.read_file(name = 'a.txt'), 'bonjour m')
        self.assertMultiLineEqual(repl.write_file(name = 'a.txt', text = ' m', format = 'w'), '')
        self.assertMultiLineEqual(repl.remove_file(name = 'a.txt'), '')
        with self.assertRaises(FileNotFoundError):
            repl.create_file(name = 'a.txt')
        with self.assertRaises(FileNotFoundError):
            repl.read_file(name = 'a.txt')
        self.assertListEqual(repl.list_file(), array_file)

    def test_ead_input(self):
        # test read_input function
        self.assertDictEqual(repl.read_input({'method':'liste', 'params':{}, 'id' : 1}, how_send = 'return'), {'result': array_file, 'id': 1})
        self.assertDictEqual(repl.read_input({'method':'liste', 'params':[], 'id' : '1'}, how_send = 'return'), {'result': array_file, 'id': '1'})
        self.assertDictEqual(repl.read_input({'method':'liste', 'params':{}, 'id' : None}, how_send = 'return'), {'result': array_file, 'id': None})

        self.assertDictEqual(repl.read_input({'method':'liste', 'params':{}}, how_send = 'return'), {'result': {"code": -32600, "message": "Invalid Request"}, 'id': None})
        self.assertDictEqual(repl.read_input({'method':'liste', 'params':{}, 'id' : [1]}, how_send = 'return'), {'result': {"code": -32600, "message": "Invalid Request"}, 'id': None})
        self.assertDictEqual(repl.read_input({'method':0, 'params':{}, 'id' : 1}, how_send = 'return'), {'result': {"code": -32600, "message": "Invalid Request"}, 'id': None})

        self.assertDictEqual(repl.read_input({'method':'aaasssafddsgdf', 'params':{}, 'id' : 1}, how_send = 'return'), {'result': {"code": -32601, "message": "Method not found"}, 'id': None})
        self.assertDictEqual(repl.read_input({'method':'liste', 'params':'sdfds', 'id' : 1}, how_send = 'return'), {'result': {"code": -32602, "message": "Invalid params"}, 'id': None})
        self.assertDictEqual(repl.read_input({'method':'liste', 'params':12.34, 'id' : 1}, how_send = 'return'), {'result': {"code": -32602, "message": "Invalid params"}, 'id': None})

    def test_file_func(self):
        # test decode_input function
        self.assertDictEqual(repl.decode_input(b"{'method':'liste', 'params':{}, 'id' : 1}\n", how_send = 'return'), {'result': array_file, 'id': 1})
        self.assertDictEqual(repl.decode_input(b"{'method':'liste', 'params':{}, 'id' 1}\n", how_send = 'return'), {'error': {"code": -32700, "message": "Parse error"}, 'id': 1})






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




if __name__ == '__main__':
    unittest.main(verbosity=2)