from flask import Flask, jsonify, request
from random import seed
from random import randint

app = Flask(__name__)

current_values = [0, 0]

@app.route('/')
def print_instructions():
    return "Spirometer-Hardware Group REST API"

@app.route('/api/v1/reading', methods=['GET'])
def get_reading():
    return jsonify({'values': current_values})

@app.route('/api/v1/reading', methods=['POST'])
def send_reading():

    data = request.get_json()
    current_values[0] = data['volume']
    current_values[1] = data['flow']
    return "Success"


if __name__ == '__main__':
    app.run(debug=True)
