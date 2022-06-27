var port;
var encoder = new TextEncoder();
var decoder = new TextDecoder();

var returnLignString = '';
var returnLignNumber = 10;

var id = 0;

var url_mpy = "https://raw.githubusercontent.com/MaelC001/sensor_blinx/main/";

async function connect(usbV = not_required, usbP = not_required){
    if(port){
        port.close();
    }
    port = await navigator.serial.requestPort({filters: [{usbVendorId: usbV, usbProductId: usbP}]});
    await port.open({ baudRate: 115200 });
}

function write(cmd, arg = [], idCmd = id, repl = true){
    if (repl){
        cmd = "\x01"+cmd+"\x04";
    } else{
        cmd = JSON.stringify({'method' : cmd, 'arg' : arg, 'id' : idCmd});
    }
    cmd = encoder.encode(cmd) + returnLignNumber;
    var writer = port.writable.getWriter();
    writer.write(cmd);
    /*for(var i=0; i<cmd.length; i+=32){
        writer.write(encoder.encode(cmd.substring(i,i+32)));
    }*/
    writer.releaseLock();
}

 function read(){
    const reader = port.readable.getReader();
    var text = '';
    var nmb = 0;
    try {
      while (true) {
        const { value, done } = await reader.read();
        text += decoder.decode(value);
        for (var i = 0; i<value.length; i++){
            if(value[i] == 10){
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

async function read_all_file(callback){
    var cmd = 'liste_file';
    write(cmd, idCmd = id);
    read().then( e => back(e, id));
    async function back(e, id){
        var json = JSON.parse(e);
        if (!json['error']){
            if (id == json['id']){
                return verify_json(e, json => {return Promise.all(json['result'].map(read_file)).then(callback);});
            } else{
                return 'no corresponding in id';
            }
        } else{
            return json['error'];
        }
        async function read_file(name){
            var cmd = "read";
            var arg = [name]
            write(cmd, arg = arg, idCmd = id);
            id += 1;
            return read().then(e => parse(e, id-1));
        }
        function parse(e, id){
            return verify_json(e, json => {return json['result'];});
        }
    }
}

function verify_json(e, func){
    var json = JSON.parse(e);
    if (!json['error']){
        if (id == json['id']){
            return func(json);
        } else{
            console.log('no corresponding in id');
            return 'no corresponding in id';
        }
    } else{
        console.log(json['error']);
        return json['error'];
    }
}

async function config_sensor(json_config, json_sensor){
    var cmd = 'remove_config';
    write(cmd, idCmd = id);
    read().then( e => etape2(e));
    async function etape2(e){
        verify_json(e, json => {});
        Promise.all(json_config.map(move_mpy)).then(e => etape3(e));
        async function move_mpy(j){
            var name = j['name'];
            var url = url_mpy + j['file'] + '.mpy';
            var content = getText(url);
            var cmd = 'write';
            var arg = {'name' : name, 'value' : content};
            write(cmd, arg = arg, idCmd = id);
        }
        async function etape3(e){
            var cmd = 'write';
            var arg = {'name' : 'config_file.py', 'value' : ""};
            write(cmd, arg = arg, idCmd = id);
            read().then(e => etape4(e));
            async function etape4(e){
                var cmd = 'config_sensor';
                var arg = json_sensor;
                write(cmd, arg = arg, idCmd = id);
                read();
            }
        }
    }
}


function getText(url){
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

