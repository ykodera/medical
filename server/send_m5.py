str = '''
import socket
import m5stack as m5
from machine import I2C, Pin
from mpu9250 import MPU9250

lcd = m5.lcd
lcd.clear()

address = ('192.168.24.10', 50000)
max_size = 1024

#print('Starting the client at', datetime.now())

i2c = I2C(scl=Pin(22), sda=Pin(21))
imu = MPU9250(i2c)

lcd.println("Starting the client at")
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lcd.print("socketOK")
c.connect(address)
lcd.print("connectOK")
while True:

    a = imu.acceleration
    x = str(a[0]).encode("UTF-8")
    y = str(a[1]).encode("UTF-8")
    z = str(a[2]).encode("UTF-8")
    data = b'm5,'+b'X:'+ x + b','+ b'Y:'+ y +b','+ b'Z:'+ z+b'\\n'
    c.send(data)
    if m5.buttonC.isPressed():
        break

lcd.print("finish")

c.close()
'''
f = open('main.py', 'w')
f.write(str)
f.close()
