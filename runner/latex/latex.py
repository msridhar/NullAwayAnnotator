import json

names = ["Conductor", "Mockito", "SpringBoot", "LitiEngine", "MPAndroid", "Glide", "EventBus",
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
        # & \hspace{1em} \texttt{Conductor} & 9.2K & 138 & 163 (+18.1 \%) & 78 (+18.1 \%) & 69 (+18.1 \%) \\\cline{2-7}
        line = "& \hspace{}1em{} \\texttt{}{}{} &  & {} & {} ({}{} \%) & {} ({} \%) & {} ({} \%)".format("{", "}", "{",
                                                                                                        name, "}",
                                                                                                        initial, dummy,
                                                                                                        sign,
                                                                                                        format(p_dummy,
                                                                                                               ".1f"),
                                                                                                        d0,
                                                                                                        format(p_d0,
                                                                                                               ".1f"),
                                                                                                        d4,
                                                                                                        format(p_d4,
                                                                                                               ".1f"))
        line += "\\\\\cline{2-7}\n"
        lines.append(line)
        with open("latex_row_table_1.txt", "w") as f:
            f.writelines(lines)


def quick():
    data = json.load(open("../numbers/time.json", "r"))
    sum = 0
    cnt = 0
    min  = 1000
    max = -10000
    for name in names:
        proj = data[name]
        t = proj['c_ftt4']
        r = proj['c_ttt4']
        a = (r/t)
        if a < min:
            min = a
        if a > max:
            max = a

    print(max)
    print(min)



def latex_row_table_4():
    # & \hspace{1em} \texttt{Glide} & 419 & 53 & 0 & 16410 & 472 & 0 \\\cline{2-8}
    builds = json.load(open("../numbers/build.json", "r"))
    times = json.load(open("../numbers/time.json", "r"))
    lines = []
    for name in names:
        t = format(times[name]['u_ttt4'], ".2f") if times[name]['u_ttt4'] != "time-out" else "time-out"
        # & \hspace{1em} \texttt{Conductor} & 1333.53 & 472.79(?X) & 511.40(?X) & 187  & 64 & 71\\\cline{2-8}
        line = "& \hspace{}1em{} \\texttt{}{}{} & {} & {} ({}X) & {} & {}".format("{", "}", "{", name, "}",
                                                                                     format(times[name]['u_ttt4'] /60, ".1f"),
                                                                                     format(times[name]['c_ttt4'] / 60,
                                                                                            ".1f"),
                                                                                     format(times[name]['u_ttt4'] / times[name]['c_ttt4'],
                                                                                            ".1f"),
                                                                                     builds[name]['u_ttt4']['opt'],
                                                                                     builds[name]['c_ttt4']['opt'],
                                                                                     )
        line += "\\\\\cline{2-6}\n"
        lines.append(line)
        with open("latex_row_table_4.txt", "w") as f:
            f.writelines(lines)


# latex_row_table_4()
quick()
# data = "562 & 496 & 441 & 426"
# nums = [d.strip() for d in data.split("&")]
# l = "{}{} & {} & {}"
# base = int(nums[0])
# d0 = int(nums[1])
# d1 = int(nums[2])
# d5 = int(nums[3])
# sign = "+" if d0 > base else ""
# p_d0 = -100 * (1 - d0 / base)
# p_d1 = -100 * (1 - d1 / base)
# p_d5 = -100 * (1 - d5 / base)
# print(l.format(sign, format(p_d0, ".2f"), format(p_d1, ".2f"), format(p_d5, ".2f")))
