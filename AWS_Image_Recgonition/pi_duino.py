#!/user/bin/env python
import serial
import sys
from time import sleep

port = "/dev/ttyUSB0"
s1 = serial.Serial(port,9600)

while True:
    mode = input('Write the mode(1~3) you want: ').lower()

    if mode == '1':
        print('Degree is 50L.')
        s1.write(b'deg0\n')
        sleep(3)
        s1.write(b'deg50\n')
        sleep(0.5)
    elif mode == '2':
        print('Degree is 110L.')
        s1.write(b'deg0\n')
        sleep(3)
        s1.write(b'deg110\n')
        sleep(0.5)
    elif mode == '3':
        print('Degree is 170L.')
        s1.write(b'deg0\n')
        sleep(3)
        s1.write(b'deg170\n')
        sleep(0.5)
    elif mode == '4':
        print('Degree is 50R.')
        s1.write(b'deg180\n')
        sleep(3)
        s1.write(b'deg50\n')
        sleep(0.5)
    elif mode == '5':
        print('Degree is 110R.')
        s1.write(b'deg180\n')
        sleep(3)
        s1.write(b'deg110\n')
        sleep(0.5)
    else:
        print('command error!')

    while s1.in_waiting:
        feedback = s1.readline().decode()
        print('reply: ',feedback)

