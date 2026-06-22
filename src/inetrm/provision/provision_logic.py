from pathlib import Path
from ..renderer import render_template

def generate(cfg, output_path):
    context = cfg["provision"]

    template_dir = (Path(__file__).parent / "templates").resolve()
    template_file = "topology.py.j2"

    output_path = Path(output_path)

    render_template(str(template_dir), template_file, context, str(output_path))

def provision():
    ...
