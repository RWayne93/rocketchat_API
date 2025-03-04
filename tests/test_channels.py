import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def add_owner(logged_rocket, user):
    """Add test user as owner in GENERAL channel in every test in this module"""
    await logged_rocket.channels_add_owner("GENERAL", username=user.name)


@pytest.fixture
@pytest.mark.asyncio
async def testuser_id(logged_rocket):
    testuser = (await logged_rocket.users_info(username="testuser1")).json()
    if not testuser.get("success"):
        testuser = (await logged_rocket.users_create(
            "testuser1@domain.com", "testuser1", "password", "testuser1"
        )).json()

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    await logged_rocket.users_delete(_testuser_id)

@pytest.mark.asyncio
async def test_channels_list(logged_rocket):
    channels_list = await logged_rocket.channels_list().json()
    assert channels_list.get("success")
    assert "channels" in channels_list

@pytest.mark.asyncio
async def test_channels_list_joined(logged_rocket):
    channels_list_joined = await logged_rocket.channels_list_joined().json()
    assert channels_list_joined.get("success")
    assert "channels" in channels_list_joined

@pytest.mark.asyncio
async def test_channels_info(logged_rocket):
    channels_info = await logged_rocket.channels_info(room_id="GENERAL").json()
    assert channels_info.get("success")
    assert "channel" in channels_info
    assert channels_info.get("channel").get("_id") == "GENERAL"

    channel_name = channels_info.get("channel").get("name")
    channels_info = await logged_rocket.channels_info(channel=channel_name).json()
    assert channels_info.get("success")
    assert "channel" in channels_info
    assert channels_info.get("channel").get("_id") == "GENERAL"
    assert channels_info.get("channel").get("name") == channel_name

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_info()


@pytest.mark.asyncio
async def test_channels_history(logged_rocket):
    channels_history = await logged_rocket.channels_history(room_id="GENERAL")
    assert channels_history.get("success")
    assert "messages" in channels_history


@pytest.mark.asyncio
async def test_channels_add_all(logged_rocket):
    channels_add_all = await logged_rocket.channels_add_all("GENERAL")
    assert channels_add_all.get("success")


@pytest.mark.asyncio
async def test_channels_add_and_remove_moderator(logged_rocket):
    me = (await logged_rocket.me()).json()
    channels_add_moderator = await logged_rocket.channels_add_moderator(
        "GENERAL", me.get("_id")
    )
    assert channels_add_moderator.get("success")
    channels_remove_moderator = await logged_rocket.channels_remove_moderator(
        "GENERAL", me.get("_id")
    )
    assert channels_remove_moderator.get("success")

@pytest.mark.asyncio
async def test_channels_list_moderator(logged_rocket):
    channels_list_moderator = await logged_rocket.channels_moderators(
        room_id="GENERAL"
    ).json()
    assert channels_list_moderator.get("success")
    channel_name = (
        await logged_rocket.channels_info(room_id="GENERAL").json().get("channel").get("name")
    )
    channels_list_moderator_by_name = logged_rocket.channels_moderators(
        channel=channel_name
    ).json()
    assert channels_list_moderator_by_name.get("success")
    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_moderators()

@pytest.mark.asyncio
async def test_channels_add_and_remove_owner(logged_rocket, testuser_id):
    channels_add_owner = await logged_rocket.channels_add_owner(
        "GENERAL", user_id=testuser_id
    ).json()
    assert channels_add_owner.get("success"), channels_add_owner.get("error")
    another_owner_id = (
        await logged_rocket.users_info(username="user1").json().get("user").get("_id")
    )
    logged_rocket.channels_add_owner("GENERAL", user_id=another_owner_id).json()
    channels_remove_owner = await logged_rocket.channels_remove_owner(
        "GENERAL", user_id=testuser_id
    ).json()
    assert channels_remove_owner.get("success"), channels_remove_owner.get("error")

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_add_owner(room_id="GENERAL")


@pytest.mark.asyncio
async def test_channels_add_and_remove_leader(logged_rocket, testuser_id):
    channels_invite = await logged_rocket.channels_invite("GENERAL", testuser_id)
    assert channels_invite.get("success")
    channels_add_leader = await logged_rocket.channels_add_leader(
        "GENERAL", user_id=testuser_id
    )
    assert channels_add_leader.get("success"), channels_add_leader.get("error")
    channels_remove_leader = await logged_rocket.channels_remove_leader(
        "GENERAL", user_id=testuser_id
    )
    assert channels_remove_leader.get("success"), channels_remove_leader.get("error")

@pytest.mark.asyncio
async def test_channels_archive_unarchive(logged_rocket):
    channels_archive = await logged_rocket.channels_archive("GENERAL")
    assert channels_archive.get("success")
    channels_unarchive = await logged_rocket.channels_unarchive("GENERAL")
    assert channels_unarchive.get("success")


@pytest.mark.asyncio
async def test_channels_close_open(logged_rocket):
    channels_close = await logged_rocket.channels_close("GENERAL")
    assert channels_close.get("success")
    channels_open = await logged_rocket.channels_open("GENERAL")
    assert channels_open.get("success")


@pytest.mark.asyncio
async def test_channels_create_delete(logged_rocket):
    name = str(uuid.uuid1())
    channels_create = await logged_rocket.channels_create(name)
    assert channels_create.get("success")
    assert name == channels_create.get("channel").get("name")
    channels_delete = await logged_rocket.channels_delete(channel=name)
    assert channels_delete.get("success")
    channels_create = await logged_rocket.channels_create(name)
    assert channels_create.get("success")
    room_id = channels_create.get("channel").get("_id")
    channels_delete = await logged_rocket.channels_delete(room_id=room_id)
    assert channels_delete.get("success")

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_delete()


@pytest.mark.asyncio
async def test_channels_get_integrations(logged_rocket):
    channels_get_integrations = await logged_rocket.channels_get_integrations(
        room_id="GENERAL"
    )
    assert channels_get_integrations.get("success")


@pytest.mark.asyncio
async def test_channels_invite(logged_rocket, testuser_id):
    channels_invite = await logged_rocket.channels_invite("GENERAL", testuser_id)
    assert channels_invite.get("success")


@pytest.mark.asyncio
async def test_channels_join(logged_rocket, testuser_id):
    name = str(uuid.uuid1())
    channels_create = await logged_rocket.channels_create(name)
    assert (
        await logged_rocket.channels_invite(
            room_id=channels_create.get("channel").get("_id"), user_id=testuser_id
        )
    ).get("success")

    assert (
        await logged_rocket.channels_add_owner(
            channels_create.get("channel").get("_id"), user_id=testuser_id
        )
    ).get("success")

    join_code = str(uuid.uuid1())
    channels_set_join_code = await logged_rocket.channels_set_join_code(
        channels_create.get("channel").get("_id"), join_code
    )
    assert channels_set_join_code.get("success")

    channels_leave = await logged_rocket.channels_leave(
        channels_create.get("channel").get("_id")
    )
    assert channels_leave.get("success")

    channels_join = await logged_rocket.channels_join(
        channels_create.get("channel").get("_id"), join_code
    )
    assert channels_join.get("success")

@pytest.mark.asyncio
async def test_channels_kick(logged_rocket, testuser_id):
    channels_kick = await logged_rocket.channels_kick("GENERAL", testuser_id).json()
    assert channels_kick.get("success")

@pytest.mark.asyncio
async def test_channels_leave(logged_rocket, testuser_id):
    channels_leave = await logged_rocket.channels_leave("GENERAL")
    assert not channels_leave.get("success")
    assert channels_leave.get("errorType") == "error-you-are-last-owner"

    name = str(uuid.uuid1())
    channels_create = await logged_rocket.channels_create(name)
    assert (
        await logged_rocket.channels_invite(
            room_id=channels_create.get("channel").get("_id"), user_id=testuser_id
        )
    ).get("success")

    assert (
        await logged_rocket.channels_add_owner(
            channels_create.get("channel").get("_id"), user_id=testuser_id
        )
    ).get("success")

    channels_leave = await logged_rocket.channels_leave(
        channels_create.get("channel").get("_id")
    )
    assert channels_leave.get("success")


@pytest.mark.asyncio
async def test_channels_rename(logged_rocket):
    name = str(uuid.uuid1())
    name2 = str(uuid.uuid1())
    channels_create = (await logged_rocket.channels_create(name)).json()
    channels_rename = (await logged_rocket.channels_rename(
        room_id=channels_create.get("channel").get("_id"), name=name2
    )).json()
    assert channels_rename.get("success")
    assert channels_rename.get("channel").get("name") == name2


@pytest.mark.asyncio
async def test_channels_set_description(logged_rocket):
    description = str(uuid.uuid1())
    channels_set_description = (await logged_rocket.channels_set_description(
        "GENERAL", description
    )).json()
    assert channels_set_description.get("success")
    assert (
        channels_set_description.get("description") == description
    ), "Description does not match"


@pytest.mark.asyncio
async def test_channels_set_join_code(logged_rocket):
    join_code = str(uuid.uuid1())
    channels_set_join_code = (await logged_rocket.channels_set_join_code(
        "GENERAL", join_code
    )).json()
    assert channels_set_join_code.get("success")


@pytest.mark.asyncio
async def test_channels_set_read_only(logged_rocket):
    channels_set_read_only = (await logged_rocket.channels_set_read_only(
        "GENERAL", True
    )).json()
    assert channels_set_read_only.get("success")
    channels_set_read_only = (await logged_rocket.channels_set_read_only(
        "GENERAL", False
    )).json()
    assert channels_set_read_only.get("success")


@pytest.mark.asyncio
async def test_channels_set_topic(logged_rocket):
    topic = str(uuid.uuid1())
    channels_set_topic = (await logged_rocket.channels_set_topic("GENERAL", topic)).json()
    assert channels_set_topic.get("success")
    assert channels_set_topic.get("topic") == topic, "Topic does not match"


@pytest.mark.asyncio
async def test_channels_set_type(logged_rocket):
    name = str(uuid.uuid1())
    channels_create = (await logged_rocket.channels_create(name)).json()
    assert channels_create.get("success")

    channels_set_type = (await logged_rocket.channels_set_type(
        channels_create.get("channel").get("_id"), "p"
    )).json()
    assert channels_set_type.get("success")
    assert channels_set_type.get("channel").get("t"), "p"

    channels_set_type = (await logged_rocket.channels_set_type(
        channels_create.get("channel").get("_id"), "c"
    )).json()
    # should fail because this is no more a channel
    assert not channels_set_type.get("success")


@pytest.mark.asyncio
async def test_channels_set_announcement(logged_rocket):
    announcement = str(uuid.uuid1())
    channels_set_announcement = (await logged_rocket.channels_set_announcement(
        "GENERAL", announcement
    )).json()
    assert channels_set_announcement.get("success")
    assert (
        channels_set_announcement.get("announcement") == announcement
    ), "Topic does not match"


@pytest.mark.asyncio
async def test_channels_set_custom_fields(logged_rocket):
    cf = {"key": "value"}
    channels_set_custom_fields = (
        await logged_rocket.channels_set_custom_fields("GENERAL", cf)
    ).json()
    assert channels_set_custom_fields.get("success")
    assert cf == channels_set_custom_fields["channel"]["customFields"]


@pytest.mark.asyncio
async def test_channels_members(logged_rocket):
    channels_members = (await logged_rocket.channels_members(room_id="GENERAL")).json()
    assert channels_members.get("success")
    channels_members = (await logged_rocket.channels_members(channel="general")).json()
    assert channels_members.get("success")

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_members()


@pytest.mark.asyncio
async def test_channels_roles(logged_rocket):
    channels_roles = (await logged_rocket.channels_roles(room_id="GENERAL")).json()
    assert channels_roles.get("success")
    assert channels_roles.get("roles") is not None
    channels_roles = (await logged_rocket.channels_roles(room_name="general")).json()
    assert channels_roles.get("success")
    assert channels_roles.get("roles") is not None

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_roles()


@pytest.mark.asyncio
async def test_channels_files(logged_rocket):
    channels_files = (await logged_rocket.channels_files(room_id="GENERAL")).json()
    assert channels_files.get("success")

    channels_files = (await logged_rocket.channels_files(room_name="general")).json()
    assert channels_files.get("success")

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_files()


@pytest.mark.asyncio
async def test_channels_get_all_user_mentions_by_channel(logged_rocket):
    channels_get_all_user_mentions_by_channel = (
        await logged_rocket.channels_get_all_user_mentions_by_channel(
            room_id="GENERAL"
        )
    ).json()
    assert channels_get_all_user_mentions_by_channel.get("success")


@pytest.mark.asyncio
async def test_channels_counters(logged_rocket):
    channels_counters = (await logged_rocket.channels_counters(room_id="GENERAL")).json()
    assert channels_counters.get("success")
    channels_counters_by_name = (
        await logged_rocket.channels_counters(room_name="general")
    ).json()
    assert channels_counters_by_name.get("success")
    with pytest.raises(RocketMissingParamException):
        await logged_rocket.channels_counters()


@pytest.mark.asyncio
async def test_channels_online(logged_rocket):
    channels_online = (
        await logged_rocket.channels_online(query={"_id": "GENERAL"})
    ).json()
    assert channels_online.get("success")
    assert len(channels_online.get("online")) >= 1


@pytest.mark.skip(reason="Broken in 6.3")
def test_channels_set_default(logged_rocket):
    channels_set_default = logged_rocket.channels_set_default(
        room_id="GENERAL", default=False
    ).json()
    assert channels_set_default.get("success")
    assert channels_set_default.get("channel").get("default") is False
    channels_set_default = logged_rocket.channels_set_default(
        room_id="GENERAL", default=True
    ).json()
    assert channels_set_default.get("channel").get("default")
