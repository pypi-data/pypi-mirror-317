import base64
from pathlib import Path
import click
import yaml
from .cli_utils import get_default_config_path
from .get_commands import get
from .create_commands import create
from .delete_commands import delete
from .download_commands import download
from .update_commands import update
from .add_commands import add


@click.group()
@click.option(
    "--config", default=get_default_config_path(), help="Path to the configuration file"
)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["config"] = config


# Add the command groups to the main CLI
cli.add_command(get)
cli.add_command(create)
cli.add_command(delete)
cli.add_command(download)
cli.add_command(update)
cli.add_command(add)


# Other top-level commands
@cli.command()
def init():
    """Initialize the tableau_toolkit configuration."""
    home_dir = Path.home()
    config_dir = home_dir / ".tableau_toolkit"
    config_file = config_dir / "tableau.yaml"

    if config_file.exists():
        click.echo("Configuration file already exists. Do you want to overwrite it?")
        if not click.confirm("Overwrite?"):
            click.echo("Initialization cancelled.")
            return

    config_dir.mkdir(exist_ok=True)

    default_config = {
        "tableau_server": {"url": "https://hostname"},
        "authentication": {"type": "tableau_auth"},
        "personal_access_token": {"name": "name", "secret": "secret"},
        "tableau_auth": {"username": "username", "password": "password"},
        "site": {"content_url": ""},
        "api": {"version": "3.24"},
        "postgres": {
            "host": "host",
            "port": 8060,
            "dbname": "workgroup",
            "user": "readonly",
            "password": "password",
        },
    }

    with config_file.open("w") as f:
        yaml.dump(default_config, f, default_flow_style=False)

    click.echo(f"Configuration file created at {config_file}")


@cli.command()
@click.argument("string")
def encode(string):
    """Encode a string using Base64 encoding."""
    encoded_bytes = base64.b64encode(string.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    click.echo(encoded_str)


@cli.command()
@click.argument("encoded_string")
def decode(encoded_string):
    """Decode a Base64 encoded string."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_str = decoded_bytes.decode("utf-8")
        click.echo(decoded_str)
    except UnicodeDecodeError as e:
        click.echo(f"Error decoding string: {e}")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
