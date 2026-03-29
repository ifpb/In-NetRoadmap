from pathlib import Path
import sys

import tomli


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.is_file():
        print(f"Error: Configure file '{config_path}' not found.")
        sys.exit(1)

    try:
        with open(path, "rb") as f:
            return tomli.load(f)
    except tomli.TOMLDecodeError as e:
        print(f"Error parsing TOML file: {e}")
        sys.exit(1)
