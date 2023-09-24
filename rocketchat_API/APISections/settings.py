from rocketchat_API.APISections.base import RocketChatBase


class RocketChatSettings(RocketChatBase):
    async def settings_get(self, _id, **kwargs):
        """Gets the setting for the provided _id."""
        return await self.call_api_get("settings/" + _id, kwargs=kwargs)

    async def settings_update(self, _id, value, **kwargs):
        """Updates the setting for the provided _id."""
        return await self.call_api_post("settings/" + _id, value=value, kwargs=kwargs)

    async def settings(self, **kwargs):
        """List all private settings."""
        return await self.call_api_get("settings", kwargs=kwargs)

    async def settings_public(self, **kwargs):
        """List all private settings."""
        return await self.call_api_get("settings.public", kwargs=kwargs)

    async def settings_oauth(self, **kwargs):
        """List all OAuth services."""
        return await self.call_api_get("settings.oauth", kwargs=kwargs)

    async def settings_addcustomoauth(self, name, **kwargs):
        """Add a new custom OAuth service with the provided name."""
        return await self.call_api_post("settings.addCustomOAuth", name=name, kwargs=kwargs)

    async def service_configurations(self, **kwargs):
        """List all service configurations."""
        return await self.call_api_get("service.configurations", kwargs=kwargs)
