from .generate_p4 import generate_p4
from .generate_tables import generate_tables
from .read_tree import exportar_regras_modelo


def convert_decision_tree(
    cfg: dict, model, p4_output_path: str, table_output_path: str
) -> None:
    features_list = cfg["ml"]["features"]
    res = exportar_regras_modelo(model, features_list)

    regras_list = res.pop("regras")
    features_thresholds = res

    generate_p4(features_list, p4_output_path)
    generate_tables(regras_list, features_thresholds, table_output_path)
