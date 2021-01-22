import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize("model", ["category", "option"])
def test_interest_detail(
    db,
    client,
    expected_status,
    model,
    interest_option,
):
    include = {"include": "options"}
    obj = interest_option.category
    if model == "option":
        include = {"include": "category"}
        obj = interest_option

    url = reverse(f"interest{model}-detail", args=[obj.pk])

    response = client.get(url, include)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(obj.pk)
    json_type = "interest-options"
    obj_id = str(interest_option.pk)
    if model == "option":
        json_type = "interest-categories"
        obj_id = str(interest_option.category.pk)
    assert json["included"][0]["type"] == json_type
    assert json["included"][0]["id"] == obj_id


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
@pytest.mark.parametrize("model", ["category", "option"])
def test_interest_list(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
    interest_option_factory,
):
    factory = interest_category_factory
    if model == "option":
        factory = interest_option_factory
    factory.create_batch(3)

    url = reverse(f"interest{model}-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == 3


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
    ["category", "option"],
)
def test_interest_create(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
):
    category = interest_category_factory()

    url = reverse(f"interest{model}-list")

    data = {
        "data": {"type": "interest-categories", "attributes": {"title": {"de": "Foo"}}}
    }
    if model == "option":
        data["data"]["type"] = "interest-options"
        data["data"]["relationships"] = {
            "category": {
                "data": {"id": str(category.pk), "type": "interest-categories"}
            }
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
    ["category", "option"],
)
def test_interest_update(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
    interest_option_factory,
):
    factory = interest_category_factory
    if model == "option":
        factory = interest_option_factory
    obj = factory(title="Bar")

    url = reverse(f"interest{model}-detail", args=[obj.pk])

    data = {
        "data": {
            "id": str(obj.pk),
            "type": "interest-categories",
            "attributes": {"title": {"de": "Foo"}},
        }
    }
    if model == "option":
        category = interest_category_factory()
        data["data"]["type"] = "interest-options"
        data["data"]["relationships"] = {
            "category": {
                "data": {"id": str(category.pk), "type": "interest-categories"}
            }
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
@pytest.mark.parametrize("model", ["category", "option"])
def test_interest_delete(
    db,
    client,
    expected_status,
    model,
    interest_category_factory,
    interest_option_factory,
):
    factory = interest_category_factory
    if model == "option":
        factory = interest_option_factory
    obj = factory()

    url = reverse(f"interest{model}-detail", args=[obj.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_204_NO_CONTENT:
        return

    with pytest.raises(obj.__class__.DoesNotExist):
        obj.refresh_from_db()
