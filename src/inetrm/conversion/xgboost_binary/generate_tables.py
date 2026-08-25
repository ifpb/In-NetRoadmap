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
            if not conditions:
                continue

            weight = re.findall(r"then\s+(-?\d+)", line)
            if not weight:
                continue
            weight = int(weight[0])

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
                "weight": weight,
            })
        parsed_trees[tree_name] = rules
    return parsed_trees

def generate_tables(regras_dict: dict, features: dict, output_path: str, threshold: int = 0):
    parsed_trees = process_xgboost_rules(regras_dict, features)

    with open(output_path, "w") as f:
        for idx, fea in enumerate(features.keys()):
            max_value = get_datatype(fea) or 48
            features[fea].append(0)
            features[fea].append(2**max_value - 1)
            features[fea].sort()
            
            for i in range(len(features[fea]) - 1):
                range_str = f"{features[fea][i]}->{features[fea][i+1]}"
                f.write(f"table_add feature{idx+1}_exact set_actionselect{idx+1} {range_str} => {i+1} 0\n")
        
        for tree_idx, (tree_name, rules) in enumerate(parsed_trees.items()):
            table_name = f"tree{tree_idx}_exact"
            for rule in rules:
                ranges_str = ""
                for fea in features.keys():
                    a = rule["ranges"][fea]
                    ranges_str += f"{a[0] + 1}->{a[-1] + 1} "
                
                f.write(f"table_add {table_name} add_tree_weight {ranges_str.strip()} => {rule['weight']} 0\n")
        
        min_score = -2147483648
        max_score = 2147483647
        
        f.write(f"table_add apply_threshold set_final_result {min_score}->{threshold - 1} => 0 0\n")
        f.write(f"table_add apply_threshold set_final_result {threshold}->{max_score} => 1 0\n")
