#!/usr/bin/env python3

from urllib.request import Request, urlopen
from os import path
import matplotlib.pyplot as plt
import json

MAX_PER_PAGE = 100

def getUserBoolean(sentence):
    print(sentence)
    choice = input()
    while choice != 'n' and choice != 'N' and choice != 'y' and choice != 'Y' and choice != '':
        print(sentence)
        choice = input()
    return choice == '' or choice == 'y' or choice == 'Y'

def readConfigFromInput():
    print("Please enter your GitHub username:")
    username = input()
    print("Please enter your personal access token (can be generated at https://github.com/settings/tokens):")
    token = input()
    j = '{ "username": "' + username + '", "token": "' + token + '" }'
    if getUserBoolean("Do you want to save the data of this user for futur use? [Y/n]"):
        with open('config.json', 'w') as f:
            f.write(j)
    return json.loads(j)

def readConfigFromJson():
    with open('config.json', 'r') as f:
        data = f.read()
        j = json.loads(data)
        if getUserBoolean("Do you want to load the data for " + j['username'] + "? [Y/n]"):
            return j
        return readConfigFromInput()

def main():
    if path.exists("config.json"):
        j = readConfigFromJson()
    else:
        j = readConfigFromInput()

    names = []
    page = 1
    while True:
        tmp = []
        req = Request(f"https://api.github.com/users/{j['username']}/repos?per_page=" + str(MAX_PER_PAGE) + "&page=" + str(page), headers={'Authorization': 'token ' + j['token']})
        content = urlopen(req).read()
        for elem in json.loads(content):
            tmp.append(elem['name'])
        names += tmp
        if len(tmp) < MAX_PER_PAGE:
            break
        page += 1

    print(str(len(names)) + " repositories found", flush=True)

    labels = []
    values = []

    for elem in names:
        req = Request(f"https://api.github.com/repos/{j['username']}/{elem}/traffic/views", headers={'Authorization': 'token ' + j['token']})
        response = urlopen(req).read()
        jA = json.loads(response)
        if jA['uniques'] > 1:
            labels.append(elem)
            values.append(jA['uniques'])
        print(f"{elem} - Unique views: {jA['uniques']}", flush=True)

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels)
    plt.show()

if __name__ == "__main__":
    main()