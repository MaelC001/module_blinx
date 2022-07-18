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
            'channels': [{
                'type': 'I2C',
                'id': 0,
            }],
        },
        "humid-sht3x": {
            "text": "humidity (in micro controller)",
            "addr": "0x70",
            "file": "",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': 'https://wiki.seeedstudio.com/Grove-I2C_High_Accuracy_Temp&Humi_Sensor-SHT35/',
            'channels': [{
                'type': 'I2C',
                'id': 0,
            }],
        },
    },
    "DigiAnalog": {
        "buzzer_digi": {
            "text": "Digital Buzzer",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/7/7d/KS0349_5-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "buzzer_passive": {
            "text": "Passive Buzzer",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/a/af/KS0019_%284%29.jpg',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "relay_5v": {
            "text": "5V Relay",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/b/b0/Ks0011.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "servo_9g": {
            "text": "9G Servo Motor Blue 90°",
            "file": "pwm",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/a/a4/Ks0209.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Analog',
                'id': 0,
                'pin': 0,
            }],
        },
        "3w_led": {
            "text": "3W LED",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/7/75/KS0010_%284%29.jpg',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "white_led": {
            "text": "White LED",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/3/38/Ks0016-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "red_led": {
            "text": "Red LED",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/4/4d/Ks0232-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "green_led": {
            "text": "Green LED",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/d/da/Ks0233-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "yellow_led": {
            "text": "Yellow LED",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/b/b2/Ks0234-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "blue_led": {
            "text": "Blue LED",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/f/ff/Ks0235-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "SFE_Reed_Switch": {
            "text": "Hall Magnetic Sensor",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/d/db/KS0020_%282%29.jpg',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "Reed_Switch": {
            "text": "Reed Switch",
            "file": "digital",
            'is_input': true,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/8/86/Ks0038.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 0,
            }],
        },
        "AD_KEY_Button": {
            "text": "AD KEY Button Module",
            "file": "analog",
            'is_input': true,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/e/ee/Ks0466-1.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Analog',
                'id': 0,
                'pin': 0,
            }],
        },
        "knock_sensor": {
            "text": "Knock Sensor",
            "file": "analog",
            'is_input': true,
            'is_display': false,
            'urlImage': 'https://wiki.keyestudio.com/images/c/c9/Ks0024.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'analog',
                'id': 0,
                'pin': 0,
            }],
        },
    },
    "In": {
        "led": {
            "text": "led (in micro controller) (pin 2)",
            "file": "digital",
            'is_input': false,
            'is_display': false,
            'urlImage': 'http://icons.iconarchive.com/icons/icons8/ios7/512/Users-User-Male-icon.png',
            'url': '',
            'numberPin': 1,
            'channels': [{
                'type': 'Digital',
                'id': 0,
                'pin': 2,
            }],
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