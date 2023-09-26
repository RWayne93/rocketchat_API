import pytest

@pytest.mark.asyncio
async def test_assets_set_asset(logged_rocket):
    assets_set_asset = await logged_rocket.assets_set_asset(
        asset_name="logo", file="tests/assets/logo.png"
    )
    assert assets_set_asset.get("success")

@pytest.mark.asyncio
async def test_assets_unset_asset(logged_rocket):
    assets_unset_asset = await logged_rocket.assets_unset_asset(asset_name="logo")
    assert assets_unset_asset.get("success")