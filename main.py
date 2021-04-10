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

    # Get all repositories
    names = []
    page = 1
    while True:
        tmp = []
        req = Request(f"https://api.github.com/users/{j['username']}/repos?per_page=" + str(MAX_PER_PAGE) + "&page=" + str(page))
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

    # Get metrics about all repositories
    for elem in names:
        req = Request(f"https://api.github.com/repos/{j['username']}/{elem}/traffic/views", headers={'Authorization': 'token ' + j['token']})
        response = urlopen(req).read()
        jA = json.loads(response)
        if jA['uniques'] > 1:
            labels.append(elem)
            values.append(jA['uniques'])
        print(f"{elem} - Unique views: {jA['uniques']}", flush=True)

    # Sort data get from biggest to lowest
    values, labels = zip(*sorted(zip(values, labels), reverse=True))

    # Display data
    plt.bar(labels, height=values)
    plt.title("Unique view per repository (14 last days)")

    for index, data in enumerate(values):
        plt.text(x=index, y=data + 1, s=data, ha='center')

    plt.tick_params(left=False, labelleft=False)
    plt.box(False)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()