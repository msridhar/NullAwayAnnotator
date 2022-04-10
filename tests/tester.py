# MIT License
#
# Copyright (c) 2020 Nima Karimipour
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import json
import sys
import shutil
import filecmp

PROJECT_PATH = "{}/tests".format(os.getcwd())
ALL_TESTS_PATH = "units/"

data = json.load(open('config.json'))
data['PROJECT_PATH'] = PROJECT_PATH
with open('config.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)


def print_status(msg: str, status):
    green = "\033[1;32;40m"
    red = "\033[1;31;40m"
    normal = '\033[0m'
    color = green if status else red
    print("{}{}{}".format(color, msg, normal))


def compare_dirs(dir1: str, dir2: str):
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or \
            len(dirs_cmp.funny_files) > 0:
        return False, []
    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)
    if len(mismatch) > 0 or len(errors) > 0:
        return False, mismatch
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        status, dif = compare_dirs(new_dir1, new_dir2)
        if not status:
            return False, dif
    return True, []


def show_tests():
    return [x for x in os.listdir(ALL_TESTS_PATH) if x != "build" and os.path.isdir(ALL_TESTS_PATH + x)]


def test(name: str):
    if name not in show_tests():
        print("No test found with name: {}".format(name))
        return
    test_dir = ALL_TESTS_PATH + name + "/{}"
    try:
        shutil.rmtree(test_dir.format("out/"))
    except OSError:
        print("Error in test{}".format(name))
    os.system("cp -R {} {}".format(test_dir.format("src/"), test_dir.format("tmp/")))

    config = json.load(open('config.json'))
    config['PROJECT_PATH'] = PROJECT_PATH
    config['BUILD_COMMAND'] = "./gradlew :units:{}:build -x test".format(name)
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile, indent=4)
    os.system("python3 run.py loop tests/config.json")
    os.renames(test_dir.format("src/"), test_dir.format("out/"))
    os.renames(test_dir.format("tmp/"), test_dir.format("src/"))
    os.system("cd {} && ./gradlew goJF".format(PROJECT_PATH))
    status, difs = compare_dirs(test_dir.format("out/main/"), test_dir.format("expected/main/"))
    if status:
        print_status("{} - TEST WAS SUCCESSFUL".format(name), True)
    else:
        print_status("{} - TEST WAS UNSUCCESSFUL - {}".format(name, difs), False)


def test_all():
    print("Executing all tests")
    for name in show_tests():
        test(name)


COMMAND = sys.argv[1]
if COMMAND == "tests":
    print("All tests are:")
    for test in show_tests():
        print(test)
elif COMMAND == "test":
    if int(len(sys.argv)) == 3:
        test(sys.argv[2])
    else:
        test_all()
