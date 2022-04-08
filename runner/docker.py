import sys
import os
import json
import time

GIT_USERNAME = str(sys.argv[1])
GIT_KEY = str(sys.argv[2])

config = json.load(open("config.json", "r"))
projects = json.load(open("projects.json", "r"))
root = "/tmp/projects/{}"
os.makedirs(root.format(""))


def execute(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


def clone_project(project):
    command = "cd {} && git clone https://{}:{}@github.com/nimakarimipour/{}.git"
    if not os.path.isdir(root.format(project['path'])):
        os.system(command.format(root.format(""), GIT_USERNAME, GIT_KEY, project['path']))
    os.system("cd {} && {}".format(root.format(project['path']), project['build']))


for proj in projects['projects']:
    if proj['path'] != 'libgdx':
        continue
    print("Working on {}".format(proj['name']))
    clone_project(proj)
    path = root.format(proj['path'])
    config['PROJECT_PATH'] = path
    config['BUILD_COMMAND'] = proj['build']
    config['ANNOTATION']['NULLABLE'] = proj['annot']['nullable']
    config['ANNOTATION']['INITIALIZER'] = proj['annot']['init']
    config['CACHE'] = True
    config['OPTIMIZED'] = True
    config['BAILOUT'] = True
    config['CHAIN'] = False
    with open("config.json", "w") as f:
        json.dump(config, f)

    password = "https://{}:{}@github.com/nimakarimipour/{}.git".format(GIT_USERNAME, GIT_KEY, proj['path'])

    for i in range(0, 11):
        if i % 2 == 1:
            continue
        # t: only_root, t: cache, t: bailout
        branch = "c_ttt{}".format(i)
        COMMAND = "cd {} && {}".format(config['PROJECT_PATH'], "{}")
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git fetch"))
        os.system(COMMAND.format("git pull"))
        os.system(COMMAND.format("git checkout nullaway"))
        os.system(COMMAND.format("git pull"))
        os.system(COMMAND.format("git branch -D {}".format(branch)))
        os.system(COMMAND.format("git push {} --delete {}".format(password, branch)))
        os.system(COMMAND.format("git checkout -b {}".format(branch)))
        os.system(COMMAND.format("git push --set-upstream {} {}".format(password, branch)))
        config["DEPTH"] = i
        with open("config.json", "w") as f:
            json.dump(config, f)

        start = time.time()
        os.system("python3 run.py run")
        duration = time.time() - start

        with open("{}/elapsed_time.txt".format(config['PROJECT_PATH']), "w") as f:
            f.write(str(duration))

        os.system("cd /tmp && zip -r annotator.zip NullAwayFix/")
        os.system("mv /tmp/annotator.zip {}/annotator.zip".format(config['PROJECT_PATH']))

        os.system(COMMAND.format("git add ."))
        os.system(COMMAND.format("git commit -m \"Final Result\""))
        os.system(COMMAND.format("git push {}".format(password)))
