<style>
    colorR{
        color: red;
    }
    colorB{
        color: blue;
    }
    colorG{
        color: green;
    }
    colorO{
        color: orange;
    }
</style>

# Update firmware
With the make file : `make`, from [module_blinx](https://github.com/MaelC001/module_blinx/)

Or the docker function :

```shell
docker pull blinxcb/docker-micropython-esp8266:latest\
    && docker run -it -d --name docker-micropython-esp8266 blinxcb/docker-micropython-esp8266:latest bash \
	&& docker exec -it docker-micropython-esp8266 bash /create_bin.sh \
    && docker cp "docker-micropython-esp8266:micropython/ports/esp8266/build-GENERIC/firmware-combined.bin" ./esp8266_micropython_build.bin
```

Then use [`esptool`](https://github.com/espressif/esptool/) or [`mu editor`](https://codewith.mu/), for example, to flash the micro-controller.

For `esptool`, the command to use are (`PORT` is the port of the micro-controller, in windows it will be : `COM`+number (`COM8`) and in linux (ubuntu) it will normally be : `/dev/ttyUSB`+number (`/dev/ttyUSB0`)) :

```shell
esptool --port PORT erase_flash
esptool --port PORT -baud 460800 write_flash --flash_size=detect -fm dout 0 esp8266_micropython_build.bin
```

## <colorR>Attention :</colorR>
the `make` use the docker, and the docker use the repo [micropython](https://github.com/MaelC001/micropython) to do the firmware.
So if you want to do a custom firmware, you will have to create a new docker :

- clone the repo of [docker micropython](https://github.com/MaelC001/docker-micropython/) : `git clone https://github.com/MaelC001/docker-micropython/.git`
- in the file `Dockerfile` change the repo (l.58 : `RUN git clone https://github.com/MaelC001/micropython.git`) by our repo of micropython

# Compile python file to `.mpy`:
Download repo micropython : `git clone https://github.com/MaelC001/micropython.git` (or our repo of micropython)

Now go to the `mpy-cross` folder in micropython : `cd micropython/mpy-cross`

Then, do : `make`

You have now a binary file : `mpy-cross`

Use : `./mpy-cross pythonFile.py` to get the `pythonFile.mpy` file

# Modules :
The different modules :

- the repl/rpc module :
    - file `repl.py` have all the function you can call with the rpc, do the receiver/sender for the message and the async loop between the rpc and the 'get data from sensor' loop
    - file `sensors.py` read all the file for the sensors
    - file `blinxSensor.py` have the class for blinx, witch have sensor (a class). Each sensor have different channel/pin (a class). And each channel stock the data of him, at different time (in a circular buffer, a class)
- the repl/rpc by wifi + web server :
    - a modify the webrepl of micropython, so he can get `HTML` requests and not only `WS`
    - By default, the rpc and the web server is activated, and the webrepl of micropython is deactivated. But you can diactivate rpc/web server and/or activate the webrepl of micropython
    - for the path :
        - the `/` (by `GET` request):
            - if connected to wifi, it will be codeboot page
            - else it will be the wifi manager
        - the `/codeboot` (by `GET` request) will be the codeboot page
        - the `/wifi_manager` (by `GET` request) will be the wifi manager
        - the `/blinx` (by `POST` request) will be the rpc
    - the wifi manager is from [tayfunulu/WiFiManager](https://github.com/tayfunulu/WiFiManager)
- ota updater :
    - from [rdehuyss/micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater)
    - for update firmware of micropython, using a release form github


How to put the modules in a firmware of micropython :

1. put the file after the flash of the micro-controller, you can use `Mu editor` or by command python or by the webRepl of micropython.
2. put the file before create the firmware (they will be in th firmware):
    1. go in the folder : `extmod/webrepl` in micropython
    2. if you want to use my repl/rpc with the web server, you have to remove all the file in the folder
    3. put the all the python file (the `.py` and not the compile file (`.mpy`)) in the folder
    (I have not verify, yet, if it work with the compile file)
    1. then create a file with the name : `manifest.py`, with content : `freeze(".", ("name1", "name2", ...))` replacing `name1, name2, ...` with the name of the files you put in the folder (with the extension : `.py`)
    for example : `freeze(".", ("toto.py", "bob.py", "a.py"))`


# method in codeboot :
There is 2 method in codeboot :

- <colorB>`readFile`</colorB>
- <colorG>`writeFile`</colorG>

How to use it :

1. know the method to speak to the micro-controller :
    1. by usb : `usb`
    2. by wifi :
        1. with the hostname of the micro-controller (for the mdns) : `hostname.local` (example : `blinx.local`)
        2. with the ip of the micro-controller : `ip` (example : `0.0.0.0`)
2. the name of the sensor you want to speak (if it is the <colorB>`readFile`</colorB> function you can speak to multiple sensors)
3. if it is the <colorB>`readFile`</colorB> function :
    1. know what time you want to have :
        1. `1s` for the 1 second
        2. `10s` for the 10 seconds
        3. `1m` for the 1 minute
        4. `10m` for the 10 minutes
        5. `1h` for the 1 hour
4. if it is the <colorG>`writeFile`</colorG> function :
    1. know the type of the sensor you want to speak:
        1. a output sensor : `sensors_output`
        2. a display sensor : `display`
    2. know what you want to send to the sensor


The syntax :

1. for the <colorB>`readFile`</colorB> function : `readFile('blinx://method_to_speak/name1/name2/.../time')`
2. for the <colorG>`writeFile`</colorG> function : `readFile('blinx://method_to_speak/type_sensor/name', 'data1,data2,data3,data4,...')`

Example :

```python
readFile('blinx://usb/toto/bob/1s')
readFile('blinx://usb/toto/10s')
readFile('blinx://192.168.0.100/toto/10s')
readFile('blinx://blinx.local/toto/bob/10m')

writeFile('blinx://usb/sensors_output/toto', '0')
writeFile('blinx://192.168.0.101/sensors_output/bob', '0,2,7,14,5')
writeFile('blinx://blinx.local/display/toto', 'text,Hello Word,1,1,0')
writeFile('blinx://blinx.local/display/toto', 'show')
```

# config page in codeboot :

Action you can do in the config page :

- see the wifi information of the micro-controller :
    - if connected
    - ip
    - hostname
    - ssid
- config the wifi : give the ssid and password of the wifi
- config the sensor of the micro-controller

When the config page is open, it will see if the page is connected to a micro-controller by usb. If it is not the case, it will try to connect. If success, it will ask the wifi info to the micro-controller



# code of blinx:
## sensors.py :
  - read the file for the sensors, this file will be add at the configuration of the blinx (to avoid storing everything and using space for nothing)
  - get the information et store it
  - the info the code is loking for is (for each type of sensors) :
    - i2c :
      - address I2C
      - the byte to send, when want to get the data
      - the time to wait
      - the number of byte we will receive
      - the function :
        - verify the byte receive
        - transformed the bytes so that it is understandable
        - the immediate function : to get the data from this instant (not to save in the log)
    - analog :
      - the frequence to send data
      - the function :
        - verify the byte receive
        - transformed the bytes so that it is understandable
        - the immediate function : to get the data from this instant (not to save in the log)
    - digital :
      - the function :
        - verify the byte receive
        - transformed the bytes so that it is understandable
        - the immediate function : to get the data from this instant (not to save in the log)
    - function :
      - this type of sensors is the sensors who micropython already have a function for this
## otaUpdater :
  - to update the firmware of blinx, using github release
## repl.py :
  - for send data we use the `sys.stdout` and for receive it we use the `sys.stdin` (we can use `UART` and `os.dupterm`, from micropython (work in esp8266, but not in esp32))
  - for the communication we use `json_rpc` :
    - sender parameter :
      - `id` : the id of the command
      - `method` : the command to execute
      - `params` : the arguments of the command
    - send respond paramter :
      - `id` : the id of the command
      - `result`or `error`
  - first create all variable (I2C, the blinx (where are all the sensors), wifi, ...)
  - function
    - register :
      - to create a register of all the function the user, from codeboot, can use
      - and catch the error, to send it
      - the register take 2 args (and the function) :
        - the name of the function (the name to write to use this command)
        - a bool : to know if this function use other function for the user (to get the message result/error of this function)
    - sender :
      - send data with serial port (we can't send anything, after this, related to the user command)
    - senderDonneeSensor :
      - sent a part of the data (for not store it in blinx)
    - receiver :
      - get data form the serial port (line by line : one line is one command (json))
    - decode_input :
      - try to transform the byte receive into string, then into json
    - read_input :
      - try to get the info from the json
      - verify the type of the info
      - then try to execute the command
      - then send the result / error
    - save_sensor_while_request :
      - to save the data of the sensors (in a buffer), while send the data of the sensors to the user
    - verification_list_sensor :
      - verify the list of sensors the user want to use :
        - verify if the sensors exists and get the info of the sensors
    - verification :
      - verify the type of the variable
      - verify if the variable have a correct value
    - save_all_sensor :
      - while the repl/rpc is running, save the data of the sensors
    - launch :
      - launch the repl/rpc and the get the data of the sensors
    - ota_update :
      - update firmware
  - function for the user :
    - write_file :
      - for write a file in blinx:
        - `name` : the name of the file
        - `text` : the text to write
        - `format` : the format to write (`a` : append at the end, `w` : overwrite the data)
    - read_file :
      - for read a file in blinx :
        - `name` : the name of the file
    - create_file :
      - create a file in blinx (a empty file) :
        - `name` : the name of the file
    - remove_file :
      - remove a file in blinx :
        - `name` : the name of the file
    - list_file :
      - get the list of file in blinx
    - wifi :
      - get all the wifi information
    - wifi_active :
      - activate or disactivate the wifi
    - wifi_connect :
      - connect to the wifi using :
        - the `ssid`
        - the `password`
    - wifi_server :
      - create a wifi server (access point) :
        - the `ssid` of the access point
        - the `password` of the access point
        - the type of authentication (`auth`) of the access point
        - `activate` or desactivate the access point
    - sensor_stop :
      - stop to get the data of the sensors
      - and remove all the config
    - config_sensor :
      - config the sensors to get the data
    - remove_all_function_sensor :
      - remove all the file of the sensors (where we get all the info)
    - output_sensors :
      - modify the output sensors :
        - `sensor_name` : the name of the sensors
        - `array_value` : the value for each channel (pin) of the sensors
    - display_sensors :
      - modify the display of the sensors :
        - `sensor_name` : the name of the sensors
        - `func_name` : the function to use for modify the display (for exemple : text, fill, line, show ...)
        - `array_value` : the args of the function to use
    - get_sensors :
      - get the data form the sensors, in the format `csv` :
        - `list_sensors` : the list of sensors we want to get the data
        - `times` : which time we want (`0s` for immediate, `1s` for the data for each second, ...)
      - send the data part by part, for not stocking a large json in blinx
      - create a crc, of each line of the csv (without the name of the data)
    - scan_i2c :
      - scan all the I2C sensors connecting to the blinx
      - and can verify if a certain sensor is connected
## blinxSensor.py :
- Blinx :
- Sensor :
- Channel :
  - DigitalChannel :
  - AnalogChannel :
  - I2CChannel :
  - functionChannel :
- Buffer :
  - CircularBuffer :
- sensors_create_dict :
- next_time :
- diff_ticks :
- reset_ticks :
## html_template.py :
- template of html, for website (for the wifiManager)
## (webrepl.py) :
- same of micropython, but can also setup website and repl/rpc of blinx
## webrepl_setup.py :
- same of micropython
## websocket_helper.py :
- same of micropython, but don't get only `ws`, also `http`
  - `ws` :
    - for the webrepl of micropython
  - `http` :
    - website
    - repl/rpc of blinx
    - the wifiManager
## manifest.py :
- tell to micropython with file to add (like a library) in micropython
## wifiManager :
- the connect to wifi, using a web interface

# code of codeboot, config blinx page :