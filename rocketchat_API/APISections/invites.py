from rocketchat_API.APISections.base import RocketChatBase


class RocketChatInvites(RocketChatBase):
    async def find_or_create_invite(self, rid, days, max_uses):
        """
        Creates or return an existing invite with the specified parameters.
        Requires the create-invite-links permission
        """
        return await self.call_api_post(
            "findOrCreateInvite", rid=rid, days=days, maxUses=max_uses
        )

    async def list_invites(self, **kwargs):
        """Lists all of the invites on the server. Requires the create-invite-links permission."""
        return await self.call_api_get("listInvites", kwargs=kwargs)
