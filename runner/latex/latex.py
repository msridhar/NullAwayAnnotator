import json


def latex_row_table_1():
    data = json.load(open("../numbers/error.json", "r"))
    lines = []
    for name in data.keys():
        proj = data[name]
        dummy = proj['dummy']
        d4 = proj['c_ttt4']
        initial = proj['nullaway']
        percentage = 1 - d4 / initial
        # & \hspace{1em} \texttt{Conductor}& 9.2K & 1 & 1 & 1 & 1\\\cline{2-7}
        line = "& \hspace{}1em{} \\texttt{}{}{} &  & {} & {} & {} & {}".format("{", "}", "{", name, "}", initial, dummy, d4, format(percentage, ".2f"))
        line += "\\\\\cline{2-7}\n"
        lines.append(line)
        with open("latex_row_table_1.txt", "w") as f:
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


latex_row_table_1()
