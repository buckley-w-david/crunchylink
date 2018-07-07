import click
from crunchyroll.apis.android import AndroidApi
import crunchyroll

@click.group()
@click.option("--username", required=True, envvar="CRUNCHYROLL_USERNAME")
@click.option("--password", envvar="CRUNCHYROLL_PASSWORD")
@click.option(
    "--stdin-password", is_flag=True, default=False, help="Read password in from stdin"
)
@click.pass_context
def main(
    ctx: click.core.Context,
    username: str,
    password: str,
    stdin_password: bool,
) -> None:
    if not (password or stdin_password):
        raise click.UsageError("Must supply one of `password` or `stdin_password`")

    if stdin_password:
        password = input()
    ctx.obj = api = AndroidApi()
    api.start_session()
    api.login(account=username, password=password)


@main.command()
@click.option(
    '--series-id',
    required=True,
    type=int
)
@click.option('--offset', type=int, default=0)
@click.pass_context
def play_series(ctx: click.core.Context, series_id: int, offset: int):
    api = ctx.obj
    media = api.list_media(series_id=series_id, offset=offset)
    click.echo(media)
    try:
        api.logout()
    except KeyError:
        pass # logout throws a KeyError
    api.end_session()


