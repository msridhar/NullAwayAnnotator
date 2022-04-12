import os
import json
import random

projects = json.load(open("../projects.json", "r"))
root = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
infos = {}


# helps to make sure at every 4 line we have one error
def helper(path):
    lines = open(path, "r").readlines()
    for i, l in enumerate(lines):
        if i % 4 == 3 and (l != "    (see http://t.uber.com/nullaway )\n"):
            print(str(i) + " " + l)


def remove_line_number(error):
    start = error.index(".java:")
    end = error.index(": error: [NullAway] ")
    return error[0:start + 6] + error[end:], int(error[start+6:end])


def list_contains_error(err, error_list):
    err_body, err_line = remove_line_number(err.strip())
    for e in error_list:
        e_body, e_line = remove_line_number(e.strip())
        if e_body == err_body and abs(err_line - e_line) < 40:
            return True
    return False


def read_errors(path):
    lines = open(path, "r").readlines()
    error = None
    errors = []
    for i, l in enumerate(lines):
        if i % 4 == 2 or i % 4 == 3:
            continue
        if i % 4 == 0:
            error = l
        else:
            error += l
            errors.append(error)
            error = None
    return errors


def capture_errors_in_branches(name):
    for proj in projects['projects']:
        if proj['name'] != name:
            continue
        print("Working on {}".format(proj['name']))
        COMMAND = "cd {} && {}".format(root.format(proj['path']), "{}")
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git fetch"))
        for branch in ["nullaway", "c_ttt10"]:
            os.system(COMMAND.format("git checkout {}".format(branch)))
            os.system(COMMAND.format("git pull"))
            os.system("{} 2> error.txt".format(COMMAND.format(proj['build'])))
            if not os.path.exists("../results/errors/{}".format(proj['name'])):
                os.system("mkdir ../results/errors/{}".format(proj['name']))
            os.system(
                "mv {}/error.txt ../results/errors/{}/error_{}.txt".format(root.format(proj['path']), proj['name'],
                                                                           branch))


def sample_remaining_errors(name):
    for proj in projects['projects']:
        if proj['name'] != name:
            continue
        print("Working on {}".format(proj['name']))
        before = read_errors("../results/errors/{}/error_nullaway.txt".format(proj['name']))
        after = read_errors("../results/errors/{}/error_c_ttt10.txt".format(proj['name']))
        to_remove = []
        for e in after:
            if not list_contains_error(e, before):
                to_remove.append(e)
        for e in to_remove:
            after.remove(e)
        print("Choosing 5 from: {}".format(len(after)))
        sampled = random.sample(after, 1)
        with open("../results/errors/{}/remaining1.txt".format(proj['name']), "w") as f:
            f.writelines(sampled)
        exit()

# capture_errors_in_branches("Jadx")
# helper("../results/errors/Zuul/error_nullaway.txt")
# sample_remaining_errors("LitiEngine")
