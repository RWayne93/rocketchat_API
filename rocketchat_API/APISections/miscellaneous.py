from rocketchat_API.APISections.base import RocketChatBase

class RocketChatMiscellaneous(RocketChatBase):
    # Miscellaneous information
    async def directory(self, query, **kwargs):
        """Search by users or channels on all server."""
        if isinstance(query, dict):
            query = str(query).replace("'", '"')

        return await self.call_api_get("directory", query=query, kwargs=kwargs)

    async def spotlight(self, query, **kwargs):
        """Searches for users or rooms that are visible to the user."""
        return await self.call_api_get("spotlight", query=query, kwargs=kwargs)
