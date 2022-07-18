var port;
var encoder = new TextEncoder();
var decoder = new TextDecoder();

var returnLignString = '\n';
var returnLignNumber = 10;

var id = 0;

var url_mpy = "https://raw.githubusercontent.com/MaelC001/sensor_blinx/main/";

async function connect(idError = null, callback = null) {
    let textError;
    if (port) {
        port.close();
    }
    try {
        await navigator.serial.requestPort().then((p) => {
            port = p;
            port.open({
                baudRate: 115200
            });
        });
        if(callback != null){
            callback();
        }
    } catch (e) {
        error(e);
    }
    if(idError == null){
        console.log(textError);
    } else{
        document.getElementById(idError).innerHTML = textError;
    }

    function error(e){
        e = e + '';
        if (e == 'TypeError: navigator.serial is undefined') {
            textError = "\
                <div class='ui error floating message'>\
                    <div class='header'>\
                    The navigator is not compatible with the api of webserial\
                    </div>\
                    <p>We need the webserial api for the connection with the microcontroller.</p>\
                    <p>Chrome is compatible with the api.</p>\
                </div>";
        } else if (e == 'DOMException: No port selected by the user.' || e == "NotFoundError: No port selected by the user.") {
            textError = "\
                <div class='ui error floating message'>\
                    <div class='header'>\
                    Chose port\
                    </div>\
                    <p>You have to chose the port of the micro controller, so we can tlak with it.</p>\
                    <button type='button' class='ui labeled button' onclick='connect(idError = 'error')'>\
                        Re-try\
                    </button>\
                </div>";
        } else if (e == "SecurityError: Failed to execute 'requestPort' on 'Serial': Must be handling a user gesture to show a permission request.") {
            textError = "\
                <div class='ui error floating message'>\
                    <div class='header'>\
                    Security Error\
                    </div>\
                    <p>Your browser block the request of the port for the micro-controller.</p>\
                    <button type='button' class='ui labeled button' onclick='connect(idError = 'error')'>\
                        Re-try\
                    </button>\
                </div>";
        } else {
            console.log(e);
            throw e;
        }
    }
}

function write(method, arg, idCmd, repl = true) {
    if (repl) {
        method = "\x01" + method + "\x04";
    } else {
        method = JSON.stringify({
            'method': method,
            'params': arg,
            'id': idCmd
        }) + returnLignString;
    }
    method = encoder.encode(method);
    console.log(method);
    var writer = port.writable.getWriter();
    //writer.write(method);
    var step = 95;
    for(var i=0; i<method.length; i+=step){
        writer.write(encoder.encode(method.substring(i,i+step)));
    }
    writer.releaseLock();
}

async function read() {
    const reader = port.readable.getReader();
    var text = '';
    var finBoucle = true;
    try {
        while (finBoucle) {
            const {
                value,
                done
            } = await reader.read();
            text += decoder.decode(value);
            for (var i = 0; i < value.length; i++) {
                if (value[i] == returnLignNumber) {
                    finBoucle = false;
                    break;
                }
            }
        }
    } finally {
        reader.releaseLock();
        //text = text.split(cle)[0];
        //console.log(text);
        return text;
    }
}

async function cmd(method, arg = [], idCmd = id) {
    write(method, arg, idCmd, repl=false);
    return await read();
}

async function read_all_file(callback) {
    var method = 'liste_file';
    cmd(method, idCmd = id).then(e => back(e, id));
    async function back(e, id) {
        var json = JSON.parse(e);
        if (!json['error']) {
            if (id == json['id']) {
                return verify_json(e, json => {
                    return Promise.all(json['result'].map(read_file)).then(callback);
                });
            } else {
                return 'no corresponding in id';
            }
        } else {
            return json['error'];
        }
        async function read_file(name) {
            var method = "read";
            var arg = [name]
            var tempResult = cmd(method, arg = arg, idCmd = id).then(e => parse(e, id));
            id += 1;
            return tempResult;
        }

        function parse(e, id) {
            return verify_json(e, json => {
                return json['result'];
            });
        }
    }
}

function verify_json(e, func) {
    var json = JSON.parse(e);
    if (!json['error']) {
        if (id == json['id']) {
            return func(json);
        } else {
            console.log('no corresponding in id');
            return 'no corresponding in id';
        }
    } else {
        console.log(json['error']);
        return json['error'];
    }
}

async function config_sensor_serial(json_config, json_sensor) {
    var method = 'remove_config';
    cmd(method, idCmd = id).then(e => etape2(e));
    async function etape2(e) {
        verify_json(e, json => {});
        Promise.all(json_config.map(move_mpy)).then(e => etape3(e));
        async function move_mpy(name) {
            var file = name + '.mpy';
            var url = url_mpy + file;
            var content = await getText(url);
            var method = 'write';
            var arg = {
                'name': file,
                'value': content
            };
            return cmd(method, arg = arg, idCmd = id);
        }
        async function etape3(e) {
            var method = 'write';
            var arg = {
                'name': 'config_file.py',
                'value': "array = [\"" + json_config.toString().replaceAll(',','","')+"\"]",
            };
            cmd(method, arg = arg, idCmd = id).then(e => etape4(e));
            async function etape4(e) {
                var method = 'config_sensor';
                var arg = json_sensor;
                cmd(method, arg = arg, idCmd = id);
            }
        }
    }
}


async function getText(url) {
    // read text from URL location
    return fetch(url).then(res => {return res.text()}).then(e => {return e});
}

function infoWifi(){
    var method = 'wifi';
    cmd(method,arg = [], idCmd = id).then(e => getInfo(e));
    function getInfo(e) {
        verify_json(e, json => {
            let t = json['result']['wlan_sta'];
            let connected = t['isconnected'];
            let ip = t['config']['ifcongif'][0];
            let ssid = t['config']['ssid'];
            let hostname = t['config']['dhcp_hostname'];
            if (connected){
                _('wifiConnected').innerHTML = '';
                _('wifiInfoConnected').style.display = 'block';
                _('wifiSSID').innerHTML = ssid;
                _('wifiIP').innerHTML = ip;
                _('wifiMDNS').innerHTML = hostname;
            }
        });
    }
}