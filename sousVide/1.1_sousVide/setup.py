#!/usr/bin/env python3

import time
import sys
import json
#from subprocess import Popen
from VideCrock import *

param = sys.argv[1]         # First argument: parameter to set
                            #   ["Temperature": set temperature (float)]
                            #   ["Kill": to kill (1) or not (0)]
value = sys.argv[2]         # Second argument: value

# Check for valid parameters and set value types
l_param_check = True

if (param == "Temperature"):
    value = float(value)

elif (param == "Kill"):
    value = int(value)

elif (param == "Kp" or param == "Ki" or param == "Kd"):
    value = float(value)

else:
    print("unknown parameter: "+param)
    l_param_check = False


# Update settings file
#setfilename = "settings.json"
if (l_param_check):
    try:
        settings = read_settings()
    except:
        settings = {}


    settings[param] = value


    #write out settings
    write_settings(settings)
    #with open(setfilename, "w") as f:
    #    f.write(json.dumps(settings))
