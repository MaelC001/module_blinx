try:
    import ubinascii as binascii
except :
    import binascii

import json, network, os

fileConfig = "config.json"

def creation():
    if fileConfig not in os.listdir():
        mac = binascii.hexlify(network.WLAN().config('mac'),'-').decode()
        id = binascii.hexlify(network.WLAN().config('mac')[-3:]).decode()

        dictionary = {
            'wifi':{},
            "librairie": {
                "nom": [
                    "lien",
                    "info",
                ]
            },
            'info':{
                'mac':mac,
                'id':id,
                'password_webrepl':'blinx',
                'port_webrepl':8266,
                'name_wifi':'blinx_'+id,
                'password_wifi':'micropythoN',
                'authmode_wifi':3, #WPA2
                'port_cb':80,
                'ip':[],
                "mdns":""
            },
            "codeboot_html": """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>codeBoot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="apple-mobile-web-app-capable" content="yes">

        <!-- Uncomment to test with 'make min' -->
        <!-- <script src="codeboot.min.js"></script> -->
        <link rel="stylesheet" href="https://blinx.codeboot.org/3.1.12/codeboot.bundle.css">
        <script src="https://blinx.codeboot.org/3.1.12/codeboot.bundle.js"></script>
    </head>
    <body>
        <div id="main"></div>
        <div class="cb-vm" data-cb-lang="py-novice"></div>
    </body>
</html>
"""
        }

        configurationWrite(dictionary)

def file():
    return fileConfig
def infoWifi():
    return jsonRead['info']['name_wifi'], jsonRead['info']['password_wifi'], jsonRead['info']['authmode_wifi'], jsonRead['info']['id'], jsonRead['info']['port_cb']
def infoWebrepl():
    return jsonRead['info']['password_webrepl'], jsonRead['info']['port_webrepl']

def setIp(ip):
    jsonRead['info']['ip'] = ip
    configurationWrite(jsonRead)
def getIp():
    return jsonRead['info']['ip']

def configurationWrite(dictionary):
    with open(fileConfig, 'w') as outfile:
        json.dump(dictionary, outfile)

def configurationRead():
    with open(fileConfig, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

creation()
jsonRead = configurationRead()