import os
import json

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
root = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
infos = {}
branches = ["dummy", "nullaway"] + ["deep_{}".format(i) for i in range(0, 11)]


def read_errors_num():
    return len(list(filter(lambda x: not x[0].isspace(), open("/tmp/NullAwayFix/errors.tsv", "r").readlines()))) - 1


for proj in projects['projects']:
    if not proj['active']:
        continue
    print("Working on {}".format(proj['name']))
    COMMAND = "cd {} && {}".format(root.format(proj['path']), "{}")
    errors = {}
    os.system(COMMAND.format("git config pull.rebase false"))
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git fetch"))
    for branch in branches:
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git fetch"))
        if branch != "nullaway":
            os.system(COMMAND.format("git checkout nullaway"))
            os.system(COMMAND.format("git branch -D {}".format(branch)))
            os.system(COMMAND.format("git fetch"))
        os.system(COMMAND.format("git fetch"))
        os.system(COMMAND.format("git pull"))
        os.system(COMMAND.format("git checkout {}".format(branch)))
        os.system(COMMAND.format("git pull"))
        os.system("rm /tmp/NullAwayFix/errors.tsv")
        os.system("{} > /dev/null 2>&1".format(COMMAND.format(proj['build'])))
        errors[branch] = read_errors_num()
    infos[proj['name']] = errors
    with open("error.json", "w") as f:
        json.dump(infos, f)
