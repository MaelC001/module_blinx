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

function loadPAge() {
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
    /*
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
    */

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
            textHtmlTemp += loopDic(info, templatePortAnlogDigi);
        });
        textHtmlTemp += templatePortI2C;
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

loadPAge();