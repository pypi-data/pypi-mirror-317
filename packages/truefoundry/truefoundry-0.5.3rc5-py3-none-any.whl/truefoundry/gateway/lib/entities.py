from typing import Any, Dict, List, Optional, Union

from truefoundry.pydantic_v1 import BaseModel


class GatewayModel(BaseModel):
    id: str
    name: str
    provider: str
    model_id: Optional[str]
    provider_account_name: str
    tfy_application_id: Optional[str] = None
    enabled: bool = True
    types: Union[str, List[str]] = ""
    created_by: str
    tenant_name: str
    model_fqn: str

    def list_row_data(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_fqn,
            "provider": self.provider,
            "provider_model_id": self.model_id,
        }


class ProviderModels(BaseModel):
    __root__: Dict[str, Dict[str, List[GatewayModel]]]
