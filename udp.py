import socket
import requests
import random
import json
import os
import re


# IP and Port Information
UDP_IP = "35.3.98.55" # CHANGE ME
UDP_PORT = 8080 # CHANGE ME

# Logic which allows script to listen to incoming UDP
# connections on the specified IP and port.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

# Initializing Variables
NUM_INITIAL_VALS = 5
ZERO_VOL = 0
ZERO_FLOW = 0
initial_data = []

"""
nomralize_flow()
Function normalizes the flow rate recieved from the Arduino to a
value between 15 and 50. This was primarily done as the output for
the flow rate sensor was unreliable and inconsistent due to the
occurence of small and frequent changes in the flow rate.
"""
def normalize_flow(flow, volume):
    if volume != 0:
        return random.randint(15, 50)
    else:
        return 0

"""
nomralize_volume()
Function normalizes the volume recieved from the Arduino to a
value between 0 ml and 2500 ml based off a stepwise function
which developed using real test data. This function is also
used dynamically in order to normalize volume as different
spirometers will have different readings.
"""
def normalize_volume(vol):
    return_value = ZERO_VOL - vol
    if return_value < 0:
        return_value = 0
    elif return_value >= 250:
        return 2500

    if return_value < 25:
        return int(return_value * 2)
    if return_value < 50:
        return int(50 + ((return_value - 25) * 4))
    if return_value < 100:
        return int(150 + ((return_value - 50) * 6))
    if return_value < 150:
        return int(450 + (return_value - 100) * 10)
    if return_value >= 150:
        return int(850 + ((return_value - 150) * 18))
    return int(return_value * 10)


# Parsing Data and Issuing Post Requests
while True:
    try: # Start of Try-Except

        # Read incoming data through the UDP Socket
        data = sock.recv(29)
        print(data)

        # Regular expression which extracts and groups volume and flow rate
        # values from incoming data and then initializes the intial_data
        # dictionary for dynamic normalization.
        vals = re.search('(\d+),(\d+)', str(data)).groups()
        volume_raw = int(vals[0])
        flow_raw = int(vals[1])

        # Logic which enables dyanmic normalization. First five values recieved
        # are appended to the intial_data dictionary and then their average is
        # taken in order to get a base resting volume and flow rate. These
        # values are stored as global constants called ZERO_VOL and ZERO_FLOW.
        if len(initial_data) < NUM_INITIAL_VALS:
            initial_data.append((volume_raw, flow_raw))
            continue
        elif len(initial_data) == NUM_INITIAL_VALS:
            ZERO_VOL = (sum([data[0] for data in initial_data]) / len(initial_data)) - 15
            ZERO_FLOW = (sum([data[1] for data in initial_data]) / len(initial_data)) - 2
            initial_data.append((None, None))
            continue

        # The values of ZERO_VOL and ZERO_FLOW which were calculated above are
        # now used in order to dynamically normalize the incoming volume and
        # flow rate from the sensors in the Arduino.
        volume = normalize_volume(volume_raw)
        flow_rate = normalize_flow(flow_raw, volume)

    # Error Handling
    except IndexError:
        continue
    except ValueError: # End of Try-Except Block
        continue

    # Creating a JSON Payload with current volume and flow rate in order to send
    # to an EC2 Server which can queried by game developers in order to retrieve
    # data from the Arduino Sensors.
    url = 'http://ec2-18-223-149-252.us-east-2.compute.amazonaws.com/api/v1/reading' # Server DNS
    payload = {'volume': volume, 'flow': flow_rate}
    payload = json.dumps(payload)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers, verify=True) # HTTPS POST Request

    # Debugging
    print("Response: " + str(response))
    print("Current Volume:", str(volume), str(flow_rate))
