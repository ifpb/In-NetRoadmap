import re

from inetrm.module_b.datatypes import get_datatype


def find_classification(regras_list: list[str], features: dict[str, list[int]]):
    rules = []

    for line in regras_list:
        line = line.strip()
        if not line.startswith("when"):
            continue

        pattern = r"(\w+)\s*(<=|>)\s*(\d+(?:\.\d+)?)"
        conditions = re.findall(pattern, line)
        if not conditions:
            continue

        classification = re.findall(r"then\s+(\d+)", line)
        if not classification:
            continue
        classification = int(classification[0])

        feature_ranges = {}

        for feature in features.keys():
            feature_ranges[feature] = [k for k in range(len(features[feature]) + 1)]

        for fea, sign, num in conditions:
            if fea not in features:
                continue

            thres = int(float(num))
            id = features[fea].index(thres)

            if sign == "<=":
                while id < len(features[fea]):
                    if id + 1 in feature_ranges[fea]:
                        feature_ranges[fea].remove(id + 1)
                    id = id + 1
            else:
                while id >= 0:
                    if id in feature_ranges[fea]:
                        feature_ranges[fea].remove(id)
                    id = id - 1

        rules.append(
            {
                "conditions": conditions,
                "ranges": feature_ranges,
                "classification": classification,
            }
        )

    return rules


def writeactionrule(writer, ranges, action, result):
    command = f"table_add classify_exact {action} "
    for i in range(len(ranges)):
        command += f"{ranges[i][0]}->{ranges[i][1]} "
    command += f"=> {str(result)} 0\n"

    writer.write(command)
    # print("add action rule")


def writefeatureXrule(writer, range, table, action, ind):
    # print(range)
    # print(ind)
    # print(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)}")
    writer.write(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)} 0\n")
    # print(f"add {table} rule")


def generate_tables(
    regras_list: list[str], features: dict[str, list[int]], output_path: str
):

    rules = find_classification(regras_list, features)

    with open(output_path, "w") as f:
        for i in range(len(rules)):
            ranges = []

            for fea in features.keys():
                a = rules[i]["ranges"][fea]
                a = [a[0] + 1, a[-1] + 1]
                ranges.append(a)

            ind = int(rules[i]["classification"])

            writeactionrule(f, ranges, "set_result", ind)

        for idx, fea in enumerate(features.keys()):
            max_value = get_datatype(fea)
            if max_value is None:
                max_value = 48

            features[fea].append(0)
            features[fea].append(2**max_value - 1)
            features[fea].sort()
            for i in range(len(features[fea]) - 1):
                writefeatureXrule(
                    f,
                    features[fea][i : i + 2],
                    f"feature{idx+1}_exact",
                    f"set_actionselect{idx+1}",
                    i + 1,
                )
