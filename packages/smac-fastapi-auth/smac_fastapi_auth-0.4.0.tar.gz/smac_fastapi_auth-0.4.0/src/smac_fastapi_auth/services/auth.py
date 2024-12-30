from fastapi import HTTPException
from fastapi_cognito import CognitoAuth, CognitoSettings
from loguru import logger
from starlette.requests import Request

from ..automation.sec_mgr_helper import SecretsManagerHelper
from ..cognito.jwt_helper import CognitoJwtHelper
from ..core.constants import (
    ERROR_CODE_AUTH_ENFORCED_BUT_NOT_CONFIGURED,
    ERROR_CODE_AUTH_ENFORCED_PROVIDER_NOT_SUPPORTED,
)
from ..core.settings import AuthProvider, AuthSettings
from ..models.context import AuthenticatedContext
from ..models.principal import AuthenticatedPrincipal, PrincipalType


class AuthenticationService:
    def __init__(self, settings: AuthSettings):
        self._settings = settings

        if self._settings.provider == AuthProvider.cognito:
            self._cognito_auth = CognitoAuth(
                settings=CognitoSettings.from_global_settings(
                    self._settings.provider_cognito
                )
            )
            self._cognito_jwt_helper = CognitoJwtHelper(
                settings=self._settings.provider_cognito
            )

        if self._settings.automation_principals is not None:
            self._secrets_manager_helper = SecretsManagerHelper(
                settings=self._settings.automation_principals
            )

    async def enforce(self, request: Request) -> AuthenticatedContext:
        if self._settings.automation_principals is not None:
            # check if both headers are present, if so we assume it's an automation principal
            if request.headers.get(
                self._settings.automation_principals.id_header_name
            ) and request.headers.get(
                self._settings.automation_principals.token_header_name
            ):
                return await self._enforce_automation_principal(request)

        if self._settings.provider == AuthProvider.none:
            logger.error("No authentication provider is set, but auth is enforced.")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error (Code: {ERROR_CODE_AUTH_ENFORCED_BUT_NOT_CONFIGURED})",
            )

        if self._settings.provider == AuthProvider.cognito:
            return await self._enforce_cognito(request)

        raise HTTPException(
            status_code=500,
            detail=f"Internal server error (Code: {ERROR_CODE_AUTH_ENFORCED_PROVIDER_NOT_SUPPORTED})",
        )

    async def optional(self, request: Request) -> AuthenticatedContext:
        if self._settings.automation_principals is not None:
            # check if both headers are present, if so we assume it's an automation principal
            if request.headers.get(
                self._settings.automation_principals.id_header_name
            ) and request.headers.get(
                self._settings.automation_principals.token_header_name
            ):
                return await self._enforce_automation_principal(request)

        if self._settings.provider == AuthProvider.none:
            return AuthenticatedContext(
                principal=AuthenticatedPrincipal.create_anonymous()
            )

        if self._settings.provider == AuthProvider.cognito and request.headers.get(
            self._settings.provider_cognito.jwt_header_name
        ):
            return await self._enforce_cognito(request)

        return AuthenticatedContext(principal=AuthenticatedPrincipal.create_anonymous())

    async def _enforce_cognito(self, request: Request) -> AuthenticatedContext:
        # if the request is not authorized, this will raise an exception
        await self._cognito_auth.auth_required(request)
        # at this point the request is authorized, so we need to only resolve the principal
        auth_header_value = request.headers.get(
            self._settings.provider_cognito.jwt_header_name
        )
        try:
            principal_info = await self._cognito_jwt_helper.get_principal_info(
                auth_header_value
            )
            principal_id = principal_info.get(self._settings.user_id, None)
            if principal_id is None:
                logger.error("Principal ID not found in the principal information.")
                raise HTTPException(status_code=401, detail="Unauthorized")
            principal = AuthenticatedPrincipal(
                id=principal_id, principal_type=PrincipalType.User
            )
            return AuthenticatedContext(principal=principal)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=401, detail="Unauthorized")

    async def _enforce_automation_principal(
        self, request: Request
    ) -> AuthenticatedContext:
        principal_id = request.headers.get(
            self._settings.automation_principals.id_header_name
        )
        principal_token = request.headers.get(
            self._settings.automation_principals.token_header_name
        )

        # we don't need to check if the principal_id and principal_token are None,
        # because we already checked that in the calling function.

        try:
            secret_data = self._secrets_manager_helper.get_secret_data(principal_id)
            if secret_data.token != principal_token:
                logger.error("Token does not match the token in the secrets manager.")
                raise HTTPException(status_code=401, detail="Unauthorized")
            principal = AuthenticatedPrincipal(
                id=secret_data.id, principal_type=PrincipalType.Service
            )
            return AuthenticatedContext(principal=principal)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=401, detail="Unauthorized")
