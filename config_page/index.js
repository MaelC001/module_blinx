function strUcFirst(a) {
    return (a + '').charAt(0).toUpperCase() + a.substr(1);
}

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
let sensorInMicro = ['led', 'button', 'screen', 'temperature', 'humidity'];
let sensorInMicroPlus = ['light'];
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
            'numberPin': 1,
        },
    },
};

let listSensors = {};
let listSensorsI2C = [];
let listSensorsAD = [];
let pinListSensor = [
    [1, 2, ],
    [1, 2, ],
];
let listSensorsSelectAD = [
    ['', '', ],
    ['', '', ],
];
let sensorMicroController = [];
let infoUserSensor = [[{}, {},],
    {}, [{}, {},], {},
];