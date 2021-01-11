from caluma.extensions.permissions import MySAGWPermission


def test_permissions_default(mocker, admin_info):
    admin_info.context.user.claims["roles"] = ["Admin"]

    perm = MySAGWPermission()

    mutation = mocker.Mock()
    mutation.__name__ = "SomeMutation"
    assert perm.has_permission(mutation, admin_info) is True
