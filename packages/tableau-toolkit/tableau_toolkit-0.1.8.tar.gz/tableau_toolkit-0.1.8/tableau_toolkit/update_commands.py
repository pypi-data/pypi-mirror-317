import click
import tableauserverclient as TSC
from .cli_utils import load_config
from .cli_utils import authenticate
from .cli_utils import get_csv_data


@click.group()
def update():
    """Update various Tableau resources"""


@update.group()
def users():
    """Update user attributes"""


@users.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-luid-col", default="site_luid", help="Column name for Site LUID")
@click.option(
    "--user-luid-col", default="object_luid", help="Column name for User LUID"
)
@click.option(
    "--val-col", default="object_email", help="Column name containing the new site role values"
)
@click.pass_context
def email(ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col):
    """Update user email addresses"""
    update_user_attribute(
        ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col, "email"
    )


@users.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-luid-col", default="site_luid", help="Column name for Site LUID")
@click.option(
    "--user-luid-col", default="object_luid", help="Column name for User LUID"
)
@click.option(
    "--val-col", default="object_full_name", help="Column name containing the new site role values"
)
@click.pass_context
def fullname(ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col):
    """Update user full names"""
    update_user_attribute(
        ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col, "fullname"
    )


@users.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-luid-col", default="site_luid", help="Column name for Site LUID")
@click.option(
    "--user-luid-col", default="object_luid", help="Column name for User LUID"
)
@click.option(
    "--val-col", default="site_role_name", help="Column name containing the new site role values"
)
@click.pass_context
def site_role(ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col):
    """Update user site roles"""
    update_user_attribute(
        ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col, "site_role"
    )


def update_user_attribute(
    ctx, file, stdin, delimiter, site_luid_col, user_luid_col, val_col, attribute
):
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    csv_data = get_csv_data(file, stdin, delimiter)

    for row in csv_data:
        site_luid = row[site_luid_col]
        user_luid = row[user_luid_col]
        new_value = row[val_col]

        try:
            # Switch to the specified site
            site = next(
                (site for site in TSC.Pager(server.sites) if site.id == site_luid), None
            )
            if not site:
                click.echo(f"Site with LUID '{site_luid}' not found", err=True)
                continue
            server.auth.switch_site(site)

            # Get the user
            user = server.users.get_by_id(user_luid)

            # Update the specified attribute
            setattr(user, attribute, new_value)
            server.users.update(user)
            click.echo(
                f"Updated {attribute} for user {user.name} ({user_luid}) on site {site.name} ({site_luid})"
            )

        except TSC.ServerResponseError as e:
            click.echo(f"Error updating user {user_luid}: {str(e)}", err=True)
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    server.auth.sign_out()
