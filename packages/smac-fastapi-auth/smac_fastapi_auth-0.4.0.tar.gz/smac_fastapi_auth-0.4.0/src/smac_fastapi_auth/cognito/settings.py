from typing import Any, Optional

from pydantic import BaseModel, Field, HttpUrl, field_serializer
from pydantic_settings import BaseSettings


class UserPoolSettings(BaseModel):
    region: str = Field(
        ...,
        description="The AWS region of the user pool.",
        max_length=100,
    )
    userpool_id: str = Field(
        ...,
        description="The id of the user pool.",
        max_length=100,
    )
    app_client_id: str = Field(
        ...,
        description="The id or ids of the app client/s.",
    )
    domain: HttpUrl = Field(
        ...,
        description="The domain of the user pool.",
    )

    @field_serializer("domain", return_type=str)
    def serialize_domain(self, value: HttpUrl):
        # return the domain without trailing slash
        return str(value)[:-1]


class UserPoolsSettings(BaseModel):
    primary: UserPoolSettings = Field(
        ...,
        description="The settings of the primary user pool.",
    )
    secondary: Optional[UserPoolSettings] = Field(
        None,
        description="The settings of the secondary user pool.",
    )


class ProviderCognitoSettings(BaseSettings):
    check_expiration: bool = Field(
        True,
        description="Check the token expiration, defaults to True.",
    )
    jwt_header_prefix: str = Field(
        "Bearer",
        description="The prefix for the JWT token in the header, defaults to 'Bearer'.",
        max_length=50,
    )
    jwt_header_name: str = Field(
        "Authorization",
        description="The header name for the JWT token, defaults to 'Authorization'.",
        max_length=50,
    )
    userpools: UserPoolsSettings = Field(
        ...,
        description="The settings of the primary and optional secondary user pools.",
    )

    # when model_dump is called, we need to return the userpools as a dict
    @field_serializer("userpools", return_type=dict[str, dict[str, Any]])
    def serialize_userpools(self, value: UserPoolsSettings):
        serialized = {
            "primary": value.primary.model_dump(),
        }
        if value.secondary:
            serialized["secondary"] = value.secondary.model_dump()
        print(serialized)
        return serialized
