#!/usr/bin/env python3

import time
import RPi.GPIO
import sys
import json

from VideCrock import *


class crockPID:
    def __init__(self, T_set, dt, logfilename="T_log.txt"):
        # defaults
        self.Kp = -1.0
        self.Ki = 0.0
        self.Kd = -100.0

        web_settings = read_web_settings()
        self.Kp = web_settings["Kp"]
        self.Ki = web_settings["Ki"]
        self.Kd = web_settings["Kd"]


        self.T_set = T_set
        self.dt = dt

        self.T = read_temp()
        self.T_err = self.calc_err()
        self.time = 0.0

        self.startTime = time.strftime("%Y-%m-%d %H:%M")

        self.T_err_sum = self.T_err
        self.T_oldErr = self.T_err
        self.dT_err = 0.0
        self.pidVal = 0.0

        self.l_on = True

        self.p_term = 0.0
        self.i_term = 0.0
        self.d_term = 0.0

        self.logfilename = logfilename
        self.webLogFilename = webLogFilename
        self.webRecentFilename = webRecentFilename

        #self.logfile = open(logfilename, "w")
        print("Initializing crockPID.")
        print("    T_set = {T_set:.2f}".format(T_set=self.T_set))
        print("    Initial T = {T}".format(T=self.T))
        print()

        self.write_header()
        self.write_vals()

    def set_log_list(self):
        self.log_list = {"time":self.time,
                         "Temperature":self.T,
                         "T_set": self.T_set,
                         "Kp": self.Kp,
                         "Ki": self.Ki,
                         "Kd": self.Kd,
                         "T_error":self.T_err,
                         "T_err_sum": self.T_err_sum,
                         "dT_err":self.dT_err,
                         "p_term":self.p_term,
                         "i_term":self.i_term,
                         "d_term":self.d_term,
                         "pidVal":self.pidVal,
                         "l_on":self.l_on }

    def write_header(self):
        self.set_log_list()
        txt = ""
        for k, v in self.log_list.items():
            txt += k + ","
        txt += "Start="+self.startTime
        txt += '\n'
        with open(self.logfilename, "w") as f:
            f.write(txt)
        with open(self.webLogFilename, "w") as f:
            f.write(txt)

    def write_vals(self):
        self.set_log_list()
        txt = ""
        for k, v in self.log_list.items():
            txt += str(v) + ","
        txt = txt[:-1]+'\n'
        with open(self.logfilename, "a") as f:
            f.write(txt)
        with open(self.webLogFilename, "a") as f:
            f.write(txt)
        with open(self.webRecentFilename, "w") as f:
            f.write(json.dumps(self.log_list))

    def print_vals(self):
        self.set_log_list()
        txt = ""
        for k, v in self.log_list.items():
            txt += '{k}={v}, '.format(k=k, v=v)
        print(txt)

    def calc_err(self):
        return self.T - self.T_set

    def calc_PID(self, dt=0.0):

        self.T = read_temp()
        self.T_err = self.calc_err()
        self.T_err_sum += self.T_err
        self.dT_err = (self.T_err - self.T_oldErr) / self.dt
        self.time += self.dt

        self.p_term = self.Kp * self.T_err
        self.i_term = self.Ki * self.T_err_sum
        self.d_term = self.Kd * self.dT_err

        self.pidVal = self.p_term + self.i_term + self.d_term

        self.T_oldErr = self.T_err

        return self.pidVal

    def get_switch(self):

        self.pidVal = self.calc_PID()
        if self.pidVal > 0:
            self.l_on = True
        else:
            self.l_on = False

        self.write_vals()
        self.print_vals()

        return self.l_on


# def read_settings(inFile = "settings.json"):
#     with open(inFile, "r") as f:
#         settings = json.load(f)
#     return settings



settings = read_settings()
T_set = settings["Temperature"]

crockPin = 17

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(crockPin, RPi.GPIO.OUT)


#setup
dt = 10.0
fstartTime = time.strftime("%Y-%m-%d_%H-%M")
logfilename = "T_log_" + fstartTime + ".txt"
pid = crockPID(T_set = T_set, dt = dt, logfilename=logfilename)

#startTime = time.time()
#dt = 10.0
tm = 0.0
while True:
    if (pid.get_switch()):
        RPi.GPIO.output(crockPin, True)
    else:
        RPi.GPIO.output(crockPin, False)


    settings = read_settings()
    try:
        # check if we need to end program
        if (settings["Kill"] == 1):
            pid.l_on = False
            pid.write_vals()
            break

        # update any settings
        pid.T_set = settings["Temperature"]
        pid.Kp = settings["Kp"]
        pid.Ki = settings["Ki"]
        pid.Kd = settings["Kd"]
    except:
        break
    time.sleep(dt)
    tm += dt

# turn off relay
RPi.GPIO.output(crockPin, False)
print("Switching Off (pin no.", crockPin, ')')
