"""
Hush OAuth2 plugin for HTTPie.
"""

from __future__ import absolute_import, print_function

import json
import os
import sys
import tempfile
import time
from urllib.parse import urlparse

import requests
from httpie.plugins import AuthPlugin
from httpie.status import ExitStatus

__version__ = "0.2"
__author__ = "Gilad Sever"
__licence__ = "Apache 2.0"

# APIs
LOGIN_API = "/v1/authn/login"
GRANT_TOKEN_API = "/v1/oauth/token"


class HushAuth(object):
    def __init__(self, username, password, org, eorg):
        self.username = username
        self.password = password
        self.org = org
        self.eorg = eorg
        self.verbose = bool(os.getenv("VERBOSE", False))
        self.host_url = None

    def __call__(self, r):
        self.host_url = self._get_host_url(r)
        if not (token := self._load_token_if_valid()):
            token = self._get_token()
            self._store_token(token, token["expires_in"])
        if token:
            r.headers["Authorization"] = f"Bearer {token}"
        return r

    def _get_token(self):
        # Skip token API if the token endpoint doesn't exist
        # This is the case when calling a non-hush endpoint
        if not self._is_token_endpoint_exists():
            return None
        if self.username.startswith("key-") and "@" not in self.username:
            return self._get_api_key_token()
        else:
            return self._get_user_token()

    def _get_api_key_token(self):
        body = {
            "grant_type": "client_credentials",
            "client_id": self.username,
            "client_secret": self.password,
        }
        if self.eorg:
            body["effective_org"] = self.eorg
        return self._call(GRANT_TOKEN_API, "post", body=body)

    def _get_user_token(self):
        body = {
            "org_shortname": self.org,
            "username": self.username,
            "password": self.password,
        }
        response = self._call(LOGIN_API, "post", body=body)
        if response["status"] != "success":
            raise Exception("Could not log in. Returned status: %s", response["status"])

        body = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": response.json()["token"],
        }
        if self.eorg != self.org:
            body["effective_org"] = self.eorg
        return self._call(GRANT_TOKEN_API, "post", body=body)

    def _is_token_endpoint_exists(self):
        url = self.host_url + GRANT_TOKEN_API
        response = requests.options(url=url)
        return response.status_code == 200

    def _call(self, api, method, params=None, body=None):
        url = self.host_url + api
        msg = f"httpie-hush: [{self.eorg}] url={url}"
        if params:
            msg += f", params={params}"
        if body:
            msg += f", body={body}"
        self._vprint(msg)
        response = requests.request(method, url, params=params, json=body)
        response.raise_for_status()
        ret = response.json()
        self._vprint(f"httpie-hush: [{self.eorg}] response={ret}")
        return ret

    @staticmethod
    def _get_host_url(r):
        parsed_url = urlparse(r.url)
        netloc_no_port = parsed_url.netloc.split(":")[0]
        if parsed_url.scheme:
            return f"{parsed_url.scheme}://{netloc_no_port}"
        return netloc_no_port

    def _load_token_if_valid(self):
        path = self._get_token_path()
        try:
            with open(path) as f:
                token_info = json.load(f)
        except BaseException:
            return None
        if token_info["host_url"] != self.host_url:
            return None
        if token_info.get("eorg", self.eorg) != self.eorg:
            return None
        now = time.time()
        if now > (token_info.get("exp", now) - 30):
            return None
        return token_info["token"]

    def _store_token(self, token, expires_in):
        path = self._get_token_path()
        exp = time.time() + expires_in - 30
        token_info = {"token": token, "host_url": self.host_url, "exp": exp}
        if self.eorg:
            token_info["eorg"] = self.eorg
        with open(path, "w") as f:
            json.dump(token_info, f)

    def _get_token_path(self):
        tmpdir = tempfile.gettempdir()
        eorg = f"{self.eorg}." if self.eorg else ""
        org = f"{self.org}." if self.org else ""
        return os.path.join(tmpdir, f"httpie-hush.{eorg}{org}{self.username}")

    def _vprint(self, msg):
        if self.verbose:
            print(msg)


class HushAuthPlugin(AuthPlugin):
    name = "Hush OAuth 2"
    auth_type = "hush"
    description = ""
    auth_require = False

    def get_auth(self, username=None, password=None):
        parts = self.raw_auth.split(":")
        if not 2 <= len(parts) <= 4:
            print("Invalid auth arguments provided")
            sys.exit(ExitStatus.PLUGIN_ERROR)

        username = parts[0] or username or os.getenv("HTTPIE_HUSH_USERNAME")
        password = parts[1] or password or os.getenv("HTTPIE_HUSH_PASSWORD")
        org = parts[2] if len(parts) > 2 else os.getenv("HTTPIE_HUSH_ORG")
        eorg = parts[3] if len(parts) > 3 else os.getenv("EORG")

        self._verify_input(username=username, password=password)
        return HushAuth(username, password, org, eorg)

    @staticmethod
    def _verify_input(**input_params):
        missing = [k for k, v in input_params.items() if not v]
        if missing:
            print(f"httpie-hush error: missing {", ".join(missing)}", file=sys.stderr)
            sys.exit(ExitStatus.PLUGIN_ERROR)
