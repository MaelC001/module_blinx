

function config_sensor() {
    if (!scanI2C('a', boolPopup = false)) {
        alert('i2c not correct');
    } else {
        let json_config = [];
        let json_sensor = {};

        let portAD = [_('sensorsPort1').value, _('sensorsPort3').value];
        let portI2C = _('sensorsPort2').value;

        portAD.forEach(DigiAnalogFunction);
        let i = 0;

        function DigiAnalogFunction(name) {
            if (name != "" && name != "costum") {
                json_config_push(name, 'DigiAnalog');
                let info = infoUserSensor[i];
                for (let indexPin = 0; indexPin < 2; indexPin++) {
                    if (Object.keys(info[indexPin]).length > 0) {
                        if (listAllSensors['DigiAnalog'][name]['is_display']) {} else {
                            json_sensor_push(info[indexPin], name);
                        }
                    } else {
                        alert('please configure all sensors');
                    }
                }
                i = 2;
            }
        }

        portI2C.forEach(I2CFunction);

        function I2CFunction(name) {
            json_config_push(name, 'I2C');
            let infos = infoUserSensor[1];
            infos.forEach(setConfigJson);

            function setConfigJson(info) {
                if (Object.keys(info).length > 0) {
                    if (listAllSensors['I2C'][name]['is_display']) {} else {
                        json_sensor_push(info, name);
                    }
                } else {
                    alert('please configure all sensors');
                }
            }
        }

        config_sensor_serial(json_config, json_sensor);

        function json_config_push(name, type) {
            json_config.push({
                'name': name,
                'file': listAllSensors[type][name]['file'],
            });
        }

        function json_sensor_push(info, name) {
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors['DigiAnalog'][name]['is_input'],
                'is_display': listAllSensors['DigiAnalog'][name]['is_display'],
                'channels': info['channels'],
            }
        }

        function json_sensor_display_push(info, name) {
            json_sensor[info['name']] = {
                'new_name': info['userName'],
                'is_input': listAllSensors['DigiAnalog'][name]['is_input'],
                'is_display': listAllSensors['DigiAnalog'][name]['is_display'],
                'channels': info['channels'],
            }
        }
    }
}