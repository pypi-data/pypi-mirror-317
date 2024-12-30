import click
from datafact.proj import target_to_str, load_config


@click.group()
def target_cli():
    """Manage publishing targets."""
    pass


@target_cli.command()
@click.argument('label', type=str)
@click.option('--type', '-t', 'target_type',
              type=click.Choice(['local', 'remote'], case_sensitive=False),
              help='Specify the target type: [local, remote].')
@click.option('--name', type=str, help='target dataset name.')
@click.option('--host', type=str, default=None,
              help='Specify the host (required if type is remote).')
@click.option('--profile', type=str, default=None,
              help='Specify the profile (required if type is remote).')
def add(label, target_type, name, host, profile):
    """
    add a publishing target.
    """
    if not target_type:
        target_type = click.prompt('Target type is missing. Enter the type (local or remote)',
                                   type=click.Choice(['local', 'remote'], case_sensitive=False))
    if not name:
        name = click.prompt('Name is missing. Enter the name', type=str)

    # If type is remote, prompt for host and profile if missing
    if target_type.lower() == 'remote':
        if not host:
            host = click.prompt('Host is missing. Enter the host', type=str)
        if not profile:
            profile = click.prompt('Profile is missing. Enter the profile', type=str)

    click.echo(
        f"Configuration:\n  Type: {target_type}\n  Name: {name}\n  Host: {host if host else 'N/A'}\n  Profile: {profile if profile else 'N/A'}")

    cfg = load_config()
    cfg.add_target(target_type, name, host, profile, label=label)


@target_cli.command('list')
@click.option('--type', '-t', 'target_type',
              type=click.Choice(['local', 'remote'], case_sensitive=False),
              default=None,
              help='Filter by target type: [local, remote].')
def _list(target_type):
    """
    list publishing targets.
    """
    cfg = load_config()
    for label, target in cfg.list_targets(target_type):
        print(target_to_str(label, target))


@target_cli.command('remove')
@click.argument('label', type=str)
def remove(label):
    """
    remove a publishing target.
    """
    cfg = load_config()
    cfg.remove_target(label)
    cfg.save()


if __name__ == "__main__":
    target_cli()
