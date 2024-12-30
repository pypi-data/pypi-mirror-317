from enum import StrEnum
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from smac_fastapi_auth.automation.settings import AutomationPrincipalSettings
from smac_fastapi_auth.cognito.settings import ProviderCognitoSettings


class AuthProvider(StrEnum):
    none = "NONE"
    cognito = "COGNITO"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="SMAC__AUTH__",
    )
    user_id: str = Field(
        "email",
        description="The claim name to use as the unique user identifier, defaults to 'email'.",
    )
    provider: AuthProvider = Field(
        AuthProvider.none,
        description="The authentication provider to use, defaults to 'NONE'.",
    )
    provider_cognito: Optional[ProviderCognitoSettings] = Field(
        None,
        description="The settings for the Cognito authentication provider.",
    )
    automation_principals: Optional[AutomationPrincipalSettings] = Field(
        None,
        description="The settings for automation principals which do not connect with a regular provider.",
    )

    @model_validator(mode="after")
    def validate_chosen_provider(self):
        if self.provider == AuthProvider.cognito and self.provider_cognito is None:
            raise ValueError(
                "The provider is set to COGNITO, but the settings for Cognito are not provided."
            )

        return self
