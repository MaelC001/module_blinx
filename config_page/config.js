function _(el){
    return document.getElementById(el);
}

let rootCSS = document.querySelector(':root');

// number of port
let nmbPort = 3;
let infoUserSensor = [{}]*nmbPort;
// which port have i2c
let PortsI2C = [1];
// list of sensor for each different port
let listSensors = {
    "I2C" : [
        {
            "id" : "temp-sht3x",
            "text" : "temperature (in micro controller)",
        }, {
            "id" : "humid-sht3x",
            "text" : "humidity (in micro controller)",
        },
    ],
    "DigiAnalog" : [
        {
            "id" : "",
            "text" : "",
        }, {
            "id" : "led pin2",
            "text" : "led (in micro controller) (pin 2)",
        }, {
            "id" : "custom",
            "text" : "custom",
        }
    ],
};
let listPortAfficher = [0,0,0];

textPopup = "\
<div class='form-popup' id='myForm$IdPopupReplacement$'>\
    <form class='form-container'>\
        <div id='myFormSensor$IdPopupReplacement$'></div>\
        \
        <button type='button' class='btn' onclick='alert(\"TO DO\")'>Saving</button>\
        <button type='button' class='btn cancel' onclick='closeForm($IdPopupReplacement$)'>Close (without saving)</button>\
    </form>\
</div>\
";
textPopupName = "\
<label for='typeSensor'><b>Sensor Type</b></label>\
<input type='text' name='typeSensor' value='$TypePopupReplacement$' disabled>\
<label for='name_port$IdPopupReplacement$'><b>Name</b></label>\
<input type='text' placeholder='Your name of the sensor' name='name_port$IdPopupReplacement$' id='name_port$IdPopupReplacement$'>\
\
<div id='popupPlus$IdPopupReplacement$'></div>\
";
idPopup = [1, 2, 3];


function loadSelectPort(){
    // load the different element in the html page
    let htmlItem =  _("selectorPorts");
    let textHTML = '';
    // the information of the sensor on the micro controller
    textHTML += "<div class='grid-item itemOnMicro'>";
    textHTML += " <p>";
    textHTML += "     Led (PIN 2)<br>Sensor Humidity (SHT3x)<br>";
    textHTML += "     Sensor Temperature (SHT3x)<br>";
    textHTML += "     Display (small: SSD1306 | big: SH1107)";
    textHTML += " </p>";
    textHTML += "</div>";
    // the image
    textHTML += "<div class='grid-item itemImage'><img src='./image.png'></div>";
    for (let i = 0; i < nmbPort; i++) {
        let y = i+1;
        let nameResultID = "sensorsPort"+y;
        if(PortsI2C.includes(i)){
            // the sensor selector, for each port
            textHTML += "<div class='grid-item itemPortSensor"+y+"' id='div_"+nameResultID+"'>";
            textHTML += " <p>I2C Port</p>"
            textHTML += " <select class='singleSensorI2C' id='"+nameResultID+"'";
            textHTML += "     name='sensorsPort' onchange='changeSensor(\""+y+"\")'></select>";
            textHTML += " <button type='button' class='btn' onclick='alert(\"TO DO\")'>Scan I2C</button>";
            textHTML += " <button type='button' onclick='openForm("+y+")'> Config the sensor </button>";
            textHTML += "</div>";
        } else{
            // the sensor selector, for each port
            textHTML += "<div class='grid-item itemPortSensor"+y+"' id='div_"+nameResultID+"'>";
            textHTML += " <select class='singleSensor' id='"+nameResultID+"'";
            textHTML += "     name='sensorsPort' onchange='changeSensor(\""+y+"\")'></select>";
            textHTML += " <button type='button' onclick='openForm("+y+")'> Config the sensor </button>";
            textHTML += "</div>";
        }
    }

    textHTML += '<div id="listPopup">';
    idPopup.forEach( id => {
        textHTML += textPopup.replaceAll("$IdPopupReplacement$", id)
    });
    textHTML += '</div>';
    textHTML += '<div id="Save">';
    textHTML += " <button type='button' onclick='alert(\"To Do\")'>Save configuration</button>";
    textHTML += '</div>';

    htmlItem.innerHTML = textHTML;
    // change the selector to a select2, and put data on each select
    $(".singleSensor").select2({
        placeholder: "Select type sensor",
        data: listSensors['DigiAnalog'],
        width: '75%', // need to override the changed default
        templateResult: format,
        escapeMarkup: function (m) {
            return m;
        }
    });
    $(".singleSensorI2C").select2({
        placeholder: "Select type sensor",
        data: listSensors['I2C'],
        width: '75%', // need to override the changed default
        templateResult: format,
        multiple: true,
        escapeMarkup: function (m) {
            return m;
        }
    });
}

function changeSensor(port){
    value = _('sensorsPort'+port).value;
    let tempo = {
        "name" : value,
        "userName" : "",
        "port" : port,
        "borne inferieure" : -1,
        "borne supeieure" : -1,
    };
    infoUserSensor[port-1] = tempo;
}

function format(option) {
    console.log(option);
    if (!option.id || option.id == 'custom') {
        return option.text;
    }
    var ob = '<span class="spanSelector">' + option.text + '</span><br><img class="imgSelector" src="https://lh4.ggpht.com/wKrDLLmmxjfRG2-E-k5L5BUuHWpCOe4lWRF7oVs1Gzdn5e5yvr8fj-ORTlBF43U47yI=w64"/>';	// replace image source with option.img (available in JSON)
    return ob;
};

function openForm(y) {
    let types = $('#sensorsPort'+y).val();
    document.getElementById("myForm"+y).style.display = "block";
    if (typeof(types) == "string"){
        if(types == ""){
            closeForm(y);
        }
        else{
            let text = textPopupName.replaceAll("$IdPopupReplacement$", y);
            document.getElementById("myFormSensor"+y).innerHTML = text.replaceAll("$TypePopupReplacement$", types);
        }
    } else if (typeof(types) == "object"){
        if(types.length <= 0){
            closeForm(y);
        }
        else{
            let text = '';
            let number = 0;
            types.forEach(type => {
                let tempo = textPopupName.replaceAll("$IdPopupReplacement$", ''+y+number);
                text += tempo.replaceAll("$TypePopupReplacement$", type);
                number += 1;
            });
            document.getElementById("myFormSensor"+y).innerHTML = text;
        }
    }
}

function closeForm(y) {
    document.getElementById("myForm"+y).style.display = "none";
}

function saveConfigPort(port){}
function saveConfig(){
    console.log(infoUserSensor);
}




loadSelectPort();
