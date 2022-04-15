import json

names = ["Conductor", "Mockito", "SpringBoot", "LitiEngine", "LibGdx", "MPAndroid", "Glide", "EventBus",
         "LottieAndroid", "UCrop", "Gson", "Eureka", "Retrofit", "Jadx", "Zuul"]


def latex_row_table_1():
    data = json.load(open("../numbers/error.json", "r"))
    lines = []
    for name in names:
        proj = data[name]
        dummy = proj['dummy']
        d0 = proj['c_ttt0']
        d4 = proj['c_ttt4']
        initial = proj['nullaway']
        p_d4 = -1 * (1 - d4 / initial) * 100
        p_dummy = -1 * (1 - dummy / initial) * 100
        p_d0 = -1 * (1 - d0 / initial) * 100
        sign = "+" if p_dummy > 0 else ""
        # & \hspace{1em} \texttt{Conductor} & 9.2K & 138 & 163 & 78 & 69 & 0.50 & &\\\cline{2-10}
        line = "& \hspace{}1em{} \\texttt{}{}{} &  & {} & {} & {} & {} & {}{} & {}".format("{", "}", "{", name, "}", initial, dummy, d0,
                                                                            d4, sign ,format(p_dummy, ".2f"), format(p_d0, ".2f"), format(p_d4, ".2f"))
        line += "\\\\\cline{2-10}\n"
        lines.append(line)
        with open("latex_row_table_1.txt", "w") as f:
            f.writelines(lines)


def latex_row_table_4():
    # & \hspace{1em} \texttt{Glide} & 419 & 53 & 0 & 16410 & 472 & 0 \\\cline{2-8}
    builds = json.load(open("../numbers/build.json", "r"))
    times = json.load(open("../numbers/time.json", "r"))
    lines = []
    for name in names:
        t = format(times[name]['u_ttt4'], ".2f") if times[name]['u_ttt4'] != "time-out" else "time-out"
        # & \hspace{1em} \texttt{Conductor}& 9.2K & 1 & 1 & 1 & 1\\\cline{2-7}
        line = "& \hspace{}1em{} \\texttt{}{}{} & {}  & 0 & {} & {} & 0 & {}".format("{", "}", "{", name, "}",
                                                                                     builds[name]['u_ttt4']['opt'],
                                                                                     builds[name]['c_ttt4']['opt'],
                                                                                     t,
                                                                                     format(times[name]['c_ttt4'], ".2f")
                                                                                     )
        line += "\\\\\cline{2-8}\n"
        lines.append(line)
        with open("latex_row_table_4.txt", "w") as f:
            f.writelines(lines)


def latex_row_compare_builds_dept():
    data = json.load(open("../numbers/build.json", "r"))
    lines = []
    for name in data.keys():
        proj = data[name]
        # & \hspace{1em} \texttt{Mockito} &  325 & 55 & 61\hspace{1em} &  63\hspace{1em} \\\cline{2-6}
        line = "& \hspace{}1em{} \\texttt{}{}{}".format("{", "}", "{", name, "}")
        line += "& {} ".format(proj['deep_0']['total'])
        for depth in proj.keys():
            if depth != "dummy":
                line += "& {} ".format(proj[depth]['opt'])

        line += "\\\\\cline{2-14}\n"
        lines.append(line)
        with open("../results/latex_row_compare_builds_dept.txt", "w") as f:
            f.writelines(lines)


def latex_row_compare_errors_dept():
    data = json.load(open("../numbers/error.json", "r"))
    lines = []
    for name in data.keys():
        proj = data[name]
        line = "& \hspace{}1em{} \\texttt{}{}{}".format("{", "}", "{", name, "}")
        for depth in proj.keys():
            if depth != "dummy":
                line += "& {} ".format(proj[depth])

        line += "\\\\\cline{2-14}\n"
        lines.append(line)
        with open("../results/latex_row_compare_errors_dept.txt", "w") as f:
            f.writelines(lines)


def latex_row_num_annot():
    data = json.load(open("../numbers/annot.json", "r"))
    lines = []
    for name in data.keys():
        proj = data[name]
        line = "& \hspace{}1em{} \\texttt{}{}{}".format("{", "}", "{", name, "}")
        for depth in ['dummy', 'deep_10']:
            for annot in proj[depth].keys():
                line += "& {} ".format(proj[depth][annot])

        line += "\\\\\cline{2-14}\n"
        lines.append(line)
        with open("../results/latex_row_num_annot.txt", "w") as f:
            f.writelines(lines)


data = "562 & 496 & 441 & 426"
nums = [d.strip() for d in data.split("&")]
l = "{}{} & {} & {}"
base = int(nums[0])
d0 = int(nums[1])
d1 = int(nums[2])
d5 = int(nums[3])
sign = "+" if d0 > base else ""
p_d0 = -100 * (1 - d0/base)
p_d1 = -100 * (1 - d1/base)
p_d5 = -100 * (1 - d5/base)
print(l.format(sign, format(p_d0, ".2f"), format(p_d1, ".2f"), format(p_d5, ".2f")))

