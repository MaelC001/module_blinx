# This module should be imported from REPL, not run from command line.
import socket
import uos
import network
import uwebsocket
import websocket_helper
import _webrepl

listen_s = None
client_s = None

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

html_codeboot = """<!DOCTYPE html>
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
</html>"""
html_tempo = None

def setup_conn(port=8266, accept_handler=None, webrepl=True):
    global listen_s
    if accept_handler is None and webrepl:
        accept_handler=accept_conn_webrepl

    ai = socket.getaddrinfo("0.0.0.0", port)
    addr = ai[0][-1]

    type = 'ws' if webrepl else 'http'

    listen_s = socket.socket()
    listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_s.bind(addr)
    listen_s.listen(1)
    if accept_handler:
        listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
    if wlan_ap.active():
        print(f"WebREPL daemon started on {type}://{wlan_ap.ifconfig()[0]}:{port}")
    if wlan_sta.active():
        print(f"WebREPL daemon started on {type}://{wlan_sta.ifconfig()[0]}:{port}")
    return listen_s


def accept_conn_webrepl(listen_sock, html = False):
    global client_s
    cl, remote_addr = listen_sock.accept()
    prev = uos.dupterm(None)
    uos.dupterm(prev)
    if prev:
        print("\nConcurrent WebREPL connection from", remote_addr, "rejected")
        cl.close()
        return

    print("\nWebREPL connection from:", remote_addr)

    client_s = cl

    if not html:
        print('0a')
        accept_fin(html)

def accept_conn_website(listen_sock):
    accept_conn_webrepl(listen_sock, html = True)

    string_request = client_s.recv(2048).decode('utf-8')

    print("Request:" + string_request)
    try:
        request_line = string_request.split("\r\n")[0]    # only consider first line
        request_line = request_line.split()     # separate by whitespace

        (request_method, path, request_version) = request_line
        print(request_method, path, request_version)

        if request_method == "GET" and "favicon" not in path:
            if html_tempo is None:
                send_response(client_s, html_codeboot)
            else :
                send_response(client_s, html_tempo)

    except Exception as e:
        print("Exception", e)
    finally:

        accept_fin(True)

def accept_fin(html):
    accepted = websocket_helper.server_handshake(client_s, html)

    if accepted:
        ws = uwebsocket.websocket(client_s, True)
        ws = _webrepl._webrepl(ws)
        client_s.setblocking(False)
        # notify REPL on socket incoming data (ESP32/ESP8266-only)
        if hasattr(uos, "dupterm_notify"):
            client_s.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
        uos.dupterm(ws)




def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
        client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")

def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()

def stop():
    global listen_s, client_s
    uos.dupterm(None)
    if client_s:
        client_s.close()
    if listen_s:
        listen_s.close()


def start(port=8266, password=None, ssid_wifi=None, password_wifi=None, authmode_wifi=None, html=False, html_text=None):
    global html_tempo
    html_tempo = html_text

    if html:
        accept = accept_conn_website
    else :
        accept = accept_conn_webrepl

    stop()
    if not (ssid_wifi is None) and not (password_wifi is None) and not (authmode_wifi is None):
        startWifi(ssid_wifi, password_wifi, authmode_wifi)
        if not (password is None) :
            _webrepl.password(password)
        setup_conn(port, accept, not html)
        print("Started webrepl in manual override mode, with perso wifi")
    elif password is None:
        try:
            import webrepl_cfg

            _webrepl.password(webrepl_cfg.PASS)
            setup_conn(port, accept, not html)
            print("Started webrepl in normal mode")
        except:
            print("WebREPL is not configured, run 'import webrepl_setup'")
    else:
        _webrepl.password(password)
        setup_conn(port, accept, not html)
        print("Started webrepl in manual override mode")

def startWifi(ssid_wifi, password_wifi, authmode_wifi):
    wlan_ap.config(essid=ssid_wifi, password=password_wifi, authmode=authmode_wifi)

    print('Connect to WiFi ssid ' + ssid_wifi + ', default password: ' + password_wifi)
    print('and access the ESP via your favorite web browser at 192.168.4.1.')

def start_foreground(port=8266):
    stop()
    s = setup_conn(port, None)
    accept_conn_webrepl(s)
