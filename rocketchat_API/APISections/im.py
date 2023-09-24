from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatIM(RocketChatBase):
    async def im_list(self, **kwargs):
        """List the private im chats for logged user"""
        return await self.call_api_get("im.list", kwargs=kwargs)

    async def im_list_everyone(self, **kwargs):
        """List all direct message the caller in the server."""
        return await self.call_api_get("im.list.everyone", kwargs=kwargs)

    async def im_history(self, room_id, **kwargs):
        """Retrieves the history for a private im chat"""
        return await self.call_api_get("im.history", roomId=room_id, kwargs=kwargs)

    async def im_create(self, username, **kwargs):
        """Create a direct message session with another user."""
        return await self.call_api_post("im.create", username=username, kwargs=kwargs)

    async def im_create_multiple(self, usernames, **kwargs):
        """Create a direct message session with one or more users."""
        return await self.call_api_post(
            "im.create", usernames=",".join(usernames), kwargs=kwargs
        )

    async def im_open(self, room_id, **kwargs):
        """Adds the direct message back to the user's list of direct messages."""
        return await self.call_api_post("im.open", roomId=room_id, kwargs=kwargs)

    async def im_close(self, room_id, **kwargs):
        """Removes the direct message from the user's list of direct messages."""
        return await self.call_api_post("im.close", roomId=room_id, kwargs=kwargs)

    async def im_members(self, room_id):
        """Retrieves members of a direct message."""
        return await self.call_api_get("im.members", roomId=room_id)

    async def im_messages(self, room_id=None, username=None):
        """Retrieves direct messages from the server by username"""
        if room_id:
            return await self.call_api_get("im.messages", roomId=room_id)

        if username:
            return await self.call_api_get("im.messages", username=username)

        raise RocketMissingParamException("roomId or username required")

    async def im_messages_others(self, room_id, **kwargs):
        """Retrieves the messages from any direct message in the server"""
        return await self.call_api_get("im.messages.others", roomId=room_id, kwargs=kwargs)

    async def im_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the direct message"""
        return await self.call_api_post(
            "im.setTopic", roomId=room_id, topic=topic, kwargs=kwargs
        )

    async def im_files(self, room_id=None, user_name=None, **kwargs):
        """Retrieves the files from a direct message."""
        if room_id:
            return await self.call_api_get("im.files", roomId=room_id, kwargs=kwargs)
        if user_name:
            return await self.call_api_get("im.files", username=user_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or username required")

    async def im_counters(self, room_id, user_name=None):
        """Gets counters of direct messages."""
        if user_name:
            return await self.call_api_get("im.counters", roomId=room_id, username=user_name)
        return await self.call_api_get("im.counters", roomId=room_id)
