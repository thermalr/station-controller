#!/usr/bin/env python
import time
import serial
import struct

flag = 0
#Set end of file
eof = b"\xff\xff\xff"
txt = b'Send\"'

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while 1:
        print('loop')
        ser.write(b't0.txt=\"'+txt+eof)
        time.sleep(1);
        
        while (flag==0):
            #ser.write(b't0.txt=\"'+txt+eof)
            x=ser.readline()
            passw = '233'
            recei = x.decode('utf8')
            if (recei == passw): 
                print('unlocked')
                flag = 1
                ser.write(b't0.txt=\"'+b'ThermalR\"'+eof)
            print(recei)
