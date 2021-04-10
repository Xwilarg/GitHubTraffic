#!/usr/bin/env python3

from urllib.request import Request, urlopen
import json

print("Please enter your GitHub username:")
username = input()
print("Please enter your personal access token (can be generated at https://github.com/settings/tokens):")
token = input()
content = urlopen(f"https://api.github.com/users/{username}/repos?per_page=5").read()
for elem in json.loads(content):
    req = Request(f"https://api.github.com/repos/{username}/{elem['name']}/traffic/clones", headers={'Authorization': 'token ' + token})
    current = urlopen(req).read()
    print(current)
    print("\n\n")