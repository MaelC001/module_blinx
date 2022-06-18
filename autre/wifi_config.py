import network
import socket
import ure
import time
import random
import config_file
from machine import Pin,I2C
import ssd1306

server_socket=None

NETWORK_PROFILES=config_file.file()

wlan_ap=network.WLAN(network.AP_IF)
wlan_sta=network.WLAN(network.STA_IF)

display=None

def get_connection(ap_ssid=None,ap_password=None,ap_authmode=None,port=None):
    """return a working WLAN(STA_IF) instance or None"""

    # First check if there already is any connection:
    connected=wlan_sta.isconnected()
    if connected:
        return wlan_sta


    try:
        # ESP connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        connected=wlan_sta.isconnected()
        if connected:
            return wlan_sta

        # Read known network profiles from file
        profiles=read_profiles()

        # Search WiFis in range
        wlan_sta.active(True)
        networks=wlan_sta.scan()

        AUTHMODE={0: "open",1: "WEP",2: "WPA-PSK",3: "WPA2-PSK",4: "WPA/WPA2-PSK"}
        for ssid,bssid,channel,rssi,authmode,hidden in sorted(networks,key=lambda x: x[3],reverse=True):
            ssid=ssid.decode('utf-8')
            encrypted=authmode>0
            print("ssid: %s chan: %d rssi: %d authmode: %s" % (ssid,channel,rssi,AUTHMODE.get(authmode,'?')))
            if ssid in profiles:
                if encrypted:
                    if ssid in profiles:
                        password=profiles[ssid]
                        connected=do_connect(ssid,password)
                    else:
                        print("skipping unknown encrypted network")
                else:  # open
                    connected=do_connect(ssid,None)
            if connected:
                break

    except OSError as e:
        print("exception",str(e))

    # start web server for connection manager:
    if not connected:
        connected=start(ap_ssid=ap_ssid,ap_password=ap_password,ap_authmode=ap_authmode,port=port)
        affichageClear(display)

    return wlan_sta if connected else None


def read_profiles():
    dictionary=config_file.configurationRead()
    profiles=dictionary['wifi']
    return profiles


def write_profiles(profiles):
    dictionary=config_file.configurationRead()
    dictionary['wifi']=profiles
    config_file.configurationWrite(dictionary)


def do_connect(ssid,password):
    wlan_sta.active(True)
    connected=wlan_sta.isconnected()
    if connected:
        return connected
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid,password)
    for retry in range(100):
        connected=wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.',end='')
    if connected:
        print('\nConnected. Network config: ',wlan_sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: '+ssid)
    return connected


def send_header(client,status_code=200,content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
        client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")


def send_response(client,payload,status_code=200):
    content_length=len(payload)
    send_header(client,status_code,content_length)
    if content_length>0:
        client.sendall(payload)
    client.close()


def handle_root(client):
    wlan_sta.active(True)
    ssids=sorted(ssid.decode('utf-8') for ssid,*_ in wlan_sta.scan())
    send_header(client)
    client.sendall("""\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Wi-Fi Client Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """)
    while len(ssids):
        ssid=ssids.pop(0)
        client.sendall("""\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid))
    client.sendall("""\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
            <hr />
            <h5>
                <span style="color: #ff0000;">
                    Your ssid and password information will be saved into the
                    "%(filename)s" file in your ESP module for future usage.
                    Be careful about security!
                </span>
            </h5>
            <hr />
            <h2 style="color: #2e6c80;">
                Some useful infos:
            </h2>
            <ul>
                <li>
                    Original code from <a href="https://github.com/cpopp/MicroPythonSamples"
                        target="_blank" rel="noopener">cpopp/MicroPythonSamples</a>.
                </li>
                <li>
                    This code available at <a href="https://github.com/tayfunulu/WiFiManager"
                        target="_blank" rel="noopener">tayfunulu/WiFiManager</a>.
                </li>
            </ul>
        </html>
    """ % dict(filename=NETWORK_PROFILES))    # question
    client.close()


def handle_configure(client,request):
    match=ure.search("ssid=([^&]*)&password=(.*)",request)

    if match is None:
        send_response(client,"Parameters not found",status_code=400)
        return False
    # version 1.9 compatibility
    try:
        ssid=match.group(1).decode("utf-8").replace("%3F","?").replace("%21","!")
        password=match.group(2).decode("utf-8").replace("%3F","?").replace("%21","!")
    except Exception:
        ssid=match.group(1).replace("%3F","?").replace("%21","!")
        password=match.group(2).replace("%3F","?").replace("%21","!")

    if len(ssid)==0:
        send_response(client,"SSID must be provided",status_code=400)
        return False

    if do_connect(ssid,password):
        response="""\
            <html>
                <center>
                    <br><br>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP successfully connected to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client,response)
        try:
            profiles=read_profiles()
        except OSError:
            profiles={}
        profiles[ssid]=password
        write_profiles(profiles)

        time.sleep(5)

        return True
    else:
        response="""\
            <html>
                <center>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP could not connect to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                    <form>
                        <input type="button" value="Go back!" onclick="history.back()"></input>
                    </form>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client,response)
        return False


def handle_not_found(client,url):
    send_response(client,"Path not found: {}".format(url),status_code=404)


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket=None


def start(ap_ssid=None,ap_password=None,ap_authmode=None,port=None):
    # using default address 0x3C

    global server_socket

    ap_ssid_t,ap_password_t,ap_authmode_t,id_t,port_t=config_file.infoWifi()

    if not(ap_ssid is None):
        ap_ssid=ap_ssid_t
    if not(ap_password is None):
        ap_password=ap_password_t
    if not(ap_authmode is None):
        ap_authmode=ap_authmode_t
    if not(port_t is None):
        port=port_t

    addr=socket.getaddrinfo('0.0.0.0',port)[0][-1]

    stop()

    wlan_sta.active(True)
    wlan_ap.active(True)

    # a modifier,mael #
    wlan_ap.config(essid=ap_ssid,password=ap_password,authmode=ap_authmode)

    server_socket=socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)

    global display
    display=affichageWifi(display=display,wlan_sta=wlan_sta,wlan_ap=wlan_ap,password=ap_password)

    print('Connect to WiFi ssid '+ap_ssid+',default password: '+ap_password)
    print('and access the ESP via your favorite web browser at 192.168.4.1.')
    print('Listening on:',addr)

    while True:
        if wlan_sta.isconnected():
            wlan_ap.active(False)
            return True

        client,addr=server_socket.accept()
        print('client connected from',addr)
        try:
            client.settimeout(5.0)

            request=b""
            try:
                while "\r\n\r\n" not in request:
                    request+=client.recv(512)
            except OSError:
                pass

            print("Request is: {}".format(request))
            if "HTTP" not in request:  # skip invalid requests
                continue

            # version 1.9 compatibility
            try:
                url=ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP",request).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url=ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP",request).group(1).rstrip("/")
            print("URL is {}".format(url))

            if url=="":
                handle_root(client)
            elif url=="configure":
                handle_configure(client,request)
            else:
                handle_not_found(client,url)

        finally:
            client.close()



def affichageWifi(display=None,wlan_sta=None,wlan_ap=None,password=''):
    if display is None:
        i2c=I2C(sda=Pin(4),scl=Pin(5))
        display=ssd1306.SSD1306_I2C(128,32,i2c)
    else:
        affichageClear(display)

    if not wlan_sta is None and wlan_sta.isconnected():
        display.text(wlan_sta.config('essid'),0,0,1)
        display.text(wlan_sta.ifconfig[0],0,11,1)
        display.show()
    elif not wlan_ap is None:
        display.text(wlan_ap.config('essid'),0,0,1)
        display.text(password,0,11,1) # wlan_ap.config('password')
        display.text(wlan_ap.ifconfig()[0],0,22,1)
        display.show()
    else:
        display.text('Aucun reseau',0,0,1)
        display.text('connecte',0,11,1)
        display.show()
    return display

def affichageClear(display=None):
    if not display is None:
        display.fill(0)
        display.show()