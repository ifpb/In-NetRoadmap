
import tomli
import sys
import csv
import os
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

def initiate_jupyter(config):
    ipynb_file = Model.JUPYTER_MAPPING[config['ml']['model']]
    target = f"{os.path.dirname(os.path.abspath(__file__))}/jupyter"
    subprocess.run(["jupyter", "notebook", ipynb_file], cwd=target)
