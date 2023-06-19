from django.core.cache import cache

from caluma.caluma_workflow.models import WorkItem
from caluma.extensions.settings import settings

from .api_client import APIClient


def get_api_user_attributes(token, idp_id):
    client = APIClient(token=token)
    result = client.get(f"/identities?filter%5BidpIds%5D={idp_id}")
    attributes = result["data"][0]["attributes"]
    return attributes


def get_cases_for_user_by_access(user):
    cache_key = f"get_case_accesses_for_user_by_access_{user.username}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    client = APIClient(token=user.token.decode())
    result = client.get(f"/case/accesses?filter%5BidpId%5D={user.username}")
    case_ids = set([case["attributes"]["case-id"] for case in result["data"]])
    cache.set(cache_key, case_ids, settings.CASE_ID_CACHE_SECONDS)
    return case_ids


def get_cases_for_user_by_circulation_invite(user):
    cache_key = f"get_case_accesses_for_user_by_circulation_{user.username}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    work_items = WorkItem.objects.filter(
        assigned_users__contains=[user.username], task_id="circulation-decision"
    )
    case_ids_raw = work_items.values_list("case__family__id", "case__id").distinct()
    case_ids = set([str(c_id) for c_ids in case_ids_raw for c_id in c_ids])
    cache.set(cache_key, case_ids, settings.CASE_ID_CACHE_SECONDS)
    return case_ids


def get_cases_for_user(user):
    case_ids = list(get_cases_for_user_by_access(user)) + list(
        get_cases_for_user_by_circulation_invite(user)
    )

    return set(case_ids)


def get_users_for_case(case):
    client = APIClient()
    token = client.get_admin_token()
    result = client.get(
        f"/case/accesses?filter%5BcaseIds%5D={str(case.pk)}&include=identity",
        token=token,
    )
    users = []
    for include in result.get("included", []):
        users.append(include["attributes"])

    return users


def format_currency(value, currency):
    if currency and (isinstance(value, float) or isinstance(value, int)):
        value = f"{currency.upper()} {value:_.2f}".replace(".00", ".-").replace(
            "_", "'"
        )
    return value
