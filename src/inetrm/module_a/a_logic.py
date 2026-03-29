import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import tomli
import sys
import csv
import subprocess
from pathlib import Path
from inetrm.module_a.catalog import Model


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.is_file():
        print(f"Error: Configure file '{config_path}' not found.")
        sys.exit(1)
    
    try:
        with open(path, 'rb') as f:
            return tomli.load(f)
    except tomli.TOMLDecodeError as e:
        print(f"Error parsing TOML file: {e}")
        sys.exit(1)


def validate_model(cfg):
    ml = Model(cfg['ml']['model'], cfg['ml']['features'])
    print("Model Validated")

def validate_data(cfg, file_path):
    with open(file_path, 'r', encoding='utf-8') as data:
        header = next(csv.reader(data))
        for feature in cfg['ml']['features']:
            assert feature in header, f"No match for {feature} found in dataset. Name your CSV header accordingly."


def create_symlink(config, data):
    target = f"{os.path.dirname(os.path.abspath(__file__))}/jupyter"

    if os.path.islink(f"{target}/data.csv"): os.unlink(f"{target}/data.csv")
    if os.path.islink(f"{target}/config.toml"): os.unlink(f"{target}/config.toml")

    os.symlink(f"{os.getcwd()}/{data}", f"{target}/data.csv")
    os.symlink(f"{os.getcwd()}/{config}", f"{target}/config.toml")

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

    vars_code = "\n".join(
        [
            f"input_dataset = {repr(str(data_path))}",
            f'output_dir = "{out_dir}"',
            f'output_tree = "{out_dir}/tree.txt"',
            f"features = {repr(features_list)}",
        ]
    )

    md_cell = new_markdown_cell("# Variáveis")
    code_cell = new_code_cell(vars_code)

    nb.cells.insert(1, md_cell)
    nb.cells.insert(2, code_cell)

    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    return notebook_path


def initiate_jupyter(notebook_path):
    subprocess.run(["jupyter", "notebook", notebook_path])
