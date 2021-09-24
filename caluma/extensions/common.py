from .api_client import APIClient


def get_api_user_attributes(token, idp_id):
    client = APIClient(token=token)
    result = client.get(f"/identities?filter%5BidpIds%5D={idp_id}")
    attributes = result["data"][0]["attributes"]
    return attributes
