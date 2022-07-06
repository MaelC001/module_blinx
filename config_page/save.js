function config_sensor() {
    if (!scanI2C('a', boolPopup = false)) {
        alert('i2c not correct');
    } else {
        let json_config = [];
        let json_sensor = {};

        let portAD = infoUserSensor[0].concat(infoUserSensor[2]);
        let portI2C = infoUserSensor[1];
        let portSensors = infoUserSensor[3];

        let type = 'DigiAnalog';
        portAD.forEach(DigiAnalogFunction);

        type = 'I2C';
        portI2C.forEach(SensorFunction);

        portSensors.forEach(SensorInFunction);

        config_sensor_serial(json_config, json_sensor);

        function SensorFunction(info) {
            if (Object.keys(info).length > 0) {
                let val = info['value'];
                json_config_push(type, val);
                if (listAllSensors[type][val]['is_display']) {} else {
                    json_sensor_push(info);
                }
            }
        }

        function SensorInFunction(info){
            if (Object.keys(info).length > 0) {
                let val = info['value'];
                let type = info['type'];
                let t =  _(val+'Config').children[0];
                if (t.children.length == 2){
                    info['userName'] = t.children[0].children[0].value;
                } else{
                    info['userName'] = t.children[0].children[0].children[0].value;
                    info['borne inferieure'] = t.children[1].children[0].children[0].value;
                    info['borne supeieure'] = t.children[2].children[0].children[0].value;
                }
                json_config_push(type, val);
                if (val == 'screen') {} else {
                    json_sensor_push(info);
                }
            }
        }

        function json_config_push(type, name) {
            json_config.push({
                'name': name,
                'file': listAllSensors[type][name]['file'],
            });
        }

        function json_sensor_push(info) {
            let value = info['value'];
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors['DigiAnalog'][value]['is_input'],
                'is_display': listAllSensors['DigiAnalog'][value]['is_display'],
                'channels': info['channels'],
            }
        }

        function json_sensor_display_push(info) {
            let value = info['value'];
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors['DigiAnalog'][value]['is_input'],
                'is_display': listAllSensors['DigiAnalog'][value]['is_display'],
                'channels': info['channels'],
            }
        }
    }
}