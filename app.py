import json
import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

cities = requests.get('http://127.0.0.1:1026/v2/entities?type=City').json()


@app.route('/')
def index():
    return render_template('index.html', cities=cities)


@app.route('/', methods=['POST'])
def get_city_data():
    city_id = request.form.get('city_id')
    city_data = requests.get(
        f'http://127.0.0.1:1026/v2/entities?type=City&id={city_id}').json()[0]
    coordinates = json.dumps(city_data['coordinates']['value'].split(' '))
    return render_template('index.html', cities=cities, data=city_data, coordinates=coordinates)


@app.route('/subscribe', methods=['POST'])
def publish():
    data = request.get_json()
    socketio.send(data, broadcast=True)
    return ('', 204)


@socketio.event
def connect():
    print('Client connected')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
