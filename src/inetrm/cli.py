import pickle
from pathlib import Path
import os
import click

from inetrm import core
from inetrm.training import a_logic as a
from inetrm.conversion.decision_tree.generate_p4 import generate_p4
from inetrm.conversion.decision_tree.generate_tables import generate_tables
from inetrm.conversion.decision_tree.read_tree import exportar_regras_modelo
from inetrm.provisioning.copy_template import copy_yaml_template


@click.group()
@click.option(
    "--config",
    default="config.toml",
    type=click.Path(),
    help="Path to the TOML configuration file.",
)
@click.pass_context
def main(ctx, config):
    ctx.ensure_object(dict)

    if ctx.invoked_subcommand == "init":
        return

    try:
        ctx.obj["config"] = core.load_config(config)
    except (FileNotFoundError, ValueError) as e:
        click.secho(str(e), fg="red", err=True)
        raise click.Abort()


@main.command()
@click.option(
    "--output-dir",
    default=str(Path.cwd()),
    type=click.Path(),
    help="Path to the output dir for artifacts.",
)
def init(output_dir):
    click.secho("Initializing default configuration...", fg="cyan")

    try:
        dest_path = core.run_init(output_dir)
        click.secho(f"Success! Created configuration at: {dest_path}", fg="green")
        click.secho(
            "You can now edit this file and run your training commands.", dim=True
        )

    except Exception as e:
        click.secho(f"Initialization skipped/failed: {e}", fg="yellow", err=True)
        raise click.Abort()


@main.command()
@click.option(
    "--output-dir",
    default=str(Path.cwd()),
    type=click.Path(),
    help="Path to the output dir for artifacts.",
)
@click.argument("data", type=click.Path(exists=True))
@click.pass_context
def train(ctx, output_dir, data):
    cfg = ctx.obj.get("config", {})

    click.secho("Validating configuration and generating notebook...", fg="cyan")

    try:
        notebook_path = core.run_train(cfg, data, output_dir)
        click.secho(f"Notebook created at: {notebook_path}", fg="green")

        a.initiate_jupyter(notebook_path)
    except Exception as e:
        click.secho(f"Training generation failed: {e}", fg="red", err=True)
        raise click.Abort()


@main.command()
@click.option(
    "--output-dir",
    default=str(Path.cwd()),
    type=click.Path(),
    help="Path to the output dir for artifacts.",
)
@click.argument("model-file", type=click.Path(exists=True))
@click.pass_context
def convert(ctx, output_dir, model_file):
    cfg = ctx.obj.get("config", {})

    click.secho("Generating P4 source code and table entries...", fg="cyan")

    try:
        paths = core.run_convert(cfg, model_file, output_dir)
        click.secho(f"P4 source generated at: {paths['p4_path']}", fg="green")
        click.secho(f"Table entries generated at: {paths['table_path']}", fg="green")
    except Exception as e:
        click.secho(f"Conversion failed: {e}", fg="red", err=True)
        raise click.Abort()


@main.command()
@click.option(
    "--output-dir",
    default=str(Path.cwd()),
    type=click.Path(),
    help="Path to the output dir for artifacts.",
)
@click.argument("p4-source", type=click.Path(exists=True))
@click.argument("table", type=click.Path(exists=True))
@click.pass_context
def provision(ctx, output_dir, p4_source, table):
    click.secho("Provisioning artifacts...", fg="cyan")

    try:
        core.run_provision(p4_source, table, output_dir)
        click.secho("Provisioning successful.", fg="green")
    except Exception as e:
        click.secho(f"Provisioning failed: {e}", fg="red", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
