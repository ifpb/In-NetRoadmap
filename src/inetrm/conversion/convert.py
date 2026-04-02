from decision_tree import convert_decision_tree


def convert(cfg: dict, model, p4_output_path: str, table_output_path: str):
    model_type = cfg.get("ml", {}).get("model_type")

    if model_type == "decision_tree":
        convert_decision_tree(cfg, model, p4_output_path, table_output_path)

    else:
        raise ValueError(
            f"Unsupported model type defined in configuration: '{model_type}'"
        )
