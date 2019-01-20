str = '''
import socket
import m5stack as m5
import machine
import time
import math

lcd = m5.lcd
lcd.clear()
num = 0

def printarea(a):
    if a > 240:
        a = 0
        lcd.clear()
    return a

address = ('192.168.24.10', 50000)
max_size = 1024

pulse_id = 'pulse'
lcd.println("pulsesencer")
lcd.println("Starting the client at")
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(address)
lcd.println('connect')
#pulse-35

while True:
    time.sleep(0.04)
    pulse = machine.ADC(35)


    pulse_ad = pulse.read()
    pulse_d = str(pulse_ad)

 
    # num = printarea(num)
    # lcd.println(x, 0, num, color = lcd.GREEN)
    #num += 15

    ms =time.time()
    integer = math.floor(ms)
    temp1=ms-integer
    temp2 = temp1*1000000
    msec=round(temp2)
    t = time.localtime()
    Time = time.strftime('%Y_%m_%d_%H:%M:%S.',t)+'{:06}'.format(msec)
    pulse_data = Time + ',' + pulse_id + ',' + pulse_d +'\\n'


    c.send(pulse_data)

    if m5.buttonC.isPressed():
        break
c.close()
lcd.print("finish")
'''
f = open('main.py', 'w')
f.write(str)
f.close()

