from inetrm.conversion.random_forest.generate_p4 import generate_p4
from inetrm.conversion.random_forest.generate_table import generate_table
from inetrm.conversion.random_forest.read_model import extract_model


def convert_random_forest(
    cfg: dict, model, p4_output_path: str, table_output_path: str
) -> None:
    features_list = cfg["ml"]["features"]
    res = extract_model(model, features_list)

    generate_p4(res["n_trees"], res["n_classes"], features_list, p4_output_path)
    generate_table(res, table_output_path)
