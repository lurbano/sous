import glob
import time
import RPi.GPIO
import sys

from subprocess import Popen

crockPin = 17
T_set = float(sys.argv[1])

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

Kp = 1.0
Ki = 0.0
Kd = 0.0
dt = 10.0

T_err_sum = 0.0
T_oldErr = 0.0
oldTime = 0.0

with open("T_log.txt", 'w') as logfile:
    tm = 0
    while True:
        T = read_temp()
        T_err = T - T_set   #calculate error
        T_err_sum += T_err
        dT_err = (T_err - T_oldErr) / dt

        p_term = Kp * T_err
        i_term = Ki * T_err_sum
        d_term = Kd * dT_err

        pidVal = p_term + i_term + d_term

        if (pidVal > 0.0):
            RPi.GPIO.output(crockPin, True)
            print("Switching On")
            l_on = True
        else:
            RPi.GPIO.output(crockPin, False)
            print("Switching Off")
            l_on = False

        #prep for next loop
        T_oldErr = dT_err

        outln = str(p_term) + ','
        outln += str(i_term) + ','
        outln += str(d_term) + ',|,'
        outln += str(pidVal) + ',|,'
        outln += str(tm) + ','
        outln += str(T) + ','
        outln += str(setT) + ','
        outln += str(l_on) + '\n'
        logfile.write(outln)
        print(outln)
        time.sleep(dt)
        tm += dt
