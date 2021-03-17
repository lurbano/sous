#!/usr/bin/env python3

import glob
import time
import RPi.GPIO
import sys

from subprocess import Popen

def read_temp():
    l_yes = False
    while (not l_yes):
        with open(device_file) as f:
            lns = f.readlines()
            if (lns[0].strip()[-3:] == 'YES'):
                l_yes = True
                equals_pos = lns[1].find('t=')
                if equals_pos != -1:
                    T_str = lns[1][equals_pos+2:]
                    T_C = float(T_str) / 1000.0
            #print(lns[0])
            #print(lns[1])
        time.sleep(0.25)
    return T_C


class crockPID:
    def __init__(self, T_set, dt, logfilename="T_log.txt"):
        self.Kp = -1.0
        self.Ki = 0.0
        self.Kd = -100.0

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

        self.logfile = open(logfilename, "w")
        print("Initializing crockPID.")
        print("    T_set = {T_set:.2f}".format(T_set=self.T_set))
        print("    Initial T = {T}".format(T=self.T))
        print()

        self.write_header()
        self.write_vals()

    def set_log_list(self):
        self.log_list = {"time":self.time/60.0,
                         "Temperature":self.T,
                         "T_set": self.T_set,
                         "T_error":self.T_err,
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
        self.logfile.write(txt)

    def write_vals(self):
        self.set_log_list()
        txt = ""
        for k, v in self.log_list.items():
            txt += str(v) + ","
        txt = txt[:-1]+'\n'
        self.logfile.write(txt)

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

    def close(self):
        self.logfile.close()







crockPin = 17
T_set = float(sys.argv[1])

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(crockPin, RPi.GPIO.OUT)

Popen(['modprobe', 'w1-gpio'])
Popen(['modprobe', 'w1-therm'])

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
#print(device_file)

#setup
dt = 10.0
startTime = time.strftime("%Y-%m-%d_%H-%M")
logfilename = "T_log_" + startTime + ".txt"
pid = crockPID(T_set = T_set, dt = dt, logfilename=logfilename)


#dt = 10.0
tm = 0.0
while True:
    if (pid.get_switch()):
        RPi.GPIO.output(crockPin, True)
    else:
        RPi.GPIO.output(crockPin, False)
    time.sleep(dt)
    tm += dt

pid.close()
