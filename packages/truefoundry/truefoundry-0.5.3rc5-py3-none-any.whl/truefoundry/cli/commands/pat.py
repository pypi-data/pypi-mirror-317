import click

from truefoundry.cli.console import console
from truefoundry.cli.const import COMMAND_CLS
from truefoundry.deploy.lib.clients.servicefoundry_client import (
    ServiceFoundryServiceClient,
)


@click.command(cls=COMMAND_CLS, name="generate-api-key")
@click.option(
    "--name",
    required=True,
    help="Name for the API key",
)
def generate_pat(name: str):
    """Generate a new Personal Access Token with specified name"""
    client = ServiceFoundryServiceClient()
    pat = client.create_pat(name)
    console.print(pat)


def get_generate_pat_command():
    return generate_pat
