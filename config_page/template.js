let templatePortAnlogDigi = "\
<div class='port$numberPort$ blocSensor' id='port$numberPort$'>\
    <div class='infoPort$numberPort$ infoPort'>\
        <div class='namePort$numberPort$'>\
            <p>Port Analogic/Digital</p><br>\
        </div>\
        <div class='actionPort$numberPort$'>\
            <div class='ui toggle checkbox'>\
                <input type='checkbox' name='public' onclick='customPort(this, $numberPortAD$)'>\
                <label>cable splitter</label>\
            </div><br>\
        </div>\
    </div>\
    <div class='selectPort$numberPort$1'>\
        <div class='ui fluid search selection dropdown selectAnalogDigi$numberPortAD$' id='selectAnalogDigi$numberPortAD$1'\
            name='selectAnalogDigi$numberPortAD$'>\
            <input type='hidden' name='sensorPort$numberPortAD$1'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor Analogic/Digital</div>\
            <div class='menu' id='listSelectAnalogDigi$numberPortAD$1'>\
            </div>\
        </div>\
    </div>\
    <div class='selectPort$numberPort$2'>\
        <div class='ui fluid search selection dropdown selectAnalogDigi$numberPortAD$' id='selectAnalogDigi$numberPortAD$2'\
            name='selectAnalogDigi$numberPortAD$'>\
            <input type='hidden' name='sensorPort$numberPortAD$2'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor Analogic/Digital</div>\
            <div class='menu' id='listSelectAnalogDigi$numberPortAD$2'>\
            </div>\
        </div>\
    </div>\
</div>";
let templatePortI2C = "\
<div class='port2 blocSensor' id='port2'>\
    <div class='infoPort2 infoPort'>\
        <div class='namePort2'>\
            <p>Port I2C</p><br>\
        </div>\
        <div class='actionPort2'>\
            <button type='button' class='ui labeled icon myBlue button scan'>\
                <i class='icon fa-regular fa-magnifying-glass'></i>\
                Scan I2C\
            </button><br>\
        </div>\
    </div>\
    <div class='selectPort2'>\
        <div class='ui fluid search selection dropdown' id='selectI2C' name='selectI2C'>\
            <input type='hidden' name='sensorPort1'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor I2C</div>\
            <div class='menu' id='listSelectI2c'>\
            </div>\
        </div>\
    </div>\
    <div class='listSensorPort2'></div>\
</div>";
let templatePortSensorInMicro = "\
<div class='$idSensor$ blocSensor' id='$idSensor$'>\
    <div class='buttonActivate$idSensorMaj$'>\
        <div class='ui toggle checkbox'>\
            <input type='checkbox' name='public' onclick='sensorInMicroConfig(this, \"$idSensor$\")'>\
            <label>$idSensorMaj$</label>\
        </div><br>\
    </div>\
    <div id='$idSensor$Config'>\
        <div class='action$idSensorMaj$'>\
            <div class='ui input'>\
                <input type='text' placeholder='Name for the sensor'>\
            </div><br>\
        </div>\
        <div class='info$idSensorMaj$'>\
            <p>Info</p><br>\
        </div>\
    </div>\
</div>";
let templateButtonGeneral = "\
<div class='$idButtonCourt$Button'>\
    <button type='button' class='ui labeled icon myBlue button' id='button$idButton$'>\
        <i class='icon $iconButton$'></i>\
        $textButton$\
    </button><br>\
</div>";
let templateGeneralPage = "\
    <div class='divImage'>\
        <img src='image_color.png' alt='image_of_micro_controller' class='ui centered image'>\
    </div>\
    <div class='general'>\
        $htmlButtonGeneral$\
        <div class='nameUser'>\
        </div>\
        <div class='infoWifi'>\
            <p>Info Wifi</p><br>\
        </div>\
        <div class='libre1'></div>\
        <div class='libre2'></div>\
    </div>\
    $htmlSensor$\
    <div class='error'></div>\
";