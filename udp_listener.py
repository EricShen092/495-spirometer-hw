import socket
import requests
import os

# IP and Port Information
UDP_IP = "35.3.49.165"
UDP_PORT = 8080

# Setting up logic to listen in on port
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

# Parsing Data and Issuing Post Requests
while True:
    data = sock.recv(28) # buffer size is 1024 byte
    data = str(data[21::], 'utf-8')
    data = data.split(',')
    volume = data[0]
    flow_rate = data[1]

    url = 'http://localhost:5000/api/v1/reading'
    payload = {'volume': volume, 'flow': flow_rate}
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    response = requests.post(url, data=payload, headers=headers)

    
    print ("Current Volume: " + volume + ", Current Flow Rate: " + flow_rate )
    print("Response: " + str(response))
    