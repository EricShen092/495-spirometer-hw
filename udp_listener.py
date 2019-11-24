import socket
import requests
import json
import os

# IP and Port Information
UDP_IP = "35.2.87.43" 
UDP_PORT = 8080

# Setting up logic to listen in on port
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

# Parsing Data and Issuing Post Requests
while True:
    try:
        data = sock.recv(29) # buffer size is 1024 byte
        data = str(data[21::], 'utf-8')
        data = data.split(',')
        volume = data[0]
        flow_rate = data[1].strip()
    except: 
        continue

    url = 'http://ec2-3-14-152-39.us-east-2.compute.amazonaws.com/api/v1/reading'
    payload = {'volume': volume, 'flow': flow_rate}
    payload = json.dumps(payload)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data = payload, headers = headers, verify=True)

    
    print ("Current Volume: " + volume + ", Current Flow Rate: " + flow_rate )
    print("Response: " + str(response))
    