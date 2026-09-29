# pyright: reportAttributeAccessIssue=false

from sklearn.tree import _tree


def _simplify_conditions(conditions, features):
    """
    A partir de uma lista de (feature, sinal, threshold), calcula o
    intervalo [lo, hi] mais justo por feature.
    Convenção: lo default = 0; hi default = None (range completo).
    """
    bounds = {f: {"lo": 0, "hi": None} for f in features}

    for feature, sign, threshold in conditions:
        t = int(threshold)

        if sign == "<=":
            if bounds[feature]["hi"] is None or t < bounds[feature]["hi"]:
                bounds[feature]["hi"] = t
        else:  # ">"
            lo = t + 1
            if lo > bounds[feature]["lo"]:
                bounds[feature]["lo"] = lo

    return bounds


def exportar_regras_modelo(modelo, features):
    """
    Retorna uma lista de regras, uma por folha, com o intervalo
    [lo, hi] mais justo por feature (inteiros).
    """
    tree = modelo.tree_
    regras = []

    def _recursive(node, conditions):
        if tree.children_left[node] == _tree.TREE_LEAF:
            bounds = _simplify_conditions(conditions, features)
            regras.append({
                "bounds": bounds,
                "class": int(modelo.classes_[tree.value[node].argmax()]),
                "samples": int(tree.n_node_samples[node]),
            })
            return

        feature = features[tree.feature[node]]
        threshold = tree.threshold[node]

        _recursive(
            tree.children_left[node],
            conditions + [(feature, "<=", threshold)],
        )
        _recursive(
            tree.children_right[node],
            conditions + [(feature, ">", threshold)],
        )

    _recursive(0, [])
    return regras
