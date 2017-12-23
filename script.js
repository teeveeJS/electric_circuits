const counts = {
  "Resistor": 0,
  "DC_Battery": 0,
  "Light_Bulb": 0,
  "Junction": 0,
  "Voltmeter": 0,
  "Ammeter": 0,
  "Capacitor": 0,
  "Switch": 0,
  "Wire": 0
};
const properties = {
  //voltage, current, resistance, wattage, capacitance, inductance, state, num_cxns
  //[defaulValue, lowerBound, upperBound] bounds are inclusive
  //NOTE: bounds are checked by python (currently not used in JS at all)
  "Resistor": {"resistance": [5.0, 1e-6, 1e4]},
  "DC_Battery": {"voltage": [9.0, 1e-03, 1e4]},
  "Light_Bulb": {
                  "resistance": [5.0, 1e-6, 1e4],
                  "wattage": [16.2, 1e-6, 1e6]
                },
  "Junction": {"num_cxns": [3, 3, 4]},
  "Voltmeter": {},
  "Ammeter": {},
  "Capacitor": {
                  "voltage": [0.0, 1e-3, 1e3],
                  "capacitance": [10.0, 1e-3, 1e4]
                },
  "Switch": {"state": ["OFF", "ON", "OFF"]},
  "Wire": {}
};

let WIRECONNECTION = {"start": null, "end": null};

// let CANVAS = document.getElementById("sandbox");
// let CTX = CANVAS.getContext('2d');

// $(".comp").click(function(event) {
//   console.log(event.target + " was clicked");
//   addComponent(event);
// });

function addComponent(event) {
  let type = event.target.innerHTML;
  if (type === "Wire") {
    let sandbox = document.getElementById("sandbox");
    sandbox.style.cursor = "crosshair";

    for (let child of sandbox.childNodes) {
      child.addEventListener("click", addWire);
    }
  } else {
    let newComp = document.createElement("IMG");
    newComp.id = type + counts[type]++;
    newComp.className = type;

    newComp.style.position = "absolute";

    newComp.src = type + ".png";
    newComp.style.height = "50px";
    newComp.style.width = "50px";

    newComp.draggable = "true";

    //event listeners
    // newComp.addEventListener("click", selectComp);
    newComp.addEventListener("dblclick", editProperties);
    // newComp.addEventListener("drag", whileDragging);
    newComp.addEventListener("dragend", moveComp);

    document.getElementById("sandbox").appendChild(newComp);

    let comp_data = {"type": type};
    for (let key of Object.keys(properties[type])) {
      comp_data[key] = properties[type][key][0];
    };

    // sendJSON("newcomp?", JSON.stringify(comp_data)).close();
    $.get("newcomp?" + JSON.stringify(comp_data), function(data, status) {
      console.log(data + " " + status);
    });
  }
}


function addWire() {
  if (WIRECONNECTION['start'] === null) {
    WIRECONNECTION['start'] = event.target.id;
  } else if (WIRECONNECTION['end'] === null) {
    WIRECONNECTION['end'] = event.target.id;

    document.getElementById("sandbox").style.cursor = "auto";

    //draw the wire

    let wire_data = JSON.stringify(WIRECONNECTION);
    WIRECONNECTION['start'] = null;
    WIRECONNECTION['end'] = null;

    for (let child of document.getElementById("sandbox").childNodes) {
      child.removeEventListener("click", addWire);
    }

    // sendJSON("newwire?", wire_data).close();
    $.get("newwire?" + wire_data, function(data, status) {
      console.log(data + " " + status);
    });
  }
}


// function selectComp() {
//   //highlight the selected component
//   //show a little circle in the top-left corner where the user can drag the element
//   //the user should have a way to rotate the element
// }


function editProperties() {
  //stop event propagation?

  /*
  TODO:
  0. use <FORM> !!
  1. send a GET request to python server
  1.1. 'popup' will be opened in another .html file
  2. display connections
  3. allow the user to rotate the element



  */

  let popup = document.getElementById("popup");

  console.log(String(event.clientX) + " " + String(event.clientY));

  let props = properties[event.target.className];
  if (popup.style.visibility === "visible" ||
      Object.keys(props).length === 0 && props.constructor === Object) {
        // the popup is already open OR
        // the component has no properties that can be changed
        return 1;
  }

  let popuphead = document.createElement("DIV");
  popuphead.innerHTML = event.target.className;
  popuphead.style['font-weight'] = "bold";
  popuphead.style['text-align'] = "center";
  popup.appendChild(popuphead);

  for (let key of Object.keys(props)) {
    let propText = document.createElement("DIV");
    propText.innerHTML = key;
    propText.style['text-align'] = "center";
    propText.style.cursor = "help";
    propText.addEventListener("click", function() { getInfo(key) });

    let propInput = document.createElement("INPUT");
    propInput.className = "propInput";
    propInput.id = event.target.id + "|" + key;

    //instead of default values, propInputs should have the component's current values
    //requires GET with python
    propInput.value = props[key][0];

    propInput.style.width = "116px";

    popup.appendChild(propText);
    popup.appendChild(propInput);
  }

  let btn = document.createElement("BUTTON");
  btn.innerHTML = "Save Changes";
  btn.style.width = "120px";
  btn.addEventListener("click", submitProperties);
  popup.appendChild(btn);

  popup.style.visibility = "visible";

  return 0;
}


function whileDragging() {
  document.body.style.cursor = "none";
}


function moveComp() {
  let drag_comp = document.getElementById(event.target.id);

  // document.body.style.cursor = "auto";

  let mT = event.clientY - document.getElementById("sandbox").offsetTop;
  let mL = event.clientX - document.getElementById("sandbox").offsetLeft;
  drag_comp.style.marginTop = String(mT) + "px";
  drag_comp.style.marginLeft = String(mL) + "px";
}


function getInfo(prop) {
  //create a little window with info about bounds and units
}


function submitProperties() {
  let prop_data = {};

  for (let inp of document.getElementsByClassName("propInput")) {
    prop_data["name"] = inp.id.split("|")[0];

    let property = inp.id.split("|")[1];
    prop_data[property] = inp.value;
  }

  let popup = document.getElementById("popup");
  for (let child of popup.childNodes) {
    popup.removeChild(child);
  }
  popup.style.visibility = "hidden";

  // sendJSON("update?", JSON.stringify(data)).close();
  $.get("update?" + JSON.stringify(prop_data), function(data, status) {
    console.log(data + " " + status);
  });

  return 0;
}


function linedraw(ax, ay, bx, by) {
  /*
  credit for this function goes to Craig Taub on stackoverflow
  https://stackoverflow.com/questions/14560302/html-line-drawing-without-canvas-just-js
  */
  if (ay > by) {
    bx = ax + bx;
    ax = bx - ax;
    bx = bx - ax;
    by = ay + by;
    ay = by - ay;
    by = by - ay;
  }
  let calc = Math.atan((ay - by) / (bx - ax));
  calc = calc * 180 / Math.PI;
  let length = Math.sqrt((ax - bx) * (ax - bx) + (ay - by) * (ay - by));
  document.body.innerHTML += "<div id='line' style='height:" + length + "px;width:1px;background-color:black;position:absolute;top:" + (ay) + "px;left:" + (ax) + "px;transform:rotate(" + calc + "deg);-ms-transform:rotate(" + calc + "deg);transform-origin:0% 0%;-moz-transform:rotate(" + calc + "deg);-moz-transform-origin:0% 0%;-webkit-transform:rotate(" + calc  + "deg);-webkit-transform-origin:0% 0%;-o-transform:rotate(" + calc + "deg);-o-transform-origin:0% 0%;'></div>"
}


// function sendJSON(loc, JSONstr) {
//   let url = window.location.href + loc + JSONstr;
//   console.log(url);
//   let newWin = window.open(url, "_blank");
//   return newWin;
// }
