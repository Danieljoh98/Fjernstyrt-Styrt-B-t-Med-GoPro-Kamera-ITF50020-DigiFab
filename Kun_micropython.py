import network
import socket
import time
from machine import Pin

right_motor = Pin(15, Pin.OUT)
left_motor = Pin(14, Pin.OUT)

ssid = 'MakerSpace'
password = '321drossap'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """


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
