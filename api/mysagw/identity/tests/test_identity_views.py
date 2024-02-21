import datetime

import pyexcel
import pytest
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from psycopg2._range import DateRange
from rest_framework import status
from syrupy import filters

from mysagw.identity.models import Identity
from mysagw.identity.views import DMSClient

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_identity_detail(db, client, expected_status):
    identity = client.user.identity

    url = reverse("identity-detail", args=[identity.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(identity.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_identity_list(db, client, expected_status):
    url = reverse("identity-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == Identity.objects.count() == 3


@pytest.mark.freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_201_CREATED),
        ("admin", status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_identity_create(db, client, expected_status):
    url = reverse("identity-list")

    data = {
        "data": {
            "type": "identities",
            "attributes": {"first_name": "foo", "salutation": "neutral"},
        },
    }

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    identity = Identity.objects.get(first_name="foo")
    assert identity.created_by_user == identity.modified_by_user == client.user.id
    json = response.json()
    assert (
        json["data"]["attributes"]["created-at"]
        == json["data"]["attributes"]["modified-at"]
        == TIMESTAMP
    )


@pytest.mark.parametrize("attributes", [{}, {"first-name": None}, {"first-name": ""}])
def test_identity_create_empty_failure(db, client, attributes):
    url = reverse("identity-list")

    data = {
        "data": {
            "type": "identities",
            "attributes": attributes,
        },
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["errors"][0]["detail"] == (
        "Identities need at least an email, first_name, last_name or "
        "organisation_name."
    )


def test_identity_update_empty_failure(db, client, identity):
    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {
                "first-name": None,
                "last-name": "",
                "organisation-name": "",
                "email": None,
            },
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["errors"][0]["detail"] == (
        "Identities need at least an email, first_name, last_name or "
        "organisation_name."
    )


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_identity_update(db, client, expected_status, identity_factory):
    identity = identity_factory()
    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo", "email": ""},
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    identity.refresh_from_db()
    assert identity.modified_by_user == client.user.id
    assert identity.email is None


@pytest.mark.parametrize(
    "is_organisation,field,error_msg_vars",
    [
        (True, "identity", ["set", "memberships"]),
        (False, "organisation", ["unset", "members"]),
    ],
)
def test_identity_update_is_organisation_membership_failure(
    db,
    client,
    membership_factory,
    is_organisation,
    field,
    error_msg_vars,
):
    membership = membership_factory(organisation__is_organisation=True)
    instance = getattr(membership, field)

    url = reverse("identity-detail", args=[instance.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(instance.pk),
            "attributes": {"is-organisation": is_organisation},
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert (
        response.json()["errors"][0]["detail"]
        == f'Can\'t {error_msg_vars[0]} "is_organisation", because there are {error_msg_vars[1]}.'
    )


@pytest.mark.parametrize(
    "identity__organisation_name,identity__is_organisation,expected_status",
    [
        ("AllSafe", True, [status.HTTP_200_OK, status.HTTP_201_CREATED]),
        (None, False, [status.HTTP_400_BAD_REQUEST]),
    ],
)
@pytest.mark.parametrize("update", [True, False])
def test_identity_update_is_organisation_organisation_name_failure(
    db,
    client,
    identity,
    expected_status,
    update,
):
    is_organisation = not identity.is_organisation

    data = {
        "data": {
            "type": "identities",
            "attributes": {
                "is-organisation": is_organisation,
                "email": "test@example.com",
                "organisation-name": identity.organisation_name,
            },
        },
    }

    url = reverse("identity-list")
    method = client.post
    if update:
        data["data"]["id"] = str(identity.pk)
        url = reverse("identity-detail", args=[identity.pk])
        method = client.patch

    response = method(url, data=data)

    assert response.status_code in expected_status

    result = response.json()

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        assert (
            result["errors"][0]["detail"]
            == 'Can\'t set "is_organisation" without an organisation_name.'
        )
        return

    new_identity = Identity.objects.get(pk=result["data"]["id"])
    assert new_identity.organisation_name is None


@pytest.mark.parametrize(
    "identity__is_organisation,field",
    [
        (False, "is-expert-association"),
        (False, "is-advisory-board"),
    ],
)
def test_identity_update_organisation_type_failure(db, client, identity, field):
    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"is-organisation": identity.is_organisation, field: True},
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert (
        response.json()["errors"][0]["detail"]
        == 'Can\'t set "is_expert_association" or "is_advisory_board", because it isn\'t a organisation.'
    )


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_identity_delete(db, client, expected_status, identity_factory):
    identity = identity_factory()
    url = reverse("identity-detail", args=[identity.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(Identity.DoesNotExist):
            identity.refresh_from_db()


def test_identity_set_interests(db, client, identity_factory, interest_factory):
    identity = identity_factory()
    assert identity.interests.count() == 0

    interests = interest_factory.create_batch(2)

    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo"},
            "relationships": {
                "interests": {
                    "data": [
                        {"id": str(interests[0].pk), "type": "interests"},
                        {"id": str(interests[1].pk), "type": "interests"},
                    ],
                },
            },
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    identity.refresh_from_db()
    assert identity.interests.count() == 2


@pytest.mark.parametrize(
    "search,expected",
    [
        ("Winst", [0]),
        ("agw@", [0]),
        ("Präsi", [1]),
        ("SAGW", [0, 1, 2, 3]),
        ("@sag", [0, 3]),
        ("123456", [4]),
        ("pHil", [5, 6]),
        ("philosophy class", [5, 6]),
        ('"philosophy class"', [6]),
        ('"philosophy class', [6]),
        ('"philosophy -class"', []),
        ("SAGW -winst", [1, 2, 3]),
        ("-example", [0]),
        ("nonexistent", []),
    ],
)
def test_identity_search(
    db,
    client,
    identity_factory,
    membership_role_factory,
    membership_factory,
    email_factory,
    phone_number_factory,
    interest_factory,
    search,
    expected,
):
    identities = [identity_factory(first_name="Winston", email="sagw@sagw.ch")]

    membership_role = membership_role_factory(title={"de": "PräsidentIn"})
    membership = membership_factory(
        role=membership_role,
        organisation__organisation_name="SAGW",
        organisation__is_organisation=True,
    )
    identities.append(membership.identity)
    identities.append(membership.organisation)

    membership_factory(  # inactive, must not show up
        organisation=membership.organisation,
        inactive=True,
    )
    membership_factory(  # expired, must not show up
        organisation=membership.organisation,
        inactive=False,
        time_slot=DateRange(
            lower=datetime.date(2020, 1, 1),
            upper=(timezone.now() - timezone.timedelta(days=1)).date(),
        ),
    )

    membership_factory(  # expired, must not show up
        organisation=membership.organisation,
        inactive=False,
        time_slot=DateRange(
            upper=(timezone.now() - timezone.timedelta(days=1)).date(),
        ),
    )

    email = email_factory(email="test@sagw.ch")
    identities.append(email.identity)

    phone = phone_number_factory(phone="+41771234567")
    identities.append(phone.identity)

    phil_interest_identity = identity_factory()
    phil_interest = interest_factory(title={"de": "philosophy"})
    class_interest = interest_factory(title={"de": "class"})
    phil_interest_identity.interests.add(phil_interest)
    phil_interest_identity.interests.add(class_interest)
    identities.append(phil_interest_identity)

    phil_class_interest_identity = identity_factory()
    phil_class_interest = interest_factory(title={"de": "philosophy class"})
    phil_class_interest_identity.interests.add(phil_class_interest)
    identities.append(phil_class_interest_identity)

    url = reverse("identity-list")

    response = client.get(url, {"filter[search]": search})

    assert response.status_code == status.HTTP_200_OK

    expected_ids = sorted([str(identities[ex].pk) for ex in expected])

    json = response.json()

    received_ids = sorted([s["id"] for s in json["data"]])

    assert expected_ids == received_ids


def test_identity_search_membership_handling(
    db,
    client,
    identity_factory,
    membership_role_factory,
    membership_factory,
):
    identity = identity_factory(first_name="Winston", email="sagw@sagw.ch")

    membership = membership_factory(
        role=membership_role_factory(title={"de": "Präsident·in"}),
        organisation__organisation_name="SAGW",
        organisation__is_organisation=True,
        identity=identity,
    )

    membership_factory(
        role=membership_role_factory(title={"de": "Vizepräsident·in"}),
        organisation=membership.organisation,
        organisation__is_organisation=True,
        inactive=True,
        identity=identity,
    )

    url = reverse("identity-list")

    response = client.get(url, {"filter[search]": "Präsident·in -Vizepräsident·in"})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    received_ids = sorted([s["id"] for s in json["data"]])
    assert len(received_ids) == 1

    assert received_ids == [str(identity.pk)]


@pytest.mark.parametrize("is_organisation", [True, False, None])
def test_identity_organisation_filters(db, client, identity_factory, is_organisation):
    identities = list(Identity.objects.all())  # created by the `client` fixture
    assert len(identities) == 3

    organisations = identity_factory.create_batch(3, is_organisation=True)

    expected = identities + organisations
    if is_organisation is True:
        expected = organisations
    elif is_organisation is False:
        expected = identities

    expected_ids = sorted([str(ex.pk) for ex in expected])

    url = reverse("identity-list")

    filters = {}
    if is_organisation in [True, False]:
        filters = {"filter[is-organisation]": is_organisation}

    response = client.get(url, filters)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    received_ids = sorted([i["id"] for i in json["data"]])

    assert expected_ids == received_ids


def test_identity_organisation_multi_filter_distinct(
    db,
    client,
    identity_factory,
    membership_factory,
    snapshot,
):
    sagw = identity_factory(is_organisation=True, organisation_name="SAGW")
    sagw_membership = membership_factory(organisation=sagw, role=None)
    membership_factory(identity=sagw_membership.identity, organisation=sagw, role=None)
    nwp = identity_factory(is_organisation=True, organisation_name="NWP")
    nwp_membership = membership_factory(organisation=nwp, role=None)
    membership_factory(identity=nwp_membership.identity, organisation=nwp, role=None)

    url = reverse("identity-list")

    response = client.get(url, {"filter[memberOfOrganisations]": "SAGW,NWP"})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == 2
    assert json == snapshot(exclude=filters.props("id", "created-at", "modified-at"))


def test_identity_idp_ids_filters(db, client, identity_factory):
    identities = identity_factory.create_batch(3)

    expected_ids = sorted([str(i.idp_id) for i in identities])

    url = reverse("identity-list")

    response = client.get(url, {"filter[idpIds]": ",".join(expected_ids)})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    received_ids = sorted([i["attributes"]["idp-id"] for i in json["data"]])

    assert expected_ids == received_ids


def test_identity_export(
    db,
    client,
    identity_factory,
    phone_number_factory,
    email_factory,
    membership_factory,
    address_factory,
    snapshot,
):
    identities = sorted(
        identity_factory.create_batch(
            10,
        ),
        key=lambda item: (
            item.last_name,
            item.first_name,
            item.email,
        ),  # use same ordering as the model
    )
    identity_factory()  # create another one to make sure the filtering actually works

    org = identity_factory(is_organisation=True)

    for i in identities:
        phone_number_factory.create_batch(3, identity=i)
        email_factory.create_batch(3, identity=i)
        address_factory(identity=i)
        membership_factory(identity=i, organisation=org)

    identities[1].salutation = Identity.SALUTATION_MR
    identities[1].language = "fr"
    identities[1].save()
    identities[2].salutation = Identity.SALUTATION_MRS
    identities[2].language = "en"
    identities[2].save()

    url = reverse("identity-export")

    response = client.post(url, QUERY_STRING=f"filter[search]={org.organisation_name}")

    assert response.status_code == status.HTTP_200_OK

    sheet = pyexcel.get_sheet(file_type="xlsx", file_content=response.content)

    assert len(sheet.array) == len(identities) + 2
    snapshot.assert_match(sheet.array)


def test_membership_export(
    db,
    client,
    identity_factory,
    phone_number_factory,
    email_factory,
    membership_factory,
    address_factory,
    snapshot,
):
    identities = sorted(
        identity_factory.create_batch(
            9,
        ),
        key=lambda item: (
            item.last_name,
            item.first_name,
            item.email,
        ),  # use same ordering as the model
    )
    org1 = identity_factory(is_organisation=True, organisation_name="E Corp")
    org2 = identity_factory(is_organisation=True, organisation_name="Allsafe")
    org3 = identity_factory(is_organisation=True, organisation_name="Nonsafe")
    memberships = []

    for c, i in enumerate(identities):
        phone_number_factory.create_batch(3, identity=i)
        email_factory.create_batch(3, identity=i)
        address_factory(identity=i)
        org = org2
        if c < 3:
            org = org1
        elif c > 5:
            org = org3
        memberships.append(membership_factory(identity=i, organisation=org))

    memberships[4].role = None
    memberships[4].time_slot = DateRange(
        lower=datetime.date(2020, 1, 1),
        upper=datetime.date(2020, 1, 2),
    )
    memberships[4].next_election = datetime.date(2020, 11, 23)
    memberships[4].save()
    memberships[5].inactive = True
    memberships[5].time_slot = DateRange(lower=datetime.date(2020, 1, 1))
    memberships[5].save()

    identities[1].salutation = Identity.SALUTATION_MR
    identities[1].language = "fr"
    identities[1].save()
    identities[2].salutation = Identity.SALUTATION_MRS
    identities[2].language = "en"
    identities[2].save()

    url = reverse("identity-export-memberships")

    response = client.post(url, QUERY_STRING="filter[search]=safe")

    assert response.status_code == status.HTTP_200_OK

    sheet = pyexcel.get_sheet(file_type="xlsx", file_content=response.content)

    assert len(sheet.array) == org2.members.count() + org3.members.count() + 1
    snapshot.assert_match(sorted(sheet.array, reverse=True))


def test_identity_export_email(
    db,
    client,
    identity_factory,
):
    identities = sorted(
        identity_factory.create_batch(10, last_name="Smith"),
        key=lambda item: (
            item.last_name,
            item.first_name,
            item.email,
        ),  # use same ordering as the model
    )

    url = reverse("identity-export-email")

    response = client.post(url, QUERY_STRING="filter[search]=smith")

    assert response.status_code == status.HTTP_200_OK

    sheet = pyexcel.get_sheet(file_type="xlsx", file_content=response.content)
    assert len(sheet.array) == len(identities) + 1
    assert sheet.array[0] == ["email"]

    for i in range(10):
        assert sheet.array[i + 1][0] == identities[i].email


@pytest.mark.usefixtures("_dms_mock")
@pytest.mark.parametrize(
    "_dms_mock,error_response_type,expected_status",
    [
        ("success", None, status.HTTP_200_OK),
        ("json_error", "json", status.HTTP_500_INTERNAL_SERVER_ERROR),
        ("text_error", "text", status.HTTP_500_INTERNAL_SERVER_ERROR),
        ("unknown_error", "unknown", status.HTTP_500_INTERNAL_SERVER_ERROR),
    ],
    indirect=["_dms_mock"],
)
def test_identity_export_labels(
    db,
    client,
    identity_factory,
    snapshot,
    expected_status,
    error_response_type,
):
    identity_factory.create_batch(10)

    url = reverse("identity-export-labels")

    response = client.post(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert (
            response.get("content-type")
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        assert response.content == b"I'm the merged document"
        return

    if error_response_type == "json":
        assert response.get("content-type") == "application/json"
        assert response.json() == {
            "source": "DMS",
            "status": 400,
            "errors": {"error": "something went wrong"},
        }
    elif error_response_type == "text":
        assert (
            response.get("content-type") == "application/json"
        )  # we still respond with json
        assert response.json() == {
            "source": "DMS",
            "status": 400,
            "errors": "something went wrong",
        }
    elif error_response_type == "unknown":
        assert response.get("content-type") == "application/json"
        assert response.json() == {
            "source": "DMS",
            "status": 400,
            "errors": "something went wrong",
        }


def test_identity_export_labels_context(
    db,
    client,
    identity_factory,
    phone_number_factory,
    email_factory,
    address_factory,
    mocker,
    snapshot,
):
    identities = identity_factory.create_batch(11)
    for i in identities:
        phone_number_factory.create_batch(3, identity=i)
        email_factory.create_batch(3, identity=i)
        address_factory(identity=i)

    identities[1].organisation_name = "SAGW"
    identities[1].save()
    identity1_address = identities[1].addresses.first()
    identity1_address.address_addition_1 = "Haus der Akademien"
    identity1_address.po_box = "23"
    identity1_address.save()

    url = reverse("identity-export-labels")

    merge_mock = mocker.patch.object(
        DMSClient,
        "get_merged_document",
        return_value=HttpResponse(
            "content",
            status=status.HTTP_200_OK,
            content_type="text/plain",
        ),
    )

    response = client.post(url)

    assert response.status_code == status.HTTP_200_OK
    merge_mock.assert_called_once()
    snapshot.assert_match(merge_mock.mock_calls[0].args[0])
