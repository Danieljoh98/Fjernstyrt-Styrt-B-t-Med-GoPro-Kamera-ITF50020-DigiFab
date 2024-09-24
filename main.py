import network
import socket
import time
from machine import Pin

right_motor = Pin(15, Pin.OUT)
left_motor = Pin(14, Pin.OUT)

ssid = 'MakerSpace'
password = 'Passord123'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>

<head>
    <title>Digifab Boat</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

        body {
            font-family: 'Arial', Courier;
            text-align: center;
            font-size: 20px;
        }

        .button {
            padding: 15px 25px;
            font-size: 20px;
            color: white;
            background-color: #4CAF50;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }

        .button:hover {
            background-color: #45a049;
        }

        .button:active {
            background-color: #3e8e41;
        }

        .red {
            background-color: #f44336;
        }

        .red:hover {
            background-color: #e53935;
        }

        .red:active {
            background-color: #d32f2f;
        }

        #icon-header {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            font-family: "Pacifico", cursive;
          font-weight: 400;
          font-style: normal;
        }

        #icon-header img {
            height: 8rem;
        }

        #icon-header h1 {
            font-size: 5rem;
        }

        .flipped-img {
            transform: scaleX(-1);
        }

        #test-buttons {
            margin-top: 100rem;
        }

        #gopro-box {
            display: flex;
            justify-content: center;
            width: 100%;
        }

        #livestream {
            width: 45%;
            height: 25rem;
            background-color: #cfebf7;
        }

        h3 {
            margin: 0;
            margin-bottom: 1rem
        }

        h1 {
            margin-top: 0;
        }

        #joystick {
            margin-top: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 1rem;
        }

        #bottom-row {
            display: flex;
            justify-content: center;
            gap: 9rem;
        }

        .control-button {
            width: 8rem;
            height: 8rem;
            font-weight: 700;
            background-color: #cfebf7;
            font-size: 1rem;
        }

        .control-button:hover {
            background-color: #bddfee;
        }

        .control-button:active {
            background-color: #eebdbd;
        }
        
        .active {
            background-color: #dfed81 !important;
        }

    </style>
    <script>
        function sendRequest(url) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", url, true);
            xhttp.send();
        }
        
        document.addEventListener('keydown', function(event) {
            if (event.code === 'ArrowLeft') {
                sendRequest('/right_motor/on');
                document.getElementById('left-button').classList.add('active');
            } else if (event.code === 'ArrowUp') {
                sendRequest('/both_motors/on');
                document.getElementById('forward-button').classList.add('active');
            } else if (event.code === 'ArrowRight') {
                sendRequest('/left_motor/on');
                document.getElementById('right-button').classList.add('active');
            }
        });

        document.addEventListener('keyup', function(event) {
            if (event.code === 'ArrowLeft') {
                sendRequest('/right_motor/off');
                document.getElementById('left-button').classList.remove('active');
            } else if (event.code === 'ArrowUp') {
                sendRequest('/both_motors/off');
                document.getElementById('forward-button').classList.remove('active');
            } else if (event.code === 'ArrowRight') {
                sendRequest('/left_motor/off');
                document.getElementById('right-button').classList.remove('active');
            }
        });
    </script>
</head>

<body>
    <div id="icon-header">
        <img src="https://i.imgur.com/9gJnMUw.png" />
        <h1>Digifab Boat</h1>
        <img src="https://i.imgur.com/9gJnMUw.png" class="flipped-img" />
    </div>

    <!--
    <h3>GoPro</h3>
    <div id="gopro-box">
        <div id="livestream">
            <h3>Livestream...</h3>
        </div>
    </div>
    -->

    <div id="joystick">
        <div id="top-row">
            <button id="forward-button" class="control-button" onmousedown="sendRequest('/both_motors/on')" onmouseup="sendRequest('/both_motors/off')">Forward</button>
        </div>
        <div id="bottom-row">
            <button id="left-button" class="control-button" onmousedown="sendRequest('/right_motor/on')" onmouseup="sendRequest('/right_motor/off')">Left</button>
            <button id="right-button" class="control-button" onmousedown="sendRequest('/left_motor/on')" onmouseup="sendRequest('/left_motor/off')">Right</button>
        </div>
    </div>

    <div id="test-buttons">
        <button class="button" onclick="sendRequest('/left_motor/on')">Turn right On</button>
        <button class="button red" onclick="sendRequest('/left_motor/off')">Turn right Off</button>
        <button class="button" onclick="sendRequest('/right_motor/on')">Turn left On</button>
        <button class="button red" onclick="sendRequest('/right_motor/off')">Turn left Off</button>
        <button class="button" onclick="sendRequest('/both_motors/on')">Turn both On</button>
        <button class="button red" onclick="sendRequest('/both_motors/off')">Turn both Off</button>
        <br><br>
        <button class="button" onmousedown="sendRequest('/left_motor/on')" onmouseup="sendRequest('/left_motor/off')">Hold to Turn
            right On</button>
        <button class="button" onmousedown="sendRequest('/right_motor/on')" onmouseup="sendRequest('/right_motor/off')">Hold to Turn
            left On</button>
        <button class="button" onmousedown="sendRequest('/both_motors/on')" onmouseup="sendRequest('/both_motors/off')">Hold to Turn
            both On</button>
    </div>
</body>

</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection faimotor')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        left_motor_on = request.find('/left_motor/on')
        left_motor_off = request.find('/left_motor/off')
        right_motor_on = request.find('/right_motor/on')
        right_motor_off = request.find('/right_motor/off')
        both_motors_on = request.find('/both_motors/on')
        both_motors_off = request.find('/both_motors/off')

        if left_motor_on != -1:
            print("left_motor on")
            left_motor.value(1)
            
        if left_motor_off != -1:
            print("left_motor off")
            left_motor.value(0)

        if right_motor_on != -1:
            print("right_motor on")
            right_motor.value(1)
            
        if right_motor_off != -1:
            print("right_motor off")
            right_motor.value(0)

        if both_motors_on != -1:
            print("both motors on")
            left_motor.value(1)
            right_motor.value(1)
            
        if both_motors_off != -1:
            print("both motors off")
            left_motor.value(0)
            right_motor.value(0)

        response = html

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except Exception as e:
        print('Error:', e)
        cl.close()
        print('connection closed')
