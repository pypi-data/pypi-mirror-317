from typing import List, Literal, Optional

from truefoundry.deploy.lib.clients.servicefoundry_client import (
    ServiceFoundryServiceClient,
)
from truefoundry.gateway.lib.entities import GatewayModel


def list_models(
    model_type: Optional[Literal["chat", "completion", "embedding"]] = None,
) -> List[GatewayModel]:
    """List available models filtered by type

    Args:
        model_type (Optional[str], optional): Filter models by type ('chat' or 'completion'). Defaults to None.

    Returns:
        List: List of enabled models
    """
    client = ServiceFoundryServiceClient()
    models = client.get_gateway_models(model_type)

    enabled_models = []
    for _, accounts in models.__root__.items():
        for _, model_list in accounts.items():
            for model in model_list:
                enabled_models.append(model)

    return enabled_models
