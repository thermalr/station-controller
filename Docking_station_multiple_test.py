import paho.mqtt.client as mqtt
import serial
import json
import RPi.GPIO as GPIO
import urllib.request
from urllib.error import HTTPError
from time import sleep
import threading


rs485_pin = 18

# creating list       
Dock_list = [] 
initial_start = True

#url_onRelease = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleUnlock?bicycleId=bike001"
#url_onError = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleUnlockError?bicycleId=bike001&statusCode=500"
#url2_onPark = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleLock?bicycleId=bike001"

url_onRelease = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleUnlock?bicycleId="
url_onError_p1 = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleUnlockError?bicycleId="
url_onError_p2 = "&statusCode=500"
url_onPark = "https://us-central1-ev-firestore-2019.cloudfunctions.net/onBicycleLock?bicycleId="

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(rs485_pin, GPIO.OUT)
GPIO.output(rs485_pin, GPIO.HIGH)

#b'{"bicycleId":"bike001","unlocking":true,"secretKey":251449}'
# added test comment

try:
    ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
    )
except:
    exit()

try:
    ser2 = serial.Serial ("/dev/ttyAMA0", 9600,timeout=1)    #Open port with baud rate
except:
    ser.write(b'page 6'+eof)
    ser.write(b't0.txt=\"'+b'serial_con_Er\"'+eof)
    exit()


    
class Dock:
    def __init__(self, dockID):
        self.dockID = dockID
        self.bikeID = 0
        self.bikein = False
        self.batlevel = 0 
        self.serverUpdated = False
        self.statusNow = False
        self.statusPre = False
        self.isDetected = False
        Dock_list.append(self)
    
    def check(self):
        print('check sent')
        ser2.write(self.dockID.encode())
        ser2.write(b'check')
        sleep(0.2)
        GPIO.output(rs485_pin, GPIO.LOW)
        sleep(0.3)
        
        print('reading started')
        
        global reply_data
        #for x in range(2):
            
        rece_data = ser2.readline()
        #recei = x.decode('utf8')
        reply_data = rece_data.decode('ISO-8859-1')
        print(rece_data)
        print(reply_data)
        print(reply_data.rstrip())
        print('reading finished')
        GPIO.output(rs485_pin, GPIO.HIGH)        
        print('out of for loop')
        
        formated = (reply_data.rstrip()).replace('\x00','')
        global bike_parked_check
        global initial_start
        
        if(formated == "bikeNo"):
            self.statusNow = False
            print('No bike available')
            if(self.bikein):
                self.bikein = False
            initial_start = False
                      
            
        elif  (formated[0:4] == "bike"):
            #self.statusNow = True
            
                
            
            if(~(self.bikein) & (self.isDetected == False)):
                self.bikein = True
                self.bikeID = formated[0:7]
                
                print('Bike parking detected')
                print("Bicycle ID: " + self.bikeID)
                self.batlevel = formated[8:10]
                print("Battery Level %: " + self.batlevel)
                self.isDetected = True
                
                               
                if(initial_start == True):
                    initial_start = False
                    
                else:
                    ser.write(b'page 8'+eof)
                    try:
                        handler = urllib.request.urlopen(url_onPark + self.bikeID)
                    except HTTPError as e:
                        content = e.read()
                        sleep(3)
                    ser.write(b'page 1'+eof)
                
            
            print('bike detected')
        elif  (rece_data == b'\x00'):
            print('No data received')
        sleep(1)    
        # if ((self.statusPre != self.statusNow) & (self.statusNow == True)):
            
                
        # self.statusPre = self.statusNow
    
    def unlock(self,userdata):
#try:
    
        timeout_flag = False
        timeout_count = 0
        invalid_attempts_flag = False
        invalid_attempts_count = 0

        y = json.loads(userdata.strip())
        get_PIN = True
        print('Enter PIN' + str(y["secretKey"]))
        #ser.write(b't0.txt=\"'+b'Enter\"'+eof)
        ser.write(b'page 2'+eof)
        password = str(y["secretKey"])
        while (get_PIN == True):
            #ser.write(b't0.txt=\"'+txt+eof)
            x=ser.readline()
            #recei = x.decode('utf8')
            recei = x.decode('ISO-8859-1')
            print(recei)
            
            if (recei==''):
                print('no input')
                timeout_count += 1
            
            elif (password == recei):
                ser.write(b'page 5'+eof)
                ser2.write(self.dockID.encode())
                ser2.write(b'unclock')
                print('unlocked')
                self.isDetected = False
                get_PIN = False
                sleep(1)            
                print('check sent')
                ser2.write(b'check')
                sleep(0.1)
                GPIO.output(rs485_pin, GPIO.LOW)
                sleep(0.5)
                
                print('reading started')
                
                global reply_data
                #for x in range(2):
                    
                rece_data = ser2.readline()
                #recei = x.decode('utf8')
                reply_data = rece_data.decode('ISO-8859-1')
                print(rece_data)
                print(reply_data)
                    
                    # if(rece_data != ''):
                        # print('break')
                        # x = 2
                print('reading finished')
                GPIO.output(rs485_pin, GPIO.HIGH)        
                print('out of for loop')
                            
                print(reply_data)
               
                
                #if((reply_data.strip()).replace('\x00','') == "bikeNo"):
                print('request GET')
                try:
                    handler = urllib.request.urlopen(url_onRelease + self.bikeID)
                    ser.write(b'page 3'+eof)
                    sleep(2)
                except HTTPError as e:
                    ser.write(b'page 4'+eof)
                    content = e.read()
                    
                    sleep(2)
                    
                else:
                    # do this if no exception occured
                    self.bikeID = 0
                    self.bikein = False
                    self.batlevel = 0 
                    
            else:
                invalid_attempts_count+= 1
                timeout_count = 0
                ser.write(b'page 7'+eof)
                sleep(2)
                ser.write(b'page 2'+eof)
            
            if (invalid_attempts_count >=3 ):
                ser.write(b'page 9'+eof)
                get_PIN = False
                
                try:
                    handler = urllib.request.urlopen(url_onError_p1 + self.bikeID + url_onError_p2)
                except HTTPError as e:
                    ser.write(b'page 4'+eof)
                    content = e.read()
                sleep(2)
                
            if (timeout_count >=30 ):
                ser.write(b'page 10'+eof)
                get_PIN = False
                
                try:
                    handler = urllib.request.urlopen(url_onError_p1 + self.bikeID + url_onError_p2)
                except HTTPError as e:
                    ser.write(b'page 4'+eof)
                    content = e.read()
                sleep(2)
                
            #print('reached end of while')
        print('reached end of 2nd thread')
        sleep(2)
        ser.write(b'page 1'+eof)
        
#---------------------------------------------------Define Docks------------------------------------------------
        
d1 = Dock("D01")
#d2 = Dock("D02")
#d3 = Dock("D03")


eof = b"\xff\xff\xff"
get_PIN = False

bike_parked = False
bike_parked_check = False


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic

    client.subscribe("ev/bikes")

class FifoList:
    def __init__(self):
        self.data = []
        self.lock = threading.Lock()
    def append(self, data):
        self.lock.acquire()
        print('append locked')
        self.data.append(data)
        self.lock.release()
        print('append unlocked')
    def pop(self):
        self.lock.acquire()
        print('pop locked')
        b = self.data.pop(0)
        self.lock.release()
        print('pop unlocked')
        return b
        
    def data_size(self):
        return (len(self.data))

#------------------------------------------------------------------------------------------------------------

def unlock_procress(data):

    y = json.loads(data.strip())
    BikeID_Received = str(y["bicycleId"])
    print('Bike ID' + BikeID_Received)
    
    for obj in Dock_list:
        if(obj.bikeID == BikeID_Received):
            obj.unlock(data)
            break
#-----------------------------------------------------------------------------------------------------------

def check_availability():
    
    for obj in Dock_list:
        obj.check()

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    a.append(msg.payload)
    
def main():
    while True:
        if a.data_size() > 0 :
            unlock_procress(a.pop())
        check_availability()
        # global bike_parked_check
        # global bike_parked
        # print("OLD")
        # print(bike_parked)
        # print("NEW")
        # print(bike_parked_check)
         
        
   
#except:
    #print("Something went wrong")

a = FifoList()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
    

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively

#client.connect("broker.hivemq.com", 1883, 60)
#client.username_pw_set(username="yqtfqiyd",password="WjPAP0wpFo_9")

try:
    #client.connect("soldier.cloudmqtt.com", 16367, 60)
    client.connect("broker.hivemq.com", 1883, 60)
except:
    ser.write(b'page 6'+eof)
    ser.write(b't0.txt=\"'+b'Client_con_Er\"'+eof)
    print("mqtt not connecting")
    exit()
#client.connect("soldier.cloudmqtt.com", 16367, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
def subscribing():

    client.on_message = on_message
    client.loop_forever()

sub=threading.Thread(target=subscribing)
pub=threading.Thread(target=main)

### Start MAIN ###

# print('Initial test')
# check_availability()
# print('done')

# bike_parked = bike_parked_check

ser.write(b'page 1'+eof)
print(bike_parked)
print(bike_parked_check)
sub.start()
pub.start()

