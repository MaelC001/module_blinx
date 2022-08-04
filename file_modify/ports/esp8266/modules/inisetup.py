from textwrap import indent
import uos
import network
from flashbdev import bdev
import json

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
    print("wifi:")
    wifi()
    print('other:')
    uos.VfsLfs2.mkfs(bdev)
    vfs = uos.VfsLfs2(bdev)
    uos.mount(vfs, "/")
    print("config file:")
    config_file_blinx
    print('boot file:')
    with open("boot.py", "w") as f:
        f.write("""\
#import esp
#esp.osdebug(None)
from machine import Pin,I2C
import gc, ssd1306, webrepl #, repl
gc.collect()
#webrepl.change_rpc(repl.read_input)
#webrepl.start()
p2 = Pin(2, Pin.OUT)
p2.value(0)
i2c=I2C(sda=Pin(4),scl=Pin(5))
display=ssd1306.SSD1306_I2C(128,32,i2c)
display.text('MicroPython',0,0,1)
display.show()
#repl.launch()
""")
    return vfs



def config_file_blinx():
    f = open("config_file.json", "w")
    j = {'id':'a'}
    f.write(json.loads(j, indent = 4))