from random import shuffle

from mysagw.identity.helpers import (
    get_membership_roles_order,
    set_membership_roles_order,
)


def test_set_membership_roles_order(db, membership_role_factory):
    for sort in range(10, 0, -1):
        membership_role_factory(sort=sort)

    roles_list = get_membership_roles_order()

    shuffle(roles_list)

    new_roles_list = [[ct, role[1], role[2]] for ct, role in enumerate(roles_list)]
    new_roles_list.reverse()

    set_membership_roles_order(new_roles_list)

    assert new_roles_list == get_membership_roles_order()
