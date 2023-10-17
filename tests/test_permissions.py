async def test_permissions_list_all(logged_rocket):
    
    permissions_list_all = await logged_rocket.permissions_list_all()
    assert permissions_list_all.get("success")
    assert "update" in permissions_list_all
    assert "remove" in permissions_list_all


# pylint: disable=invalid-name
async def test_permissions_list_all_with_updatedSince(logged_rocket):
    permissions_list_all = await logged_rocket.permissions_list_all(
        updatedSince="2017-11-25T15:08:17.248Z"
    )
    assert permissions_list_all.get("success")
    assert "update" in permissions_list_all
    assert "remove" in permissions_list_all


async def test_permissions_update(logged_rocket):
    def get_updated_roles(permission, permissions_update):
        for permission_update in permissions_update:
            if permission.get("_id", "A") == permission_update.get("_id", "B"):
                return permission_update.get("roles")

        # Permission not found
        raise ValueError

    def check_update(permissions, permissions_update):
        for permission in permissions:
            try:
                if permission.get("roles") != get_updated_roles(
                    permission, permissions_update
                ):
                    return False
            except ValueError:
                return False

        return True

    permissions = [
        {"_id": "access-permissions", "roles": ["admin", "bot"]},
        {"_id": "add-user-to-any-c-room", "roles": ["admin"]},
    ]
    permissions_update = await logged_rocket.permissions_update(
        permissions=permissions
    )
    assert permissions_update.get("success")
    assert check_update(permissions, permissions_update.get("permissions", []))

    permissions_wrong_id = [
        {"_id": "wrong-id", "roles": ["admin", "bot"]},
    ]
    assert (
        check_update(permissions_wrong_id, permissions_update.get("permissions", []))
        is False
    )

    permissions_wrong_roles = [
        {"_id": "access-permissions", "roles": ["bot"]},
    ]
    assert (
        check_update(permissions_wrong_roles, permissions_update.get("permissions", []))
        is False
    )
