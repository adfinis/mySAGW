import pytest
from django.conf import settings

from mysagw.identity.models import Identity


@pytest.mark.parametrize(
    "identity__salutation", Identity.SALUTATION_LOCALIZED_MAP.keys()
)
@pytest.mark.parametrize("identity__title", Identity.TITLE_LOCALIZED_MAP.keys())
@pytest.mark.parametrize("identity__first_name", ["Winston", None])
@pytest.mark.parametrize("identity__last_name", ["Smith", None])
@pytest.mark.parametrize(
    "identity__language", settings.LOCALIZED_FIELDS_FALLBACKS.keys()
)
def test_fullname(db, identity, snapshot):
    snapshot.assert_match(identity.full_name)


@pytest.mark.parametrize(
    "address__address_addition_1, address__address_addition_2, address__address_addition_3",
    [
        (None, None, None),
        ("Some", "Nice", "Addition"),
        (None, "Nice", "Addition"),
        ("Some", None, "Addition"),
    ],
)
@pytest.mark.parametrize("lang", settings.LOCALIZED_FIELDS_FALLBACKS.keys())
@pytest.mark.parametrize("address__po_box", ["23", None])
def test_address_block(db, snapshot, address, lang):
    address.identity.language = lang
    address.identity.save()
    snapshot.assert_match(address.identity.address_block)


def test_address_block_missing_address(db, snapshot, identity):
    snapshot.assert_match(identity.address_block)
