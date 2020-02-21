#! /usr/bin/env pyhton3
import ambient
import time
import datetime
import re
from sense_hat import SenseHat

# chenge to your ID and Pass
AMBIENT_CHANNEL_ID = "YourID"
AMBIENT_WRITE_KEY = "YourPassword"

CHECK_SPAN = 30
sense = SenseHat()

if __name__ == '__main__':
    # create Ambient Object
    am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY)

    # main loop
    while True:
        accs = sense.get_accelerometer()
        # get acceleromener values
        acc_values = [round(x,2) for x in accs.values()]

        # create send data
        data = {
            'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'd1': round(sense.get_temperature(), 1),
            'd2': round(sense.get_humidity(), 1),
            'd3': round(sense.get_pressure(), 1),
            'd4': sense.get_compass(),
            'd5': acc_values[0],
            'd6': acc_values[1],
            'd7': acc_values[2]}
        # output data on Raspberry Pi
        print(data)
        # send data
        am.send(data)
        # wait time to next send timing
        time.sleep(CHECK_SPAN)
