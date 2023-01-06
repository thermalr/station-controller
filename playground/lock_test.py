# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
lockPin = 23 # Broadcom pin 23 (P1 pin 16)
statusPin = 17 # Broadcom pin 17 (P1 pin 11)
rs485_pin = 18

unlock_flag = 0


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(lockPin, GPIO.OUT) # LED pin set as output

GPIO.setup(statusPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(lockPin, GPIO.HIGH)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        #print("outer while loop")
        lock_status = GPIO.input(statusPin)
        #print(lock_status)
        if not(lock_status): 
            #print(GPIO.input(statusPin))
            time.sleep(1)
            if (unlock_flag == 0):
                print("Unlocked..")
                unlock_flag = 1
        else: # button is pressed:
            unlock_flag = 0
            while lock_status:
                val = input("Enter password to unlock: ")
                print(val)
                if (val=="1234"):
                    GPIO.output(lockPin, GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(lockPin, GPIO.HIGH)
                    #print(GPIO.input(statusPin))
                    lock_status = 0 
                    time.sleep(1)
                else:
                    print("Wrong password. Please try again..")
                    #print(GPIO.input(statusPin))
                    
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
