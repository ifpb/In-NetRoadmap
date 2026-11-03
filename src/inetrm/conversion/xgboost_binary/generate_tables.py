import re
from ..datatypes import get_datatype

def process_xgboost_rules(regras_dict: dict, features: dict[str, list[float]]):
    parsed_trees = {}
    
    for tree_name, regras_list in regras_dict.items():
        rules = []
        for line in regras_list:
            line = line.strip()
            if not line.startswith("when"):
                continue

            pattern = r"(\w+)\s*(<=|>)\s*(-?\d+(?:\.\d+)?)"
            conditions = re.findall(pattern, line)
            
            weight_match = re.search(r"then\s+(add|sub)\s+(\d+)", line)
            if not weight_match:
                continue
            
            action, weight = weight_match.groups()
            weight = int(weight)

            feature_ranges = {fea: [k for k in range(len(features[fea]) + 1)] for fea in features.keys()}

            for fea, sign, num in conditions:
                if fea not in features:
                    continue
                thres = float(num)
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

            rules.append({
                "ranges": feature_ranges,
                "action": f"{action}_tree_weight",
                "weight": weight,
            })
        parsed_trees[tree_name] = rules
    return parsed_trees

def generate_tables(regras_dict: dict, features: dict, output_path: str):
    parsed_trees = process_xgboost_rules(regras_dict, features)

    with open(output_path, "w") as f:
        for idx, fea in enumerate(features.keys()):
            max_value = get_datatype(fea) or 48
            features[fea].append(0)
            features[fea].append(2**max_value - 1)
            features[fea].sort()
            
            for i in range(len(features[fea]) - 1):
                range_str = f"{int(features[fea][i])}->{int(features[fea][i+1])}"
                f.write(f"table_add feature{idx+1}_exact set_actionselect{idx+1} {range_str} => {i+1} 0\n")
        
        for tree_idx, (tree_name, rules) in enumerate(parsed_trees.items()):
            table_name = f"tree{tree_idx}_exact"
            for rule in rules:
                ranges_str = ""
                for fea in features.keys():
                    a = rule["ranges"][fea]
                    ranges_str += f"{a[0] + 1}->{a[-1] + 1} "
                
                f.write(f"table_add {table_name} {rule['action']} {ranges_str.strip()} => {rule['weight']} 0\n")
