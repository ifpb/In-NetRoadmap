from pathlib import Path
import pickle
import shutil
import tomli

from inetrm.conversion.generate_p4 import generate_p4
from inetrm.conversion.generate_tables import generate_tables
from inetrm.conversion.read_tree import exportar_regras_modelo
from inetrm.provisioning.copy_template import copy_yaml_template
from inetrm.training import a_logic as a


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    try:
        with open(path, "rb") as f:
            return tomli.load(f)
    except tomli.TOMLDecodeError as e:
        raise ValueError(f"Error parsing TOML file: {e}")


def run_init(output_dir: str):
    dest_dir = Path(output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_path = dest_dir / "config.toml"

    if dest_path.exists():
        raise FileExistsError(
            f"A 'config.toml' already exists at: {dest_path.resolve()}"
        )

    source_path = Path(__file__).resolve().parent.parent.parent / "config.toml"

    if not source_path.is_file():
        raise FileNotFoundError(
            "Default configuration template 'config.toml' not found in the package."
        )

    shutil.copy(source_path, dest_path)
    return str(dest_path.resolve())


def run_train(cfg: dict, data_path: str, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    a.validate_model(cfg)
    a.validate_data(cfg, data_path)

    notebook_path = a.create_notebook(cfg, data_path, output_dir)
    return notebook_path


def run_convert(cfg: dict, model_file: str, output_dir: str) -> dict:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    p4_output_path = str(out_dir / "decision_tree.p4")
    table_output_path = str(out_dir / "table.txt")

    with open(model_file, "rb") as f:
        model = pickle.load(f)

    features_list = cfg["ml"]["features"]
    res = exportar_regras_modelo(model, features_list)

    regras_list = res.pop("regras")
    features_thresholds = res

    generate_p4(features_list, p4_output_path)
    generate_tables(regras_list, features_thresholds, table_output_path)

    return {
        "p4_path": p4_output_path,
        "table_path": table_output_path,
    }


def run_provision(p4_source: str, table: str, output_dir: str) -> None:
    ansible_dir = Path(output_dir) / "ansible"
    ansible_dir.mkdir(parents=True, exist_ok=True)

    copy_yaml_template(output_dir, p4_source, table)
