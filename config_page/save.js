function config_sensor(e) {
    if (false && !scanI2C('a', boolPopup = false)) {
        alert('i2c not correct');
    } else {
        let json_config = [];
        let json_sensor = {};

        let portAD = infoUserSensor[0].concat(infoUserSensor[2]);
        let portI2C = infoUserSensor[1];
        let portSensors = infoUserSensor[3];

        let type = '';

        if (Object.keys(portAD[0]).length > 0 || (Object.keys(portAD[1]).length > 0 && _('sensorSplitter1').checked) ||
            Object.keys(portAD[2]).length > 0 || (Object.keys(portAD[3]).length > 0 && _('sensorSplitter2').checked)) {
            type = 'DigiAnalog';
            portAD.forEach(dict => {
                for (let id in dict) {
                    SensorFunction(type, dict[id]);
                }
            });
        }

        if (Object.keys(portI2C).length > 0) {
            type = 'I2C';
            for (let id in portI2C) {
                SensorFunction(type, portI2C[id]);
            }
        }

        if (Object.keys(portSensors).length > 0) {
            for (let id in portSensors) {
                SensorInFunction(portSensors[id]);
            }
        }

        console.log(json_config);
        console.log(json_sensor);

        //config_sensor_serial(json_config, json_sensor);

        function SensorFunction(type, info) {
            if (Object.keys(info).length > 0) {
                let val = info['idSensor'];
                json_config_push(type, val);
                if (listAllSensors[type][val]['is_display']) {} else {
                    json_sensor_push(type, info);
                }
            }
        }

        function SensorInFunction(info) {
            if (Object.keys(info).length > 0) {
                let val = info['idSensor'];
                let type = info['type'];
                let t = _(val + 'Config').children[0];
                if (t.children.length == 2) {
                    info['userName'] = t.children[0].children[0].value;
                } else {
                    info['userName'] = t.children[0].children[0].children[0].value;
                    info['borne inferieure'] = t.children[1].children[0].children[0].value;
                    info['borne supeieure'] = t.children[2].children[0].children[0].value;
                }
                json_config_push('In', val);
                if (val == 'screen') {} else {
                    json_sensor_push('In', info);
                }
            }
        }

        function json_config_push(type, name) {
            json_config.push({
                'name': name,
                'file': listAllSensors[type][name]['file'],
            });
        }

        function json_sensor_push(type, info) {
            let value = info['idSensor'];
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors[type][value]['is_input'],
                'is_display': listAllSensors[type][value]['is_display'],
                'config': listAllSensors[type][value]['channels'],
            }
        }

        function json_sensor_display_push(type, info) {
            let value = info['value'];
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors[type][value]['is_input'],
                'is_display': listAllSensors[types][value]['is_display'],
                'config': listAllSensors[type][value]['channels'],
            }
        }
    }
}