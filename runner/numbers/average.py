import os
import json
import re

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
root = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
infos = {}
# branches = ["c_ttt{}".format(i) for i in range(0, 11)] + ["dummy", "u_ttt4"]
branches = ["c_ttt4"]


def read_number_of_builds(branch, path):
    try:
        lines = open(path, "r").readlines()
        if branch == "dummy":
            return len(lines), 0
        total = 0
        build = 0
        for l in lines:
            infos = l.split(",")
            total += int(re.sub("[^0-9]", "", infos[2]))
            build += int(re.sub("[^0-9]", "", infos[4]))
        return total, build, 1
    except Exception:
        return 1, 0, 0


total_avg = 0
cnt = 0
for proj in projects['projects']:
    print("Working on {}".format(proj['name']))
    proj_path = root.format(proj['path'])
    COMMAND = "cd {} && {}".format(proj_path, "{}")
    os.system(COMMAND.format("git config pull.rebase false"))
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git fetch"))
    for branch in branches:
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git checkout {}".format(branch)))
        os.system(COMMAND.format("git pull"))
        os.system(COMMAND.format("rm -rvf NullAwayFix"))
        os.system(COMMAND.format("unzip annotator.zip"))
        t_total, t_build, c = read_number_of_builds(branch, "{}/NullAwayFix/log.txt".format(proj_path))
        cnt += c
        total_avg += t_build / t_total
        os.system(COMMAND.format("rm -rvf NullAwayFix"))

print(total_avg)
print(cnt)
print(total_avg / cnt)
