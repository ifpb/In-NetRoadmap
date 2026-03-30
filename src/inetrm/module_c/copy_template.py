import shutil
from pathlib import Path


def copy_yaml_template(output_dir: str):
    current_dir = Path(__file__).parent
    out_dir = Path(output_dir)

    shutil.copy(current_dir / "host-1.yml", out_dir / "ansible")
    shutil.copy(current_dir / "host-2.yml", out_dir / "ansible")
    shutil.copy(current_dir / "table_ipv4.txt", out_dir / "ansible")
    shutil.copy(current_dir / "Vagrantfile", out_dir)
    shutil.copy(current_dir / "ansible.cfg", out_dir)
    shutil.copy(current_dir / "inventory.ini", out_dir)

