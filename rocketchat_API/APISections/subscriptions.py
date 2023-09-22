from rocketchat_API.APISections.base import RocketChatBase


class RocketChatSubscriptions(RocketChatBase):
    async def subscriptions_get(self, **kwargs):
        """Get all subscriptions."""
        return await self.call_api_get("subscriptions.get", kwargs=kwargs)

    async def subscriptions_get_one(self, room_id, **kwargs):
        """Get the subscription by room id."""
        return await self.call_api_get("subscriptions.getOne", roomId=room_id, kwargs=kwargs)

    async def subscriptions_unread(self, room_id, **kwargs):
        """Mark messages as unread by roomId or from a message"""
        return await self.call_api_post("subscriptions.unread", roomId=room_id, kwargs=kwargs)

    async def subscriptions_read(self, rid, **kwargs):
        """Mark room as read"""
        return await self.call_api_post("subscriptions.read", rid=rid, kwargs=kwargs)
