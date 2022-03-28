import os
import json
import time

f = open("config.json", "r")
data = json.load(f)

for i in range(1, 11):
    print("START")
    branch = "deep_{}".format(i)
    COMMAND = "cd {} && {}".format(data['PROJECT_PATH'], "{}")
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git checkout nullaway"))
    os.system(COMMAND.format("git branch -D {}".format(branch)))
    os.system(COMMAND.format("git push origin --delete {}".format(branch)))
    os.system(COMMAND.format("git checkout -b {}".format(branch)))
    data["DEPTH"] = i
    with open("config.json", "w") as f:
        json.dump(data, f)

    start = time.time()
    os.system("python3 run.py run")
    duration = time.time() - start

    with open("elapsed_time.txt", "w") as f:
        f.write(str(duration))

    os.system("cd /tmp && zip -r annotator.zip NullAwayFix/")
    os.system("mv /tmp/annotator.zip {}/annotator.zip".format(data['PROJECT_PATH']))

    os.system(COMMAND.format("git add ."))
    os.system(COMMAND.format("git commit -m \"Final Result\""))
    os.system(COMMAND.format("git push --set-upstream origin {}".format(branch)))
