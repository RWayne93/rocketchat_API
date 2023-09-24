from rocketchat_API.APISections.base import RocketChatBase


class RocketChatStatistics(RocketChatBase):
    async def statistics(self, **kwargs):
        """Retrieves the current statistics"""
        return await self.call_api_get("statistics", kwargs=kwargs)

    async def statistics_list(self, **kwargs):
        """Selectable statistics about the Rocket.Chat server."""
        return await self.call_api_get("statistics.list", kwargs=kwargs)
