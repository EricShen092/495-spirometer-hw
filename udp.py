import socket
import requests
import random
import json
import os
import re
# IP and Port Information
UDP_IP = "35.1.70.210"
UDP_PORT = 8080
# Setting up logic to listen in on port
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

NUM_INITIAL_VALS = 5
ZERO_VOL = 0
ZERO_FLOW = 0
initial_data = []

def max_normalize(val, old_max):
    """Convert values from between 0 and max to 0 and 100"""
    new_max = 100.0
    normalized = (val / old_max) * new_max
    # Cap at new_max
    if normalized > new_max:
        return new_max
    return normalized

def normalize_flow(flow):
    return_value = ZERO_FLOW - flow
    if return_value < 0:
        return 0
    elif return_value > 20:
        return 70
    else:
        return int((return_value * 3) + 10)

def normalize_volume(vol):
    return_value = ZERO_VOL - vol
    if return_value < 0: 
        return_value = 0
    elif return_value >= 250:
        return 2500
    return int(return_value * 10)


# Parsing Data and Issuing Post Requests
while True:
    try:
        data = sock.recv(29) # buffer size is 1024 byte
        print(data)
        vals = re.search('(\d+),(\d+)', str(data)).groups()
        volume_raw = int(vals[0])
        flow_raw = int(vals[1])
        if len(initial_data) < NUM_INITIAL_VALS:
            initial_data.append((volume_raw, flow_raw))
            continue
        elif len(initial_data) == NUM_INITIAL_VALS:
            ZERO_VOL = (sum([data[0] for data in initial_data]) / len(initial_data)) - 15
            ZERO_FLOW = (sum([data[1] for data in initial_data]) / len(initial_data)) - 2
            initial_data.append((None, None))
            continue
        volume = normalize_volume(volume_raw)
        flow_rate = normalize_flow(flow_raw)
    except IndexError:
        continue
    except ValueError:
        continue
    url = 'http://ec2-18-223-149-252.us-east-2.compute.amazonaws.com/api/v1/reading'
    payload = {'volume': volume, 'flow': flow_rate}
    payload = json.dumps(payload)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers, verify=True)
    # print ("Current Volume: " + str(volume) + str(step_function(volume)) + ", Current Flow Rate: " + str(flow_rate))
    print("Response: " + str(response))
    print("Current Volume:", str(volume), str(flow_rate))
