import serial

ser2 = serial.Serial("/dev/ttyAMA0", 9600,timeout=1)    #Open port with baud rate

while (True):
        #ser.write(b't0.txt=\"'+txt+eof)
        x=ser2.readline()
        #recei = x.decode('utf8')
        recei = x.decode('ISO-8859-1')
        print(recei)