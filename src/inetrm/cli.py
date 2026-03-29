from pathlib import Path

import click

from inetrm.module_a import a_logic as a


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--config",
    default="config.toml",
    type=click.Path(exists=True),
    help="Path to the TOML configuration file.",
)
@click.option(
    "--output-dir",
    default=str(Path.cwd()),
    type=click.Path(),
    help="Path to the output dir for artifacts.",
)
@click.argument("data", type=click.Path(exists=True))
@click.pass_context
def train(ctx, config, output_dir, data):
    ctx.ensure_object(dict)

    cfg = a.load_config(config)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    a.validate_model(cfg)
    a.validate_data(cfg, data)

    click.echo("Generating notebook...")
    notebook_path = a.create_notebook(cfg, data, output_dir)
    click.echo(click.style(f"Notebook created at: {notebook_path}", fg="green"))

    a.initiate_jupyter(notebook_path)


if __name__ == "__main__":
    main()
