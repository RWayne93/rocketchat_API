from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase
from typing import Optional, Any
from httpx import Response

class RocketChatChat(RocketChatBase):
    async def chat_post_message(self, 
                                text: str,
                                room_id: Optional[str] = None,
                                channel: Optional[str] = None,
                                **kwargs: Any) -> Response:
        """Posts a new chat message."""
        if room_id:
            if text:
                return await self.call_api_post(
                    "chat.postMessage", roomId=room_id, text=text, **kwargs
                )
            return await self.call_api_post(
                "chat.postMessage", roomId=room_id, **kwargs)
        if channel:
            if text:
                return await self.call_api_post(
                    "chat.postMessage", channel=channel, text=text, **kwargs
                )
            return await self.call_api_post(
                "chat.postMessage", channel=channel, **kwargs
            )
        raise RocketMissingParamException("roomId or channel required")

    async def chat_send_message(self, message) -> Response:
        if "rid" in message:
            return self.call_api_post(
                "chat.sendMessage", message=message)
        raise RocketMissingParamException("message.rid required")

    async def chat_get_message(self, msg_id, **kwargs) -> Response:
        return await self.call_api_get("chat.getMessage", msgId=msg_id, kwargs=kwargs)

    async def chat_pin_message(self, msg_id, **kwargs) -> Response:
        return await self.call_api_post(
            "chat.pinMessage", messageId=msg_id, kwargs=kwargs)

    async def chat_unpin_message(self, msg_id, **kwargs) -> Response:
        return await self.call_api_post(
            "chat.unPinMessage", messageId=msg_id, kwargs=kwargs)

    async def chat_star_message(self, msg_id, **kwargs) -> Response:
        return await self.call_api_post(
            "chat.starMessage", messageId=msg_id, kwargs=kwargs)

    async def chat_unstar_message(self, msg_id, **kwargs) -> Response:
        return await self.call_api_post(
            "chat.unStarMessage", messageId=msg_id, kwargs=kwargs)

    async def chat_delete(self, room_id, msg_id, **kwargs) -> Response:
        """Deletes a chat message."""
        return await self.call_api_post(
            "chat.delete", roomId=room_id, msgId=msg_id, kwargs=kwargs
        )

    async def chat_update(self, room_id, msg_id, text, **kwargs) -> Response:
        """Updates the text of the chat message."""
        return await self.call_api_post(
            "chat.update", roomId=room_id, msgId=msg_id, text=text, kwargs=kwargs
        )

    async def chat_react(self, msg_id, emoji="smile", **kwargs) -> Response:
        """Updates the text of the chat message."""
        return await self.call_api_post(
            "chat.react", messageId=msg_id, emoji=emoji, kwargs=kwargs
        )

    async def chat_search(self, room_id, search_text, **kwargs) -> Response:
        """Search for messages in a channel by id and text message."""
        return await self.call_api_get(
            "chat.search", roomId=room_id, searchText=search_text, kwargs=kwargs
        )

    async def chat_get_message_read_receipts(self, message_id, **kwargs) -> Response:
        """Get Message Read Receipts"""
        return await self.call_api_get(
            "chat.getMessageReadReceipts", messageId=message_id, kwargs=kwargs
        )

    async def chat_get_starred_messages(self, room_id, **kwargs) -> Response:
        """Retrieve starred messages."""
        return await self.call_api_get(
            "chat.getStarredMessages", roomId=room_id, kwargs=kwargs
        )

    async def chat_report_message(self, message_id, description, **kwargs) -> Response:
        """Reports a message."""
        return await self.call_api_post(
            "chat.reportMessage",
            messageId=message_id,
            description=description,
            kwargs=kwargs,
        )

    async def chat_follow_message(self, mid, **kwargs) -> Response:
        """Follows a chat message to the message's channel."""
        return await self.call_api_post("chat.followMessage", mid=mid, kwargs=kwargs)
