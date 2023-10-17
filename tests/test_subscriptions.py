async def test_subscriptions_get(logged_rocket):
    subscriptions_get = await logged_rocket.subscriptions_get().json()
    assert subscriptions_get.get("success")
    assert "update" in subscriptions_get


async def test_subscriptions_get_one(logged_rocket):
    subscriptions_get_one = await logged_rocket.subscriptions_get_one(
        room_id="GENERAL"
    ).json()
    assert subscriptions_get_one.get("success")
    assert "subscription" in subscriptions_get_one


async def test_subscriptions_unread(logged_rocket):
    subscriptions_unread = await logged_rocket.subscriptions_unread(room_id="GENERAL").json()
    assert subscriptions_unread.get("success"), "Call did not succeed"


async def test_subscriptions_read(logged_rocket):
    subscriptions_read = await logged_rocket.subscriptions_read(rid="GENERAL").json()
    assert subscriptions_read.get("success"), "Call did not succeed"
