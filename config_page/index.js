function _(el) {
    return document.getElementById(el);
}

let numberOfPortAnalogDigi = [{
        'numberPort': '1',
        'numberPortAD': '1',
    },
    {
        'numberPort': '3',
        'numberPortAD': '2',
    },
];
let sensorInMicro = ['led', 'button', 'screen', 'temperature', 'humidity', 'light'];
let infoButtonGeneral = [{
    'idButton': 'SaveConfig',
    'idButtonCourt': 'config',
    'textButton': 'Save Configuration',
    'iconButton': 'settings',
}, {
    'idButton': 'ConnectWifi',
    'idButtonCourt': 'wifi',
    'textButton': 'Configure WiFi',
    'iconButton': 'wifi',
}, ];



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



function loadPAge() {
    create_dic();
    listSensorsI2C = listSensors['I2C'];

    let textHtml = templateGeneralPage;
    textHtml = textHtml.replaceAll('$htmlButtonGeneral$', getHtmlForButton());
    textHtml = textHtml.replaceAll('$htmlSensor$', getHtmlForSensor());
    _('container').innerHTML = textHtml;


    $("#selectAnalogDigi11").dropdown({
        onChange: e => selectAnalogDigi(e, 0),
    });
    $("#selectAnalogDigi12").dropdown({
        onChange: e => selectAnalogDigi(e, 0),
    });
    $("#selectAnalogDigi12").hide();
    $('#selectI2C').dropdown({
        onChange: selectI2C,
    });
    $("#selectAnalogDigi21").dropdown({
        onChange: e => selectAnalogDigi(e, 2),
    });
    $("#selectAnalogDigi22").dropdown({
        onChange: e => selectAnalogDigi(e, 2),
    });
    $("#selectAnalogDigi22").hide();

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

    sensorInMicro.forEach(id => $("#" + id + "Config").hide());

    function getHtmlForButton() {
        let textHtmlTemp = '';
        infoButtonGeneral.forEach(info => {
            textHtmlTemp += loopDic(info, templateButtonGeneral);
        });
        return textHtmlTemp;
    }

    function getHtmlForSensor() {
        let textHtmlTemp = '';
        numberOfPortAnalogDigi.forEach(info => {
            let temp = loopDic(info, templatePortAnlogDigi);
            temp = temp.replaceAll('$optionSelect$', setOptionSelect(listSensors['DigiAnalog']))
            textHtmlTemp += temp;
        });
        textHtmlTemp += templatePortI2C.replaceAll('$optionSelect$', setOptionSelect(listSensorsI2C));
        sensorInMicro.forEach(id => {
            let temp = templatePortSensorInMicro.replaceAll('$idSensor$', id);
            temp = temp.replaceAll('$idSensorMaj$', strUcFirst(id));
            textHtmlTemp += temp;
        });
        return textHtmlTemp;
    }

    function loopDic(dic, template){
        let temp = template;
        for (let key in dic) {
            temp = temp.replaceAll('$' + key + '$', dic[key]);
        }
        return temp;
    }
}


function customPort(check, port) {
    if (check.checked) {
        $("#selectAnalogDigi" + port + "2").show();
    } else {
        $("#selectAnalogDigi" + port + "2").hide();
    }
}

function sensorInMicroConfig(check, id) {
    if (check.checked) {
        $("#" + id + "Config").show();
    } else {
        $("#" + id + "Config").hide();
    }
}

function strUcFirst(a) {
    return (a + '').charAt(0).toUpperCase() + a.substr(1);
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

function selectAnalogDigi(e, id, pin = 0) {
    let item;
    listSensors['DigiAnalog'].forEach(getItem);

    addToInfoUserAD(id, item['value'], item['name'], nameUser = '', idPin = pin);

    function getItem(value) {
        if (value['value'] == e) {
            item = value;
        }
    }
}

function selectI2C(e) {
    let item = {};
    listSensorsI2C = listSensorsI2C.filter(removeItemI2C);

    let temp = templateCardI2C;
    temp = temp.replaceAll('$IdSensor$', item['value']);
    temp = temp.replaceAll('$NameSensor$', item['name']);
    temp = temp.replaceAll('$ImageSensor$', item['urlImage']);
    temp = temp.replaceAll('$UrlSensor$', item['url']);

    _('listCardI2C').innerHTML += temp;

    addToInfoUserI2C(item['value'], item['name'], nameUser = '');

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

function savePopupConfig(idPort, idPin = 0) {
    let idIndex;
    let nameSensor;
    let idSensor;
    let nameUser = _('nameSensor').value;
    if (idPort == 'AnalogDigi1') {
        idSensor = $('#select' + idPort).dropdown('get value');
        nameSensor = listAllSensors['DigiAnalog'][idSensor]['text'];
        idIndex = 0;
        addToInfoUserAD(idIndex, idSensor, nameSensor, nameUser, idPin = idPin);
    } else if (idPort == 'AnalogDigi2') {
        idSensor = $('#select' + idPort).dropdown('get value');
        nameSensor = listAllSensors['DigiAnalog'][idSensor]['text'];
        idIndex = 2;
        addToInfoUserAD(idIndex, idSensor, nameSensor, nameUser, idPin = idPin);
    } else {
        idSensor = idPort.substring(idPort.length - 6, 0);
        valueItem = listAllSensors['I2C'][idItem]['text'];
        idIndex = 1;
        addToInfoUserI2C(idSensor, nameSensor, nameUser);
    }
}

function addToInfoUserAD(idIndex, idSensor, nameSensor, nameUser = '', idPin = 0) {
    infoUserSensor[idIndex][idPin] = {};
    infoUserSensor[idIndex][idPin][idSensor] = {
        "name": nameSensor,
        "idSensor": idSensor,
        "userName": nameUser,
        "channels": [],
        "borne inferieure": -1,
        "borne supeieure": -1,
    };
}
function addToInfoUserI2C(idSensor, nameSensor, nameUser = '') {
    idIndex = 1
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
                for(let indexPin = 0; indexPin < 2; indexPin++){
                    if (Object.keys(info[indexPin]).length > 0) {
                        if (listAllSensors['DigiAnalog'][name]['is_display']) {} else {
                            json_sensor_push(info[indexPin], name);
                        }
                    } else {
                        alert('please configure all sensors');
                    }
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

loadPAge();