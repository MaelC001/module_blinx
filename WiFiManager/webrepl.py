# This module should be imported from REPL, not run from command line.
import socket
import uos
import network
import websocket_helper
import _webrepl

listen_s = None
client_s = None

# the read input function for read the input frome the rpc wifi
read_input = None

websocket_helper._webrepl = _webrepl
websocket_helper.socket = socket

# accept the webrepl of micropython
accept_webrepl = None
only_webrepl = None

def setup_conn(port, accept_handler, accept_webrepl_boolean, only_webrepl_boolean):
    global listen_s, accept_webrepl, only_webrepl

    accept_webrepl = accept_webrepl_boolean
    only_webrepl = only_webrepl_boolean

    listen_s = socket.socket()
    listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ai = socket.getaddrinfo("0.0.0.0", port)
    addr = ai[0][4]

    listen_s.bind(addr)
    listen_s.listen(1)
    if accept_handler:
        listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
    for i in (network.AP_IF, network.STA_IF):
        iface = network.WLAN(i)
        if iface.active():
            if accept_webrepl or only_webrepl:
                print("WebREPL daemon started on ws://%s:%d" % (iface.ifconfig()[0], port))
            if not only_webrepl:
                print("web site daemon started on http://%s:%d" % (iface.ifconfig()[0], port))
    return listen_s


def accept_conn(listen_sock):
    global client_s
    cl, remote_addr = listen_sock.accept()
    prev = uos.dupterm(None)
    uos.dupterm(prev)
    websocket_helper.uos = uos
    if prev:
        print("\nConcurrent WebREPL connection from", remote_addr, "rejected")
        cl.close()
        return
    print("\nWebREPL connection from:", remote_addr)

    stop = websocket_helper.server_handshake(cl, accept_webrepl = accept_webrepl, only_webrepl = only_webrepl)

    if stop:
        client_s = cl
    else:
        uos.dupterm(None)
        websocket_helper.uos = uos

def wifi_manager_handler():
    pass
def codeboot_handler():
    pass



def stop():
    global listen_s, client_s
    uos.dupterm(None)
    websocket_helper.uos = uos
    if client_s:
        client_s.close()
    if listen_s:
        listen_s.close()


def start(port=80, password=None, accept_handler=accept_conn, accept_webrepl = False, only_webrepl = False):
    stop()
    if accept_webrepl or only_webrepl:
        webrepl_pass = password
        if webrepl_pass is None:
            try:
                import webrepl_cfg

                webrepl_pass = webrepl_cfg.PASS
            except:
                print("WebREPL is not configured, run 'import webrepl_setup'")

        _webrepl.password(webrepl_pass)

    s = setup_conn(port, accept_handler, accept_webrepl, only_webrepl)

    if accept_handler is None:
        print("Starting webrepl in foreground mode")
        accept_conn(s)
    elif password is None:
        print("Started webrepl in normal mode")
    else:
        print("Started webrepl in manual override mode")


def start_foreground(port=80, password=None):
    start(port, password, None)

def change_rpc(func):
    global read_input
    read_input = func
    websocket_helper.read_input = func