import paho.mqtt.client as paho
import os
import socket
import ssl


# making connection
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )                              # Subscribe to all topics


# receiving message
def on_message(client, userdata, msg):
    print("topic: " + msg.topic)
    print("payload: " + str(msg.payload))


#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))


# mqttc object
mqttc = paho.Client()
# assign on_connect func
mqttc.on_connect = on_connect
# assign on_message func
mqttc.on_message = on_message
#mqttc.on_log = on_log


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

# pass parameters
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# connect to aws server
mqttc.connect(awshost, awsport, keepalive=60)
# listen the publisher
mqttc.loop_forever() 