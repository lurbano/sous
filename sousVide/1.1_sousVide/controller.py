#!/usr/bin/env python3

import sys
from subprocess import Popen
from VideCrock import *

def set_K(id):
    if (id == "Kp" or id == "Ki" or id == "Kd"):
        web_val = float(info[id])
        set_val = settings[id]

        if (web_val != set_val):
            print(str(web_val)+ "|"+str(set_val))
            print("SETTING "+id +" to "+ str(web_val))
            Popen([homedir+"setup.py", id, str(web_val)])


setP = Popen([homedir+"setup.py", "Kill", "0"])
settings = read_settings()
l_on = 0    # is the crockpot on?

for i in settings:
    print(i)

try:
    set_T = float(sys.argv[1])     # set temperature
except:
    set_T = settings["Temperature"]

setP = Popen([homedir+"setup.py", "Temperature", str(set_T)])

# compare web settings and program settings
info = read_web_settings()
print("Web settings:")
for i in info:
    print(i+ ": " + str(info[i]))

print("SET_T:" + str(info["set_T"]))


try:
    print("  Examining web settings:")
    print("a. "+str(float(info["set_T"])))
    web_set_T = float(info["set_T"])
    print("wet_set_T"+web_set_T)

    if (web_set_T != settings["Temperature"]):
        Popen([homedir+"setup.py", "Temperature", web_set_T])
        print(" Setting temperature to web_set_T")

except:
    info["set_T"] = settings["Temperature"]
    # for id in ["Kp", "Ki", "Kd"]:
    #     info[id] = settings[id]

for id in ["Kp", "Ki", "Kd"]:
    K = float(info[id])
    try:
        if (K != settings[id]):
            print("Setting "+id+" to web value")
            Popen([homedir+"setup.py", id, str(K)])
    except:
        Popen([homedir+"setup.py", id, str(K)])

info["runCrockpot"] = l_on
write_web_settings(info)


#run program
print("Starting program...")
#sousP = Popen(["./sous.py"])

while True:
    # check for Temperature check request (T_check)
    with open(webComFilename, "r") as f:
        info = json.load(f)

        # CHECK TEMPERATURE USING PROBE
        if (info["check"] != 0):
            T_now = Popen([homedir+"check_T.py"])

        # TURN CROCKPOT ON AND OFF
        if (info["runCrockpot"] == 1 and l_on == 0):
            l_on = 1
            Popen([homedir+"setup.py", "Kill", '0'])
            sousP = Popen([homedir+"sous.py"])
        if (info["runCrockpot"] == 0 and l_on == 1):
            l_on = 0
            Popen([homedir+"setup.py", "Kill", '1'])

        # SET TEMPERATURE
        web_set_T = float(info["set_T"])

        if (web_set_T != settings["Temperature"]):
            print("SETTING TEMPERATURE TARGET: "+str(web_set_T))
            Popen([homedir+"setup.py", "Temperature", str(web_set_T)])

        # SET PID coefficients (Kp, Ki, Kd)
        for id in ["Kp", "Ki", "Kd"]:
            set_K(id)

    # update settings
    settings = read_settings()
    time.sleep(1)


# sousP.kill()
#
# # turn off the relay
# print("")
# endP = Popen(["./off.py"])
# endP.wait(10)
#
# print("\nDone")
