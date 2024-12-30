from pydantic import BaseModel, Field

from .principal import AuthenticatedPrincipal


class AuthenticatedContext(BaseModel):
    principal: AuthenticatedPrincipal = Field(
        ...,
        description="The authenticated principal.",
    )
