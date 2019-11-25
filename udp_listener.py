import socket
import requests
import json
import os

# IP and Port Information
UDP_IP = "35.1.117.224"
UDP_PORT = 8080

# Setting up logic to listen in on port
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def max_normalize(val, old_max):
    """Convert values from between 0 and max to 0 and 100"""
    new_max = 100.0
    normalized = (val / old_max) * new_max
    # Cap at new_max
    if normalized > new_max:
        return new_max
    return normalized

def normalize_flow(flow):
    zero = 620
    return zero - flow  # change from decreasing with height to increasing.

def normalize_volume(vol):
    zero = 970
    return zero - vol

def step_function(vol):
    if vol <= 53:
        return 0
    elif vol < 76:
        return 40
    elif vol < 81:
        return 60
    elif vol >= 89:
        return 100
    else:
        return 80


# Parsing Data and Issuing Post Requests
while True:
    try:
        data = sock.recv(29) # buffer size is 1024 byte
        data = str(data[21::], 'utf-8')
        data = data.split(',')
        volume = normalize_volume(float(data[0]))
        flow_rate = normalize_flow(float(data[1].strip()))

        volume = max_normalize(volume, 645)
        # volume = step_function(volume)
        flow_rate = max_normalize(flow_rate, 300)
    except IndexError:
        continue
    except ValueError:
        continue

    url = 'http://ec2-3-14-152-39.us-east-2.compute.amazonaws.com/api/v1/reading'
    payload = {'volume': volume, 'flow': flow_rate}
    payload = json.dumps(payload)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers, verify=True)

    
    # print ("Current Volume: " + str(volume) + str(step_function(volume)) + ", Current Flow Rate: " + str(flow_rate))
    # print("Response: " + str(response))
    print("Current Volume:", str(step_function(volume)), str(volume))
