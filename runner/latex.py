import json

data = json.load(open("build.json", "r"))


def latex_row_compare_builds_dept():
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
        with open("results/latex_row_compare_builds_dept.txt", "w") as f:
            f.writelines(lines)



latex_row_compare_builds_dept()
