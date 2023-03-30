from random import shuffle

from mysagw.identity.helpers import (
    get_membership_roles_order,
    set_membership_roles_order,
)


def test_set_membership_roles_order(db, membership_role_factory):
    roles = []
    for sort in range(10, 0, -1):
        roles.append(membership_role_factory(sort=sort))

    roles_list = get_membership_roles_order()

    shuffle(roles_list)

    new_roles_list = [[ct, l[1], l[2]] for ct, l in enumerate(roles_list)]
    new_roles_list.reverse()

    set_membership_roles_order(new_roles_list)

    assert new_roles_list == get_membership_roles_order()
