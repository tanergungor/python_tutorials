# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import random
import string
import json
from time import sleep
from random import uniform
 
connflag = False

 # func for making connection
def on_connect(client, userdata, flags, rc):
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc))

# Func for Sending msg
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str
    
def getMAC(interface='eth0'):
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]
def getEthName():
  # Get name of the Ethernet interface
  try:
    for root,dirs,files in os.walk('/sys/class/net'):
      for dir in dirs:
        if dir[:3]=='enx' or dir[:3]=='eth':
          interface=dir
  except:
    interface="None"
  return interface
 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

# mqttc object
mqttc = paho.Client()
# assign on_connect func
mqttc.on_connect = on_connect
# assign on_message func
mqttc.on_message = on_message
#mqttc.on_log = on_log

#### Change following parameters ####
# Endpoint
awshost   = "a383abyrkdwlua-ats.iot.us-east-1.amazonaws.com"
# Port No
awsport   = 8883
# Thing Name  
clientId  = "RaspberryPi"                                     
# Thing Name
thingName = "RaspberryPi"
# Root_CA_Certificate_Name
caPath    = "/workspaces/python_tutorials/iot/certificates/AmazonRootCA1.pem"
# <Thing_Name>.cert.pem
certPath  = "/workspaces/python_tutorials/iot/certificates/03fc1ec4579eb603098f80ecf2203f13eaebc19da97ddda0e321ba21a3b2f12b-certificate.pem.crt"
# <Thing_Name>.private.key
keyPath   = "/workspaces/python_tutorials/iot/certificates/03fc1ec4579eb603098f80ecf2203f13eaebc19da97ddda0e321ba21a3b2f12b-private.pem.key"
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
# connect to aws server
mqttc.connect(awshost, awsport, keepalive=60)

# Start the loop
mqttc.loop_start()
 
while 1 == 1:
    sleep(5)
    if connflag == True:
        ethName=getEthName()
        ethMAC=getMAC(ethName)
        macIdStr = ethMAC
        randomNumber = uniform(20.0,25.0)
        random_string= get_random_string(8)
        paylodmsg0="{"
        paylodmsg1 = "\"mac_id\": \""
        paylodmsg2 = "\", \"random_number\":"
        paylodmsg3 = ", \"random_string\": \""
        paylodmsg4="\"}"
        paylodmsg = "{} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, macIdStr, paylodmsg2, randomNumber, paylodmsg3, random_string, paylodmsg4)
        paylodmsg = json.dumps(paylodmsg) 
        paylodmsg_json = json.loads(paylodmsg)
        # topic: temperature # Publishing Temperature values
        mqttc.publish("RaspberryPiMessage", paylodmsg_json , qos=1)
        # Print sent temperature msg on console
        print("Message sent: RaspberryPiMessage" )
        print(paylodmsg_json)
    else:
        print("Waiting for connection...")
