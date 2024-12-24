import sys
import csv
import click
import tableauserverclient as TSC
from .cli_utils import load_config
from .cli_utils import authenticate
from .cli_utils import get_csv_data


@click.group()
def delete():
    """Delete various Tableau resources"""


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site LUID", help="Column name for Site LUID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option("--task-id-col", default="Task LUID", help="Column name for Task LUID")
@click.option(
    "--task-name-col", default="Schedule Name", help="Column name for Task Name"
)
@click.option(
    "--content-type-col", default="Content Type", help="Column name for Content Type"
)
@click.option(
    "--content-name-col", default="Content Name", help="Column name for Content Name"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def tasks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    task_id_col,
    task_name_col,
    content_type_col,
    content_name_col,
    owner_name_col,
):
    """Delete Tableau tasks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}
    csv_data = get_csv_data(file, stdin, delimiter)

    for row in csv_data:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        task_id = row[task_id_col]
        task_name = row[task_name_col]
        site_name = row[site_name_col]
        content_type = row[content_type_col]
        content_name = row[content_name_col]
        owner_name = row[owner_name_col]

        try:
            server.auth.switch_site(site)
            server.tasks.delete(task_id)
            click.echo(
                f"Successfully deleted task: {task_name} "
                f"(ID: {task_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Content: {content_type} - {content_name}")
            click.echo(f"Owner: {owner_name}")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting task {task_name} " f"(ID: {task_id}): {str(e)}",
                err=True,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    server.auth.sign_out()


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--workbook-id-col", default="Workbook ID", help="Column name for Workbook ID"
)
@click.option(
    "--workbook-name-col", default="Workbook Name", help="Column name for Workbook Name"
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def workbooks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    workbook_id_col,
    workbook_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau workbooks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        csv_data = sys.stdin
    elif file:
        with open(file, "r", encoding="utf-8", newline="") as csv_file:
            csv_data = csv.DictReader(csv_file, delimiter=delimiter)
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        workbook_id = row[workbook_id_col]
        workbook_name = row[workbook_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.workbooks.delete(workbook_id)
            click.echo(
                f"Successfully deleted workbook: {workbook_name} "
                f"(ID: {workbook_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting workbook {workbook_name} "
                f"(ID: {workbook_id}): {str(e)}",
                err=True,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    server.auth.sign_out()


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--datasource-id-col", default="Datasource ID", help="Column name for Datasource ID"
)
@click.option(
    "--datasource-name-col",
    default="Datasource Name",
    help="Column name for Datasource Name",
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def datasources(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    datasource_id_col,
    datasource_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau datasources specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        csv_data = sys.stdin
    elif file:
        with open(file, "r", encoding="utf-8", newline="") as csv_file:
            csv_data = csv.DictReader(csv_file, delimiter=delimiter)

    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        datasource_id = row[datasource_id_col]
        datasource_name = row[datasource_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.datasources.delete(datasource_id)
            click.echo(
                f"Successfully deleted datasource: {datasource_name} "
                f"(ID: {datasource_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting datasource {datasource_name} "
                f"(ID: {datasource_id}): {str(e)}",
                err=True,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()
