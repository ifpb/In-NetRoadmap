# pyright: reportAttributeAccessIssue=false

from sklearn.tree import DecisionTreeClassifier, _tree


def exportar_regras_modelo(
    modelo: DecisionTreeClassifier,
    features: list[str],
):

    def _add_value(table, key, value):
        # value = int(new_value)
        if key not in table:
            table[key] = []
            table[key].append(value)
            return

        if value not in table[key]:
            table[key].append(value)

    res = {}

    regras = []

    def _recursive(node, conditions):
        if modelo.tree_.children_left[node] == _tree.TREE_LEAF:
            regras.append(
                f"when {' and '.join(conditions)} then {modelo.tree_.value[node].argmax()}"
            )
            return

        feature = features[modelo.tree_.feature[node]]
        threshold = int(modelo.tree_.threshold[node])

        _add_value(res, feature, threshold)

        left_conditions = conditions + [f"{feature}<={threshold}"]
        _recursive(modelo.tree_.children_left[node], left_conditions)

        right_conditions = conditions + [f"{feature}>{threshold}"]
        _recursive(modelo.tree_.children_right[node], right_conditions)

    _recursive(0, [])

    res["regras"] = regras

    for feature in features:
        try:
            res[feature] = sorted(res[feature])
        except:
            res[feature] = []

    return res
