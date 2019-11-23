#!flask/bin/python
from flask import Flask, jsonify, request
from random import seed
from random import randint

app = Flask(__name__)

current_values = []

@app.route('/')
def print_instructions():
    return "Spirometer-Hardware Group REST API"

@app.route('/api/v1/reading', methods=['GET'])
def get_reading():
    return jsonify({'values': current_values})

@app.route('/api/v1/reading', methods=['POST'])
def send_reading():

    seed(1)
    current_volume = randint(0, 3000)
    current_values.append(current_volume)
    current_flow = randint(0, 100)
    current_flow.append(current_flow)

    return "Success"


if __name__ == '__main__':
    app.run(debug=True)
