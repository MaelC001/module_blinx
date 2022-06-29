function _(el) {
    return document.getElementById(el);
}

let templatePopup = "\
<div class='form-popup' id='formConfigPopup'>\
    <form class='form-container'>\
            <label for='typeSensor'><b>Sensor Type</b></label>\
            <input type='text' name='typeSensor' value='$ValuePopup$' id='typeSensor' disabled>\
            <label for='nameSensor'><b>Name</b></label>\
            <input type='text' placeholder='Your name of the sensor' name='nameSensor' id='nameSensor'>\
            <div id='popupPlus'></div>\
        <button type='button' class='btn' onclick='saveConfig(\"$IdPortSensor$\")'>Saving</button>\
    </form>\
</div>";

let templateCardI2C = "\
<div class='card' id='$IdSensor$'>\
    <div class='content'>\
        <img class='right floated mini ui image' src='$ImageSensor$'>\
        <div class='header' id='$IdSensor$Name'>\
            $NameSensor$\
        </div>\
        <div class='meta'>\
            $UrlSensor$\
        </div>\
    </div>\
    <div class='extra content'>\
        <div class='ui two buttons'>\
            <div class='ui labeled green button icon config' data-position='right center' id='$IdSensor$Config'><i\
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
            "addr": "",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': '',
        },
        "humid-sht3x": {
            "text": "humidity (in micro controller)",
            "addr": "",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': '',
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



function loadSelectPort() {
    create_dic();
    listSensorsI2C = listSensors['I2C'];

    let textHTML = "";
    textHTML += "<div class='boutton'>\
    <div class='save'>\
        <button type='button' class='ui labeled icon button' class='btn' onclick='alert(\"to do\")''><i class='\
            icon settings'></i>Save Configuration</button>\
    </div>\
    <div class='wifi'>\
        <button type='button' class='ui labeled icon button' class='btn' onclick='alert(\"to do\")''><i class='\
            icon wifi'></i>Configure WiFi</button>\
    </div>\
</div>\
<div class='imageDiv'>\
    <img src='image.png' alt='image_of_micro_controller' class='ui centered image'>\
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
        <button type='button' class='ui labeled icon button config' data-position='right center' id='AnalogDigi1'><i\
                class='icon settings'></i>Config the sensor</button>\
    </div>\
</div>\
<div class='I2C'>\
    <div class='buttonI2C'>\
        I2C Port \
        <button type='button' class='ui labeled icon button scan' class='btn'><i class='icon fa-regular fa-magnifying-glass'></i>Scan I2C</button>\
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
    <div class='ui cards' id='listCardI2C'></div>\
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
        <button type='button' class='ui labeled icon button config' data-position='left center' id='AnalogDigi2'><i\
                class='icon settings'></i>Config the sensor</button>\
    </div>\
</div>";

    _("container").innerHTML = textHTML;

    $("#selectAnalogDigi1").dropdown();
    $('#selectI2C').dropdown({
        onChange: selectI2C,
    });
    $("#selectAnalogDigi2").dropdown();

    $('.ui.button.config').popup({
        on: 'click',
        exclusive: true,
        onShow: createPopup,
        html: '<i class="notched circle loading icon green"></i> wait...',
    });
    $('.ui.button.scan').popup({
        on: 'click',
        exclusive: true,
        onShow: scanI2C,
        html: '<i class="notched circle loading icon green"></i> wait...',
    });
}

function selectI2C(e) {
    let item;
    listSensorsI2C = listSensorsI2C.filter(removeItemI2C);

    let temp = templateCardI2C;
    temp = temp.replaceAll('$IdSensor$', item['value']);
    temp = temp.replaceAll('$NameSensor$', item['name']);
    temp = temp.replaceAll('$ImageSensor$', item['urlImage']);
    temp = temp.replaceAll('$UrlSensor$', item['url']);

    _('listCardI2C').innerHTML += temp

    changeSelectI2C();

    $('#'+e+'Config').popup({
        on: 'click',
        exclusive: true,
        onShow: createPopup,
        html: '<i class="notched circle loading icon green"></i> wait...',
    });

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
    changeSelectI2C();
}

function changeSelectI2C() {
    _('listSelectI2c').innerHTML = setOptionSelect(listSensorsI2C);
    $('#selectI2C').dropdown('refresh');
}

function scanI2C() {}

function createPopup(e) {
    let popup = this;
    let idItem = e.id;
    let temp = '<p>error</p>';
    let valueItem = ''
    if (idItem == 'AnalogDigi1' || idItem == 'AnalogDigi2') {
        valueItem = $('#select' + idItem).dropdown('get value');
    } else{
        idItem = idItem.substring(idItem.length-6,0);
        valueItem = _(idItem + 'Name').innerText
    }
    if (valueItem != '') {
        temp = templatePopup.replace('$IdPortSensor$', idItem);
        temp = temp.replace('$ValuePopup$', valueItem);
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
    for (var key1 in listAllSensors) {
        listSensors[key1] = [];
        for (var key2 in listAllSensors[key1]) {
            listSensors[key1].push({
                'value': key2,
                'name': listAllSensors[key1][key2]['text'],
                'urlImage': listAllSensors[key1][key2]['urlImage'],
                'ulr': listAllSensors[key1][key2]['url'],
            });
        }
    }
}

loadSelectPort();