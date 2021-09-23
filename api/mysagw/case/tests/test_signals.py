import pytest

from mysagw.identity.models import Identity


@pytest.mark.parametrize(
    "identity_email,assigned", [("foo@example.com", True), ("bar@example.com", False)]
)
def test_assign_cases(db, case_access_factory, identity_email, assigned):
    case_access = case_access_factory(
        email="foo@example.com", case_id="00000000-0000-0000-0000-000000000000"
    )
    identity = Identity.objects.create(email=identity_email)

    case_access.refresh_from_db()

    if assigned:
        assert case_access.email is None
        assert case_access.identity == identity
    else:
        assert case_access.email == "foo@example.com"
        assert case_access.identity is None
