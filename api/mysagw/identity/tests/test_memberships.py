import datetime

import pytest
from django.utils import timezone
from psycopg2._range import DateRange


@pytest.mark.parametrize(
    "membership__time_slot,membership__inactive,is_included",
    [
        (None, False, True),
        (None, True, False),
        (
            DateRange(lower=datetime.date(2020, 1, 1), upper=datetime.date(2020, 1, 2)),
            False,
            False,
        ),
        (
            DateRange(
                lower=datetime.date(2020, 1, 1),
                upper=(timezone.now() + timezone.timedelta(days=1)).date(),
            ),
            False,
            True,
        ),
        (
            DateRange(
                lower=datetime.date(2020, 1, 1),
                upper=(timezone.now() + timezone.timedelta(days=1)).date(),
            ),
            True,
            False,
        ),
        (
            DateRange(
                lower=(timezone.now() + timezone.timedelta(days=1)).date(),
                upper=(timezone.now() + timezone.timedelta(days=2)).date(),
            ),
            False,
            False,
        ),
        (
            DateRange(
                lower=(timezone.now() + timezone.timedelta(days=1)).date(),
                upper=(timezone.now() + timezone.timedelta(days=2)).date(),
            ),
            True,
            False,
        ),
    ],
)
def test_member_of(db, django_assert_num_queries, membership, is_included):
    with django_assert_num_queries(1):
        assert (membership.organisation in membership.identity.member_of) is is_included
