import pytest
from django.urls import reverse
from rest_framework import status


def remove_underscore(value):
    return value.replace("_", "")


@pytest.mark.parametrize(
    "client,public,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_200_OK),
        ("staff", False, status.HTTP_200_OK),
        ("admin", False, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize("model", ["interest_category", "interest"])
def test_interest_detail(
    db,
    client,
    expected_status,
    model,
    interest,
    public,
):
    include = {"include": "interests"}
    obj = interest.category
    obj.public = public
    obj.save()
    if model == "interest":
        include = {"include": "category"}
        obj = interest

    url = reverse(f"{remove_underscore(model)}-detail", args=[obj.pk])

    response = client.get(url, include)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(obj.pk)
    json_type = "interests"
    obj_id = str(interest.pk)
    if model == "interest":
        json_type = "interest-categories"
        obj_id = str(interest.category.pk)
    assert json["included"][0]["type"] == json_type
    assert json["included"][0]["id"] == obj_id


@pytest.mark.parametrize(
    "client,public,expected_count",
    [
        ("user", False, 0),
        ("user", True, 3),
        ("staff", False, 3),
        ("admin", False, 3),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize("model", ["interest_category", "interest"])
def test_interest_list(
    db,
    client,
    public,
    expected_count,
    model,
    interest_category_factory,
    interest_factory,
):
    factory = interest_category_factory
    factory_kwargs = {"public": public}
    if model == "interest":
        factory = interest_factory
        factory_kwargs = {"category__public": public}
    factory.create_batch(3, **factory_kwargs)

    url = reverse(f"{remove_underscore(model)}-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_201_CREATED),
        ("admin", status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize(
    "model",
    ["interest_category", "interest"],
)
def test_interest_create(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
):
    category = interest_category_factory()

    url = reverse(f"{remove_underscore(model)}-list")

    data = {
        "data": {"type": "interest-categories", "attributes": {"title": {"de": "Foo"}}},
    }
    if model == "interest":
        data["data"]["type"] = "interests"
        data["data"]["relationships"] = {
            "category": {
                "data": {"id": str(category.pk), "type": "interest-categories"},
            },
        }

    response = client.post(url, data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_201_CREATED:
        return

    json = response.json()
    assert json["data"]["attributes"]["title"] == {"de": "Foo", "en": "", "fr": ""}


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize(
    "model",
    ["interest_category", "interest"],
)
def test_interest_update(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
    interest_factory,
):
    factory = interest_category_factory
    if model == "interest":
        factory = interest_factory
    obj = factory(title="Bar")

    url = reverse(f"{remove_underscore(model)}-detail", args=[obj.pk])

    data = {
        "data": {
            "id": str(obj.pk),
            "type": "interest-categories",
            "attributes": {"title": {"de": "Foo"}},
        },
    }
    if model == "interest":
        category = interest_category_factory()
        data["data"]["type"] = "interests"
        data["data"]["relationships"] = {
            "category": {
                "data": {"id": str(category.pk), "type": "interest-categories"},
            },
        }

    response = client.patch(url, data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["attributes"]["title"] == {"de": "Foo", "en": "", "fr": ""}
    obj.refresh_from_db()
    assert dict(obj.title) == {"de": "Foo", "en": "", "fr": ""}


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize("model", ["interest_category", "interest"])
def test_interest_delete(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
    interest_factory,
):
    factory = interest_category_factory
    if model == "interest":
        factory = interest_factory
    obj = factory()

    url = reverse(f"{remove_underscore(model)}-detail", args=[obj.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_204_NO_CONTENT:
        return

    with pytest.raises(obj.__class__.DoesNotExist):
        obj.refresh_from_db()
