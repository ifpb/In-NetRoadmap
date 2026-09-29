from .generate_p4 import generate_p4
from .generate_tables import generate_tables
from .read_tree import exportar_regras_modelo

def convert_decision_tree(cfg, model, p4_output_path, table_output_path):
    features_list = cfg["ml"]["features"]
    rules = exportar_regras_modelo(model, features_list)
    n_classes = len(model.classes_)

    generate_p4(features_list, p4_output_path,
                n_rules=len(rules), n_classes=n_classes)
    generate_tables(rules, features_list, table_output_path)
