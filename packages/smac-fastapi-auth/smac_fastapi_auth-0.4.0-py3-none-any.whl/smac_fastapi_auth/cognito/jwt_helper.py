import aiohttp
from cachebox import TTLCache, cachedmethod

from .settings import ProviderCognitoSettings
from ..core.provider_helper import ProviderHelper


class CognitoJwtHelper(ProviderHelper):
    def __init__(self, settings: ProviderCognitoSettings):
        self.settings = settings

    @cachedmethod(cache=TTLCache(100, ttl=60))
    async def get_principal_info(self, auth_header_value: str) -> dict:
        """
        Get the principal information from the Cognito provider.

        Args:
            auth_header_value (str): The value of the Authorization header.

        Returns:
            dict: The principal information.
        """
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": auth_header_value,
            }
            async with session.get(
                f"{self.settings.userpools.primary.domain}/oauth2/userInfo",
                headers=headers,
            ) as response:
                response.raise_for_status()
                return await response.json()
