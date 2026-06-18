from pathlib import Path
import pickle
import shutil
import tomli

from inetrm.conversion import convert
# from inetrm.provisioning.copy_template import copy_yaml_template
from inetrm.training import a_logic as a


def get_root(start_path: str | Path = None, marker: str = ".inetrm"):
    current_path = Path(start_path or Path.cwd()).resolve()
    if (current_path / marker).exists():
        return current_path
    if (current_path == current_path.parent):
        raise FileNotFoundError (
                f"Direcotry is not part of an inetrm project"
    )
    
    return get_root(current_path.parent)

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
    dest_path = Path(output_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    if (dest_path / '.inetrm').exists():
        raise FileExistsError(
            f"{dest_path.resolve()} is already an INETRM project."
        )

    (dest_path / '.inetrm').mkdir(parents=True, exist_ok=True)
    source_path = (Path(__file__).parent / 'init').resolve()

    if not (source_path / 'config.toml').is_file():
        raise FileNotFoundError(
            "Default configuration template 'config.toml' not found in package."
        )

    shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
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

    model_type = cfg.get("ml", {}).get("model")
    p4_output_path = str(out_dir / f"{model_type}.p4")
    table_output_path = str(out_dir / "table.txt")

    with open(model_file, "rb") as f:
        model = pickle.load(f)

    convert(cfg, model, p4_output_path, table_output_path)

    return {
        "p4_path": p4_output_path,
        "table_path": table_output_path,
    }


def run_provision(p4_source: str, table: str, output_dir: str) -> None:
    ...
