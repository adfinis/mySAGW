from mysagw.identity.models import MembershipRole


def get_membership_roles_order():
    roles_order = [
        [r.sort, r.title.de, str(r.pk)] for r in MembershipRole.objects.iterator()
    ]
    print(roles_order)
    return roles_order


def set_membership_roles_order(roles_order):
    """
    Set the order of the roles.

    This function accepts a list in the same format of the output of
    `get_roles_order()`.
    """
    for raw_role in roles_order:
        role = MembershipRole.objects.get(pk=raw_role[2])
        role.sort = raw_role[0]
        role.save()
