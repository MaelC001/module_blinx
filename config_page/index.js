// https://cmsdk.com/css3/how-to-connect-html-divs-with-lines-duplicate.html

function adjustLine(from, positionF, to, positionT, line) {
    let fT = from.offsetTop;
    let fH = from.offsetWidth;
    let fL = from.offsetLeft;
    let fW = from.offsetHeight;
    let tL = to.offsetLeft;
    let tW = to.offsetHeight;
    let tT = to.offsetTop;
    let tH = to.offsetWidth;

    let listPositionFrom = [
        [fT, fL],
        [fT, fL + fW / 2],
        [fT, fL + fW],
        [fT + fH / 2, fL],
        [fT + fH / 2, fL + fW / 2],
        [fT + fH / 2, fL + fW],
        [fT + fH, fL],
        [fT + fH, fL + fW / 2],
        [fT + fH, fL + fW],
    ];
    let listPositionTo = [
        [tT, tL],
        [tT, tL + tW / 2],
        [tT, tL + tW],
        [tT + tH / 2, tL],
        [tT + tH / 2, tL + tW / 2],
        [tT + tH / 2, tL + tW],
        [tT + tH, tL],
        [tT + tH, tL + tW / 2],
        [tT + tH, tL + tW],
    ];

    fT = listPositionFrom[positionF][0];
    fL = listPositionFrom[positionF][1];
    if(positionT!=10){
        tT = listPositionTo[positionT][0];
        tL = listPositionTo[positionT][1];
    } else{
        tT = tT + tH / 4;
        tL = tL;
    }

    var CA = Math.abs(tT - fT);
    var CO = Math.abs(tL - fL);
    var H = Math.sqrt(CA * CA + CO * CO);
    var ANG = 180 / Math.PI * Math.acos(CA / H);
    let top, left;

    if (tT > fT) {
        top = (tT - fT) / 2 + fT;
    } else {
        top = (fT - tT) / 2 + tT;
    }
    if (tL > fL) {
        left = (tL - fL) / 2 + fL;
    } else {
        left = (fL - tL) / 2 + tL;
    }

    if ((fT < tT && fL < tL) || (tT < fT && tL < fL) || (fT > tT && fL > tL) || (tT > fT && tL > fL)) {
        ANG *= -1;
    }
    top -= H / 2;

    let textAng = 'rotate(' + ANG + 'deg)';

    line.style["-webkit-transform"] = textAng;
    line.style["-moz-transform"] = textAng;
    line.style["-ms-transform"] = textAng;
    line.style["-o-transform"] = textAng;
    line.style["-transform"] = textAng;
    line.style.top = top + 'px';
    line.style.left = left + 'px';
    line.style.height = H + 'px';
}
adjustLine(
    document.getElementById('p1Arrow'),
    2,
    document.getElementById('port1'),
    10,
    document.getElementById('line1')
);
adjustLine(
    document.getElementById('p2Arrow'),
    2,
    document.getElementById('port2'),
    10,
    document.getElementById('line2')
);
adjustLine(
    document.getElementById('p3Arrow'),
    2,
    document.getElementById('port3'),
    10,
    document.getElementById('line3')
);
adjustLine(
    document.getElementById('ledArrow'),
    4,
    document.getElementById('blueLed'),
    0,
    document.getElementById('line4')
);
adjustLine(
    document.getElementById('buttonArrow'),
    5,
    document.getElementById('button'),
    1,
    document.getElementById('line5')
);
adjustLine(
    document.getElementById('screenArrow'),
    4,
    document.getElementById('screen'),
    0,
    document.getElementById('line6')
);