# send.py written by Russell Abernethy
import re
import requests
import os

url = 'http://127.0.0.1:5000/totes'
timeout = 5

logs = []
totes = []
ids = []

while True:
    try:
        r =  requests.get(url, timeout=timeout)
        totes = r.json()
        for tote in totes:
            ids.append(tote[2])
    except (requests.ConnectionError, requests.Timeout) as e:
        print(e)

    logs = [f for f in os.listdir("logs") if os.path.isfile(os.path.join("logs", f))]

    for log in sorted(logs):
        with open("logs/{}".format(log), "r") as f:
            for device in f:
                for id in ids:
                    print(device + " " + id + "\n\n")
                    if id == device:
                        print("here")