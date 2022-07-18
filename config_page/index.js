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
        "adxl345": {
            "text": "Three Axis Acceleration",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/4/42/Ks0012-.png",
            "url": "https://wiki.keyestudio.com/Ks0012_keyestudio_ADXL345_Three_Axis_Acceleration_Module",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "ht16k33": {
            "text": "I2C 8x8 LED Matrix",
            "addr": "",
            "file": "display",
            "is_input": false,
            "is_display": true,
            "urlImage": "https://wiki.keyestudio.com/images/4/40/Ks0064-%E5%9B%BE%E7%89%871.png",
            "url": "https://wiki.keyestudio.com/Ks0064_keyestudio_I2C_8x8_LED_Matrix_HT16K33",
            "config": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "motor_16_12": {
            "text": "16-channel 12-bit PWM/Servo Driver",
            "addr": "",
            "file": "",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/fa/Ks0065-1.png",
            "url": "https://wiki.keyestudio.com/Ks0065_keyestudio_16-channel_12-bit_PWM/Servo_Driver_-_I2C_Interface",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "mpu6050": {
            "text": "Gyroscope and Accelerometer module",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/8/80/Ks0170.png",
            "url": "https://wiki.keyestudio.com/Ks0170_keyestudio_MPU6050_Gyroscope_and_Accelerometer_module",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "apds9930": {
            "text": "Attitude Sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/5/57/KS0267--.png",
            "url": "https://wiki.keyestudio.com/Ks0267_keyestudio_APDS-9930_Attitude_Sensor_Module",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "apds9960": {
            "text": "motion detection",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "ssd1306_oled": {
            "text": "OLED Display OLED",
            "addr": "",
            "file": "display",
            "is_input": false,
            "is_display": true,
            "urlImage": "https://wiki.keyestudio.com/images/8/86/Ks0271-1.png",
            "url": "https://wiki.keyestudio.com/Ks0271_keyestudio_OLED_Display_OLED_Module",
            "config": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "bh1750fvi": {
            "text": "Digital Light Intensity",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/4/4c/KS0278.png",
            "url": "https://wiki.keyestudio.com/Ks0278_keyestudio_BH1750FVI_Digital_Light_Intensity_Module",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "bmp280": {
            "text": "temperature and air pressure sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/6/67/Ks0405.png",
            "url": "https://wiki.keyestudio.com/KS0405_Keyestudio_BMP280_Module_(Black_and_Eco-friendly)",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "ccs811": {
            "text": "Carbon Dioxide Air Quality",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/fc/0457%E5%9B%BE%E7%89%871.png",
            "url": "https://wiki.keyestudio.com/KS0457_keyestudio_CCS811_Carbon_Dioxide_Air_Quality_Sensor",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "bmp180": {
            "text": "Digital Barometric Pressure Sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/9/9c/KS0054_%284%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0054_keyestudio_BMP180_Digital_Barometric_Pressure_Sensor_Module_for_Arduino",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "ttp229l": {
            "text": "16-key Touch Sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/1/1d/KS0260.png",
            "url": "https://wiki.keyestudio.com/Ks0260_keyestudio_TTP229L_16-key_Touch_Sensor",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "mlx90614": {
            "text": "Non-contact Infrared Temperature Sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/5/53/Kso276.png",
            "url": "https://wiki.keyestudio.com/Ks0276_keyestudio_MLX90614_Non-contact_Infrared_Temperature_Sensor",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "tcs34725": {
            "text": "Color Sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/35/Ks0407-1.png",
            "url": "https://wiki.keyestudio.com/KS0407_Keyestudio_TCS34725_Color_Sensor",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "max30102": {
            "text": "Heart Rate Sensor",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/ff/Ks0462%E5%9B%BE%E7%89%871.png",
            "url": "https://wiki.keyestudio.com/KS0462_Keyestudio_MAX30102_Heart_Rate_Sensor",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "l76_l": {
            "text": "gps L76-L",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "mega8a": {
            "text": "joystick",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "mpu9150": {
            "text": "acceleration, turn rate and the magnetic field in three axes - MPU9150",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "ak8963": {
            "text": "acceleration, turn rate and the magnetic field in three axes - AK8963",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "mpu9250": {
            "text": "acceleration, turn rate and the magnetic field in three axes - MPU9250",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "mpu6500": {
            "text": "acceleration, turn rate and the magnetic field in three axes - MPU6500",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "diymall_96": {
            "text": "diymall 9.6 oled",
            "addr": "",
            "file": "display",
            "is_input": false,
            "is_display": true,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "gy521": {
            "text": "Accelerometer",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "pcf8523": {
            "text": "Real Time Clock",
            "addr": "",
            "file": "",
            "is_input": true,
            "is_display": false,
            "urlImage": "",
            "url": "",
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        }
    },
    "DigiAnalog": {
        "buzzer_digi": {
            "text": "Digital Buzzer",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/7/7d/KS0349_5-1.png",
            "url": "https://wiki.keyestudio.com/Ks0018_keyestudio_Digital_Buzzer_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "buzzer_passive": {
            "text": "Passive Buzzer",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/a/af/KS0019_%284%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0019_keyestudio_Passive_Buzzer_module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "relay_5v": {
            "text": "5V Relay",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/b/b0/Ks0011.png",
            "url": "https://wiki.keyestudio.com/Ks0011_keyestudio_5V_Relay_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "3w_led": {
            "text": "3W LED",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/7/75/KS0010_%284%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0010_keyestudio_3W_LED_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "white_led": {
            "text": "White LED",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/38/Ks0016-1.png",
            "url": "https://wiki.keyestudio.com/KS0016_Keyestudio_White_LED_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "red_led": {
            "text": "Red LED",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/4/4d/Ks0232-1.png",
            "url": "https://wiki.keyestudio.com/Ks0232_keyestudio_Red_LED_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "green_led": {
            "text": "Green LED",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/d/da/Ks0233-1.png",
            "url": "https://wiki.keyestudio.com/Ks0233_keyestudio_Green_LED_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "yellow_led": {
            "text": "Yellow LED",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/b/b2/Ks0234-1.png",
            "url": "https://wiki.keyestudio.com/Ks0234_keyestudio_Yellow_LED_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "blue_led": {
            "text": "Blue LED",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/ff/Ks0235-1.png",
            "url": "https://wiki.keyestudio.com/Ks0235_keyestudio_Blue_LED_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "sfe_reed_switch": {
            "text": "Hall Magnetic Sensor",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/d/db/KS0020_%282%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0020_keyestudio_Hall_Magnetic_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "reed_switch": {
            "text": "Reed Switch",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/8/86/Ks0038.png",
            "url": "https://wiki.keyestudio.com/Ks0038_keyestudio_Reed_Switch_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_2": {
            "text": "gas sensors - mq-2",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_3": {
            "text": "gas sensors - mq-3",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/2/23/KS0041_%283%29.png",
            "url": "https://wiki.keyestudio.com/Ks0041_keyestudio_Analog_Alcohol_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_4": {
            "text": "gas sensors - mq-4",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_5": {
            "text": "gas sensors - mq-5",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_6": {
            "text": "gas sensors - mq-6",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_7": {
            "text": "gas sensors - mq-7",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_8": {
            "text": "gas sensors - mq-8",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_9": {
            "text": "gas sensors - mq-9",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0040_keyestudio_Analog_Gas_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "mq_135": {
            "text": "gas sensors - mq-135",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/30/KS0040_%285%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0047_keyestudio_MQ135_Air_Quality_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "servo_9g": {
            "text": "9G Servo Motor Blue 90\\u00b0",
            "file": "analog",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/a/a4/Ks0209.png",
            "url": "https://wiki.keyestudio.com/Ks0209_keyestudio_9G_Servo_Motor_Blue_90%C2%B0",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "ad_key_button": {
            "text": "AD KEY Button Module",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/e/ee/Ks0466-1.png",
            "url": "https://wiki.keyestudio.com/KS0466_Keyestudio_AD_KEY_Button_Module(Black_and_Eco-friendly)",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "knock_sensor": {
            "text": "Knock Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/c/c9/Ks0024.png",
            "url": "https://wiki.keyestudio.com/Ks0024_keyestudio_Knock_Sensor_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "tilt": {
            "text": "Digital Tilt",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/2/29/KS0025_%283%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0025_keyestudio_Digital_Tilt_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "capacitive_touch": {
            "text": "Capacitive Touch",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/4/46/KS0031_%284%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0031_keyestudio_Capacitive_Touch_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "flame_sensor": {
            "text": "Flame Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/9/92/Ks0036.png",
            "url": "https://wiki.keyestudio.com/Ks0036_keyestudio_Flame_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "801s": {
            "text": "Vibration Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/f6/KS0037_%282%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0037_keyestudio_Vibration_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "infrared_obstacle": {
            "text": "Infrared Obstacle Avoidance Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/0/02/KS0051_obstacle_detector.png",
            "url": "https://wiki.keyestudio.com/Ks0051_keyestudio_Infrared_Obstacle_Avoidance_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "line_tracking": {
            "text": "Line Tracking Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/e/ea/KS0349_9-1.png",
            "url": "https://wiki.keyestudio.com/Ks0050_keyestudio_Line_Tracking_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "pir": {
            "text": "PIR Motion Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/a/a2/Ks0052_PIR_motion.png",
            "url": "https://wiki.keyestudio.com/Ks0052_keyestudio_PIR_Motion_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "xkc_y25_t12v": {
            "text": "Non-contact Liquid Level Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/4/4a/0346-1.png",
            "url": "https://wiki.keyestudio.com/KS0346_Keyestudio_Non-contact_Liquid_Level_Sensor(Black_and_Friendly)",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "dht11": {
            "text": "Temperature and Humidity Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/e/e9/%E6%97%A0%E6%A0%87%E9%A2%98-0034.png",
            "url": "https://wiki.keyestudio.com/Ks0034_keyestudio_DHT11_Temperature_and_Humidity_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "push_button": {
            "text": "Digital Push Button",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/e/ec/Ks0029-.png",
            "url": "https://wiki.keyestudio.com/Ks0029_keyestudio_Digital_Push_Button",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "collision_sensor": {
            "text": "Collision Sensor",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/2/20/211.png",
            "url": "https://wiki.keyestudio.com/Ks0021_keyestudio_Collision_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "slide_potentiometre": {
            "text": "Slide Potentiometer Module",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/a/a2/Ks0279_%E6%BB%91%E8%B0%83%E7%94%B5%E4%BD%8D%E5%99%A8.png",
            "url": "https://wiki.keyestudio.com/Ks0279_keyestudio_Slide_Potentiometer_Module_for_Arduino",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "pulse_rate": {
            "text": "Pulse Rate Monitor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/0/09/Ks0015-2.png",
            "url": "https://wiki.keyestudio.com/Ks0015_keyestudio_Pulse_Rate_Monitor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "lm35": {
            "text": "Linear Temperature",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/4/47/Ks0022-2.png",
            "url": "https://wiki.keyestudio.com/Ks0022_keyestudio_LM35_Linear_Temperature_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "photocell": {
            "text": "Photocell",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/0/0b/KS0028_%284%29.jpg",
            "url": "https://wiki.keyestudio.com/Ks0028_keyestudio_Photocell_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "analog_temperature": {
            "text": "Analog Temperature",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/2/22/Ks0033.png",
            "url": "https://wiki.keyestudio.com/Ks0033_keyestudio_Analog_Temperature_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "microphone": {
            "text": "Microphone Sound Sensor with Potentiometer",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/3/36/Ks0035%281%29.png",
            "url": "https://wiki.keyestudio.com/KS0035_Microphone_Sound_Sensor_with_Potentiometer",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "water_sensor": {
            "text": "Slide Potentiometer Module",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/c/c3/Ks0048%281%29.png",
            "url": "",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "soil_humidity": {
            "text": "Soil Humidity Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/f2/KS0049.jpg",
            "url": "https://wiki.keyestudio.com/Ks0049_keyestudio_Soil_Humidity_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "temt6000": {
            "text": "Ambient Light Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/6/60/KS0098.jpg",
            "url": "https://wiki.keyestudio.com/Ks0098_keyestudio_TEMT6000_Ambient_Light_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "steam_sensor": {
            "text": "Steam Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/c/c4/2031.png",
            "url": "https://wiki.keyestudio.com/Ks0203_keyestudio_Steam_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "guva_s12sd_3528": {
            "text": "Ultraviolet Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/9/9c/2041.png",
            "url": "https://wiki.keyestudio.com/Ks0273_keyestudio_GY-ML8511_Ultraviolet_Sensor_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "piezoelectric": {
            "text": "Analog Piezoelectric Ceramic Vibration Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/6/67/Ks0272-1-1.png",
            "url": "https://wiki.keyestudio.com/Ks0272_keyestudio_Analog_Piezoelectric_Ceramic_Vibration_Sensor",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "thin_film_pressure": {
            "text": "Thin-film Pressure Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/f/f0/KS0309.png",
            "url": "https://wiki.keyestudio.com/Ks0309_Keyestudio_Thin-film_Pressure_Sensor_(Black_and_Eco-friendly)",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "xd_58c": {
            "text": "Pulse Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/8/86/Ks0171.png",
            "url": "https://wiki.keyestudio.com/Ks0171_keyestudio_XD-58C_Pulse_Sensor_Module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "gy_ml8511": {
            "text": "Ultraviolet Sensor",
            "file": "analog",
            "is_input": true,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/e/ed/KS0273-.png",
            "url": "",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "vibration_motor": {
            "text": "Vibration Motor Module",
            "file": "analog",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/6/61/Ks0450-1.png",
            "url": "https://wiki.keyestudio.com/KS0450_Keyestudio_Vibration_Motor_Module_(Black_and_Eco-friendly)",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "l9110": {
            "text": "fan control",
            "file": "analog",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/0/03/Ks0168.png",
            "url": "https://wiki.keyestudio.com/Ks0168_keyestudio_L9110_fan_control_module",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        },
        "sg90s": {
            "text": "Micro Servo",
            "file": "analog",
            "is_input": false,
            "is_display": false,
            "urlImage": "https://wiki.keyestudio.com/images/b/be/Ks0194-_servo.png",
            "url": "https://wiki.keyestudio.com/Ks0194_keyestudio_Micro_Servo",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 0
                }
            ]
        }
    },
    "In": {
        "led": {
            "text": "led (in micro controller) (pin 2)",
            "file": "digital",
            "is_input": false,
            "is_display": false,
            "url": "",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": 2
                }
            ]
        },
        "button": {
            "text": "Button",
            "file": "digital",
            "is_input": true,
            "is_display": false,
            "url": "",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Digital",
                    "id": 0,
                    "pin": -1
                }
            ]
        },
        "ssd13006": {
            "text": "Screen",
            "file": "display",
            "is_input": false,
            "is_display": true,
            "url": "",
            "numberPin": 1,
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "sht3x_temp": {
            "text": "temperature sht3x",
            "file": "sht3x_temp",
            "is_input": true,
            "is_display": false,
            "url": "https://wiki.seeedstudio.com/Grove-I2C_High_Accuracy_Temp&Humi_Sensor-SHT35/",
            "numberPin": 1,
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "sht3x_humi": {
            "text": "humidity sht3x",
            "file": "sht3x_humi",
            "is_input": true,
            "is_display": false,
            "url": "https://wiki.seeedstudio.com/Grove-I2C_High_Accuracy_Temp&Humi_Sensor-SHT35/",
            "numberPin": 1,
            "channels": [
                {
                    "type": "I2C",
                    "id": 0
                }
            ]
        },
        "light": {
            "text": "light",
            "file": "light",
            "is_input": true,
            "is_display": false,
            "url": "",
            "numberPin": 1,
            "channels": [
                {
                    "type": "Analog",
                    "id": 0,
                    "pin": 1
                }
            ]
        }
    }
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