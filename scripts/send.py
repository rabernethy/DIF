# send.py written by Russell Abernethy
import re
import requests
import os

url = 'http://127.0.0.1:5000/totes'
timeout = 5

logs = []
tote_ids = []
r = ""

while True:
    try:
        r =  requests.get(url, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as e:
        print(e)

    logs = [f for f in os.listdir("logs") if os.path.isfile(os.path.join("logs", f))]
    
    # read through devices listed in log file

    # for each device if it is in the tote_ids list, then update the coorosponding tote in thing board