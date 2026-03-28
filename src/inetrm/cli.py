from inetrm.module_a import a_logic as a
import click

@click.group(invoke_without_command=True)
def main():
    click.echo("Rodando...")

@click.command()
@click.option("--config", default="config.toml", help="Path to the TOML configuration file.")
@click.pass_context
def train(ctx, config):
    ctx.ensure_object(dict)

    cfg = a.load_config(config)
    a.validate_model(cfg)

    mlmodel = cfg["ml"]["model"]
    mlfeatures = cfg["ml"]["features"]

    click.echo(f"Model: {mlmodel}")
    click.echo(f"Features: {mlfeatures}")


main.add_command(train)

if __name__ == "__main__":
    main()
