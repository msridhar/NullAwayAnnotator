import json


def comp_exhaustive_selective_csv():
    data = json.load(open("../numbers/error.json", "r"))
    lines = ["Project,Selective,Exhaustive\n"]
    LINE = "{},{},{}\n"
    for proj in data.keys():
        info = data[proj]
        lines.append(LINE.format(proj, str(round(info['c_ttt10'] / info['nullaway'], 3)),
                                 str(round(info['dummy'] / info['nullaway'], 3))))
    with open("../results/comp_exhaustive_selective.csv", "w") as f:
        f.writelines(lines)


def make_csv():
    MAC = "/Users/nima/Developer/NullAwayFixer/Projects/"
    LINUX = "/home/nima/Developer/AutoFixer/Evaluation/Projects/"
    DISP = "{}|{}\n"
    HYPER_LINK = "\"=HYPERLINK(\"\"{}\"\",\"\"{}\"\")\""
    LINES = ["\"Errors\"\n"]
    with open('../projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            with open("../results/errors/{}/remaining.txt".format(project['name'])) as f:
                errors = [l for i, l in enumerate(f.readlines()) if i % 2 == 0]
                for i, error in enumerate(errors):
                    message = error[error.find(": error: [NullAway]") + len(": error: [NullAway]") + 1:][:-1]
                    start = len(MAC) if error.startswith(MAC) else len(LINUX)
                    error_link = error[start:error.find(": error: [NullAway]")].replace(":", "#L")
                    start = error_link.find(project['path']) + len(project['path'])
                    error_link = "{}/blob/nullaway{}".format(error_link[:start], error_link[start:])
                    error_link = "https://github.com/nimakarimipour/{}".format(error_link)
                    error_disp = HYPER_LINK.format(error_link, "Github")
                    disp = DISP.format(error_disp, message)
                    LINES.append(disp)
    with open('../results/errors/data.csv', "w") as f:
        f.writelines(LINES)


make_csv()
