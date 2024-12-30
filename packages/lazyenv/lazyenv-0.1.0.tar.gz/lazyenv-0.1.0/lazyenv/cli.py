from importlib.metadata import version as get_version
import click

from lazyenv.main import generate_env_file

@click.group()
@click.version_option(get_version("lazyenv"))
def cli():
    """CLI for LazyEnv."""
    pass

@cli.command()
@click.option("-g","--incl-global", is_flag=True, help="Load global enviroment variables")
@click.option("-l","--incl-local", type=bool, default=True, help="Load local enviroment variables. Default 'True'")
def init(incl_global=False, incl_local=True):
    """Init LazyEnv for accessing env variables with dot notation."""
    
    if not incl_global and not incl_local:
        click.echo('No enviroment variables loaded.')
        return

    generate_env_file(incl_global, incl_local)

    sources = [source for source, include in [('global', incl_global), ('local', incl_local)] if include]   
    message = f"Environment variables loaded from {(' and '.join(sources))} source{'s' * (len(sources) > 1)}."
    click.echo(message)

# TODO
# @cli.command()
# def sync():
#     """Sync environment variables."""
#     pass

if __name__ == '__main__':
    cli()