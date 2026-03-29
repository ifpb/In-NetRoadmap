import pickle
from pathlib import Path

import click

from inetrm import core
from inetrm.module_a import a_logic as a
from inetrm.module_b.generate_p4 import generate_p4
from inetrm.module_b.generate_tables import generate_tables
from inetrm.module_b.read_tree import exportar_regras_modelo


@click.group()
@click.option(
    "--config",
    default="config.toml",
    type=click.Path(exists=True),
    help="Path to the TOML configuration file.",
)
@click.pass_context
def main(ctx, config):
    ctx.ensure_object(dict)

    ctx.obj["config"] = core.load_config(config)


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

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    a.validate_model(cfg)
    a.validate_data(cfg, data)

    click.echo("Generating notebook...")
    notebook_path = a.create_notebook(cfg, data, output_dir)
    click.echo(click.style(f"Notebook created at: {notebook_path}", fg="green"))

    a.initiate_jupyter(notebook_path)


@main.command()
@click.option(
    "--output-dir",
    default=str(Path.cwd()),
    type=click.Path(),
    help="Path to the output dir for artifacts.",
)
@click.argument("model-file", type=click.Path(exists=True))
@click.pass_context
def create_p4(ctx, output_dir, model_file):
    cfg = ctx.obj.get("config", {})

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    p4_output_path = str(out_dir / "decision_tree.p4")
    table_output_path = str(out_dir / "table.txt")

    with open(model_file, "rb") as f:
        model = pickle.load(f)

    features_list = cfg["ml"]["features"]

    res = exportar_regras_modelo(model, features_list)

    regras_list = res.pop("regras")
    features_thresholds = res

    click.secho("Generating P4 source code...", fg="green")

    generate_p4(
        features_list,
        p4_output_path,
    )

    click.secho("Generating table entries...", fg="green")

    generate_tables(
        regras_list,
        features_thresholds,
        table_output_path,
    )


if __name__ == "__main__":
    main()
