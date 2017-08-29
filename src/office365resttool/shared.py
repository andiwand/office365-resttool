import os
import json
import requests
from requests_oauthlib import OAuth2Session

FORMAT_TIME = "%Y-%m-%dT%H:%M:%SZ"

AUTHORIZATION_BASE_URL = "https://login.windows.net/0312b67a-2a67-495b-b636-952512d0b16b/oauth2/authorize"
TOKEN_URL = "https://login.windows.net/0312b67a-2a67-495b-b636-952512d0b16b/oauth2/token"
REDIRECT_URL = "https://localhost/"

class StreamList(list):
    def __init__(self, gen):
        super(StreamList, self).__init__()
        self.__gen = gen
    def __iter__(self):
        return self.__gen
    def __len__(self):
        return 1

def input_authorization(authorization_url):
    print("open this in the browser:", authorization_url)
    return input("put the redirected url here: ")

def login(client_id, scope, resource, authorization=input_authorization):
    # avoid oauthlib exceptions on warnings
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "y"

    office = OAuth2Session(client_id, scope=scope, redirect_uri=REDIRECT_URL)
    authorization_url, state = office.authorization_url(AUTHORIZATION_BASE_URL)
    authorization_response = authorization(authorization_url)
    token = office.fetch_token(TOKEN_URL, authorization_response=authorization_response, resource=resource)
    return office

def store_token(token, path):
    with open(path, "w") as f:
        json.dump(token, f, sort_keys=True, indent=4, separators=(",", ": "))

def load_token(path):
    if not os.path.isfile(path): return None
    with open(path, "r") as f:
        return json.load(f)

def login_auto(client_id, scope, resource, token_path, authorization=input_authorization):
    token = load_token(token_path)
    if token is None:
        office = login(client_id, scope, resource, authorization)
        store_token(office.token, token_path)
    else:
        office = OAuth2Session(client_id, token=token)
    return office

def get_all(office, url, headers={}):
    while True:
        response = office.get(url, headers=headers)
        response = response.json()
        for entry in response["value"]:
            yield entry
        if "@odata.nextLink" not in response: break
        url = response["@odata.nextLink"]

