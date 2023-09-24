from rocketchat_API.APISections.base import RocketChatBase


class RocketChatBanners(RocketChatBase):
    async def banners(self, platform, **kwargs):
        """Gets the banner to be shown to the authenticated user"""
        return await self.call_api_get(
            "banners",
            platform=platform,
            kwargs=kwargs,
        )
