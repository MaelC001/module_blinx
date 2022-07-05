function changeSelectSensorAD(value, text, element, booleanSelectOnChange = True){
    if(value != ''){
        let select;
        if (booleanSelectOnChange){
            select = element[0].attributes['data-selectsensor'].value;
        } else{
            select = element;
        }
        let x = parseInt(select.substring(0,1));
        let y = parseInt(select.substring(1,2));
        listSensorsSelectAD[x][y] = value;

        let id = 0;
        if (x == 1){
            id = 2;
        }
        findValue(el, id, pin = y);

        changeList();
        changeSelectAD();
    }


    function changeList(){
        listSensorsAD = [];
        listSensors['DigiAnalog'].forEach(info => {
            let value = info['info'];
            if (!listSensorsSelectAD[0].includes(value) && !listSensorsSelectAD[1].includes(value)){
                listSensorsAD.push(value);
            }
        });
    }

    function findValue(el, id, pin = 0){
        let item;
        listSensors['DigiAnalog'].forEach(getItem);

        addToInfoUserAD(id, item['value'], item['name'], nameUser = '', idPin = pin);

        function getItem(value) {
            if (value['value'] == el) {
                item = value;
            }
        }
    }
}

function changeSelectAD(){
    let idSelect = 'SelectAnalogDigi';
    let a = [0,1];
    for(let i = 1; i<=2; i++){
        for(let y = 1; y<=2; y++){
            let value = listSensorsSelectAD[i][y];
            let tempArray = listSensorsAD.concat([value]);
            let tempArrayWithout = []
            a.forEach(x2 => {
                a.forEach(y2 => {
                    if(x2 != i && y2 != y){
                        tempArrayWithout.push(listSensorsSelectAD[x2][y2]);
                    }
                });
            });
            let t = setOptionSelect(tempArray, pinNumber = pinListSensor[i], without = tempArrayWithout, x = i, y = y, item = value);
            _('list'+idSelect+i+y).innerHTML = t[0];
            $('#'+idSelect+i+y).dropdown('refresh');
            if (t[1]){
                $('#'+idSelect+i+y).dropdown('set selected', value);
            }
        }
    }
}




function customPort(check, port) {
    if (check.checked) {
        pinListSensor[parseInt(port)-1] = [1];
        $("#selectAnalogDigi" + port + "2").show();
    } else {
        pinListSensor[parseInt(port)-1] = [1, 2];
        $("#selectAnalogDigi" + port + "2").hide();
    }
    changeSelectAD();
}

function sensorInMicroConfig(check, id) {
    if (check.checked) {
        $("#" + id + "Config").show();
    } else {
        $("#" + id + "Config").hide();
    }
}


function selectI2C(e, text, $selectedItem) {
    if (e != '') {
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
    }

    function removeItemI2C(value) {
        if (value['value'] != e) {
            return true;
        } else {
            item = value;
            return false;
        }
    }
}

function changeSelectI2C() {
    _('listSelectI2c').innerHTML = setOptionSelect(listSensorsI2C)[0];
    $('#selectI2C').dropdown('refresh');
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

