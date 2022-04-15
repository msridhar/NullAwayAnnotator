import os
import json
import re

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
root = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
infos = {}
branches = ["c_ttt{}".format(i) for i in range(0, 11)] + ["u_ttt4"]


def time_spent(path):
    try:
        lines = open(path, "r").readlines()
        total = 0
        for l in lines:
            infos = l.split(",")
            total += int(re.sub("[^0-9]", "", infos[2])) / 1000
        return total
    except FileNotFoundError:
        return -1


for proj in projects['projects']:
    print("Working on {}".format(proj['name']))
    proj_path = root.format(proj['path'])
    COMMAND = "cd {} && {}".format(proj_path, "{}")
    times = {}
    os.system(COMMAND.format("git config pull.rebase false"))
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git fetch"))
    for branch in branches:
        times[branch] = {}
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git checkout {}".format(branch)))
        os.system(COMMAND.format("git pull"))
        os.system(COMMAND.format("rm -rvf NullAwayFix"))
        os.system(COMMAND.format("unzip annotator.zip"))
        times[branch] = time_spent("{}/NullAwayFix/log.txt".format(proj_path))
        os.system(COMMAND.format("rm -rvf NullAwayFix"))
    infos[proj['name']] = times
    with open("time.json", "w") as f:
        json.dump(infos, f)
