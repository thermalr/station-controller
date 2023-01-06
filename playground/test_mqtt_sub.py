import paho.mqtt.client as mqtt
import serial
import RPi.GPIO as GPIO

rs485_pin = 18


GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(rs485_pin, GPIO.OUT)
GPIO.output(rs485_pin, GPIO.HIGH)



ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
#received_data = ser.read()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("ev/bikes/bike001")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    #ser.write(msg.payload) 

client = mqtt.Client()
#client.username_pw_set(username="yqtfqiyd",password="WjPAP0wpFo_9")
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
#client.connect("soldier.cloudmqtt.com", 16367, 60)
client.connect("broker.hivemq.com", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()