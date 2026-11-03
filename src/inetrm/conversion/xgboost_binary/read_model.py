import numpy as np
import math

def exportar_regras_xgboost(
    modelo, 
    features: list[str]
):
    booster = modelo.get_booster()
    df_trees = booster.trees_to_dataframe()

    # Bounding: encontra limite extremo das arvores
    max_sum = 0
    min_sum = 0
    for tree_id, tree_data in df_trees.groupby('Tree'):
        leaves = tree_data[tree_data['Feature'] == 'Leaf']['Gain']
        max_sum += leaves.max()
        min_sum += leaves.min()

    limite_absoluto = max(abs(max_sum), abs(min_sum))
    if limite_absoluto == 0: 
        limite_absoluto = 1

    # Escala Dinamica baseada no range maximo do uint32
    espaco_disponivel = (2**31) - 1
    escala_maxima = espaco_disponivel / limite_absoluto
    fator_escala = 2 ** math.floor(math.log2(escala_maxima))

    # Score Base focado em 2^31
    base_score_real = float(booster.attr('base_score') or 0.5)
    base_log_odds = math.log(base_score_real / (1 - base_score_real)) if base_score_real != 0.5 else 0.0
    score_inicial = int((2**31)) + int(round(base_log_odds * fator_escala))

    res = {f: [] for f in features}
    regras_por_arvore = {}

    for tree_id, tree_data in df_trees.groupby('Tree'):
        regras = []
        
        def _recursive(node_id_str, conditions):
            node = tree_data[tree_data['ID'] == node_id_str].iloc[0]
            
            if node['Feature'] == 'Leaf':
                weight = int(round(node['Gain'] * fator_escala))
                action = "add" if weight >= 0 else "sub"
                regras.append(
                    f"when {' and '.join(conditions)} then {action} {abs(weight)}"
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
    res["score_inicial"] = score_inicial

    for feature in features:
        res[feature] = sorted(res[feature])

    return res
