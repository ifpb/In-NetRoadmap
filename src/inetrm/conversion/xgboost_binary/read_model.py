import numpy as np

def exportar_regras_xgboost(
    modelo, 
    features: list[str], 
    scale_factor: int = 100000
):
    
    booster = modelo.get_booster()
    df_trees = booster.trees_to_dataframe()

    res = {f: [] for f in features}
    regras_por_arvore = {}

    for tree_id, tree_data in df_trees.groupby('Tree'):
        regras = []
        
        def _recursive(node_id_str, conditions):
            node = tree_data[tree_data['ID'] == node_id_str].iloc[0]
            
            if node['Feature'] == 'Leaf':
                scaled_weight = int(node['Gain'] * scale_factor)
                regras.append(
                    f"when {' and '.join(conditions)} then {scaled_weight}"
                )
                return

            feature = node['Feature']
            threshold = float(node['Split'])

            if feature in res and threshold not in res[feature]:
                res[feature].append(threshold)

            left_node_id = node['Yes']
            left_conditions = conditions + [f"{feature}<={threshold}"]
            _recursive(left_node_id, left_conditions)

            right_node_id = node['No']
            right_conditions = conditions + [f"{feature}>{threshold}"]
            _recursive(right_node_id, right_conditions)

        root_id = f"{tree_id}-0"
        _recursive(root_id, [])
        
        regras_por_arvore[f"tree_{tree_id}"] = regras

    res["regras"] = regras_por_arvore

    for feature in features:
        res[feature] = sorted(res[feature])

    return res
