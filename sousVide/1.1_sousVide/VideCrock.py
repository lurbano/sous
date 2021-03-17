import json
from subprocess import Popen
import glob
import time

homedir = "/home/pi/sousVide/"
webdir = "/var/www/html/sous/logs/"
websetdir = "/var/www/html/sous/sets/"
webLogFilename = webdir + "T_data.txt"
webRecentFilename = webdir + "current_data.json"
webTcheckFilename = webdir + "T_check.json"
webComFilename = websetdir + "web_com.json"

web_com_defaults = {}
web_com_defaults["check"] = "default"
web_com_defaults["runCrockpot"] = False

def get_default_settings():
    s = {}
    s["Kp"] = -1
    s["Ki"] = 0
    s["Kd"] = -100
    s["Temperature"] = 55.0
    return s


setfilename = homedir+"settings.json"
def read_settings(inFile = setfilename):
    default_sets = get_default_settings()
    with open(inFile, "r") as f:
        settings = json.load(f)
    #print("  Getting Defaults")
    for i in default_sets:
        #print(i)
        l_check = False
        for j in settings:
            #print(":"+j)
            if (j == i):
                l_check = True
        if not(l_check):
            settings[i] = default_sets[i]
    return settings

def write_settings(settings, inFile = setfilename):
    #settings is a python list: see setup.py for valid settings
    with open(inFile, "w") as f:
        f.write(json.dumps(settings))

def read_web_settings(inFile = webComFilename):
    with open(inFile, "r") as f:
        web_settings = json.load(f)
        web_settings["Kp"] = float(web_settings["Kp"])
        web_settings["Ki"] = float(web_settings["Ki"])
        web_settings["Kd"] = float(web_settings["Kd"])
    return web_settings

def write_web_settings(settings, outFile = webComFilename):
    with open(outFile, "w") as f:
        f.write(json.dumps(settings))

#Thermometer setup
Popen(['modprobe', 'w1-gpio'])
Popen(['modprobe', 'w1-therm'])

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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
