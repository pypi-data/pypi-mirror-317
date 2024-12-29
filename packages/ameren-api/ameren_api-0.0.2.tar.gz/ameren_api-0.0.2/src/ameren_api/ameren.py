"""Base Ameren Class."""
import logging

from .ameren_client import AmerenClient

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class Ameren():
    """Define Ameren Class."""
    def __init__(
        self,
        username,
        password,
        debug = False,
    ):
        self._api_client = AmerenClient(username,password,debug)

        if debug:
            _LOGGER.setLevel(logging.DEBUG)
        
    async def get_token(self,session) -> str:
        """Get API Token from Ameren """
        token = await self._api_client._get_token(session)
        return token
    
    async def get_daily_usage(self,date_str) -> dict:
        """Get Daily Usage from Ameren """
        daily_usage = await self._api_client.get_daily_usage(date_str)
        return daily_usage

    async def get_monthly_usage(self,date_str) -> dict:
        """Get Monthly Usage from Ameren """
        monthly_usage = await self._api_client.get_monthly_usage(date_str)
        return monthly_usage

    async def get_yearly_usage(self,date_str) -> dict:
        """Get Yearly Usage from Ameren """
        yearly_usage = await self._api_client.get_yearly_usage(date_str)
        return yearly_usage