import paho.mqtt.client as mqttClient
import time
import serial

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

#kodingan serial
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyUSB0'
ser.open()
 
Connected = False   #global variable for the state of the connection
INTERVAL=2
next_reading = time.time() 

broker_address= "m16.cloudmqtt.com"
port = 11595
user = "mzmrwolt"
password = "qZudSm2_ZFjy"
 
client = mqttClient.Client("armansyah")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
        getData = ser.readline()
        try:
            temperature = int(getData)
            client.publish("serial/temperature",temperature)
        except:
            continue

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
 
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()