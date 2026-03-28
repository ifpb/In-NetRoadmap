from inetrm import core
import click

@click.group(invoke_without_command=True)
@click.option(
    "--config",
    default="config.toml",
    help="Path to the TOML configuration file."
)
@click.pass_context
def main(ctx, config):

    ctx.ensure_object(dict)

    cfg = core.load_config(config)

    mlmodel = cfg["ml"]["model"]
    mlfeatures = cfg["ml"]["features"]

    click.echo("Rodando...")
    click.echo(f"Model: {mlmodel}")
    click.echo(f"Features: {mlfeatures}")

if __name__ == "__main__":
    main()