import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException

@pytest.mark.asyncio
async def test_rooms_upload(logged_rocket):
    rooms_upload = await logged_rocket.rooms_upload(
        "GENERAL", file="tests/assets/avatar.png", description="hey there"
    )
    assert rooms_upload.get("success")


@pytest.mark.asyncio
async def test_rooms_get(logged_rocket):
    rooms_get = await logged_rocket.rooms_get()
    assert rooms_get.get("success")


@pytest.mark.asyncio
async def test_rooms_clean_history(logged_rocket):
    rooms_clean_history = await logged_rocket.rooms_clean_history(
        room_id="GENERAL",
        latest="2016-09-30T13:42:25.304Z",
        oldest="2016-05-30T13:42:25.304Z",
    )
    assert rooms_clean_history.get("success")


@pytest.mark.asyncio
async def test_rooms_favorite(logged_rocket):
    rooms_favorite = await logged_rocket.rooms_favorite(
        room_id="GENERAL", favorite=True
    )
    assert rooms_favorite.get("success")

    rooms_favorite = await logged_rocket.rooms_favorite(
        room_name="general", favorite=True
    )
    assert rooms_favorite.get("success")

    rooms_favorite = await logged_rocket.rooms_favorite(
        room_id="unexisting_channel", favorite=True
    )
    assert not rooms_favorite.get("success")

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.rooms_favorite()


@pytest.mark.asyncio
async def test_rooms_info(logged_rocket):
    rooms_infoby_name = await logged_rocket.rooms_info(room_name="general")
    assert rooms_infoby_name.get("success")
    assert rooms_infoby_name.get("room").get("_id") == "GENERAL"
    rooms_info_by_id = await logged_rocket.rooms_info(room_id="GENERAL")
    assert rooms_info_by_id.get("success")
    assert rooms_info_by_id.get("room").get("_id") == "GENERAL"
    with pytest.raises(RocketMissingParamException):
        await logged_rocket.rooms_info()


@pytest.mark.asyncio
async def test_rooms_create_discussion(logged_rocket):
    discussion_name = "this is a discussion"
    rooms_create_discussion = await logged_rocket.rooms_create_discussion(
        prid="GENERAL",
        t_name=discussion_name,
    )
    assert rooms_create_discussion.get("success")
    assert "discussion" in rooms_create_discussion
    assert rooms_create_discussion.get("discussion").get("fname") == discussion_name


@pytest.mark.asyncio
async def test_rooms_admin_rooms(logged_rocket):
    rooms_simple = await logged_rocket.rooms_admin_rooms()
    assert rooms_simple.get("success")

    # Using a room type filter does not seem to work
    offset = actual_count = 0
    res = {}
    while res.get("total") is None or res.get("total") > offset:
        res = await logged_rocket.rooms_admin_rooms(
            **{
                "types": [
                    "c",
                ],
                "offset": offset,
            }
        )
        assert res.get("success")
        offset += res.get("count")
        actual_count += len(list(filter(lambda x: "c" in x["t"], res.get("rooms"))))
    assert res.get("total") == actual_count

    rooms_with_filter = await logged_rocket.rooms_admin_rooms(**{"filter": "general"})
    assert rooms_with_filter.get("success")
    assert rooms_with_filter.get("rooms")[0].get("_id") == "GENERAL"
