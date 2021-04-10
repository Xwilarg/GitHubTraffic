#!/usr/bin/env python3

from urllib.request import Request, urlopen
from os import path
import json

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

    req = Request(f"https://api.github.com/users/{j['username']}/repos?per_page=5", headers={'Authorization': 'token ' + j['token']})
    content = urlopen(req).read()
    for elem in json.loads(content):
        req = Request(f"https://api.github.com/repos/{j['username']}/{elem['name']}/traffic/clones", headers={'Authorization': 'token ' + j['token']})
        response = urlopen(req).read()
        print(response)
        print("\n\n")

if __name__ == "__main__":
    main()