import mimetypes
from typing import Any

from packaging import version

from rocketchat_API.APISections.base import RocketChatBase


class RocketChatAssets(RocketChatBase):
    async def assets_set_asset(
        self, asset_name: str, file: str, **kwargs: Any
    ) -> dict[str, Any] | None:
        """Set an asset image by name."""
        server_info = self.info().json()
        content_type = mimetypes.MimeTypes().guess_type(file)

        file_name = asset_name
        if version.parse(server_info.get("info").get("version")) >= version.parse(
            "5.1"
        ):
            file_name = "asset"

        files = {
            file_name: (file, open(file, "rb"), content_type[0], {"Expires": "0"}),
        }

        return await self.call_api_post(
            "assets.setAsset",
            kwargs=kwargs,
            assetName=asset_name,
            use_json=False,
            files=files,
        )

    async def assets_unset_asset(
        self, asset_name: str
    ) -> dict[str, Any] | None:
        """Unset an asset by name"""
        return await self.call_api_post("assets.unsetAsset", assetName=asset_name)