#!/usr/bin/env python3

import time
import RPi.GPIO

crockPin = 17
dt = 10.0

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(crockPin, RPi.GPIO.OUT)


RPi.GPIO.output(crockPin, False)
print("Switching Off (pin no.", crockPin, ')')

