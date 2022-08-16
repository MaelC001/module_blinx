let tempSensorI2CAdd = [];

function scanI2C(e, boolPopup = true) {
    let popup = this;
    let tempJson;
    let method = "scan_i2c";
    return cmd(method, idCmd = 0).then(e => verify_json(e, verify));

    function verify(json) {
        tempJson = json;
        let values = _('sensorsPort' + port).value;
        values.filter(test);
        if (boolPopup) {
            let plus = recordI2C();
            let html = arrayToHtml(values, plus);
            popup.html(html);
        }
        return values;

        function test(name) {
            let addr = listAllSensors['I2C'][name]['addr'];
            let i = tempJson['result'].indexOf(addr);
            if (i !== -1) {
                tempJson['result'].splice(i, 1);
                return false;
            } else {
                return true;
            }
        }
    }

    function recordI2C() {
        let plus = [];
        if (tempJson['result'].length > 0) {
            for (let name in listAllSensors['I2C']) {
                let addr = listAllSensors['I2C'][name]['addr'];
                if (tempJson['result'].indexOf(addr) > -1 && sensorMicroController.indexOf(addr) == -1) {
                    plus.push(listAllSensors['I2C'][name]['text'])
                }
            }
        }
        return plus
    }

    function arrayToHtml(arrayError, arrayPlus) {
        let tempHtml = '';
        if (arrayError.length > 0) {
            tempHtml += '<p>You have sensors that are not (yet?) connected : ' + arrayError.toString('; ') + '</p>';
        }
        if (arrayPlus.length > 0) {
            tempSensorI2CAdd = arrayPlus;
            tempHtml += '<p>There are sensors that are connected to the microcontroller that you have not chosen: ' + arrayPlus.toString('; ') + '</p>';
            tempHtml += "<button type='button' class='ui labeled button'>Do you want to add them to your sensors?</button>";
        }
        if (tempHtml == '') {
            tempHtml += '<p>Nothing to report.</p>';
        }
        return tempHtml
    }
}
