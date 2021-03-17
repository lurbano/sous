import glob
import time
import RPi.GPIO
import sys

from subprocess import Popen

crockPin = 17
setT = float(sys.argv[1])
dt = 10.0


RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(crockPin, RPi.GPIO.OUT)

Popen(['modprobe', 'w1-gpio'])
Popen(['modprobe', 'w1-therm'])

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
#print(device_file)

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

T = read_temp()

print('Set Temp. = ', setT)
print('Water Temp = ', T)

l_on = False
l_old = l_on

with open("T_log.txt", 'w') as logfile:
    tm = 0
    while True:
        T = read_temp()
        if (T < setT):
            l_on = True
        else:
            l_on = False
        if (l_on != l_old):
            if l_on:
                RPi.GPIO.output(crockPin, True)
                print("Switching On")
            else:
                RPi.GPIO.output(crockPin, False)
                print("Switching Off")
            l_old = l_on
        outln = str(tm) + ',' + str(T) + ',' + str(setT) + ',' + str(l_on) + '\n'
        logfile.write(outln)
        print(outln)
        time.sleep(dt)
        tm += dt
