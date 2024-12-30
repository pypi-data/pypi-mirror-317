import json

import boto3
from cachebox import TTLCache, cachedmethod
from pydantic import BaseModel, Field

from .settings import AutomationPrincipalSettings


class SecretData(BaseModel):
    id: str = Field(
        ...,
        description="The id of the service principal.",
    )
    token: str = Field(
        ...,
        description="The token of the service principal.",
    )


class SecretsManagerHelper:
    def __init__(self, settings: AutomationPrincipalSettings):
        self._settings = settings
        self._boto_session = boto3.Session(
            profile_name=self._settings.secrets_manager.profile,
        )
        self._client = self._boto_session.client(
            "secretsmanager",
            region_name=self._settings.secrets_manager.region,
        )

    @cachedmethod(cache=TTLCache(100, ttl=60))
    def get_secret_data(self, service_id: str) -> SecretData:
        safe_prefix = (
            self._settings.secrets_manager.common_prefix
            if self._settings.secrets_manager.common_prefix.endswith("/")
            else f"{self._settings.secrets_manager.common_prefix}/"
        )
        composed_secret_id = f"{safe_prefix}{service_id}"
        response = self._client.get_secret_value(
            SecretId=composed_secret_id,
        )
        if not response.get("SecretString", None):
            raise ValueError("Secret is not having string data.")
        # The SecretString is a JSON string
        data_dict = json.loads(response["SecretString"])
        return SecretData(**data_dict)
