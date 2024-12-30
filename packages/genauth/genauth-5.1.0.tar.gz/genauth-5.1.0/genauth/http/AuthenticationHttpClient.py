# coding: utf-8

from pickle import FALSE
from ..version import __version__
import requests
import base64


class AuthenticationHttpClient(object):
    def __init__(
        self,
        app_id,
        app_secret,
        host,
        lang,
        use_unverified_ssl,
        token_endpoint_auth_method,
        real_ip
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.host = host
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl or FALSE
        self.access_token = None
        self.token_endpoint_auth_method = token_endpoint_auth_method
        self.real_ip = real_ip

    def set_access_token(self, access_token):
        self.access_token = access_token

    def request(self, method, url, json=None, **kwargs):
        url = "%s%s" % (self.host, url)

        # Remove null values from json
        if json:
            json = {k: v for k, v in json.items() if v is not None}
        headers = {
            "x-genauth-sdk-version": "python:%s" % __version__,
            "x-genauth-request-from": "sdk",
            "x-genauth-app-id": self.app_id,
            "x-genauth-lang": self.lang,
        }
        
        if self.real_ip:
            headers['x-real-ip'] = self.real_ip
        
        # If the tokenEndPointAuthMethod is set to client_secret_basic and the called is /oidc related interface:
        # 1. Get token: /oidc(oauth)/token
        # 2. Revoke token: /oidc(oauth)/token/revocation
        # 3. Check token: /oidc(oauth)/token/introspection
        # 4. Other login to get token interface
        endpoints_to_send_basic_header = [
            "/oidc/token",
            "/oidc/token/revocation",
            "/oidc/token/introspection",
            "/oauth/token",
            "/oauth/token/revocation",
            "/oauth/token/introspection",
            "/api/v3/signin",
            "/api/v3/signin-by-mobile",
            "/api/v3/exchange-tokenset-with-qrcode-ticket",
        ]
        if self.token_endpoint_auth_method and url in endpoints_to_send_basic_header:
            headers["authorization"] = (
                "Basic "
                + base64.b64encode(
                    ("%s:%s" % (self.app_id, self.app_secret)).encode()
                ).decode()
            )
        elif self.access_token:
            headers["authorization"] = self.access_token
        verify = not self.use_unverified_ssl
        r = requests.request(
            method=method, url=url, headers=headers, json=json, verify=verify, **kwargs
        )
        data = r.json()
        return data
