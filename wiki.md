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
the `make` use the docker, and the docker use the repo [micropython](https://github.com/MaelC001/micropython] to do the firmware.
So if you want to do a custom firmware, you will have to create a new docker :

- clone the repo of [docker micropython](https://github.com/MaelC001/docker-micropython/) : `git clone https://github.com/MaelC001/docker-micropython/.git`
- in the file `Dockerfile` change the repo (l.58 : `RUN git clone https://github.com/MaelC001/micropython.git`)

# Compile python file to `.mpy`:
Download repo micropython : `git clone https://github.com/MaelC001/micropython.git`

Now go to the `mpy-cross` folder in micropython : `cd micropython/mpy-cross`

Then, do : `make`

You have now a binary file : `mpy-cross`

To use it : `./mpy-cross pythonFile.py`

# Modules :
The different modules :

- the repl/rpc module :
- the repl/rpc by wifi + web server :
    - the wifi manager is from [tayfunulu/WiFiManager](https://github.com/tayfunulu/WiFiManager)
- otaUpdater (from [rdehuyss/micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater))


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

