# pyright: reportAttributeAccessIssue=false

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import _tree


def extract_model(
    modelo: RandomForestClassifier,
    features: list[str],
):
    n_trees = len(modelo.estimators_)
    n_classes = modelo.n_classes_

    res = {
        "n_trees": n_trees,
        "n_classes": n_classes,
    }

    for i, estimator in enumerate(modelo.estimators_):
        tree_ = estimator.tree_

        tree_info = {
            "thresholds": {f: set() for f in features},
            "regras": [],
        }

        def _recurse(node, conditions):
            if tree_.children_left[node] == _tree.TREE_LEAF:
                classe = tree_.value[node].argmax()

                regra_str = f"when {' and '.join(conditions)} then {classe}"

                tree_info["regras"].append(regra_str)
                return

            feature = features[tree_.feature[node]]
            threshold = int(tree_.threshold[node])

            tree_info["thresholds"][feature].add(threshold)

            left_conditions = [f"{feature}<={threshold}"]
            _recurse(tree_.children_left[node], conditions + left_conditions)

            right_conditions = [f"{feature}>{threshold}"]
            _recurse(tree_.children_right[node], conditions + right_conditions)

        _recurse(0, [])

        for f_name in tree_info["thresholds"]:
            tree_info["thresholds"][f_name] = sorted(
                list(tree_info["thresholds"][f_name])
            )

        res[f"t{i+1}"] = tree_info

    return res
