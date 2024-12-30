from abc import ABC, abstractmethod


class ProviderHelper(ABC):
    @abstractmethod
    async def get_principal_info(self, auth_header_value: str) -> dict:
        """
        Get the principal information from the provider.

        Args:
            auth_header_value (str): The value of the Authorization header.

        Returns:
            dict: The principal information.
        """
        raise NotImplementedError
