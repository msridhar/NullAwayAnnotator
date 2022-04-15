import os
import json
import re

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
root = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
infos = {}
branches = ["c_ttt{}".format(i) for i in range(0, 11)] + ["dummy", "u_ttt4"]


def read_number_of_builds(branch, path):
    try:
        lines = open(path, "r").readlines()
        if branch == "dummy":
            return len(lines), 0
        total = 0
        opt = 0
        for l in lines:
            infos = l.split(",")
            total += int(re.sub("[^0-9]", "", infos[0]))
            opt += int(re.sub("[^0-9]", "", infos[1]))
        return total, opt
    except FileNotFoundError:
        return -1, -1


for proj in projects['projects']:
    if not proj['active']:
        continue
    print("Working on {}".format(proj['name']))
    proj_path = root.format(proj['path'])
    COMMAND = "cd {} && {}".format(proj_path, "{}")
    builds = {}
    os.system(COMMAND.format("git config pull.rebase false"))
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git fetch"))
    for branch in branches:
        builds[branch] = {}
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git checkout {}".format(branch)))
        os.system(COMMAND.format("git pull"))
        os.system(COMMAND.format("rm -rvf NullAwayFix"))
        os.system(COMMAND.format("unzip annotator.zip"))
        builds[branch]["total"], builds[branch]["opt"] = read_number_of_builds(branch, "{}/NullAwayFix/log.txt".format(proj_path))
        os.system(COMMAND.format("rm -rvf NullAwayFix"))
    infos[proj['name']] = builds
    with open("build.json", "w") as f:
        json.dump(infos, f)
