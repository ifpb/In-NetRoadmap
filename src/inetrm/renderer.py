import os
from jinja2 import Environment, FileSystemLoader


def render_template(
    template_dir: str, template_file: str, context: dict, output_path: str
) -> None:
    env = Environment(
        loader=FileSystemLoader(searchpath=template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(template_file)
    rendered_content = template.render(**context)

    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(rendered_content)
