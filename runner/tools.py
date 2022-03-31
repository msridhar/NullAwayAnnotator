import json


def comp_exhaustive_selective_csv():
    data = json.load(open("error.json", "r"))
    lines = ["Project,Selective,Exhaustive\n"]
    LINE = "{},{},{}\n"
    for proj in data.keys():
        info = data[proj]
        lines.append(LINE.format(proj, str(round(info['deep_10']/info['nullaway'], 3)), str(round( info['dummy']/info['nullaway'], 3))))
    with open("results/comp_exhaustive_selective.csv", "w") as f:
        f.writelines(lines)

comp_exhaustive_selective_csv()
