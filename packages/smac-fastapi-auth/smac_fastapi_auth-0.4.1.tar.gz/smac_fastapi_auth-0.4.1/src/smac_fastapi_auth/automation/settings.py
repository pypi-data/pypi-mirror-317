from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class SecretsManagerSettings(BaseModel):
    region: str = Field(
        ...,
        description="The AWS region of secrets manager.",
        max_length=100,
    )
    profile: Optional[str] = Field(
        None,
        description="The AWS profile to use.",
        max_length=100,
    )
    common_prefix: str = Field(
        "",
        description="The common prefix for all secrets.",
        max_length=50,
    )


class AutomationPrincipalSettings(BaseSettings):
    secrets_manager: SecretsManagerSettings = Field(
        ...,
        description="The settings for Secrets Manager.",
    )
    id_header_name: str = Field(
        "SMAC-Principal",
        description="The header name to use for the principal ID, defaults to `SMAC-Principal`.",
        max_length=50,
    )
    token_header_name: str = Field(
        "SMAC-Token",
        description="The header name to use for the token, defaults to `SMAC-Token`.",
        max_length=50,
    )
