import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException

@pytest.mark.asyncio
async def test_chat_post_notext_message(logged_rocket):
    chat_post_message = await logged_rocket.chat_post_message(None, channel="GENERAL").json()
    assert chat_post_message.get("channel") == "GENERAL"
    assert chat_post_message.get("message").get("msg") == ""
    assert chat_post_message.get("success")

@pytest.mark.asyncio
async def test_chat_post_update_delete_message(logged_rocket):
    chat_post_message = await logged_rocket.chat_post_message(
        "hello",
        channel="GENERAL",
        attachments=[
            {"color": "#ff0000", "text": "there"},
        ],
    ).json()
    assert chat_post_message.get("channel") == "GENERAL"
    assert chat_post_message.get("message").get("msg") == "hello"
    assert (
        chat_post_message.get("message").get("attachments")[0].get("color") == "#ff0000"
    )
    assert chat_post_message.get("message").get("attachments")[0].get("text") == "there"
    assert chat_post_message.get("success")

    with pytest.raises(RocketMissingParamException):
        await logged_rocket.chat_post_message(text="text")

    msg_id = chat_post_message.get("message").get("_id")
    chat_get_message = logged_rocket.chat_get_message(msg_id=msg_id).json()
    assert chat_get_message.get("message").get("_id") == msg_id

    chat_update = await logged_rocket.chat_update(
        room_id=chat_post_message.get("channel"),
        msg_id=chat_post_message.get("message").get("_id"),
        text="hello again",
    ).json()

    assert chat_update.get("message").get("msg") == "hello again"
    assert chat_update.get("success")

    chat_delete = await logged_rocket.chat_delete(
        room_id=chat_post_message.get("channel"),
        msg_id=chat_post_message.get("message").get("_id"),
    ).json()
    assert chat_delete.get("success")

@pytest.mark.asyncio
async def test_chat_send_notext_message(logged_rocket):
    chat_send_message = await logged_rocket.chat_send_message({"rid": "GENERAL"})
    assert chat_send_message.json().get("message").get("rid") == "GENERAL"
    assert chat_send_message.json().get("message").get("msg") == ""
    assert chat_send_message.json().get("success")
    with pytest.raises(RocketMissingParamException):
        await logged_rocket.chat_send_message({"msg": "General Kenobi"})

@pytest.mark.asyncio
async def test_chat_send_custom_id_delete_message(logged_rocket):
    chat_send_message = await logged_rocket.chat_send_message(
        {"rid": "GENERAL", "msg": "Hello There", "_id": "42"}
    )
    assert chat_send_message.json().get("message").get("rid") == "GENERAL"
    assert chat_send_message.json().get("message").get("msg") == "Hello There"
    assert chat_send_message.json().get("message").get("_id") == "42"
    assert chat_send_message.json().get("success")
    chat_delete = await logged_rocket.chat_delete(
        room_id=chat_send_message.json().get("message").get("rid"),
        msg_id=chat_send_message.json().get("message").get("_id"),
    )
    assert chat_delete.json().get("success")

@pytest.mark.asyncio
async def test_chat_post_react(logged_rocket):
    message_id = (
        await logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_react = await logged_rocket.chat_react(msg_id=message_id)
    assert chat_react.json().get("success")

@pytest.mark.asyncio
async def test_post_pin_unpin(logged_rocket):
    message_id = (
        await logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_pin_message = await logged_rocket.chat_pin_message(message_id)
    assert chat_pin_message.json().get("success")
    assert chat_pin_message.json().get("message").get("t") == "message_pinned"

    chat_unpin_message = await logged_rocket.chat_unpin_message(message_id)
    assert chat_unpin_message.json().get("success")

@pytest.mark.asyncio
async def test_post_star_unstar_get_starred_messages(logged_rocket):
    message_id = (
        await logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )

    chat_get_starred_messages = await logged_rocket.chat_get_starred_messages(
        room_id="GENERAL"
    )
    assert chat_get_starred_messages.json().get("success")
    assert chat_get_starred_messages.json().get("count") == 0
    assert chat_get_starred_messages.json().get("messages") == []

    chat_star_message = await logged_rocket.chat_star_message(message_id)
    assert chat_star_message.json().get("success")

    chat_get_starred_messages = await logged_rocket.chat_get_starred_messages(
        room_id="GENERAL"
    )
    assert chat_get_starred_messages.json().get("success")
    assert chat_get_starred_messages.json().get("count") == 1
    assert chat_get_starred_messages.json().get("messages") != []

    chat_unstar_message = await logged_rocket.chat_unstar_message(message_id)
    assert chat_unstar_message.json().get("success")

@pytest.mark.asyncio
async def test_chat_search(logged_rocket):
    chat_search = await logged_rocket.chat_search(
        room_id="GENERAL", search_text="hello"
    )
    assert chat_search.json().get("success")

@pytest.mark.asyncio
async def test_chat_get_message_read_receipts(logged_rocket):
    message_id = (
        await logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_get_message_read_receipts = await logged_rocket.chat_get_message_read_receipts(
        message_id=message_id
    )
    assert chat_get_message_read_receipts.json().get("success")
    assert "receipts" in chat_get_message_read_receipts.json()

@pytest.mark.asyncio
async def test_chat_report_message(logged_rocket):
    message_id = (
        await logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_get_message_report_message = await logged_rocket.chat_report_message(
        message_id=message_id, description="this makes me angry"
    )
    assert chat_get_message_report_message.json().get("success")

@pytest.mark.asyncio
async def test_chat_follow_message(logged_rocket):
    message_id = (
        await logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_get_message_follow_message = await logged_rocket.chat_follow_message(
        mid=message_id
    )
    assert chat_get_message_follow_message.json().get("success")
