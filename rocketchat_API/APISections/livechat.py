from rocketchat_API.APISections.base import RocketChatBase

class RocketChatLivechat(RocketChatBase):
    async def livechat_rooms(self, **kwargs):
        """Retrieves a list of livechat rooms."""
        return await self.call_api_get("livechat/rooms", kwargs=kwargs)

    async def livechat_inquiries_list(self, **kwargs):
        """Lists all of the open livechat inquiries."""
        return await self.call_api_get("livechat/inquiries.list", kwargs=kwargs)

    async def livechat_inquiries_take(self, inquiry_id, **kwargs):
        """Takes an open inquiry."""
        return await self.call_api_post(
            "livechat/inquiries.take", inquiryId=inquiry_id, kwargs=kwargs
        )

    async def livechat_get_users(self, user_type, **kwargs):
        """Get a list of agents or managers."""
        return await self.call_api_get("livechat/users/{}".format(user_type), kwargs=kwargs)

    async def livechat_create_user(self, user_type, **kwargs):
        """Register a new agent or manager."""
        return await self.call_api_post("livechat/users/{}".format(user_type), kwargs=kwargs)

    async def livechat_get_user(self, user_type, user_id, **kwargs):
        """Get info about an agent or manager."""
        return await self.call_api_get(
            "livechat/users/{}/{}".format(user_type, user_id), kwargs=kwargs
        )

    async def livechat_delete_user(self, user_type, user_id):
        """Removes an agent or manager."""
        return await self.call_api_delete("livechat/users/{}/{}".format(user_type, user_id))

    async def livechat_register_visitor(self, token, **kwargs):
        """Register a new Livechat visitor."""
        if "visitor" not in kwargs:
            kwargs["visitor"] = {}
        kwargs["visitor"]["token"] = token
        return await self.call_api_post("livechat/visitor", kwargs=kwargs)

    async def livechat_get_visitor(self, token):
        """Retrieve a visitor data."""
        return await self.call_api_get("livechat/visitor/{}".format(token))

    async def livechat_room(self, token, **kwargs):
        """Get the Livechat room data or open a new room."""
        return await self.call_api_get("livechat/room/", token=token, kwargs=kwargs)

    async def livechat_message(self, token, rid, msg, **kwargs):
        """Send a new Livechat message."""
        return await self.call_api_post(
            "livechat/message", token=token, rid=rid, msg=msg, kwargs=kwargs
        )

    async def livechat_messages_history(self, rid, token, **kwargs):
        """Load Livechat messages history."""
        return await self.call_api_get(
            "livechat/messages.history/{}".format(rid), token=token, kwargs=kwargs
        )
