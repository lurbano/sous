#!/usr/bin/env python3

import requests
import json
from subprocess import check_output

url = 'http://www.soriki.com/sous/post_ip.php'

output = check_output(["hostname", "-I"])

hostname = output.strip().decode("utf-8")

print("hostname: "+ hostname)

data = { "hostname": hostname, "id": "lurb 1"}

r = requests.post(url, data=data)
print(r.text)
print("done")
