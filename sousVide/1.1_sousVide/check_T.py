#!/usr/bin/env python3

import time
import RPi.GPIO
from VideCrock import *



crockPin = 17

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(crockPin, RPi.GPIO.OUT)


T = read_temp()
tm = time.strftime("%Y-%m-%d %H:%M:%S")

#T_check = {"Temperature": T, "time": tm, "check":0}
#write data for webpage to read
with open(webComFilename, "r") as f:
    info = json.load(f)
    info["Temperature"] = T
    info["time"] = tm
    info["check"] = 0
with open(webComFilename, "w") as f:
    f.write(json.dumps(info))
#write data confirming check
# with open(webTsetFilename, "w") as f:
#     f.write(json.dumps(T_check))
print(T)
