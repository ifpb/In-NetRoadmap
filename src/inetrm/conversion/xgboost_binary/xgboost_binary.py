from .generate_p4 import generate_p4
from .generate_tables import generate_tables
from .read_model import exportar_regras_xgboost

def convert_xgboost_binary(
    cfg: dict, model, p4_output_path: str, table_output_path: str
) -> None:
    features_list = cfg["ml"]["features"]
    
    res = exportar_regras_xgboost(model, features_list)

    regras_dict = res.pop("regras")
    features_thresholds = res

    generate_p4(features_list, regras_dict, p4_output_path)
    generate_tables(regras_dict, features_thresholds, table_output_path)
