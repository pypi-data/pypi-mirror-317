from enum import StrEnum

from pydantic import BaseModel, Field


class PrincipalType(StrEnum):
    User = "user"
    Service = "service"
    Anonymous = "anonymous"


class AuthenticatedPrincipal(BaseModel):
    id: str = Field(
        ...,
        description="The unique identifier of the principal.",
    )
    principal_type: PrincipalType = Field(
        ...,
        description="The type of the principal.",
    )

    # static method to create an anonymous principal
    @staticmethod
    def create_anonymous() -> "AuthenticatedPrincipal":
        return AuthenticatedPrincipal(
            id="anonymous", principal_type=PrincipalType.Anonymous
        )
