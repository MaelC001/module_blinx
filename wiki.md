# Update firmware
With the make file : `make`, from https://github.com/MaelC001/module_blinx/

Or the docker function :
```
docker pull blinxcb/docker-micropython-esp8266:latest\
    && docker run -it -d --name docker-micropython-esp8266 blinxcb/docker-micropython-esp8266:latest bash \
	&& docker exec -it docker-micropython-esp8266 bash /create_bin.sh \
    && docker cp "docker-micropython-esp8266:micropython/ports/esp8266/build-GENERIC/firmware-combined.bin" ./esp8266_micropython_build.bin
```

# Compile python file to `.mpy`:
Download repo micropython : `git clone https://github.com/MaelC001/micropython.git`

Now go to the `mpy-cross` folder in micropython : `cd micropython/mpy-cross`

Then, do : `make`

You have now a binary file : `mpy-cross`

To use it : `./mpy-cross pythonFile.py`

# Modules


# Fonctionnement


