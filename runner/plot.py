import os
import json
import time

config = json.load(open("config.json", "r"))
projects = json.load(open("projects.json", "r"))
root = "/home/nima/Developer/AutoFixer/Evaluation/Projects/{}"

for proj in projects['projects']:
    if not proj['active']:
        continue
