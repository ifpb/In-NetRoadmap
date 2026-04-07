import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import csv
import subprocess
from pathlib import Path

from .catalog import Model


def validate_model(cfg: dict) -> Model:
    try:
        model_name = cfg["ml"]["model"]
        features = cfg["ml"]["features"]

        ml = Model(model_name, features)
        print("Model Validated Successfully")
        return ml
    except KeyError as e:
        raise ValueError(f"Malformed configuration. Missing key: {e}")


def validate_data(cfg: dict, file_path: str) -> None:
    features = cfg["ml"]["features"]

    try:
        with open(file_path, "r", encoding="utf-8") as data:
            # Grab just the first line without loading the whole file into memory
            header = next(csv.reader(data))

            # Use sets to find the difference between what we need and what we have
            required_features = set(features)
            actual_header = set(header)

            missing_features = required_features - actual_header

            if missing_features:
                raise ValueError(
                    f"Dataset is missing required features: {missing_features}. "
                    f"Name your CSV header accordingly."
                )

    except StopIteration:
        raise ValueError(f"The dataset at {file_path} is completely empty.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the dataset at {file_path}.")

    print("Data Validated Successfully")


def create_notebook(cfg: dict, data: str, output_dir: str) -> str:
    model_name = cfg["ml"]["model"]
    ipynb_file = Model.JUPYTER_MAPPING[model_name]

    templates_dir = Path(__file__).resolve().parent / "jupyter"
    template_path = templates_dir / ipynb_file

    if not template_path.is_file():
        raise ValueError(f"Invalid template path: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    data_path = Path(data).resolve()
    out_dir = Path(output_dir).resolve()
    notebook_path = f"{out_dir}/{model_name}.ipynb"
    features_list = cfg["ml"]["features"]
    model_parameters = cfg.get("ml", {}).get("parameters", {})

    code_lines = [
        f"input_dataset = {repr(str(data_path))}",
        f"output_dir = {repr(str(out_dir))}",
        f"output_tree = {repr(str(out_dir / '/tree.txt'))}",
        f"features = {repr(features_list)}",
        f"model_parameters = {repr(model_parameters)}",
    ]

    vars_code = "\n".join(code_lines)

    md_cell = new_markdown_cell("# Variáveis")
    code_cell = new_code_cell(vars_code)

    nb.cells.insert(1, md_cell)
    nb.cells.insert(2, code_cell)

    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    return notebook_path


def initiate_jupyter(notebook_path):
    subprocess.run(["jupyter", "notebook", notebook_path])
