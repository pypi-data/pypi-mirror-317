# coding: utf-8

from pickle import FALSE
from ..version import __version__
from ..ManagementTokenProvider import ManagementTokenProvider
import requests

class ManagementHttpClient(object):
    def __init__(self, host, lang, use_unverified_ssl, access_key_id, access_key_secret):
        self.host = host
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl or FALSE
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.token_provider = ManagementTokenProvider(
            host=self.host,
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret
        )

    def request(self, method, url, json=None, **kwargs):
        url = "%s%s" % (self.host, url)

        # Remove null values from json
        if json:
            json = {k: v for k, v in json.items() if v is not None}
        token, userpool_id = self.token_provider.get_access_token()
        headers = {
            "x-genauth-sdk-version": "genauth-py-sdk:%s" % __version__,
            "x-genauth-userpool-id": userpool_id if userpool_id else None,
            'x-genauth-lang': self.lang or ''
        }
        if token:
            headers["authorization"] = "Bearer %s" % token
        verify = not self.use_unverified_ssl
        r = requests.request(method=method, url=url, headers=headers, json=json, verify=verify, **kwargs)
        data = r.json()
        return data
