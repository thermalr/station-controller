# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:

rs485_pin = 18


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(rs485_pin, GPIO.OUT) # LED pin set as output


# Initial state for LEDs:
GPIO.output(rs485_pin, GPIO.HIGH)