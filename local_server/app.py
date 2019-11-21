#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

values = []

@app.route('/')
def index():
    return jsonify({'values': values})

@app.route('/api/v1/reading', methods=['GET'])
def get_reading():
    return jsonify({'values': values})

@app.route('/api/v1/reading', methods=['POST'])
def send_reading():

    data = request.json


    """
    Push single sensor value data point.

    Example:
    {
        "val": 1
    }
    """
    # if not request.json or not 'value' in request.json:
    #     flask.abort(400)
    # values.append(request.json['value'])
    return "hello"


if __name__ == '__main__':
    app.run(debug=True)
