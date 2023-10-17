import uuid


async def test_roles_list(logged_rocket):
    roles_list = await logged_rocket.roles_list()
    assert roles_list.get("success")
    assert len(roles_list.get("roles")) > 0


async def test_roles_create(logged_rocket):
    name = str(uuid.uuid1())
    roles_create = await logged_rocket.roles_create(
        name=name, scope="Subscriptions", description="a test role"
    )
    assert roles_create.get("success")
    assert roles_create.get("role").get("name") == name
    assert roles_create.get("role").get("scope") == "Subscriptions"
    assert roles_create.get("role").get("description") == "a test role"


async def test_roles_add_remove_user_to_from_role(logged_rocket):
    me = await logged_rocket.me()
    roles_add_user_to_role = await logged_rocket.roles_add_user_to_role(
        role_name="livechat-agent", username=me.get("username")
    )
    assert roles_add_user_to_role.get("success")
    assert roles_add_user_to_role.get("role").get("name") == "livechat-agent"

    roles_remove_user_from_role = await logged_rocket.roles_remove_user_from_role(
        role_name="livechat-agent", username=me.get("username")
    )

    assert roles_remove_user_from_role.get("success")


async def test_roles_get_users_in_role(logged_rocket):
    roles_get_users_in_role = await logged_rocket.roles_get_users_in_role(
        role="owner", roomId="GENERAL"
    )

    assert roles_get_users_in_role.get("success")
    assert roles_get_users_in_role.get("users")[0].get("name") == "user1"


async def test_roles_sync(logged_rocket):
    roles_sync = await logged_rocket.roles_sync(
        updated_since="2017-11-25T15:08:17.248Z"
    )
    assert roles_sync.get("success")
    assert len(roles_sync.get("roles")) > 0
