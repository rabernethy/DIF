# send.py written by Russell Abernethy
import requests
import os

tote_url = 'http://127.0.0.1:5000/totes'
thing_board_url = 'https://mis3502-shafer.com/thingsboard'
timeout = 5

logs = []
totes = []
ids = []

while True:
    try:
        r =  requests.get(tote_url, timeout=timeout)
        totes = r.json()

        # add all tote device ids to ids for reference later
        for tote in totes:
            ids.append(tote[2]) 
    except (requests.ConnectionError, requests.Timeout) as e:
        print(e)

    logs = [f for f in os.listdir("logs") if os.path.isfile(os.path.join("logs", f))]

    for log in sorted(logs):
        print("Processing Log: {}\n".format(log))
        with open("logs/{}".format(log), "r") as f:
            for device in f:
                for id in ids:
                    if id == device.replace("\n",""):
                        # find correct tote and send post to tb
                        for tote in totes:
                            if tote[2] == id:
                                data = {'latitude':39.981560274048924,
                                        'longitude': -75.15563001969575,
                                        'deviceid': tote[3]}
                                resp = requests.post(thing_board_url, data = data)
                                print("Tote {w}{n} Data Sent to ThingsBoard with response {r}\n".format(w=tote[0],n=tote[1],r=resp.status_code))
        #os.remove("logs/{}".format(log))
        print("Finished Processing Log: {}".format(log))