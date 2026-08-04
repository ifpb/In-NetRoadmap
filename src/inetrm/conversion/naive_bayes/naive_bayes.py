from .generate_p4 import generate_p4
from .generate_tables import generate_tables
from .read_model import extract_model

def convert_naive_bayes(
    cfg: dict, model, p4_output_path: str, table_output_path: str
) -> None:
    """
    Função principal que orquestra a conversão de um modelo Gaussian Naive Bayes
    treinado em código P4 e tabelas de roteamento correspondentes.
    """
    features_list = cfg["ml"]["features"]
    res = extract_model(model, features_list)
    n_classes = len(res["classes"])
    generate_p4(n_classes, features_list, p4_output_path)
    generate_tables(res, table_output_path)
