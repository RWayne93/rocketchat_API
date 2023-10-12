from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketUnsuportedIntegrationType,
)
from rocketchat_API.APISections.base import RocketChatBase
from typing import Optional, Any
from httpx import Response


class RocketChatIntegrations(RocketChatBase):
    # pylint: disable=too-many-arguments
    async def integrations_create(
        self,
        integrations_type: str,
        name: str,
        enabled: bool,
        username: str,
        channel: str,
        script_enabled: bool,
        event: Optional[str] = None,
        urls: Optional[str] = None,
        **kwargs: Any
    ) -> Response:
        """Creates an integration."""
        if integrations_type == "webhook-outgoing":
            return await self.call_api_post(
                "integrations.create",
                type=integrations_type,
                name=name,
                enabled=enabled,
                event=event,
                urls=urls,
                username=username,
                channel=channel,
                scriptEnabled=script_enabled,
                kwargs=kwargs,
            )
        elif integrations_type == "webhook-incoming":
            return self.call_api_post(
                "integrations.create",
                type=integrations_type,
                name=name,
                enabled=enabled,
                username=username,
                channel=channel,
                scriptEnabled=script_enabled,
                kwargs=kwargs,
            )
        else:
            raise RocketUnsuportedIntegrationType()

    async def integrations_get(self, integration_id: str, **kwargs: Any) -> Response:
        """Retrieves an integration by id."""
        return await self.call_api_get(
            "integrations.get", integrationId=integration_id, kwargs=kwargs
        )

    async def integrations_history(self, integration_id: str, **kwargs: Any) -> Response:
        """Lists all history of the specified integration."""
        return await self.call_api_get(
            "integrations.history", id=integration_id, kwargs=kwargs
        )

    async def integrations_list(self, **kwargs: Any) -> Response:
        """Lists all of the integrations on the server."""
        return await self.call_api_get("integrations.list", kwargs=kwargs)

    async def integrations_remove(self, integrations_type: str, integration_id: str, **kwargs: Any) -> Response:
        """Removes an integration from the server."""
        return await self.call_api_post(
            "integrations.remove",
            type=integrations_type,
            integrationId=integration_id,
            kwargs=kwargs,
        )

    async def integrations_update(
        self,
        integrations_type: str,
        name: str,
        enabled: bool,
        username: str,
        channel: str,
        script_enabled: bool,
        integration_id: str,
        **kwargs: Any
    ) -> Response:
        """Updates an existing integration."""
        return await self.call_api_put(
            "integrations.update",
            type=integrations_type,
            name=name,
            enabled=enabled,
            username=username,
            channel=channel,
            scriptEnabled=script_enabled,
            integrationId=integration_id,
            kwargs=kwargs,
        )
