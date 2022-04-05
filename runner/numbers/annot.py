import os
import json
import glob

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
root = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
infos = {}
branches = ["dummy"] + ["deep_{}".format(i) for i in range(0, 11)]


def count_annot(proj, annot):
    ans = 0
    path = proj['path']
    if proj['submodule'] != "":
        for dir in proj['submodule'].split(":"):
            path = os.path.join(path, dir)
    for file in glob.iglob(root.format(path) + '/**/*.java', recursive=True):
        with open(file, "r") as f:
            lines = f.readlines()
            for l in lines:
                ans += l.count("@" + annot)
    return ans


def read_annots(proj):
    init_annot_full_name = proj['annot']['init']
    nullable_annot_full_name = proj['annot']['nullable']
    init_annot = init_annot_full_name[init_annot_full_name.rfind(".") + 1:]
    nullable_annot = nullable_annot_full_name[nullable_annot_full_name.rfind(".") + 1:]
    return count_annot(proj, init_annot), count_annot(proj, nullable_annot)


for proj in projects['projects']:
    print("Working on {}".format(proj['name']))
    COMMAND = "cd {} && {}".format(root.format(proj['path']), "{}")
    annots = {}
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git fetch"))
    os.system(COMMAND.format("git checkout nullaway"))
    base_init, base_nullable = read_annots(proj)
    for branch in branches:
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git checkout {}".format(branch)))
        os.system(COMMAND.format("git pull"))
        annots[branch] = {}
        init, nullable = read_annots(proj)
        annots[branch]['nullable'] = nullable - base_nullable
        annots[branch]['initializer'] = init - base_init
    infos[proj['name']] = annots
    with open("annot.json", "w") as f:
        json.dump(infos, f)
