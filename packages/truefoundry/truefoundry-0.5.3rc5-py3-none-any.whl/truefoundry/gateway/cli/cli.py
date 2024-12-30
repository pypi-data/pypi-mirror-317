import click

from truefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from truefoundry.cli.display_util import print_entity_list
from truefoundry.gateway.lib.models import list_models


def get_gateway_cli():
    @click.group(cls=GROUP_CLS, help="Commands to interact with TrueFoundry Gateway")
    def gateway(): ...

    @gateway.group("list", cls=GROUP_CLS, help="List gateway resources")
    def list_group():
        """List gateway resources"""
        pass

    @list_group.command(
        "models", cls=COMMAND_CLS, help="List available models filtered by type"
    )
    @click.option(
        "--type",
        "model_type",
        type=click.Choice(["chat", "completion", "embedding"]),
        help="Filter models by type",
    )
    def list_models_cli(model_type: str):
        enabled_models = list_models(model_type)
        print_entity_list("Models", enabled_models)

    return gateway
