import pytest
from django.core.management import call_command

from mysagw.identity import models


@pytest.mark.parametrize(
    "rounds,cleanup",
    [(1, True), (5, True), (1, False), (5, False)],
)
def test_generate_demo_data_command(db, rounds, cleanup, identity):
    args = ["--rounds", rounds]
    if cleanup:
        args.append("--cleanup")

    call_command("generate_demo_data", *args)

    if cleanup:
        with pytest.raises(models.Identity.DoesNotExist):
            identity.refresh_from_db()
    else:
        identity.refresh_from_db()

    assert models.InterestCategory.objects.count() == 1
    assert models.Interest.objects.count() == 3
    assert models.Identity.objects.count() == rounds * 2 + (0 if cleanup else 1)
    assert models.Email.objects.count() == rounds * 4
    assert models.PhoneNumber.objects.count() == rounds * 4
