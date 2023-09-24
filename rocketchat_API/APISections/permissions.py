from rocketchat_API.APISections.base import RocketChatBase

class RocketChatPermissions(RocketChatBase):
    async def permissions_list_all(self, **kwargs):
        """Returns all permissions from the server."""
        return await self.call_api_get("permissions.listAll", kwargs=kwargs)

    async def permissions_update(self, permissions, **kwargs):
        """Edits permissions on the server."""
        return await self.call_api_post(
            "permissions.update", permissions=permissions, kwargs=kwargs
        )
