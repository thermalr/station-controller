import RPi.GPIO as GPIO
import time

lock_pin = 17
sens_pin = 4

time_delay = 5
time_lock = 0.5

GPIO.setmode(GPIO.BCM)

GPIO.setup(lock_pin,GPIO.OUT)
GPIO.setup(sens_pin,GPIO.IN)

while(True):
        if(GPIO.input(sens_pin)):
                print("locked")
        else:
                print("unlocked")
        GPIO.output(lock_pin,GPIO.HIGH)
        time.sleep(time_lock)
        GPIO.output(lock_pin,GPIO.LOW)
        time.sleep(time_delay)
