#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
from sense_hat import SenseHat
import os
import math

HTTP_PORT = int(os.environ.get('HTTP_PORT', '5000'))

app = Flask(__name__)
sense = SenseHat()
sense.set_imu_config(True, True, True)
sense.clear(0, 0, 0)
led_status = 0

@app.route('/environ')
def showEnviron():
    result = {
            'error': True,
            'results': {
                'humidity': None,
                'tempture': None,
                'pressure': None,
                'compass': None,
                'gyro': None,
                'leds': None
            },
     }

    try:
        global led_status
        result['results']['humidity'] = sense.get_humidity()
        result['results']['tempture'] = sense.get_temperature()
        result['results']['pressure'] = sense.get_pressure()
        result['results']['compass'] = math.ceil(sense.get_compass())
        result['results']['gyro'] = sense.get_gyroscope()
        result['results']['leds'] = led_status
        result['error'] = False

    except Exception as e:
        print(e)
        
    return jsonify(result)

@app.route('/led/<state>')
def leds(state):
    print(state)
    global led_status
    if state.lower() == 'on':
        led_status = 1
        sense.clear(255, 255, 255)
        return jsonify(result=True)
    
    print('////////////////')
    led_status = 0
    sense.clear(0, 0, 0)
    return jsonify(result=False)


@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=HTTP_PORT, threaded=True)
