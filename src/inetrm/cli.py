import pickle
from pathlib import Path
import os
import click

from inetrm import core
from inetrm.training import a_logic as a
from inetrm.conversion.decision_tree.generate_p4 import generate_p4
from inetrm.conversion.decision_tree.generate_tables import generate_tables
from inetrm.conversion.decision_tree.read_tree import exportar_regras_modelo
from inetrm.provision import provision_logic as c
# from inetrm.provisioning.copy_template import copy_yaml_template

@click.group()
@click.option(
    "--config",
    default=None,
    type=click.Path(),
    help="Path to the TOML configuration file.",
)
@click.pass_context
def main(ctx, config):
    ctx.ensure_object(dict)

    if ctx.invoked_subcommand == "init":
        return

    try:
        root_path = core.get_root()
        if config == None:
            config_path = root_path / "config.toml"
        else:
            config_path = Path(config)

        ctx.obj["root_path"] = root_path
        ctx.obj["config"] = core.load_config(str(config_path))

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
@click.option(
    "--verify",
    is_flag=True,
    default=False,
    help="Verifies if current directory is part of an inetrm project."
)
def init(output_dir, verify):
    click.secho("Initializing default configuration...", fg="cyan")

    if verify:
        try:
            project_root = core.get_root()
            click.secho(f"Project root found at {project_root}")
        except:
            click.secho("Project root not found.",err=True)
        finally:
            raise click.Abort()

    try:
        dest_path = core.run_init(output_dir)
        click.secho(f"Success! INETRM project initiated at: {dest_path}", fg="green")
        click.secho(
            "You can now edit the configuration file and proceed with development.", dim=True
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


@main.group(invoke_without_command=True)
@click.option(
    "-t",
    "--time",
    type=int,
    default=60,
    help="Provision duration"
)
@click.pass_context
def provision(ctx, time):
    try:
        chain = True if ctx.invoked_subcommand is None else False
        core.run_provision(ctx.obj['config'], chain, time)
    except Exception as e:
        click.secho(f"Provision failure: {e}", fg="red", err=True)
        raise click.Abort()

@provision.command()
@click.pass_context
def generate(ctx):
    try:
        c.generate(ctx.obj['config'], core.get_root() / "containernet" / "topology.py")
    except Exception as e:
        click.secho(f"Provision module failure: {e}", fg="red", err=True)
        raise click.Abort()

@provision.command()
@click.pass_context
def build(ctx):
    try:
        c.build(core.get_root())
    except Exception as e:
        click.secho(f"Provision module failure: {e}", fg="red", err=True)
        raise click.Abort()

@provision.command()
@click.option(
    "-t",
    "--time",
    type=int,
    default=60,
    help="Provision duration"
)
@click.pass_context
def up(ctx, time):
    try:
        params = c.get_params(core.get_root())
        c.up(params, time)
    except Exception as e:
        click.secho(f"Provision module failure: {e}", fg="red", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()
