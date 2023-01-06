import serial
import RPi.GPIO as GPIO
from time import sleep

rs485_pin = 18

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(rs485_pin, GPIO.OUT)
GPIO.output(rs485_pin, GPIO.HIGH)

ser2 = serial.Serial ("/dev/ttyAMA0", 9600,timeout=1)    #Open port with baud rate



global reply_data
#for x in range(2):

while(1):
    
    print('check sent')
    ser2.write(b'D01')
    ser2.write(b'check')
    sleep(0.2)
    GPIO.output(rs485_pin, GPIO.LOW)
    sleep(0.2)

    print('reading started')
    rece_data = ser2.readline()
    #recei = x.decode('utf8')
    reply_data = rece_data.decode('ISO-8859-1')
    print(rece_data)
    print(reply_data)
    print(reply_data.rstrip())
    print('reading finished')
    GPIO.output(rs485_pin, GPIO.HIGH)     
    sleep(0.2)    
    print('out of for loop')
    sleep(0.4)

formated = (reply_data.rstrip()).replace('\x00','')
global bike_parked_check
if(formated == "bikeNo"):
    bike_parked_check = False
    print('No bike available')
elif  (formated == "bikeIn"):
    bike_parked_check = True
    print('bike available')