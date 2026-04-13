from .decision_tree import convert_decision_tree
from .random_forest import convert_random_forest


def convert(cfg: dict, model, p4_output_path: str, table_output_path: str):
    model_type = cfg.get("ml", {}).get("model")

    if model_type == "decision-tree":
        convert_decision_tree(cfg, model, p4_output_path, table_output_path)
    elif model_type == "random_forest":
        convert_random_forest(cfg, model, p4_output_path, table_output_path)
    else:
        raise ValueError(
            f"Unsupported model type defined in configuration: '{model_type}'"
        )
