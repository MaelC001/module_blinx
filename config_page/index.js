function _(el) {
    return document.getElementById(el);
}

let loader = '<i class="notched circle loading icon green"></i> wait...';

let templatePopup = "\
<div class='form-popup' id='formConfigPopup'>\
    <form class='form-container'>\
            <div onclick='window.open(\"$UrlSensor$\",\"infoSensor\",\"height=500,width=800\");'>\
                <label for='typeSensor' class='urlPopupLabel'><b>Sensor Type</b></label>\
                <input type='text' name='typeSensor' value='$ValuePopup$' id='typeSensor' class='urlPopup' disabled>\
            </div>\
            <label for='nameSensor'><b>Name</b></label>\
            <input type='text' placeholder='Your name of the sensor' name='nameSensor' class='modify' id='nameSensor'>\
            <div id='popupPlus'></div>\
        <button type='button' class='btn' onclick='savePopupConfig(\"$IdPortSensor$\")'>Saving</button>\
    </form>\
</div>";

let templatePopupWifi = "\
<div class='form-popup' id='formWifiPopup'>\
    <form class='form-container'>\
        <label for='ssid'><b>SSID</b></label>\
        <input type='text' placeholder='SSID wifi' name='ssid' class='modify' id='ssid'>\
        <label for='password'><b>Password</b></label>\
        <input type='password' placeholder='password wifi' name='password' class='modify' id='password'>\
        <button type='button' class='btn' onclick='connectWifi()'>Connect</button>\
    </form>\
</div>";

let templateCardI2C = "\
<div class='card' id='$IdSensor$'>\
    <div class='content'>\
        <img class='right floated mini ui image' src='$ImageSensor$'>\
        <div class='header'>\
            $NameSensor$\
        </div>\
        <div class='meta'>\
            <a href='$UrlSensor$' target='_blank'>info sensor</a>\
        </div>\
    </div>\
    <div class='extra content'>\
        <div class='ui two buttons'>\
            <div class='ui labeled myBlue button icon config' data-position='right center' id='$IdSensor$Config'><i\
            class='icon settings'></i>Config the sensor</div>\
            <div class='ui labeled red button icon' onclick='removeI2C(\"$IdSensor$\")'><i class='trash icon'></i>Remove</div>\
        </div>\
    </div>\
</div>";

// list of sensor for each different port
let listAllSensors = {
    "I2C": {
        "temp-sht3x": {
            "text": "temperature (in micro controller)",
            "addr": "0x70",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': 'https://wiki.seeedstudio.com/Grove-I2C_High_Accuracy_Temp&Humi_Sensor-SHT35/',
        },
        "humid-sht3x": {
            "text": "humidity (in micro controller)",
            "addr": "0x70",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': 'https://wiki.seeedstudio.com/Grove-I2C_High_Accuracy_Temp&Humi_Sensor-SHT35/',
        },
    },
    "DigiAnalog": {
        "led pin2": {
            "text": "led (in micro controller) (pin 2)",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': '',
        },
        "custom": {
            "text": "custom",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': '',
        }
    },
};
let listSensors = {};
let listSensorsI2C = [];
let sensorMicroController = []
let infoUserSensor = [{},
    {}, {}
];



function loadSelectPort() {
    create_dic();
    listSensorsI2C = listSensors['I2C'];

    let textHTML = "";
    textHTML += "<div class='boutton'>\
    <div class='save'>\
        <button type='button' class='ui labeled icon myBlue button' id='buttonSaveConfig'><i class='\
            icon settings'></i>Save Configuration</button>\
    </div>\
    <div class='wifi'>\
        <button type='button' class='ui labeled icon myBlue button' id='buttonConnectWifi'><i class='\
            icon wifi'></i>Configure WiFi</button>\
    </div>\
</div>\
<div class='imageDiv'>\
    <img src='image_color.png' alt='image_of_micro_controller' class='ui centered image'>\
</div>\
<div class='analogDigi1'>\
    <div class='select1'>\
        <div class='ui fluid search selection dropdown' id='selectAnalogDigi1' name='selectAnalogDigi1'>\
            <input type='hidden' name='country'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor Analog/Digital</div>\
            <div class='menu'>";
    textHTML += setOptionSelect(listSensors['DigiAnalog']);
    textHTML += "            </div>\
        </div>\
    </div>\
    <div class='config1'>\
        <button type='button' class='ui labeled icon myBlue button config fluid' data-position='right center' id='AnalogDigi1'><i\
                class='icon settings'></i>Config the sensor</button>\
    </div>\
</div>\
<div class='I2C'>\
    <div class='buttonI2C'>\
        <a class='ui myBlue basic label'>Port I2C :</a> \
        <button type='button' class='ui labeled icon myBlue button scan'><i class='icon fa-regular fa-magnifying-glass'></i>Scan I2C</button>\
    </div>\
    <div class='select2'>\
        <div class='ui fluid search selection dropdown' id='selectI2C' name='selectI2C'>\
            <input type='hidden' name='country'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor I2C</div>\
            <div class='menu' id='listSelectI2c'>";
    textHTML += setOptionSelect(listSensorsI2C);
    textHTML += "         </div>\
        </div>\
    </div>\
    <div class='listI2C'>\
    <div class='ui cards centered' id='listCardI2C'></div>\
    </div>\
</div>\
<div class='analogDigi2'>\
    <div class='select3'>\
        <div class='ui fluid search selection dropdown' id='selectAnalogDigi2' name='selectAnalogDigi2'>\
            <input type='hidden' name='country'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor Analog/Digital</div>\
            <div class='menu'>";
    textHTML += setOptionSelect(listSensors['DigiAnalog']);
    textHTML += "            </div>\
        </div>\
    </div>\
    <div class='config3'>\
        <button type='button' class='ui labeled icon myBlue button config fluid' data-position='left center' id='AnalogDigi2'><i\
                class='icon settings'></i>Config the sensor</button>\
    </div>\
</div>";

    _("container").innerHTML = textHTML;

    $("#selectAnalogDigi1").dropdown({
        onChange: e => selectAnalogDigi(e, 0),
    });
    $('#selectI2C').dropdown({
        onChange: selectI2C,
    });
    $("#selectAnalogDigi2").dropdown({
        onChange: e => selectAnalogDigi(e, 2),
    });

    $('.ui.button.config').popup({
        on: 'click',
        exclusive: true,
        onShow: createPopup,
        html: loader,
    });
    $('.ui.button.scan').popup({
        on: 'click',
        exclusive: true,
        onShow: scanI2C,
        html: loader,
    });
    $('#buttonConnectWifi').popup({
        on: 'click',
        exclusive: true,
        html: templatePopupWifi,
    });
    $('#buttonSaveConfig').popup({
        on: 'click',
        exclusive: true,
        //onShow: scanI2C,
        html: loader,
    });
}

function connectWifi(){
    let ssid = _('ssid').value;
    let password = _('password').value;
    $('#buttonConnectWifi').popup('change content',loader);

    let method = 'wifi_connect';
    let arg = {'ssid' : ssid, 'password' : password};
    let result = cmd(method, arg = arg, idCmd = 0).then(e => verify_json(e, j => {return j['result']}));
    if (result == true){
        $('#buttonConnectWifi').popup('change content','<p>success</p>');
    }else{
        $('#buttonConnectWifi').popup('change content','<p>error : '+result+'</p>');
    }
}

function selectAnalogDigi(e, id) {
    let item;
    listSensors['DigiAnalog'].forEach(getItem);

    addToInfoUser(id, item['value'], item['name'], nameUser = '');

    function getItem(value) {
        if (value['value'] == e) {
            item = value;
        }
    }
}

function selectI2C(e) {
    let item;
    listSensorsI2C = listSensorsI2C.filter(removeItemI2C);

    let temp = templateCardI2C;
    temp = temp.replaceAll('$IdSensor$', item['value']);
    temp = temp.replaceAll('$NameSensor$', item['name']);
    temp = temp.replaceAll('$ImageSensor$', item['urlImage']);
    temp = temp.replaceAll('$UrlSensor$', item['url']);

    _('listCardI2C').innerHTML += temp;

    addToInfoUser(1, item['value'], item['name'], nameUser = '');

    changeSelectI2C();

    $('#' + e + 'Config').popup({
        on: 'click',
        exclusive: true,
        onShow: createPopup,
        html: loader,
    });
    $('#selectI2C').dropdown('clear');

    function removeItemI2C(value) {
        if (value['value'] != e) {
            return true;
        } else {
            item = value;
            return false;
        }
    }
}

function removeI2C(id) {
    let el = _(id);
    el.parentNode.removeChild(el);
    listSensorsI2C.push({
        'value': id,
        'name': listAllSensors['I2C'][id]['text'],
        'urlImage': listAllSensors['I2C'][id]['urlImage'],
        'url': listAllSensors['I2C'][id]['url'],
    });

    removeToInfoUserI2C(id);

    changeSelectI2C();
}

function changeSelectI2C() {
    _('listSelectI2c').innerHTML = setOptionSelect(listSensorsI2C);
    $('#selectI2C').dropdown('refresh');
}

function savePopupConfig(idPort) {
    let idIndex;
    let nameSensor;
    let idSensor;
    if (idPort == 'AnalogDigi1') {
        idSensor = $('#select' + idPort).dropdown('get value');
        nameSensor = listAllSensors['DigiAnalog'][idSensor]['text'];
        idIndex = 0;
    } else if (idPort == 'AnalogDigi2') {
        idSensor = $('#select' + idPort).dropdown('get value');
        nameSensor = listAllSensors['DigiAnalog'][idSensor]['text'];
        idIndex = 2;
    } else {
        idSensor = idPort.substring(idPort.length - 6, 0);
        valueItem = listAllSensors['I2C'][idItem]['text'];
        idIndex = 1;
    }

    let nameUser = _('nameSensor').value;
    addToInfoUser(idIndex, idSensor, nameSensor, nameUser);
}

function addToInfoUser(idIndex, idSensor, nameSensor, nameUser = '') {
    if (idIndex == 0 || idIndex == 2) {
        infoUserSensor[idIndex] = {};
    }
    infoUserSensor[idIndex][idSensor] = {
        "name": nameSensor,
        "idSensor": idSensor,
        "userName": nameUser,
        "channels": [],
        "borne inferieure": -1,
        "borne supeieure": -1,
    };
}

function removeToInfoUserI2C(idRemove) {
    let idIndex = 1;
    let dict = infoUserSensor[idIndex];

    let filtered = Object.keys(dict).reduce(function (filtered, key) {
        if (key != idRemove) {
            filtered[key] = dict[key];
        }
        return filtered;
    }, {});

    infoUserSensor[idIndex] = filtered;
}

function scanI2C(e, boolPopup = true) {
    let popup = this;
    let tempJson;
    let method = "scan_i2c";
    return cmd(method, idCmd = 0).then(e => verify_json(e, verify));

    function verify(json) {
        tempJson = json;
        let values = _('sensorsPort' + port).value;
        values.filter(test);
        if (boolPopup) {
            let plus = recordI2C();
            let html = arrayToHtml(values, plus);
            popup.html(html);
        }
        return values;

        function test(name) {
            let addr = listAllSensors['I2C'][name]['addr'];
            let i = tempJson['result'].indexOf(addr);
            if (i !== -1) {
                tempJson['result'].splice(i, 1);
                return false;
            } else {
                return true;
            }
        }
    }

    function recordI2C() {
        let plus = [];
        if (tempJson['result'].length > 0) {
            for (let name in listAllSensors['I2C']) {
                let addr = listAllSensors['I2C'][name]['addr'];
                if (tempJson['result'].indexOf(addr) > -1 && sensorMicroController.indexOf(addr) == -1) {
                    plus.push(listAllSensors['I2C'][name]['text'])
                }
            }
        }
        return plus
    }

    function arrayToHtml(arrayError, arrayPlus) {
        let tempHtml = '';
        if (arrayError.length > 0) {
            tempHtml += '<p>You have sensors that are not (yet?) connected : ' + arrayError.toString('; ') + '</p>';
        }
        if (arrayPlus.length > 0) {
            tempHtml += '<p>There are sensors that are connected to the microcontroller that you have not chosen: ' + arrayPlus.toString('; ') + '</p>';
            tempHtml += "<button type='button' class='ui labeled button'>Do you want to add them to your sensors?</button>";
        }
        if (tempHtml == '') {
            tempHtml += '<p>Nothing to report.</p>';
        }
        return tempHtml
    }
}


function config_sensor() {
    if (!scanI2C('a', boolPopup = false)) {
        alert('i2c not correct');
    } else {
        let json_config = [];
        let json_sensor = {};

        let portAD = [_('sensorsPort1').value, _('sensorsPort3').value];
        let portI2C = _('sensorsPort2').value;

        portAD.forEach(DigiAnalogFunction);
        let i = 0;

        function DigiAnalogFunction(name) {
            if (name != "" && name != "costum") {
                json_config_push(name, 'DigiAnalog');
                let info = infoUserSensor[i];
                if (Object.keys(info).length > 0) {
                    if (listAllSensors['DigiAnalog'][name]['is_display']) {} else {
                        json_sensor_push(info, name);
                    }
                } else {
                    alert('please configure all sensors');
                }
                i = 2;
            }
        }

        portI2C.forEach(I2CFunction);

        function I2CFunction(name) {
            json_config_push(name, 'I2C');
            let infos = infoUserSensor[1];
            infos.forEach(setConfigJson);

            function setConfigJson(info) {
                if (Object.keys(info).length > 0) {
                    if (listAllSensors['I2C'][name]['is_display']) {} else {
                        json_sensor_push(info, name);
                    }
                } else {
                    alert('please configure all sensors');
                }
            }
        }

        config_sensor_serial(json_config, json_sensor);

        function json_config_push(name, type) {
            json_config.push({
                'name': name,
                'file': listAllSensors[type][name]['file'],
            });
        }

        function json_sensor_push(info, name) {
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors['DigiAnalog'][name]['is_input'],
                'is_display': listAllSensors['DigiAnalog'][name]['is_display'],
                'channels': info['channels'],
            }
        }

        function json_sensor_display_push(info, name) {
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors['DigiAnalog'][name]['is_input'],
                'is_display': listAllSensors['DigiAnalog'][name]['is_display'],
                'channels': info['channels'],
            }
        }
    }
}

function createPopup(e) {
    let popup = this;
    let idPort = e.id;
    let idItem;
    let urlItem;
    let type;
    let valueItem;
    let temp = '<p>error</p>';
    if (idPort == 'AnalogDigi1' || idPort == 'AnalogDigi2') {
        idItem = $('#select' + idPort).dropdown('get value');
        type = 'DigiAnalog';
    } else {
        idItem = idPort.substring(idPort.length - 6, 0);
        type = 'I2C';
    }
    valueItem = listAllSensors[type][idItem]['text'];
    urlItem = listAllSensors[type][idItem]['url'];
    if (valueItem != '') {
        temp = templatePopup.replace('$IdPortSensor$', idPort);
        temp = temp.replace('$ValuePopup$', valueItem);
        temp = temp.replace('$UrlSensor$', urlItem);
    }
    popup.html(temp);
}

function setOptionSelect(arrayItem) {
    let tempText = '';
    arrayItem.forEach(e => {
        tempText += "<div class='item' data-text='" + e['name'] + "' data-value='" + e['value'] + "'><img class='ui image' src='" + e['urlImage'] + "' style='width:20px;'>" + e['name'] + "</div>";
    });
    return tempText;
}


function create_dic() {
    for (let key1 in listAllSensors) {
        listSensors[key1] = [];
        for (let key2 in listAllSensors[key1]) {
            listSensors[key1].push({
                'value': key2,
                'name': listAllSensors[key1][key2]['text'],
                'urlImage': listAllSensors[key1][key2]['urlImage'],
                'url': listAllSensors[key1][key2]['url'],
            });
        }
    }
}

loadSelectPort();