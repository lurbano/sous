import glob
import time

from subprocess import Popen

Popen(['modprobe', 'w1-gpio'])
Popen(['modprobe', 'w1-therm'])

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
print(device_file)

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
print('Temp = ', T)


with open("T_log.txt", 'w') as logfile:
    tm = 0
    while True:
        T = read_temp()
        outln = str(tm) + ', ' + str(T) + '\n'
        logfile.write(outln)
        print(outln)
        time.sleep(1)
        tm += 1
