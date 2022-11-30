try:
    import usys as sys
except ImportError:
    import sys

try:
    import ubinascii as binascii
except:
    import binascii
try:
    import uhashlib as hashlib
except:
    import hashlib

import uwebsocket
import html_template
import network
import time
import json
wlan_sta=network.WLAN(network.STA_IF)

DEBUG = True
_webrepl = None
uos = None
socket = None
read_input = None
decode_input = None

def read_socket(sock):
    """
    read the resquest form the socket
    """
    get_path = ''
    get_args = {}

    clr = sock.makefile("rwb", 0)
    print(clr)
    l = clr.readline()
    print(l)
    get_path = str(l).split(' ')[1][1:]
    print(get_path)
    if '?' in get_path:
        t = get_path.split('?')
        get_path = t[0]
        for i in t[1].split('&'):
            tt = i.split('=')
            get_args[tt[0]] = '='.join(tt[1:])
    #print(repr(l))
    # sys.stdout.write(repr(l))

    webkey = None

    while 1:
        l = clr.readline()
        print(l)
        if not l:
            raise OSError("EOF in headers")
        if l == b"\r\n":
            break
        #    sys.stdout.write(l)
        h, v = [x.strip() for x in l.split(b":", 1)]
        if DEBUG:
            print((h, v))
        if h == b"Sec-WebSocket-Key": # is it a ws/wss requests ?
            webkey = v

    return webkey, get_path, get_args


def server_handshake(sock, accept_webrepl = True, only_webrepl = False):
    webkey, get_path, get_args = read_socket(sock)

    if DEBUG:
        print(webkey, get_path, accept_webrepl, webkey and get_path == 'webrepl' and accept_webrepl)

    if only_webrepl and not webkey:
        raise OSError("Not a websocket request")

    if only_webrepl or (webkey and accept_webrepl):
        if DEBUG:
            print('websocket')
        webrepl_handler(sock, webkey)
        return True
    elif not webkey: # if not the webkey, than it is not a ws/wss requests but a html one
        if DEBUG:
            print('html')
        http_handler(sock, get_path, get_args)
        return False

def webrepl_handler(sock, webkey):
    if DEBUG:
        print("Sec-WebSocket-Key:", webkey, len(webkey))

    d = hashlib.sha1(webkey)
    d.update(b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
    respkey = d.digest()
    respkey = binascii.b2a_base64(respkey)[:-1]
    if DEBUG:
        print("respkey:", respkey)

    sock.send(
        b"""\
HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: """
    )
    sock.send(respkey)
    sock.send("\r\n\r\n")


    ws = uwebsocket.websocket(sock, True)
    print(ws)
    ws = _webrepl._webrepl(ws)
    print(ws)
    sock.setblocking(False)
    # notify REPL on socket incoming data (ESP32/ESP8266-only)
    if hasattr(uos, "dupterm_notify"):
        sock.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
    uos.dupterm(ws)

def http_handler(client, get_path, get_args):
    # the different path the user can use
    action = ['', 'codeboot', 'wifi_manager', 'configure', 'blinx']
    # the '' is for the root, if connected to wifi it will show the codeboot page, else it will show the wifi manager

    html = '<p>error 404, path not find</p>'
    status_code = 404

    if get_path in action:
        status_code = 200
        if get_path == '':
            if network.WLAN(network.STA_IF).isconneted():
                html = html_template.codeboot
            else:
                html = html_template.wifi_manager
        elif get_path == 'codeboot':
            html = html_template.codeboot
        elif get_path == 'wifi_manager':
            html = html_template.wifi_manager()
        elif get_path == 'configure':
            html = wifi_connect()
            if html == False:
                return
        elif get_path == 'blinx':
            read_input_rpc(client = client, status_code = status_code, **get_args)
            return
    send_response_html(client, html, status_code = status_code)

def send_response_html(client, html_code, status_code = 200, type = 'text/html'):
    """send the code of the web page to the user

    Args:
        client: the client
        html_code (str): the code of the html page
        status_code (int, optional): the status of the page 200:ok, 404:not found ... Defaults to 200.
    """
    content_length=len(html_code)

    # send the header of the page
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: "+type+"\r\n")
    if content_length is not None:
        client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")

    # send the content of the page
    if content_length>0:
        client.sendall(html_code)

    client.close()


def wifi_connect(client, get_args):
    """
        To connect to wifi
    """
    if 'ssid' not in get_args or 'password' not in get_args:
        send_response_html(client,"Parameters not found",status_code=400)
        return False

    # get the post argument
    try:
        ssid=get_args['ssid'].decode("utf-8").replace("%3F","?").replace("%21","!")
        password=get_args['password'].decode("utf-8").replace("%3F","?").replace("%21","!")
    except Exception:
        ssid=get_args['ssid'].replace("%3F","?").replace("%21","!")
        password=get_args['password'].replace("%3F","?").replace("%21","!")

    if len(ssid)==0:
        send_response_html(client,"SSID must be provided",status_code=400)
        return False

    wlan_sta.connect(ssid,password)
    connected = False
    for _ in range(100):
        connected=wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        if DEBUG:
            print('.',end='')

    if connected:
        response = html_template.wifi_manager_success
    else:
        response = html_template.wifi_manager_error
    return response % dict(ssid=ssid)

def read_input_rpc(client = None, status_code = 202, method = '', params = [], id = 0):
    """
        the rpc via wifi
    """
    def sender_to_html(text):
        if isinstance(text, dict):
            text = json.dumps(text)
            send_response_html(client, text, status_code = status_code, type = 'application/json')
        else :
            text += '\n'
            send_response_html(client, text, status_code = status_code)
    j = {
        'method': method,
        'params': params,
        'id': id,
    }
    decode_input(j, how_send = sender_to_html)