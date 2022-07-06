let templatePortAnlogDigi = "\
<div class='port$numberPort$ blocSensor' id='port$numberPort$'>\
    <div class='infoPort$numberPort$ infoPort'>\
        <div class='namePort$numberPort$'>\
            <p>Port Analogic/Digital</p><br>\
        </div>\
        <div class='actionPort$numberPort$'>\
            <div class='ui toggle checkbox'>\
                <input type='checkbox' name='public' onclick='customPort(this, $numberPortAD$)' id='sensorSplitter$numberPortAD$'>\
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
            $optionSelect1$\
            </div>\
        </div>\
        <button type='button' class='ui labeled icon myBlue button config fluid'' id='buttonAnalogDigi$numberPortAD$1'>\
            <i class='icon setting'></i>\
            Config the Sensor\
        </button><br>\
    </div>\
    <div class='selectPort$numberPort$2'>\
        <div class='ui fluid search selection dropdown selectAnalogDigi$numberPortAD$' id='selectAnalogDigi$numberPortAD$2'\
            name='selectAnalogDigi$numberPortAD$'>\
            <input type='hidden' name='sensorPort$numberPortAD$2'>\
            <i class='dropdown icon'></i>\
            <div class='default text'>Select type sensor Analogic/Digital</div>\
            <div class='menu' id='listSelectAnalogDigi$numberPortAD$2'>\
            $optionSelect2$\
            </div>\
        </div>\
        <button type='button' class='ui labeled icon myBlue button config fluid' id='buttonAnalogDigi$numberPortAD$2'>\
            <i class='icon setting'></i>\
            Config the Sensor\
        </button><br>\
    </div>\
</div>";
let templatePortI2C = "\
<div class='port2' id='port2'>\
    <div class='infoPort2 infoPort'>\
        <div class='namePort2'>\
            <p>Port I2C</p><br>\
        </div>\
        <div class='actionPort2'>\
            <button type='button' class='ui labeled icon myBlue button scan fluid'>\
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
            $optionSelect$\
            </div>\
        </div>\
    </div>\
    <div class='listSensorPort2' id='listCardI2C'></div>\
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
            <div class='ui mini input'>\
                <input type='text' placeholder='Name for the sensor'>\
            </div><br>\
        </div>\
        <div class='info$idSensorMaj$'>\
            <p>Info</p><br>\
        </div>\
    </div>\
</div>";
let templatePortSensorInMicroMinMax = "\
<div class='$idSensor$ blocSensor' id='$idSensor$'>\
    <div class='buttonActivate$idSensorMaj$'>\
        <div class='ui toggle checkbox'>\
            <input type='checkbox' name='public' onclick='sensorInMicroConfig(this, \"$idSensor$\")'>\
            <label>$idSensorMaj$</label>\
        </div><br>\
    </div>\
    <div id='$idSensor$Config'>\
        <div class='action$idSensorMaj$ blocSensor'>\
            <div class='nameInput$idSensorMaj$'>\
                <div class='ui mini input'>\
                    <input type='text' placeholder='Name for the sensor'>\
                </div><br>\
            </div>\
            <div class='minInput$idSensorMaj$'>\
                <div class='ui right labeled mini input'>\
                    <input type='text' placeholder='Min'>\
                    <a class='ui tag label'>\
                        Min\
                    </a>\
                </div><br>\
            </div>\
            <div class='maxInput$idSensorMaj$'>\
                <div class='ui right labeled mini input'>\
                    <input type='text' placeholder='Max'>\
                    <a class='ui tag label'>\
                        Max\
                    </a>\
                </div><br>\
            </div>\
        </div>\
        <div class='info$idSensorMaj$'>\
            <p>Info</p><br>\
        </div>\
    </div>\
</div>";
let templateButtonGeneral = "\
<div class='$idButtonCourt$Button'>\
    <button type='button' class='ui labeled icon myBlue button fluid' id='button$idButton$'>\
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
        <div class='infoWifi'>\
            <h3>Info Wifi:</h3>\
            <p>\
                <span id='wifiConnected'>NOT </span>Connected\
                <span id='wifiInfoConnected' style='display: none;'>\
                    </br>SSID: <span id='wifiSSID'></span>\
                    </br>IP: <span id='wifiIP'></span>\
                    </br>MDNS: <span id='wifiMDNS'></span>\
                </span>\
            </p>\
        </div>\
        <div class='libre1'></div>\
    </div>\
    $htmlSensor$\
    <div class='errorMessages' id='error'></div>\
";


let loader = '<i class="notched circle loading icon green"></i> wait...';

let templatePopupPage = "onclick='window.open(\"$UrlSensor$\",\"infoSensor\",\"height=500,width=800\");'";

let templatePopup = "\
<div class='form-popup' id='formConfigPopup'>\
    <form class='form-container'>\
            <div $PLUSURL$>\
                <label for='typeSensor' class='urlPopupLabel'><b>Sensor Type</b></label>\
                <input type='text' name='typeSensor' value='$ValuePopup$' id='typeSensor' class='urlPopup' disabled>\
            </div>\
            <label for='nameSensor'><b>Name</b></label>\
            <input type='text' placeholder='Your name of the sensor' name='nameSensor' class='modify' id='nameSensor'>\
            <div id='popupPlus'></div>\
        <button type='button' class='btn' onclick='savePopupConfig(\"$IdPortSensor$\")'>Saving</button>\
    </form>\
</div>";

let templatePopupWifi = "\
<div class='form-popup' id='formWifiPopup'>\
    <form class='form-container'>\
        <label for='ssid'><b>SSID</b></label>\
        <input type='text' placeholder='SSID wifi' name='ssid' class='modify' id='ssid'>\
        <label for='password'><b>Password</b></label>\
        <input type='password' placeholder='password wifi' name='password' class='modify' id='password'>\
        <button type='button' class='btn' onclick='connectWifi()'>Connect</button>\
    </form>\
</div>";

let templateCardI2C = "\
<div class='card' id='$IdSensor$'>\
    <div class='content'>\
        <img class='right floated mini ui image' src='$ImageSensor$'>\
        <div class='header'>\
            $NameSensor$\
        </div>\
        <div class='meta'>\
            <a href='$UrlSensor$' target='_blank'>info sensor</a>\
        </div>\
    </div>\
    <div class='extra content'>\
        <div class='ui two buttons'>\
            <div class='ui labeled myBlue button icon config' data-position='right center' id='$IdSensor$Config'><i\
            class='icon settings'></i>Config the sensor</div>\
            <div class='ui labeled red button icon' onclick='removeI2C(\"$IdSensor$\")'><i class='trash icon'></i>Remove</div>\
        </div>\
    </div>\
</div>";