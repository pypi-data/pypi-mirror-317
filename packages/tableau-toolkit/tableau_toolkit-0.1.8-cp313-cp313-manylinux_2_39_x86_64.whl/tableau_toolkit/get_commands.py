import click
from . import queries
from .cli_utils import execute_get_query


@click.group()
def get():
    """Get various Tableau resources"""


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--owner-id", default=None, help="Filter by owner id (system_user.name)")
@click.pass_context
def views(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, owner_id
):
    """Get views with usage data"""
    query = queries.get_views_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_id": owner_id,
    }
    execute_get_query(ctx, query, params, header_map)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--owner-id", default=None, help="Filter by owner id (system_user.name)")
@click.pass_context
def workbooks(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, owner_id
):
    """Get workbooks with usage data"""
    query = queries.get_workbooks_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_id": owner_id,
    }
    execute_get_query(ctx, query, params, header_map)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--owner-id", default=None, help="Filter by owner id (system_user.name)")
@click.pass_context
def datasources(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, owner_id
):
    """Get workbooks with usage data"""
    query = queries.get_datasources_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_id": owner_id,
    }
    execute_get_query(ctx, query, params, header_map)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="content_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--owner-id", default=None, help="Filter by owner id (system_user.name)")
@click.pass_context
def extract_refreshes(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, owner_id
):
    """Get extract refreshes with usage data"""
    query = queries.get_extract_refreshes_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_id": owner_id,
    }
    execute_get_query(ctx, query, params, header_map)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="content_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--owner-id", default=None, help="Filter by owner id (system_user.name)")
@click.pass_context
def subscriptions(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, owner_id
):
    """Get subscriptions with usage data"""
    query = queries.get_extract_refreshes_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_id": owner_id,
    }
    execute_get_query(ctx, query, params, header_map)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--owner-id", default=None, help="Filter by owner id (system_user.name)")
@click.pass_context
def data_alerts(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, owner_id
):
    """Get data alerts with usage data"""
    query = queries.get_data_alerts_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_id": owner_id,
    }
    execute_get_query(ctx, query, params, header_map)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--user-name", default=None, help="Filter by user name (system_user.name)"
)
@click.option(
    "--exclude-unlicensed", is_flag=True, help="Exclude unlicensed users"
)
@click.pass_context
def users(
    ctx, header_map, headers, sort_by, sort_order, limit, preview, site_name, user_name, exclude_unlicensed
):
    """Get data alerts with usage data"""
    query = queries.get_users_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "user_name": user_name,
        "exclude_unlicensed": exclude_unlicensed,
    }
    execute_get_query(ctx, query, params, header_map)
