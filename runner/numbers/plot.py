import json

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
all_errors = json.load(open("error.json"))
all_builds = json.load(open("build.json"))
infos = {}
branches = ["c_ttt{}".format(i) for i in range(0, 11)]


for proj in projects['projects']:
    print("Working on {}".format(proj['name']))
    builds = all_builds[proj['name']]
    errors = all_errors[proj['name']]
    best_error = 1 - (errors['c_ttt10'] / errors['nullaway'])
    max_build = builds['c_ttt10']['opt']
    lines = []
    line = "{},{}\n"
    proj['b'] = {}
    proj['e'] = {}
    for branch in branches:
        error_percentage = ((1 - (errors[branch] / errors['nullaway'])) / best_error) * 100
        build_percentage = builds[branch]['opt'] / max_build * 100
        proj['b']['e'] =
