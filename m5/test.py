str = '''
import m5stack as m5
lcd = m5.lcd
m5.lcd.println('Hello!', color=lcd.GREEN)
lcd
'''

f = open('main.py', 'w')
f.write(str)
f.close()
