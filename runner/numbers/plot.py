import json
import matplotlib.pyplot as plt

config = json.load(open("../config.json", "r"))
projects = json.load(open("../projects.json", "r"))
all_errors = json.load(open("error.json"))
all_times = json.load(open("time.json"))
infos = {}
branches = ["c_ttt{}".format(i) for i in range(0, 10)]


def error():
    depth = {}

    for branch in branches:
        depth[branch] = []

    for proj in projects['projects']:
        print("Working on {}".format(proj['name']))
        errors = all_errors[proj['name']]
        best_error = 1 - (errors['c_ttt9'] / errors['nullaway'])
        for branch in branches:
            error_percentage = ((1 - (errors[branch] / errors['nullaway'])) / best_error) * 100
            depth[branch].append(error_percentage)

    axis = [depth[k] for k in depth.keys()]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Depth')
    ax.set_ylabel('% of Depth 10 Error Removed')
    plt.boxplot(axis, autorange=True, whis=100)
    plt.ylim(80, 101)
    plt.show()


def time():
    depth = {}

    for branch in branches:
        depth[branch] = []

    for proj in projects['projects']:
        print("Working on {}".format(proj['name']))
        times = all_times[proj['name']]
        max_time = times['c_ttt9']
        for branch in branches:
            time_percentage = times[branch]/ max_time * 100
            depth[branch].append(time_percentage)

    axis = [depth[k] for k in depth.keys()]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Depth')
    ax.set_ylabel('% of Depth 10 Running Time')
    plt.boxplot(axis, autorange=True, whis=100)
    plt.ylim(0, 105)
    plt.show()

time()
# error()

