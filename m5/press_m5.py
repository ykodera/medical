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

pressL_id = 'pressL'
pressM_id = 'pressM'
lcd.println("presssenser!!")
lcd.println("Starting the client at")
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(address)
lcd.println('connect')
#pressL-35
#pressM-36

while True:
    time.sleep(0.04)
    pressL = machine.ADC(35)
    pressM = machine.ADC(36)

    pressL_ad = pressL.read()
    pressL_d = str(pressL_ad)

    pressM_ad = pressM.read()
    pressM_d = str(pressM_ad)

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
    pressL_data = Time + ',' + pressL_id + ',' + pressL_d +'\\n'
    pressM_data = Time + ',' + pressM_id + ',' + pressM_d +'\\n'

    c.send(pressL_data)
    c.send(pressM_data)

    if m5.buttonC.isPressed():
        break
c.close()
lcd.print("finish")
'''
f = open('main.py', 'w')
f.write(str)
f.close()

