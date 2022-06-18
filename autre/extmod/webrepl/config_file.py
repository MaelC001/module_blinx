import json, ubinascii, network, os

fileConfig = "config.json"
mac = ubinascii.hexlify(network.WLAN().config('mac'),'-').decode()
id = ubinascii.hexlify(network.WLAN().config('mac')[-3:]).decode()

def creation():
    if fileConfig not in os.listdir():
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
                'ip':[]
            }
        }

        configurationWrite(dictionary)

def file():
    return fileConfig
def infoWifi():
    json = configurationRead()
    return json['info']['name_wifi'], json['info']['password_wifi'], json['info']['authmode_wifi'], json['info']['id'], json['info']['port_cb']
def infoWebrepl():
    json = configurationRead()
    return json['info']['password_webrepl'], json['info']['port_webrepl']

def setIp(ip):
    json = configurationRead()
    json['info']['ip'] = ip
def getIp():
    json = configurationRead()
    ip = json['info']['ip']
    return ip

def configurationWrite(dictionary):
    with open(fileConfig, 'w') as outfile:
        json.dump(dictionary, outfile)

def configurationRead():
    with open(fileConfig, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

creation()
