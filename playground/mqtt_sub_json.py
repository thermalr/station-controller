import paho.mqtt.client as mqtt
import serial
import json
import RPi.GPIO as GPIO
import urllib.request

rs485_pin = 18

url = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleUnlock?bicycleId=bike001"


GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(rs485_pin, GPIO.OUT)
GPIO.output(rs485_pin, GPIO.HIGH)

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser2 = serial.Serial ("/dev/ttyAMA0", 9600)    #Open port with baud rate

eof = b"\xff\xff\xff"
get_PIN = False

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    #client.subscribe("thermalr/dock_1")
    client.subscribe("ev/bikes/bike001")

# the callback function, it will be triggered when receiving messages
#x =  '{ "bicycleId":"John", "unlocking":30, "secretKey":"New York"}'
def on_message(client, userdata, msg):
#try:
    y = json.loads((msg.payload).strip())
    get_PIN = True
    print(f"{msg.topic} {msg.payload}")
    print('Enter PIN' + str(y["secretKey"]))
    ser.write(b't0.txt=\"'+b'Enter\"'+eof)
    
    while (get_PIN == True):
        #ser.write(b't0.txt=\"'+txt+eof)
        x=ser.readline()
        #recei = x.decode('utf8')
        recei = x.decode('ISO-8859-1')
        print(recei)
        
        if (str(y["secretKey"]) == recei): 
            print('unlocked')
            get_PIN = False
            ser2.write(b'MAX')
            response = urllib.request.urlopen(url)
            print(response)

        
    ser.write(msg.payload)
#except:
    #print("Something went wrong")

    
     

client = mqtt.Client()
client.username_pw_set(username="yqtfqiyd",password="WjPAP0wpFo_9")
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
#client.connect("broker.hivemq.com", 1883, 60)
client.connect("soldier.cloudmqtt.com", 16367, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()