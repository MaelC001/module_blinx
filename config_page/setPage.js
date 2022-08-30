

function loadPAge() {
    create_dic();
    listSensorsI2C = listSensors['I2C'];
    listSensorsAD = listSensors['DigiAnalog'];

    let textHtml = templateGeneralPage;
    textHtml = textHtml.replaceAll('$htmlButtonGeneral$', getHtmlForButton());
    textHtml = textHtml.replaceAll('$htmlSensor$', getHtmlForSensor());
    _('container').innerHTML = textHtml;


    $("#selectAnalogDigi11").dropdown({
        onChange: changeSelectSensorAD,
        forceSelection: false,
    });
    $("#selectAnalogDigi12").dropdown({
        onChange: changeSelectSensorAD,
        forceSelection: false,
    });
    $("#selectAnalogDigi12").hide();
    $("#buttonAnalogDigi12").hide();

    $("#selectAnalogDigi21").dropdown({
        onChange: changeSelectSensorAD,
        forceSelection: false,
    });
    $("#selectAnalogDigi22").dropdown({
        onChange: changeSelectSensorAD,
        forceSelection: false,
    });
    $("#selectAnalogDigi22").hide();
    $("#buttonAnalogDigi22").hide();

    $('#selectI2C').dropdown({
        onChange: selectI2C,
        forceSelection: false,
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
        onShow: config_sensor,
        html: loader,
    });

    sensorInMicro.forEach(id => $("#" + id + "Config").hide());
    sensorInMicroPlus.forEach(id => $("#" + id + "Config").hide());


    connect(idError = 'error', callback = infoWifi);

    function getHtmlForButton() {
        let textHtmlTemp = '';
        infoButtonGeneral.forEach(info => {
            textHtmlTemp += loopDic(info, templateButtonGeneral);
        });
        return textHtmlTemp;
    }

    function getHtmlForSensor() {
        let textHtmlTemp = '';
        let indexAD = 0;
        numberOfPortAnalogDigi.forEach(info => {
            let temp = loopDic(info, templatePortAnlogDigi);
            temp = temp.replaceAll('$optionSelect1$', setOptionSelect(listSensorsAD, pinNumber = pinListSensor[indexAD], without = [], x = indexAD, y = 0)[0]);
            temp = temp.replaceAll('$optionSelect2$', setOptionSelect(listSensorsAD, pinNumber = pinListSensor[indexAD], without = [], x = indexAD, y = 1)[0]);
            textHtmlTemp += temp;
            indexAD += 1;
        });
        textHtmlTemp += '</div>';
        textHtmlTemp += templateImage;
        textHtmlTemp += '</div>';
        textHtmlTemp += templatePortI2C.replaceAll('$optionSelect$', setOptionSelect(listSensorsI2C)[0]);
        textHtmlTemp += '</div>';
        textHtmlTemp += '<div class="rowFlex">';
        sensorInMicro.forEach(id => {
            let t = listAllSensors['In'][id]['text'];
            let temp = templatePortSensorInMicro.replaceAll('$idSensor$', id);
            temp = temp.replaceAll('$SensorMaj$', strUcFirst(t));
            textHtmlTemp += temp;
        });
        sensorInMicroPlus.forEach(id => {
            let t = listAllSensors['In'][id]['text'];
            let temp = templatePortSensorInMicroMinMax.replaceAll('$idSensor$', id);
            temp = temp.replaceAll('$SensorMaj$', strUcFirst(t));
            textHtmlTemp += temp;
        });
        textHtmlTemp += '</div>';
        return textHtmlTemp;
    }

    function loopDic(dic, template) {
        let temp = template;
        for (let key in dic) {
            temp = temp.replaceAll('$' + key + '$', dic[key]);
        }
        return temp;
    }
}


function create_dic() {
    for (let key1 in listAllSensors) {
        listSensors[key1] = [];
        for (let key2 in listAllSensors[key1]) {
            let temp = -1;
            if ('numberPin' in listAllSensors[key1][key2]) {
                temp = listAllSensors[key1][key2]['numberPin'];
            }
            listSensors[key1].push({
                'value': key2,
                'name': listAllSensors[key1][key2]['text'],
                'urlImage': listAllSensors[key1][key2]['urlImage'],
                'url': listAllSensors[key1][key2]['url'],
                'pinNumber': temp,
            });
        }
    }
}

function setOptionSelect(arrayItem, pinNumber = [], without = [], x = 2, y = 2, item = '') {
    let tempText = '';
    let itemIn = false;
    arrayItem.forEach(e => {
        let val = e['value'];
        let pin = e['pinNumber'];
        if ((pin == -1 || pinNumber.includes(pin)) && !(without.includes(val))) {
            if (val == item){
                itemIn = true;
            }
            tempText += "<div class='item' data-text='" + e['name'] + "' data-value='" + val + "' data-selectSensor='"+ x +""+ y +"'><img class='ui image' src='" + e['urlImage'] + "' style='width:20px;'>" + e['name'] + "</div>";
        }
    });
    return [tempText, itemIn];
}



loadPAge();