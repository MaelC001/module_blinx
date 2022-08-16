

function createPopup(e) {
    let popup = this;
    let idPort = e.id;
    let idItem;
    let urlItem;
    let type;
    let valueItem;
    let temp = '<p>error</p>';
    let l = idPort.length;
    if (idPort.substring(l-2,0) == 'buttonAnalogDigi') {
        idPort = idPort.substring(6, l);
        idItem = $('#select' + idPort).dropdown('get value');
        type = 'DigiAnalog';
    } else {
        idItem = idPort.substring(idPort.length - 6, 0);
        type = 'I2C';
    }
    if(idItem != ''){
        valueItem = listAllSensors[type][idItem]['text'];
        urlItem = listAllSensors[type][idItem]['url'];
        let popupPlus = '';
        let plusUrl = '';
        if(urlItem != ''){
            plusUrl = templatePopupPage.replaceAll('$UrlSensor$', urlItem);
        }
        if (listAllSensors[type][idItem]['min_max']){
            popupPlus = templateMinMaxPopup;
        }
        if (valueItem != '') {
            temp = templatePopup.replaceAll('$IdPortSensor$', idPort);
            temp = temp.replaceAll('$ValuePopup$', valueItem);
            temp = temp.replaceAll('$PLUSURL$', plusUrl);
            temp = temp.replaceAll('$PopupPlusInput$', popupPlus);
        }
        popup.html(temp);
    }
}


function savePopupConfig(idPort) {
    let idIndex;
    let nameSensor;
    let idSensor;
    let nameUser = _('nameSensor').value;
    let l = idPort.length;
    let idPin = parseInt(idPort[l-1])-1;
    if (idPort.substring(l-2,0) == 'AnalogDigi') {
        idSensor = $('#select' + idPort).dropdown('get value');
        nameSensor = listAllSensors['DigiAnalog'][idSensor]['text'];
        if (idPort[l-2] == '1'){
            idIndex = 0;
        } else{
            idIndex = 2;
        }

        let bornMin = -1;
        let bornMax = -1;
        if(listAllSensors['DigiAnalog'][idSensor]['min_max']){
            bornMin = _('minInputPopup').value;
            bornMax = _('maxInputPopup').value;
        }

        addToInfoUserAD(idIndex, idSensor, nameSensor, nameUser, idPin = idPin, min = bornMin, max = bornMax);
    } else {
        idSensor = idPort.substring(l - 6, 0);
        valueItem = listAllSensors['I2C'][idSensor]['text'];
        idIndex = 1;

        let bornMin = -1;
        let bornMax = -1;
        if(listAllSensors['I2C'][idSensor]['min_max']){
            bornMin = _('minInputPopup').value;
            bornMax = _('maxInputPopup').value;
        }

        addToInfoUserI2C(idSensor, nameSensor, nameUser, min = bornMin, max = bornMax);
    }
    $('.ui.button.config').popup('hide');
}


function connectWifi() {
    let ssid = _('ssid').value;
    let password = _('password').value;
    $('#buttonConnectWifi').popup('change content', loader);

    let method = 'wifi_connect';
    let arg = {
        'ssid': ssid,
        'password': password
    };
    let result = cmd(method, arg = arg, idCmd = 0).then(e => verify_json(e, j => {
        if(j['result'] == true){
            $('#buttonConnectWifi').popup('change content', '<p>success</p>');
        } else {
            $('#buttonConnectWifi').popup('change content', '<p>error : ' + j['result'] + '</p>');
        }
    }));
}