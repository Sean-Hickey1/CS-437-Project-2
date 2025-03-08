document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "172.20.20.10";   // the IP address of your Raspberry PI

const ws = new WebSocket("ws://localhost:8765");
const ws2 = new WebSocket("ws://localhost:8766");


function client(){

    console.log("HI")
    
    const net = require('net');
    var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    ws.send(e.keyCode.toString());

    console.log("COLORS")

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
    }
    else if (e.keyCode == '32') {
        // right (d)
        document.getElementById("stopBar").style.backgroundColor = "green";
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    document.getElementById("stopBar").style.backgroundColor = "grey";
}


// update data for every 50ms
ws2.onmessage = (event) => {
    console.log("Received data from server:", event.data);
    
    // Process the received data (for example, displaying it in the UI)
    // Assuming data is a string that can be shown in the console
    receivedData = event.data.split(',')
    
    // Use this data in your app, e.g., display it in an HTML element
    document.getElementById("temperature").innerText = receivedData[0]
    document.getElementById("battery").innerText = receivedData[1]
    document.getElementById("movement_state").innerText = receivedData[2]
};