import uos
import network
from flashbdev import bdev


def wifi():
    import ubinascii

    ap_if = network.WLAN(network.AP_IF)
    essid = b"blinx-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=b"micropythoN")


def check_bootsec():
    buf = bytearray(bdev.SEC_SIZE)
    bdev.readblocks(0, buf)
    empty = True
    for b in buf:
        if b != 0xFF:
            empty = False
            break
    if empty:
        return True
    fs_corrupted()


def fs_corrupted():
    import time

    while 1:
        print(
            """\
The filesystem starting at sector %d with size %d sectors looks corrupt.
You may want to make a flash snapshot and try to recover it. Otherwise,
format it with uos.VfsLfs2.mkfs(bdev), or completely erase the flash and
reprogram MicroPython.
"""
            % (bdev.start_sec, bdev.blocks)
        )
        time.sleep(3)


def setup():
    check_bootsec()
    print("Performing initial setup")
    wifi()
    uos.VfsLfs2.mkfs(bdev)
    vfs = uos.VfsLfs2(bdev)
    uos.mount(vfs, "/")
    with open("boot.py", "w") as f:
        f.write(
            """\
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
gc.collect()
#import wifi_config, config_file
#wlan = wifi_config.get_connection()
#if wlan is None:
#    print("Could not initialize the network connection.")
#else :
#    config_file.setIp(wlan.ifconfig())
#password, ports = config_file.infoWebrepl()
#ap_ssid, ap_password, ap_authmode, id, port = config_file.infoWifi()
#import webrepl
#webrepl.start(port=port, password=password, ssid_wifi=ap_ssid, password_wifi=ap_password, authmode_wifi=ap_authmode, html=True, html_text=None)
#webrepl.start(port=ports, password=password)
from machine import Pin,I2C
import ssd1306
p2 = Pin(2, Pin.OUT)
p2.value(0)
i2c=I2C(sda=Pin(4),scl=Pin(5))
display=ssd1306.SSD1306_I2C(128,32,i2c)
display.text('MicroPython',0,0,1)
display.text('Connected',11,11,1)
display.show()
"""
        )
    return vfs
