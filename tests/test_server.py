from rocketchat_API.rocketchat import RocketChat


async def test_info(logged_rocket):
    info = await logged_rocket.info().json()
    assert "info" in info
    assert info.get("success")


async def test_statistics(logged_rocket):
    statistics = await logged_rocket.statistics().json()
    assert statistics.get("success")


async def test_statistics_list(logged_rocket):
    statistics_list = await logged_rocket.statistics_list().json()
    assert statistics_list.get("success")


async def test_directory(logged_rocket):
    directory = await logged_rocket.directory(
        query={"text": "rocket", "type": "users"}
    ).json()
    assert directory.get("success")


async def test_spotlight(logged_rocket):
    spotlight = await logged_rocket.spotlight(query="user1").json()
    assert spotlight.get("success")
    assert spotlight.get("users") is not None, "No users list found"
    assert spotlight.get("rooms") is not None, "No rooms list found"


async def test_login_token(logged_rocket):
    user_id = logged_rocket.headers["X-User-Id"]
    auth_token = logged_rocket.headers["X-Auth-Token"]

    another_rocket = RocketChat(user_id=user_id, auth_token=auth_token)
    logged_user = await another_rocket.me().json()

    assert logged_user.get("_id") == user_id

