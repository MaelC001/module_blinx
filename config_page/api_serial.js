var port;
var encoder = new TextEncoder();
var decoder = new TextDecoder();

var returnLignString = '';
var returnLignNumber = 10;

var id = 0;

var url_mpy = "https://raw.githubusercontent.com/MaelC001/sensor_blinx/main/";

async function connect(usbV = null, usbP = null) {
    if (port) {
        port.close();
    }
    try {
        port = await navigator.serial.requestPort({
            filters: [{
                usbVendorId: usbV,
                usbProductId: usbP
            }]
        });

        await port.open({
            baudRate: 115200
        });
    } catch (e) {
        e = e+'';
        if (e == 'TypeError: navigator.serial is undefined'){
            alert('Our navigator is not compatible with the api of webserial, we need it for the connection with the microcontroller. You can use Chrome.')
        }else{
            throw e
        }
    }
}

function write(method, arg, idCmd, repl = true) {
    if (repl) {
        method = "\x01" + method + "\x04";
    } else {
        method = JSON.stringify({
            'method': method,
            'arg': arg,
            'id': idCmd
        });
    }
    method = encoder.encode(method) + returnLignNumber;
    var writer = port.writable.getWriter();
    writer.write(method);
    /*for(var i=0; i<method.length; i+=32){
        writer.write(encoder.encode(method.substring(i,i+32)));
    }*/
    writer.releaseLock();
}

async function read() {
    const reader = port.readable.getReader();
    var text = '';
    var nmb = 0;
    try {
        while (true) {
            const {
                value,
                done
            } = await reader.read();
            text += decoder.decode(value);
            for (var i = 0; i < value.length; i++) {
                if (value[i] == 10) {
                    break;
                }
            }
        }
    } finally {
        reader.releaseLock();
        text = text.split(cle)[0];
        return JSON.parse(text);
    }
}

async function cmd(method, arg = [], idCmd = id) {
    write(method, arg, idCmd);
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
        async function move_mpy(j) {
            var name = j['name'];
            var url = url_mpy + j['file'] + '.mpy';
            var content = getText(url);
            var method = 'write';
            var arg = {
                'name': name,
                'value': content
            };
            return cmd(method, arg = arg, idCmd = id);
        }
        async function etape3(e) {
            var method = 'write';
            var arg = {
                'name': 'config_file.py',
                'value': ""
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


function getText(url) {
    // read text from URL location
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            return request.responseText;
        }
    }
}

connect();