import re
from uuid import UUID, uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from mysagw.case import models
from mysagw.case.email_texts import invite
from mysagw.case.tests.application_caluma_response import (
    CALUMA_DATA_EMPTY,
    CALUMA_DATA_FULL,
)
from mysagw.case.views import CaseDownloadViewSet
from mysagw.utils import build_url


@pytest.mark.parametrize(
    "filter_id,expected_count,expected_status",
    [
        (None, 0, status.HTTP_400_BAD_REQUEST),
        ("00000000-0000-0000-0000-000000000000", 2, status.HTTP_200_OK),
        ("11111111-1111-1111-1111-111111111111", 1, status.HTTP_200_OK),
    ],
)
def test_case_list(
    db,
    client,
    filter_id,
    expected_count,
    expected_status,
    identity_factory,
    case_access_factory,
):
    identity_0 = identity_factory(idp_id="00000000-0000-0000-0000-000000000000")
    identity_1 = identity_factory(idp_id="11111111-1111-1111-1111-111111111111")
    case_access_factory.create_batch(2, identity=identity_0, email=None)
    case_access_factory(identity=identity_1, email=None)
    case_access_factory()

    url = reverse("caseaccess-list")

    response = client.get(url, {"filter[idpId]": filter_id} if filter_id else None)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        json = response.json()
        assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "client,has_access,identity_exists,expected_status",
    [
        ("user", False, False, status.HTTP_403_FORBIDDEN),
        ("user", False, True, status.HTTP_403_FORBIDDEN),
        ("user", True, False, status.HTTP_201_CREATED),
        ("staff", False, False, status.HTTP_201_CREATED),
        ("staff", False, True, status.HTTP_201_CREATED),
        ("admin", False, False, status.HTTP_201_CREATED),
        ("admin", False, True, status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_case_create(
    db,
    case_access,
    case_access_factory,
    client,
    identity,
    has_access,
    identity_exists,
    expected_status,
    mailoutbox,
):
    first_case = case_access_factory()

    url = reverse("caseaccess-list")

    data = {
        "data": {
            "type": "case-accesses",
            "attributes": {"email": "test@example.com", "case-id": first_case.case_id},
            "relationships": {
                "identity": {},
            },
        },
    }

    if has_access:
        case_access.email = None
        case_access.identity = client.user.identity
        case_access.save()
        data["data"]["attributes"]["case-id"] = case_access.case_id
        data["data"]["attributes"]["email"] = identity.email
    elif identity_exists:
        data["data"]["attributes"]["email"] = client.user.identity.email

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        assert len(mailoutbox) == 0
        return

    assert models.CaseAccess.objects.count() == 3
    result = response.json()
    case_access = models.CaseAccess.objects.get(pk=result["data"]["id"])
    if identity_exists:
        assert case_access.email is None
        assert case_access.identity == client.user.identity
    elif has_access:
        assert case_access.email is None
        assert case_access.identity == identity
    else:
        assert case_access.email == "test@example.com"
        assert case_access.identity is None
        assert len(mailoutbox) == 1
        expected_body = invite.EMAIL_BODY_INVITE_REGISTER.format(
            link=settings.SELF_URI,
        )
        assert mailoutbox[0].body == expected_body

    if identity_exists or has_access:
        assert len(mailoutbox) == 1
        expected_body = invite.EMAIL_INVITE_BODIES[
            case_access.identity.language
        ].format(
            first_name=case_access.identity.first_name or "",
            last_name=case_access.identity.last_name or "",
            link=f"{settings.SELF_URI}/cases/{case_access.case_id}",
        )
        assert mailoutbox[0].body == expected_body


def test_case_create_first(db, client, mailoutbox):
    data = {
        "data": {
            "type": "case-accesses",
            "attributes": {
                "email": client.user.identity.email,
                "case-id": str(uuid4()),
            },
            "relationships": {
                "identity": {},
            },
        },
    }

    url = reverse("caseaccess-list")

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert len(mailoutbox) == 0


def test_case_create_already_exists(db, case_access_factory, client):
    case_access = case_access_factory(
        email=None,
        identity=client.user.identity,
        case_id=uuid4(),
    )

    data = {
        "data": {
            "type": "case-accesses",
            "attributes": {
                "email": client.user.identity.email,
                "case-id": str(case_access.case_id),
            },
            "relationships": {
                "identity": {},
            },
        },
    }

    url = reverse("caseaccess-list")

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["errors"][0]["detail"] == "Case already exists!"


@pytest.mark.parametrize(
    "client,has_access,is_only_access_for_case,expected_status",
    [
        ("user", False, False, status.HTTP_404_NOT_FOUND),
        ("user", True, False, status.HTTP_204_NO_CONTENT),
        ("staff", False, False, status.HTTP_204_NO_CONTENT),
        ("admin", False, False, status.HTTP_204_NO_CONTENT),
        ("admin", False, True, status.HTTP_400_BAD_REQUEST),
    ],
    indirect=["client"],
)
def test_case_delete(
    db,
    client,
    has_access,
    is_only_access_for_case,
    expected_status,
    case_access_factory,
):
    case_access = case_access_factory()

    if has_access:
        case_access.identity = client.user.identity
        case_access.case_id = case_access.case_id
        case_access.save()

    if not is_only_access_for_case:
        case_access_factory(case_id=case_access.case_id)

    url = reverse("caseaccess-detail", args=[case_access.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.CaseAccess.DoesNotExist):
            case_access.refresh_from_db()


def test_transfer_case(
    client, case_access_factory, identity_factory, mailoutbox, snapshot
):
    accesses = case_access_factory.create_batch(3, email=None)
    new_identity = identity_factory()
    for a in accesses:
        a.identity = identity_factory()
        a.save()

    assert models.CaseAccess.objects.count() == 3

    data = {
        # accesses[0] will be removed
        "to_remove_assignees": [str(accesses[0].identity.pk)],
        # 3 new CaseAccess-objects will br created. Two for `new_identity` and only one
        # for accesses[1].identity, because for accesses[1].case_id there already
        # exists one
        "new_assignees": [str(new_identity.pk), str(accesses[1].identity.pk)],
        "case_ids": [accesses[0].case_id, accesses[1].case_id],
        "dossier_nrs": ["2024-0001", "2024-0002"],
    }
    url = reverse("caseaccess-transfer")

    response = client.post(url, data=data, headers={"CONTENT-TYPE": "application/json"})
    assert response.json() == {"data": {"created": 3}}
    assert response.status_code == status.HTTP_201_CREATED
    with pytest.raises(models.CaseAccess.DoesNotExist):
        accesses[0].refresh_from_db()

    assert models.CaseAccess.objects.count() == 5
    assert list(
        models.CaseAccess.objects.filter(identity=new_identity)
        .order_by("case_id")
        .values_list("case_id", flat=True)
    ) == sorted([UUID(accesses[0].case_id), UUID(accesses[1].case_id)])

    assert len(mailoutbox) == 2
    assert mailoutbox[0] == snapshot
    assert mailoutbox[1] == snapshot


def test_transfer_case_fail_nonexistent_ids(client):
    to_remove = str(uuid4())
    new_1 = str(uuid4())
    new_2 = str(uuid4())
    data = {
        "to_remove_assignees": [to_remove],
        "new_assignees": [new_1, new_2],
        "case_ids": [str(uuid4()), str(uuid4())],
        "dossier_nrs": ["2024-0001", "2024-0002"],
    }
    url = reverse("caseaccess-transfer")

    response = client.post(url, data=data, headers={"CONTENT-TYPE": "application/json"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": [
            {
                "detail": f'Invalid pk "{new_1}" - object does not exist.',
                "status": "400",
                "source": {"pointer": "/data/attributes/new-assignees/0"},
                "code": "does_not_exist",
            },
            {
                "detail": f'Invalid pk "{new_2}" - object does not exist.',
                "status": "400",
                "source": {"pointer": "/data/attributes/new-assignees/1"},
                "code": "does_not_exist",
            },
            {
                "detail": f'Invalid pk "{to_remove}" - object does not exist.',
                "status": "400",
                "source": {"pointer": "/data/attributes/to-remove-assignees/0"},
                "code": "does_not_exist",
            },
        ]
    }


def test_transfer_case_fail_required_failure(client, snapshot):
    url = reverse("caseaccess-transfer")

    data = {
        "to_remove_assignees": [],
        # empty new_assignees will fail
        "new_assignees": [],
        "case_ids": [],
    }

    response = client.post(url, data=data, headers={"CONTENT-TYPE": "application/json"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot


def test_transfer_case_fail_unequal_list_len(
    client, case_access_factory, identity_factory, mailoutbox, snapshot
):
    access = case_access_factory(email=None, identity=identity_factory())

    data = {
        "to_remove_assignees": [],
        "new_assignees": [str(access.identity.pk)],
        "case_ids": [access.case_id],
        "dossier_nrs": ["2024-0001", "2024-0002"],
    }
    url = reverse("caseaccess-transfer")

    response = client.post(url, data=data, headers={"CONTENT-TYPE": "application/json"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot


@pytest.mark.freeze_time("1970-01-01")
@pytest.mark.parametrize("client", ["user", "staff", "admin"], indirect=["client"])
@pytest.mark.parametrize(
    "endpoint",
    ["acknowledgement", "credit-approval"],
)
@pytest.mark.parametrize("identity__idp_id", ["e5dabdd0-bafb-4b75-82d2-ccf9295b623b"])
@pytest.mark.parametrize("missing_identity", [False, True])
@pytest.mark.parametrize("language", [lang[0] for lang in settings.LANGUAGES])
def test_download(
    db,
    address,
    language,
    client,
    case_access_factory,
    identity_factory,
    dms_mock,
    acknowledgement_mock,
    credit_approval_mock,
    snapshot,
    endpoint,
    missing_identity,
):
    case_id = "e535ac0c-f3be-4a36-b2d4-1ef405ec71c8"
    case_access = case_access_factory(
        identity=identity_factory(), email=None, case_id=case_id
    )
    address.identity.language = language
    address.identity.save()
    if endpoint == "acknowledgement":
        acknowledgement_mock()
    else:
        credit_approval_mock()

    if missing_identity:
        address.identity.delete()

    url = reverse(f"downloads-{endpoint}", args=[case_id])

    response = client.get(url, HTTP_ACCEPT_LANGUAGE=language)

    assert response.status_code == status.HTTP_200_OK
    assert dms_mock.called_once
    assert (
        dms_mock.request_history[0].path
        == f"/api/v1/template/{endpoint}-{language}/merge/"
    )

    expected_email = (
        case_access.identity.email if missing_identity else address.identity.email
    )
    assert (
        dms_mock.request_history[0].json()["data"]["identity"]["email"]
        == expected_email
    )
    snapshot.assert_match(dms_mock.request_history[0].json())
    snapshot.assert_match(response.headers["content-disposition"])


@pytest.mark.parametrize(
    "identity_exists,external_exists,expected_email",
    [
        (True, True, "gql@example.com"),
        (False, True, "external@example.com"),
        (False, False, "staff@example.com"),
    ],
)
def test_download_get_identity(
    db,
    case_access_factory,
    identity_factory,
    membership_factory,
    identity_exists,
    external_exists,
    expected_email,
):
    gql_identity = identity_factory(email="gql@example.com")
    staff_identity = membership_factory(
        organisation__is_organisation=True,
        organisation__organisation_name=settings.STAFF_ORGANISATION_NAME,
        authorized=True,
        identity__email="staff@example.com",
    ).identity
    external_identity = identity_factory(email="external@example.com")

    case_id = uuid4()

    with freeze_time("2024-01-01"):
        case_access_factory(case_id=case_id, identity=staff_identity, email=None)

    if external_exists:
        with freeze_time("2024-01-02"):
            case_access_factory(case_id=case_id, identity=external_identity, email=None)

    identity_id = gql_identity.idp_id if identity_exists else uuid4()

    identity = CaseDownloadViewSet().get_identity(str(identity_id), str(case_id))
    assert identity.email == expected_email


@pytest.mark.parametrize(
    "endpoint",
    ["acknowledgement", "credit-approval"],
)
@pytest.mark.parametrize("identity__idp_id", ["e5dabdd0-bafb-4b75-82d2-ccf9295b623b"])
def test_download_dms_failure(
    db,
    identity,
    address_factory,
    client,
    acknowledgement_mock,
    credit_approval_mock,
    requests_mock,
    endpoint,
):
    address_factory(identity=identity)

    if endpoint == "acknowledgement":
        acknowledgement_mock()
    else:
        credit_approval_mock()

    matcher = re.compile(
        build_url(
            settings.DOCUMENT_MERGE_SERVICE_URL,
            "template",
            ".*",
            "merge",
            trailing=True,
        ),
    )

    requests_mock.post(
        matcher,
        status_code=status.HTTP_400_BAD_REQUEST,
        json=["something went wrong"],
        headers={"CONTENT-TYPE": "application/json"},
    )

    case_id = "e535ac0c-f3be-4a36-b2d4-1ef405ec71c8"
    url = reverse(f"downloads-{endpoint}", args=[case_id])

    response = client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "errors": ["something went wrong"],
        "source": "DMS",
        "status": 400,
    }


@pytest.mark.usefixtures("_caluma_files_mock")
@pytest.mark.parametrize("dms_failure", [False, True])
@pytest.mark.parametrize("data", [CALUMA_DATA_FULL, CALUMA_DATA_EMPTY])
@pytest.mark.parametrize("identity__idp_id", ["e5dabdd0-bafb-4b75-82d2-ccf9295b623b"])
def test_download_application(
    dms_mock,
    requests_mock,
    graphql_mock,
    client,
    identity,
    snapshot,
    dms_failure,
    data,
):
    graphql_id_response = {"data": {"node": {"document": {"id": "GLOBAL_ID"}}}}
    graphql_mock(graphql_id_response, data)
    if dms_failure:
        requests_mock.post(
            build_url(
                settings.DOCUMENT_MERGE_SERVICE_URL,
                "template",
                settings.DOCUMENT_MERGE_SERVICE_APPLICATION_EXPORT_SLUG,
                "merge",
                trailing=True,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
            json=["something went wrong"],
            headers={"CONTENT-TYPE": "application/json"},
        )

    url = reverse("downloads-application", args=[str(uuid4())])

    response = client.get(url)

    if dms_failure:
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {
            "errors": ["something went wrong"],
            "source": "DMS",
            "status": 400,
        }
        return

    assert response.status_code == status.HTTP_200_OK
    assert dms_mock.called_once
    assert (
        dms_mock.request_history[0].path
        == f"/api/v1/template/{settings.DOCUMENT_MERGE_SERVICE_APPLICATION_EXPORT_SLUG}/merge/"
    )

    snapshot.assert_match(dms_mock.request_history[0].json())
    snapshot.assert_match(response.headers["content-disposition"])
    snapshot.assert_match(response.getvalue())
