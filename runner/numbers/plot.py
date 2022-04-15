import json

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
all_errors = json.load(open("error.json"))
all_times = json.load(open("time.json"))
infos = {}
branches = ["c_ttt{}".format(i) for i in range(0, 11)]

PROJ = {"error": {}, "time": {}}
for branch in branches:
    PROJ["error"][branch] = 0
    PROJ["time"][branch] = 0

for proj in projects['projects']:
    print("Working on {}".format(proj['name']))
    times = all_times[proj['name']]
    errors = all_errors[proj['name']]
    best_error = 1 - (errors['c_ttt10'] / errors['nullaway'])
    max_time = times['c_ttt10']
    for branch in branches:
        error_percentage = ((1 - (errors[branch] / errors['nullaway'])) / best_error) * 100
        time_percentage = times[branch]/ max_time * 100
        PROJ["time"][branch] += time_percentage
        PROJ["error"][branch] += error_percentage

lines = []
for branch in branches:
    line = "{},{}\n"
    lines.append(line.format(format(PROJ["error"][branch] / 15, ".2f"), format(PROJ["time"][branch] / 15, ".2f")))

with open("plot/plot.csv", "w") as f:
    f.writelines(lines)




