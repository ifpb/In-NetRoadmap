from pathlib import Path

import click

from inetrm.module_a import a_logic as a


@click.group(invoke_without_command=True)
def main():
    click.echo("Rodando...")


@click.command()
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

    Path(output_dir).mkdir

    a.validate_model(cfg)
    a.validate_data(cfg, data)
    notebook_path = a.create_notebook(cfg, data, output_dir)
    click.echo(notebook_path)
    # a.create_symlink(config, data)
    a.initiate_jupyter(notebook_path)


main.add_command(train)

if __name__ == "__main__":
    main()
