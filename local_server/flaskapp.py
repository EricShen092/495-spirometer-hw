 #!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/v1/reading', methods=['POST'])
def send_reading():

    # data = request.json
    return "hello"


if __name__ == '__main__':
    app.run(debug=True)
