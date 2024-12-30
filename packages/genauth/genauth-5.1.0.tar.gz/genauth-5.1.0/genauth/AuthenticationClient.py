# coding: utf-8

from .exceptions import GenAuthWrongArgumentException
from .http.AuthenticationHttpClient import AuthenticationHttpClient
from .http.ProtocolHttpClient import ProtocolHttpClient
from .utils import get_random_string, url_join_args
import base64
import hashlib
import json
import jwt

from .utils.wss import handleMessage


class AuthenticationClient(object):
    """GenAuth Authentication Client"""

    def __init__(
            self,
            app_id,
            app_host,
            app_secret=None,
            access_token=None,
            timeout=10.0,
            protocol=None,
            token_endpoint_auth_method=None,
            introspection_endpoint_auth_method=None,
            revocation_endpoint_auth_method=None,
            redirect_uri=None,
            post_logout_redirect_uri=None,
            use_unverified_ssl=False,
            lang=None,
            websocket_host=None,
            websocket_endpoint=None,
            real_ip=None
    ):

        """
        Initialize AuthenticationClient parameters

        Args:
            app_id (str): GenAuth application ID
            app_host (str): GenAuth application URL, e.g. https://your-app.genauth.ai
            app_secret (str): GenAuth application secret
            enc_public_key (str): Password asymmetric encryption public key (optional). If you are using GenAuth public cloud service, you can ignore it; if you are using privately deployed GenAuth, please contact GenAuth IDaaS service administrator
            timeout (int): Request timeout in milliseconds, default is 10000 (10 seconds)
            lang (str): Interface Message return language format (optional), optional values are zh-CN and en-US, default is zh-CN.
            protocol (str): Protocol type, optional values are oidc, oauth, saml, cas
            token_endpoint_auth_method (str): Token endpoint authentication method, optional values are client_secret_post, client_secret_basic, none, default is client_secret_post.
            introspection_endpoint_auth_method (str): Token introspection endpoint authentication method, optional values are client_secret_post, client_secret_basic, none, default is client_secret_post.
            revocation_endpoint_auth_method (str): Token revocation endpoint authentication method, optional values are client_secret_post, client_secret_basic, none, default is client_secret_post.
            redirect_uri (str): Redirect URL after authentication. Optional, defaults to the first callback URL configured in the console.
            post_logout_redirect_uri(str): Redirect URL after logout
            real_ip (str): Client real IP, if not provided, server IP will always be used as request IP, which may affect rate limiting policies for interfaces like sending verification codes.
        """
        if not app_id:
            raise Exception('Please provide app_id')

        self.app_id = app_id
        self.app_host = app_host or "https://api.genauth.ai"
        self.timeout = timeout
        self.access_token = access_token
        self.lang = lang
        self.protocol = protocol or 'oidc'
        self.app_secret = app_secret
        self.token_endpoint_auth_method = token_endpoint_auth_method or 'client_secret_post'
        self.introspection_endpoint_auth_method = introspection_endpoint_auth_method or 'client_secret_post'
        self.revocation_endpoint_auth_method = revocation_endpoint_auth_method or 'client_secret_post'
        self.redirect_uri = redirect_uri
        self.use_unverified_ssl = use_unverified_ssl
        self.post_logout_redirect_uri = post_logout_redirect_uri
        self.websocket_host = websocket_host or "wss://events.genauth.ai"
        self.websocket_endpoint = websocket_endpoint or "/events/v1/authentication/sub"
        self.real_ip = real_ip

        # HTTP Client used for V3 API interfaces
        self.http_client = AuthenticationHttpClient(
            app_id=self.app_id,
            app_secret=self.app_secret,
            host=self.app_host,
            lang=self.lang,
            use_unverified_ssl=self.use_unverified_ssl,
            token_endpoint_auth_method=token_endpoint_auth_method,
            real_ip=real_ip
        )
        if self.access_token:
            self.http_client.set_access_token(self.access_token)

        # HTTP Client used for standard protocol related interfaces
        self.protocol_http_client = ProtocolHttpClient(
            host=self.app_host,
            use_unverified_ssl=self.use_unverified_ssl,
        )

    def set_access_token(self, access_token):
        self.access_token = access_token
        self.http_client.set_access_token(self.access_token)

    def ___get_access_token_by_code_with_client_secret_post(self, code, code_verifier=None):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            }
        )
        return data

    def ___get_access_token_by_code_with_client_secret_basic(self, code, code_verifier=None):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )
        return data

    def __get_access_token_by_code_with_none(self, code, code_verifier=None):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            }
        )
        return data

    def get_access_token_by_code(self, code, code_verifier=None):
        """
        Get user's Token information using authorization code.

        Args:
            code (str): Authorization code, which GenAuth will send to the callback address after successful authentication.
            code_verifier (str): This parameter needs to be filled in when initiating PKCE authorization login.
        """

        if self.protocol not in ['oidc', 'oauth']:
            raise GenAuthWrongArgumentException('argument protocol must be oidc or oauth')

        if not self.redirect_uri:
            raise GenAuthWrongArgumentException('argument redirect_uri must be oidc or oauth')

        if not self.app_secret and self.token_endpoint_auth_method != 'none':
            raise GenAuthWrongArgumentException('argument secret must be provided')

        if self.token_endpoint_auth_method == 'client_secret_post':
            return self.___get_access_token_by_code_with_client_secret_post(code, code_verifier)

        elif self.token_endpoint_auth_method == 'client_secret_basic':
            return self.___get_access_token_by_code_with_client_secret_basic(code, code_verifier)

        elif self.token_endpoint_auth_method == 'none':
            return self.__get_access_token_by_code_with_none(code, code_verifier)

        raise GenAuthWrongArgumentException(
            'unsupported argument token_endpoint_auth_method, must be client_secret_post, client_secret_basic or none')

    def get_access_token_by_client_credentials(self, scope, access_key, access_secret):
        """
        Get an Access Token with permissions using programming access account.

        Args:
            scope (str): Permission items, a space-separated string, each item represents a permission.
            access_key (str): Programming access account AccessKey
            access_secret (str): Programming access account SecretKey
        """

        if not scope:
            raise GenAuthWrongArgumentException(
                'must provide scope argument, see doc here: '
                'https://docs.genauth.ai/v2/guides/authorization/m2m-authz.html')

        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': access_key,
                'client_secret': access_secret,
                'grant_type': 'client_credentials',
                'scope': scope
            }
        )
        return data

    def get_user_info_by_access_token(self, access_token):
        """
        Get user information using Access token.

        Args:
            access_token (str) Access token, the content of the Access token exchanged using the authorization code Code.
        """
        url = "/%s/me" % ('oidc' if self.protocol == 'oidc' else 'oauth')

        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            bearer_token=access_token
        )
        return data

    def __build_saml_authorize_url(self):
        return "%s/api/v2/saml-idp/%s" % (self.app_host, self.app_id)

    def __build_cas_authorize_url(self, service=None):
        if service:
            return "%s/cas-idp/%s?service=%s" % (self.app_host, self.app_id, service)
        else:
            return "%s/cas-idp/%s?service" % (self.app_host, self.app_id)

    def __build_oauth_authorize_url(self, scope=None, redirect_uri=None, state=None, response_type=None):
        res = {
            'state': get_random_string(10),
            'scope': 'user',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code'
        }
        if scope:
            res['scope'] = scope

        if redirect_uri:
            res['redirect_uri'] = redirect_uri

        if state:
            res['state'] = state

        if response_type:
            if response_type not in ['code', 'token']:
                raise GenAuthWrongArgumentException('response_type must be code or token')
            res['response_type'] = response_type

        return url_join_args('%s/oauth/auth' % self.app_host, res)

    def __build_oidc_authorize_url(self, redirect_uri=None, response_type=None, response_mode=None,
                                   state=None, nonce=None, scope=None,
                                   code_challenge_method=None, code_challenge=None):
        """
        Generate user login URL for OIDC protocol.

        Args:
            redirect_uri (str): Callback URL, optional, defaults to the redirectUri parameter when SDK is initialized.
            response_type (str): Response type, optional, can be code, code id_token token, code id_token, code id_token, code token, id_token token, id_token, none; defaults to code, authorization code mode.
            response_mode (str): Response type, optional, can be query, fragment, form_post; defaults to query, which sends code to callback address via browser redirect.
            state (str): Random string, optional, automatically generated by default.
            nonce (str): Random string, optional, automatically generated by default.
            scope (str): Requested permission items, optional, OIDC protocol defaults to openid profile email phone address, OAuth 2.0 protocol defaults to user.
            code_challenge_method (str): Can be plain or S256, indicating the digest algorithm used to calculate code_challenge, plain means no algorithm is used, S256 means code_challenge is calculated using SHA256.
            code_challenge (str): A string with length greater than or equal to 43, sent to GenAuth as code_challenge.
        """
        res = {
            'nonce': get_random_string(10),
            'state': get_random_string(10),
            'scope': 'openid profile email phone address',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code'
        }

        if redirect_uri:
            res['redirect_uri'] = redirect_uri

        if response_type:
            res['response_type'] = response_type

        if response_mode:
            res['response_mode'] = response_mode

        if state:
            res['state'] = state

        if scope:
            res['scope'] = scope
            if 'offline_access' in scope:
                res['prompt'] = 'consent'

        if nonce:
            res['nonce'] = nonce

        if code_challenge:
            res['code_challenge'] = code_challenge

        if code_challenge_method:
            res['code_challenge_method'] = code_challenge_method

        return url_join_args('%s/oidc/auth' % self.app_host, res)

    def build_authorize_url(
            self,
            redirect_uri=None,
            response_type=None,
            response_mode=None,
            state=None,
            nonce=None,
            scope=None,
            code_challenge_method=None,
            code_challenge=None,
            service=None
    ):
        """
        Generate URL link for user login.
        """
        if not self.app_host:
            raise GenAuthWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.protocol == 'oidc':
            return self.__build_oidc_authorize_url(
                response_mode=response_mode,
                response_type=response_type,
                redirect_uri=redirect_uri,
                state=state,
                nonce=nonce,
                scope=scope,
                code_challenge=code_challenge,
                code_challenge_method=code_challenge_method
            )
        elif self.protocol == 'oauth':
            return self.__build_oauth_authorize_url(
                scope=scope,
                redirect_uri=redirect_uri,
                state=state,
                response_type=response_type
            )
        elif self.protocol == 'saml':
            return self.__build_saml_authorize_url()

        elif self.protocol == 'cas':
            return self.__build_cas_authorize_url(service=service)

        else:
            raise GenAuthWrongArgumentException('protocol must be oidc oauth saml or cas')

    def generate_code_challenge(self, length=43):
        """
        Generate a PKCE verification code with length greater than or equal to 43.

        Args:
            length (int): Verification code length, defaults to 43.
        """
        if not isinstance(length, int):
            raise GenAuthWrongArgumentException('length must be a int')

        if length < 43:
            raise GenAuthWrongArgumentException('length must be grater than 43')

        return get_random_string(length)

    def generate_code_challenge_digest(self, code_challenge, method=None):
        """
        Generate a PKCE verification code digest value.

        Args:
            code_challenge (str): The original code_challenge value to generate digest for, a random string with length greater than or equal to 43.
            method (str): Can be plain or S256, indicating the digest algorithm used to calculate code_challenge. plain means return as is without any algorithm, S256 means calculate code_challenge digest using SHA256.
        """
        if len(code_challenge) < 43:
            raise GenAuthWrongArgumentException('code_challenge must be a string length grater than 43')

        if not method:
            method = 'S256'

        if method not in ['S256', 'plain']:
            raise GenAuthWrongArgumentException('method must be S256 or plain')

        if method == 'S256':
            code_challenge = hashlib.sha256(code_challenge.encode('utf-8')).digest()
            code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
            code_challenge = code_challenge.replace('=', '')
            return code_challenge

        elif method == 'plain':
            return code_challenge

        else:
            raise GenAuthWrongArgumentException('unsupported method, must be S256 or plain')

    def __build_oidc_logout_url(self, redirect_uri=None, id_token=None):
        if redirect_uri and id_token:
            return "%s/oidc/session/end?id_token_hint=%s&post_logout_redirect_uri=%s" % (
                self.app_host,
                id_token,
                redirect_uri
            )
        elif (redirect_uri and not id_token) or (id_token and not redirect_uri):
            raise GenAuthWrongArgumentException('must pass redirect_uri and id_token together')
        else:
            return "%s/oidc/session/end" % self.app_host

    def __build_easy_logout_url(self, redirect_uri=None):
        if redirect_uri:
            return "%s/login/profile/logout?redirect_uri=%s" % (
                self.app_host,
                redirect_uri
            )
        else:
            return "%s/login/profile/logout" % (
                self.app_host
            )

    def __build_cas_logout_url(self, redirect_uri=None):
        if redirect_uri:
            return "%s/cas-idp/logout?url=%s" % (
                self.app_host,
                redirect_uri
            )
        else:
            return "%s/cas-idp/logout" % (
                self.app_host
            )

    def build_logout_url(self, redirect_uri=None, id_token=None, state=None):
        """Build logout URL

        Attributes:
            redirect_uri(str): The target URL to redirect to after logout
            id_token(str): ID Token obtained during user login, used to invalidate user token, recommended to pass
            state(str): Intermediate state identifier passed to target URL
        """
        if not self.app_host:
            raise GenAuthWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.protocol == 'oidc':
            return self.__build_oidc_logout_url(
                id_token=id_token,
                redirect_uri=redirect_uri or self.post_logout_redirect_uri
            )
        elif self.protocol == 'cas':
            return self.__build_cas_logout_url(redirect_uri=redirect_uri)
        else:
            return self.__build_easy_logout_url(redirect_uri)

    def __get_new_access_token_by_refresh_token_with_client_secret_post(self, refresh_token):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        return data

    def __get_new_access_token_by_refresh_token_with_client_secret_basic(self, refresh_token):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )
        return data

    def __get_new_access_token_by_refresh_token_with_none(self, refresh_token):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        return data

    def get_new_access_token_by_refresh_token(self, refresh_token):
        """
        Get new Access token using Refresh token.

        Args:
            refresh_token (str): Refresh token, can be obtained from the refresh_token in the return value of AuthenticationClient.get_access_token_by_code method.
                                Note: refresh_token is only returned when scope contains offline_access.

        """
        if self.protocol not in ['oauth', 'oidc']:
            raise GenAuthWrongArgumentException('protocol must be oauth or oidc')

        if not self.app_secret and self.token_endpoint_auth_method != 'none':
            raise GenAuthWrongArgumentException('secret must be provided')

        if self.token_endpoint_auth_method == 'client_secret_post':
            return self.__get_new_access_token_by_refresh_token_with_client_secret_post(refresh_token)
        elif self.token_endpoint_auth_method == 'client_secret_basic':
            return self.__get_new_access_token_by_refresh_token_with_client_secret_basic(refresh_token)
        elif self.token_endpoint_auth_method == 'none':
            return self.__get_new_access_token_by_refresh_token_with_none(refresh_token)
        else:
            raise GenAuthWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __revoke_token_with_client_secret_post(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'token': token
            },
            raw_content=True
        )
        return True

    def __revoke_token_with_client_secret_basic(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode(),
            raw_content=True
        )
        return True

    def __revoke_token_with_none(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'token': token
            },
            raw_content=True
        )
        return True

    def revoke_token(self, token):
        """
        Revoke Access token or Refresh token. The holder of Access token or Refresh token can notify GenAuth that the token is no longer needed and request GenAuth to revoke it.

        Args:
            token (str): Access token or Refresh token, can be obtained from access_token or refresh_token in the return value of AuthenticationClient.get_access_token_by_code method.
                        Note: refresh_token is only returned when scope contains offline_access.
        """
        if self.protocol not in ['oauth', 'oidc']:
            raise GenAuthWrongArgumentException('protocol must be oauth or oidc')

        if not self.app_secret and self.revocation_endpoint_auth_method != 'none':
            raise GenAuthWrongArgumentException('secret must be provided')

        if self.revocation_endpoint_auth_method == 'client_secret_post':
            return self.__revoke_token_with_client_secret_post(token)

        elif self.revocation_endpoint_auth_method == 'client_secret_basic':
            return self.__revoke_token_with_client_secret_basic(token)

        elif self.revocation_endpoint_auth_method == 'none':
            return self.__revoke_token_with_none(token)

        else:
            raise GenAuthWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __introspect_token_with_client_secret_post(self, token):
        url = "/%s/token/introspection" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'token': token
            }
        )

    def __introspect_token_with_client_secret_basic(self, token):
        url = "/%s/token/introspection" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )

    def __introspect_token_with_none(self, token):
        url = "/%s/token/introspection" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'token': token
            }
        )

    def introspect_token(self, token):
        """
        Online validate the status of Access token or Refresh token.

        Args:
            token (str): Access token or Refresh token, can be obtained from access_token or refresh_token in the return value of AuthenticationClient.get_access_token_by_code method.
                        Note: refresh_token is only returned when scope contains offline_access.
        """
        if self.protocol not in ['oauth', 'oidc']:
            raise GenAuthWrongArgumentException('protocol must be oauth or oidc')

        if not self.app_secret and self.introspection_endpoint_auth_method != 'none':
            raise GenAuthWrongArgumentException('secret must be provided')

        if self.introspection_endpoint_auth_method == 'client_secret_post':
            return self.__introspect_token_with_client_secret_post(token)

        elif self.introspection_endpoint_auth_method == 'client_secret_basic':
            return self.__introspect_token_with_client_secret_basic(token)

        elif self.introspection_endpoint_auth_method == 'none':
            return self.__introspect_token_with_none(token)

        else:
            raise GenAuthWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __fetch_jwks(self, server_jwks=None):
        if server_jwks:
            return server_jwks
        else:
            keys = self.protocol_http_client.request(
                method="GET",
                url="/oidc/.well-known/jwks.json"
            )
            return keys

    def introspect_token_offline(self, token, server_jwks=None):
        """
        Locally validate the status of Access token or Refresh token.

        Args:
            token (str): Access token or Refresh token, can be obtained from access_token or refresh_token in the return value of AuthenticationClient.get_access_token_by_code method.
                        Note: refresh_token is only returned when scope contains offline_access.
            serverJWKS: Server's JWKS public key used to verify Token signature, by default will be automatically obtained through network request from server's JWKS endpoint
        """
        jwks = self.__fetch_jwks(server_jwks)
        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        kid = jwt.get_unverified_header(token)['kid']
        key = public_keys[kid]
        payload = jwt.decode(token, key=key, algorithms=['RS256'], audience=self.app_id)
        return payload

    def validate_ticket_v1(self, ticket, service):
        """
        Validate CAS 1.0 Ticket validity.

        Args:
            ticket (str): Ticket issued by GenAuth after successful CAS authentication.
            service (str): CAS callback URL.
        """
        url = '/cas-idp/%s/validate?service=%s&ticket=%s' % (self.app_id, service, ticket)
        data = self.protocol_http_client.request(
            method='GET',
            url=url
        )
        raw_valid, username = data.split('\n')
        valid = raw_valid == 'yes'
        res = {
            'valid': valid
        }
        if username:
            res['username'] = username
        if not valid:
            res['message'] = 'ticket is not valid'

    # ==== Based on signInByCredentials wrapped login methods BEGIN
    def sign_in_by_email_password(self, email, password, options=None):
        """
        Login using email + password
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "email": email,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_phone_password(self, phone, password, options=None):
        """
        Login using phone number + password
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "phone": phone,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_username_password(self, username, password, options=None):
        """
        Login using username + password
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "username": username,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_account_password(self, account, password, options=None):
        """
        Login using account (username/phone/email) + password
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "account": account,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_email_passcode(self, email, pass_code, options=None):
        """
        Login using email + verification code
        """
        return self.sign_in_by_credentials(
            connection="PASSCODE",
            pass_code_payload={
                "email": email,
                "passCode": pass_code,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_phone_passcode(self, phone, pass_code, phone_country_code=None, options=None):
        """
        Login using phone number + verification code
        """
        return self.sign_in_by_credentials(
            connection="PASSCODE",
            pass_code_payload={
                "phone": phone,
                "passCode": pass_code,
                "phoneCountryCode": phone_country_code
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_ldap(self, sAMAccountName, password, options=None):
        """
        Login using LDAP account and password
        """
        return self.sign_in_by_credentials(
            connection="LDAP",
            ldap_payload={
                "sAMAccountName": sAMAccountName,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_ad(self, sAMAccountName, password, options=None):
        """
        Login using AD account and password
        """
        return self.sign_in_by_credentials(
            connection="AD",
            ad_payload={
                "sAMAccountName": sAMAccountName,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    # ==== Based on signInByCredentials wrapped login methods BEGIN

    # ==== Based on signup wrapped registration methods BEGIN
    def sign_up_by_email_password(self, email, password, profile=None, options=None):
        """
        Register using email + password
        """
        return self.sign_up(
            connection="PASSWORD",
            password_payload={
                "email": email,
                "password": password,
            },
            profile=profile,
            options=options
        )

    def sign_up_by_username_password(self, username, password, profile=None, options=None):
        """
        Register using username + password
        """
        return self.sign_up(
            connection="PASSWORD",
            password_payload={
                "username": username,
                "password": password,
            },
            profile=profile,
            options=options
        )

    def sign_up_by_email_passcode(self, email, pass_code, profile=None, options=None):
        """
        Register using email + verification code
        """
        return self.sign_up(
            connection="PASSCODE",
            pass_code_payload={
                "email": email,
                "passCode": pass_code,
            },
            profile=profile,
            options=options
        )

    def sign_up_by_phone_passcode(self, phone, pass_code, phone_country_code=None, profile=None, options=None):
        """
        Register using phone number + verification code
        """
        return self.sign_up(
            connection="PASSCODE",
            pass_code_payload={
                "phone": phone,
                "passCode": pass_code,
                "phoneCountryCode": phone_country_code
            },
            profile=profile,
            options=options
        )

    # ==== Registration methods based on signUp END

    # ==== AUTO GENERATED AUTHENTICATION METHODS BEGIN ====
    def sign_up(self, connection, password_payload=None, pass_code_payload=None, profile=None, options=None):
        """Register

        This endpoint currently supports the following registration methods:

        1. Password-based (PASSWORD): username + password, email + password.
        2. One-time verification code (PASSCODE): phone number + verification code, email + verification code. You need to call the send SMS or send email interface first to get the verification code.

        For social login and other external identity source "registration", please use the **login** interface directly, we will create a new account for them on their first login.

        Attributes:
            connection (str): Registration method:
    - `PASSWORD`: Email password method
    - `PASSCODE`: Email/phone verification code method

            password_payload (dict): Required when registration method is `PASSWORD`.
            pass_code_payload (dict): Required when authentication method is `PASSCODE`
            profile (dict): User profile
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signup',
            json={
                'connection': connection,
                'passwordPayload': password_payload,
                'passCodePayload': pass_code_payload,
                'profile': profile,
                'options': options,
            },
        )

    def generate_link_ext_idp_url(self, ext_idp_conn_identifier, app_id, id_token):
        """Generate link for binding external identity provider

        This interface is used to generate a link for binding external identity provider, after generation you can guide users to jump to it.

        Attributes:
            ext_idp_conn_identifier (str): Unique identifier of external identity provider connection
            app_id (str): GenAuth application ID
            id_token (str): User's id_token
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/generate-link-extidp-url',
            params={
                'ext_idp_conn_identifier': ext_idp_conn_identifier,
                'app_id': app_id,
                'id_token': id_token,
            },
        )

    def unlink_ext_idp(self, ext_idp_id):
        """Unbind external identity provider

        Unbind external identity provider, this interface requires passing the external identity provider ID bound by the user, **note that this is not the identity provider connection ID**.

        Attributes:
            ext_idp_id (str): External identity provider ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unlink-extidp',
            json={
                'extIdpId': ext_idp_id,
            },
        )

    def get_identities(self, ):
        """Get bound external identity providers

        As described in the **Introduction** section, one external identity provider corresponds to multiple external identity provider connections. After a user binds an external identity provider account through an external identity provider connection,
        the user will establish an association relationship with this external identity provider. This interface is used to get all external identity providers bound by this user.

        Depending on the specific implementation of the external identity provider, a user may have multiple identity IDs in the external identity provider, such as `openid` and `unionid` in the WeChat system,
        and `open_id`, `union_id` and `user_id` in Feishu. In GenAuth, we call such an `open_id` or `unionid_` an `Identity`, so a user will have multiple `Identity` records in one identity provider.

        Taking WeChat as an example, if a user logs in with WeChat or binds a WeChat account, their `Identity` information is shown as follows:

        ```json
        [
          {
            "identityId": "62f20932xxxxbcc10d966ee5",
            "extIdpId": "62f209327xxxxcc10d966ee5",
            "provider": "wechat",
            "type": "openid",
            "userIdInIdp": "oH_5k5SflrwjGvk7wqpoBKq_cc6M",
            "originConnIds": ["62f2093244fa5cb19ff21ed3"]
          },
          {
            "identityId": "62f726239xxxxe3285d21c93",
            "extIdpId": "62f209327xxxxcc10d966ee5",
            "provider": "wechat",
            "type": "unionid",
            "userIdInIdp": "o9Nka5ibU-lUGQaeAHqu0nOZyJg0",
            "originConnIds": ["62f2093244fa5cb19ff21ed3"]
          }
        ]
        ```

        You can see that their `extIdpId` is the same, which is the **identity provider ID** you created in GenAuth; `provider` is both `wechat`;
        Through `type` you can distinguish which is `openid`, which is `unionid`, and the specific value (`userIdInIdp`); they all come from the same identity provider connection (`originConnIds`).

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-identities',
        )

    def get_application_enabled_ext_idps(self, ):
        """Get list of enabled external identity providers for application

        Get list of enabled external identity providers for application, frontend can render external identity provider buttons based on this.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-enabled-extidps',
        )

    def sign_in_by_credentials(self, connection, password_payload=None, pass_code_payload=None, ad_payload=None,
                               ldap_payload=None, options=None, client_id=None, client_secret=None):
        """Sign in with user credentials

        This endpoint is a direct API call-based login endpoint, suitable for scenarios where you need to build your own login page. **This endpoint temporarily does not support MFA, information completion, first password reset and other processes. If needed, please use the OIDC standard protocol authentication endpoint.**

        Note: Depending on the **Application Type** you selected when creating the application in GenAuth and the **Token Authentication Method** configured for the application, different forms of client identity verification are required when calling this interface.

        <details>
        <summary>Click to expand details</summary>

        <br>

        You can find the **Token Authentication Method** configuration item in [GenAuth Console](https://console.genauth.ai) under **Applications** - **Self-built Applications** - **Application Details** - **Application Configuration** - **Other Settings** - **Authorization Configuration**:

        > Hidden for Single Page Web Applications and Client Applications, defaults to `none` and cannot be modified; Backend Applications and Standard Web Applications can modify this configuration item.

        ![](https://files.authing.co/api-explorer/tokenAuthMethod.jpg)

        #### When token authentication method is none

        No additional operations are required when calling this interface.

        #### When token authentication method is client_secret_post

        When calling this interface, you must pass `client_id` and `client_secret` parameters in the body as conditions for verifying client identity. Where `client_id` is the application ID and `client_secret` is the application secret.

        #### When token authentication method is client_secret_basic

        When calling this interface, you must carry the `authorization` request header in the HTTP request header as a condition for verifying client identity. The format of the `authorization` request header is as follows (where `client_id` is the application ID and `client_secret` is the application secret):

        ```
        Basic base64(<client_id>:<client_secret>)
        ```

        Result example:

        ```
        Basic NjA2M2ZiMmYzY3h4eHg2ZGY1NWYzOWViOjJmZTdjODdhODFmODY3eHh4eDAzMjRkZjEyZGFlZGM3
        ```

        JS code example:

        ```js
        'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64');
        ```

        </details>

        Attributes:
            connection (str): Authentication method:
    - `PASSWORD`: Use password method for authentication.
    - `PASSCODE`: Use one-time temporary verification code for authentication.
    - `LDAP`: Authenticate based on LDAP user directory.
    - `AD`: Authenticate based on Windows AD user directory.

            password_payload (dict): Required when authentication method is `PASSWORD`.
            pass_code_payload (dict): Required when authentication method is `PASSCODE`
            ad_payload (dict): Required when authentication method is `AD`
            ldap_payload (dict): Required when authentication method is `LDAP`
            options (dict): Optional parameters
            client_id (str): Application ID. Required when application's "Token Authentication Method" is configured as `client_secret_post`.
            client_secret (str): Application secret. Required when application's "Token Authentication Method" is configured as `client_secret_post`.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin',
            json={
                'connection': connection,
                'passwordPayload': password_payload,
                'passCodePayload': pass_code_payload,
                'adPayload': ad_payload,
                'ldapPayload': ldap_payload,
                'options': options,
                'client_id': client_id,
                'client_secret': client_secret,
            },
        )

    def sign_in_by_mobile(self, ext_idp_connidentifier, connection, wechat_payload=None, apple_payload=None,
                          alipay_payload=None, wechatwork_payload=None, wechatwork_agency_payload=None,
                          lark_public_payload=None, lark_internal_payload=None, lark_block_payload=None,
                          yidun_payload=None, wechat_mini_program_code_payload=None,
                          wechat_mini_program_phone_payload=None, wechat_mini_program_code_and_phone_payload=None,
                          google_payload=None, facebook_payload=None, qq_payload=None, weibo_payload=None,
                          baidu_payload=None, linked_in_payload=None, ding_talk_payload=None, github_payload=None,
                          gitee_payload=None, gitlab_payload=None, douyin_payload=None, kuaishou_payload=None,
                          xiaomi_payload=None, line_payload=None, slack_payload=None, oppo_payload=None,
                          huawei_payload=None, amazon_payload=None, options=None, client_id=None, client_secret=None):
        """Mobile social login

        This endpoint is for mobile social login, using temporary credentials returned by third-party mobile social login to authenticate and exchange for user's id_token and access_token. Please read the corresponding social login integration process first.

        Note: Depending on the application type and token exchange authentication method you selected when creating the application in GenAuth, different forms of client identity verification are required when calling this interface.

        <details>
        <summary>Click to expand details</summary>

        <br>

        You can find the "Token Exchange Authentication Method" configuration item in [GenAuth Console](https://console.genauth.ai) under **Applications** - **Self-built Applications** - **Application Details** - **Application Configuration** - **Other Settings** - **Authorization Configuration**:

        > Hidden for Single Page Web Applications and Client Applications, defaults to `none` and cannot be modified; Backend Applications and Standard Web Applications can modify this configuration item.

        ![](https://files.authing.co/api-explorer/tokenAuthMethod.jpg)

        #### When token exchange authentication method is none

        No additional operations required when calling this interface.

        #### When token exchange authentication method is client_secret_post

        Must pass client_id and client_secret parameters in the body when calling this interface as conditions for verifying client identity. Where client_id is the application ID and client_secret is the application secret.

        #### When token exchange authentication method is client_secret_basic

        Must carry the authorization request header in the HTTP request header when calling this interface as a condition for verifying client identity. The format of the authorization request header is as follows (where client_id is the application ID and client_secret is the application secret):

        ```
        Basic base64(<client_id>:<client_secret>)
        ```

        Example result:

        ```
        Basic NjA2M2ZiMmYzY3h4eHg2ZGY1NWYzOWViOjJmZTdjODdhODFmODY3eHh4eDAzMjRkZjEyZGFlZGM3
        ```

        JS code example:

        ```js
        'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64');
        ```

        </details>

        Attributes:
            ext_idp_connidentifier (str): External identity source connection identifier
            connection (str): Mobile social login type:
    - `apple`: Apple mobile application
    - `wechat`: WeChat mobile application  
    - `alipay`: Alipay mobile application
    - `wechatwork`: WeChat Work mobile application
    - `wechatwork_agency`: WeChat Work mobile application (agency development mode)
    - `lark_internal`: Lark mobile enterprise self-built application
    - `lark_public`: Lark mobile app store application
    - `lark_block`: Lark widget
    - `yidun`: NetEase Yidun one-click login
    - `wechat_mini_program_code`: WeChat Mini Program login using code
    - `wechat_mini_program_phone`: WeChat Mini Program login using phone number
    - `wechat_mini_program_code_and_phone`: WeChat Mini Program login using code and phone number
    - `google`: Google mobile social login
    - `facebook`: Facebook mobile social login
    - `qq`: QQ mobile social login
    - `weibo`: Sina Weibo mobile social login
    - `baidu`: Baidu mobile social login
    - `linkedin`: LinkedIn mobile social login
    - `dingtalk`: DingTalk mobile social login
    - `github`: Github mobile social login
    - `gitee`: Gitee mobile social login
    - `gitlab`: GitLab mobile social login
    - `douyin`: Douyin mobile social login
    - `kuaishou`: Kuaishou mobile social login
    - `xiaomi`: Xiaomi mobile social login
    - `line`: LINE mobile social login
    - `slack`: Slack mobile social login
    - `oppo`: OPPO mobile social login
    - `huawei`: Huawei mobile social login
    - `amazon`: Amazon mobile social login

            wechat_payload (dict): WeChat mobile social login data, required when connection is wechat.
            apple_payload (dict): Apple mobile social login data, required when connection is apple.
            alipay_payload (dict): Alipay mobile social login data, required when connection is alipay.
            wechatwork_payload (dict): WeChat Work mobile social login data, required when connection is wechatwork.
            wechatwork_agency_payload (dict): WeChat Work (agency mode) mobile social login data, required when connection is wechatwork_agency.
            lark_public_payload (dict): Lark app store application mobile social login data, required when connection is lark_public.
            lark_internal_payload (dict): Lark self-built application mobile social login data, required when connection is lark_internal.
            lark_block_payload (dict): Lark widget mobile social login data, required when connection is lark_block.
            yidun_payload (dict): NetEase Yidun mobile social login data, required when connection is yidun.
            wechat_mini_program_code_payload (dict): WeChat Mini Program code login related data, required when connection is wechat_mini_program_code.
            wechat_mini_program_phone_payload (dict): WeChat Mini Program phone login related data, required when connection is wechat_mini_program_phone.
            wechat_mini_program_code_and_phone_payload (dict): WeChat Mini Program code and phone login related data, required when connection is wechat_mini_program_code_and_phone.
            google_payload (dict): Google mobile social login data, required when connection is google.
            facebook_payload (dict): Facebook mobile social login data, required when connection is facebook.
            qq_payload (dict): QQ mobile social login data, required when connection is qq.
            weibo_payload (dict): Sina Weibo mobile social login data, required when connection is weibo.
            baidu_payload (dict): Baidu mobile social login data, required when connection is baidu, and either code or access_token in baiduPayload is required, with code being the preferred authorization login method.
            linked_in_payload (dict): LinkedIn mobile social login data, required when connection is linkedin.
            ding_talk_payload (dict): DingTalk mobile social login data, required when connection is dingtalk.
            github_payload (dict): Github mobile social login data, required when connection is github.
            gitee_payload (dict): Gitee mobile social login data, required when connection is gitee.
            gitlab_payload (dict): GitLab mobile social login data, required when connection is gitlab.
            douyin_payload (dict): Douyin mobile social login data, required when connection is douyin.
            kuaishou_payload (dict): Kuaishou mobile social login data, required when connection is kuaishou.
            xiaomi_payload (dict): Xiaomi mobile social login data, required when connection is xiaomi.
            line_payload (dict): LINE mobile social login data, required when connection is line.
            slack_payload (dict): Slack mobile social login data, required when connection is slack.
            oppo_payload (dict): OPPO mobile social login data, required when connection is oppo.
            huawei_payload (dict): Huawei mobile social login data, required when connection is huawei.
            amazon_payload (dict): Amazon mobile social login data, required when connection is amazon.
            options (dict): Optional parameters
            client_id (str): Application ID. Required when application's "Token Exchange Authentication Method" is configured as client_secret_post.
            client_secret (str): Application secret. Required when application's "Token Exchange Authentication Method" is configured as client_secret_post.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin-by-mobile',
            json={
                'extIdpConnidentifier': ext_idp_connidentifier,
                'connection': connection,
                'wechatPayload': wechat_payload,
                'applePayload': apple_payload,
                'alipayPayload': alipay_payload,
                'wechatworkPayload': wechatwork_payload,
                'wechatworkAgencyPayload': wechatwork_agency_payload,
                'larkPublicPayload': lark_public_payload,
                'larkInternalPayload': lark_internal_payload,
                'larkBlockPayload': lark_block_payload,
                'yidunPayload': yidun_payload,
                'wechatMiniProgramCodePayload': wechat_mini_program_code_payload,
                'wechatMiniProgramPhonePayload': wechat_mini_program_phone_payload,
                'wechatMiniProgramCodeAndPhonePayload': wechat_mini_program_code_and_phone_payload,
                'googlePayload': google_payload,
                'facebookPayload': facebook_payload,
                'qqPayload': qq_payload,
                'weiboPayload': weibo_payload,
                'baiduPayload': baidu_payload,
                'linkedInPayload': linked_in_payload,
                'dingTalkPayload': ding_talk_payload,
                'githubPayload': github_payload,
                'giteePayload': gitee_payload,
                'gitlabPayload': gitlab_payload,
                'douyinPayload': douyin_payload,
                'kuaishouPayload': kuaishou_payload,
                'xiaomiPayload': xiaomi_payload,
                'linePayload': line_payload,
                'slackPayload': slack_payload,
                'oppoPayload': oppo_payload,
                'huaweiPayload': huawei_payload,
                'amazonPayload': amazon_payload,
                'options': options,
                'client_id': client_id,
                'client_secret': client_secret,
            },
        )

    def switch_login_by_user(self, target_user_id, options=None):
        """Switch login by user

        Allows switching login between personal accounts and associated public accounts. This endpoint requires the account to be logged in.

        Attributes:
            target_user_id (str): Target user ID to switch login to
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/switch-login-by-user',
            json={
                'targetUserId': target_user_id,
                'options': options,
            },
        )

    def get_alipay_auth_info(self, ext_idp_connidentifier):
        """Get Alipay AuthInfo

        This interface is used to get the [initialization parameter AuthInfo](https://opendocs.alipay.com/open/218/105325) needed to initiate Alipay authentication.

        Attributes:
            extIdpConnidentifier (str): External identity provider connection identifier
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-alipay-authinfo',
            params={
                'extIdpConnidentifier': ext_idp_connidentifier,
            },
        )

    def gene_qr_code(self, type, ext_idp_conn_id=None, custom_data=None, context=None, auto_merge_qr_code=None):
        """Generate QR code for login

        Generate QR code for login. Currently supports generating QR codes for WeChat Official Account scan login, Mini Program scan login, and custom mobile APP scan login.

        Attributes:
            type (str): QR code type. Currently supports three types:
    - `MOBILE_APP`: Custom mobile APP scan
    - `WECHAT_MINIPROGRAM`: WeChat Mini Program scan
    - `WECHAT_OFFICIAL_ACCOUNT` WeChat Official Account scan
            ext_idp_conn_id (str): When `type` is `WECHAT_MINIPROGRAM` or `WECHAT_OFFICIAL_ACCOUNT`, you can specify the identity provider connection. Otherwise, it will use the first corresponding identity provider connection enabled by the application to generate the QR code.
            custom_data (dict): When `type` is `MOBILE_APP`, you can pass custom user data that will be stored in the user's custom data when the user successfully scans and authorizes.
            context (dict): When type is `WECHAT_OFFICIAL_ACCOUNT` or `WECHAT_MINIPROGRAM`, specify custom pipeline context that will be passed to the pipeline context
            auto_merge_qr_code (bool): When type is `WECHAT_MINIPROGRAM`, whether to automatically merge the custom logo into the generated image, default is false. The server merging QR code process will increase the interface response speed. It is recommended to use the default value and splice the images on the client side. If you use GenAuth's SDK, you can skip the manual splicing process.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/gene-qrcode',
            json={
                'type': type,
                'extIdpConnId': ext_idp_conn_id,
                'customData': custom_data,
                'context': context,
                'autoMergeQrCode': auto_merge_qr_code,
            },
        )

    def check_qr_code_status(self, qrcode_id):
        """Check QR code status

        According to the order of user scanning, there are six states in total: not scanned, scanned waiting for user confirmation, user agrees/cancels authorization, QR code expired and unknown error. The front end should give different feedback to users based on different states. You can learn about the detailed process of scan code login through the following article: https://docs.genauth.ai/v2/concepts/how-qrcode-works.html.

        Attributes:
            qrcodeId (str): Unique ID of QR code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-qrcode-status',
            params={
                'qrcodeId': qrcode_id,
            },
        )

    def exchange_token_set_with_qr_code_ticket(self, ticket, client_id=None, client_secret=None):
        """Exchange TokenSet with QR code ticket


    This endpoint is for exchanging user's `access_token` and `id_token` with QR code ticket.


    Note: Depending on the **Application Type** you selected when creating the application in GenAuth and the **Token Endpoint Auth Method** configured for the application, different forms of client identity verification are required when calling this interface.

    <details>
    <summary>Click to expand details</summary>

    <br>

    You can find the **Token Endpoint Auth Method** configuration item in [GenAuth Console](https://console.genauth.ai) under **Applications** - **Self-built Applications** - **Application Details** - **Application Configuration** - **Other Settings** - **Authorization Configuration**:

    > Hidden for Single Page Web Applications and Client Applications, defaults to `none` and cannot be modified; Backend Applications and Standard Web Applications can modify this configuration item.

    ![](https://files.authing.co/api-explorer/tokenAuthMethod.jpg)

    #### When Token Endpoint Auth Method is none

    No additional operations are required when calling this interface.

    #### When Token Endpoint Auth Method is client_secret_post

    When calling this interface, you must pass `client_id` and `client_secret` parameters in the body as conditions for verifying client identity. Where `client_id` is the Application ID and `client_secret` is the Application Secret.

    #### When Token Endpoint Auth Method is client_secret_basic

    When calling this interface, you must carry the `authorization` request header in the HTTP request header as a condition for verifying client identity. The format of the `authorization` request header is as follows (where `client_id` is the Application ID and `client_secret` is the Application Secret):

    ```
    Basic base64(<client_id>:<client_secret>)
    ```

    Example result:

    ```
    Basic NjA2M2ZiMmYzY3h4eHg2ZGY1NWYzOWViOjJmZTdjODdhODFmODY3eHh4eDAzMjRkZjEyZGFlZGM3
    ```

    JS code example:

    ```js
    'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64');
    ```

    </details>



        Attributes:
            ticket (str): Returned when QR code status is authorized. If "Web polling interface returns complete user information" is not enabled in Console Application Security - General Security - Login Security - APP QR Code Login Web Security (disabled by default), this ticket will be returned for exchanging complete user information.
            client_id (str): Application ID. Required when the application's "Token Endpoint Auth Method" is configured as `client_secret_post`.
            client_secret (str): Application Secret. Required when the application's "Token Endpoint Auth Method" is configured as `client_secret_post`.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/exchange-tokenset-with-qrcode-ticket',
            json={
                'ticket': ticket,
                'client_id': client_id,
                'client_secret': client_secret,
            },
        )

    def change_qr_code_status(self, action, qrcode_id):
        """Self-built APP QR Code Login: APP Side Modifies QR Code Status

        This endpoint is used to modify QR code status in self-built APP QR code login, corresponding to the process of terminal users scanning, confirming authorization, and canceling authorization after rendering QR code in browser. **This interface requires user login status**.

        Attributes:
            action (str): Action to modify QR code status:
    - `SCAN`: Modify QR code status to scanned status, should be executed immediately after mobile APP scans code;
    - `CONFIRM`: Modify QR code status to authorized, must execute SCAN operation first;
    - `CANCEL`: Modify QR code status to cancelled, must execute SCAN operation first;

            qrcode_id (str): Unique ID of QR code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-qrcode-status',
            json={
                'action': action,
                'qrcodeId': qrcode_id,
            },
        )

    def sign_in_by_push(self, account, options=None):
        """Push Login

        Push login.

        Attributes:
            account (str): User account (username/phone/email)
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin-by-push',
            json={
                'account': account,
                'options': options,
            },
        )

    def check_push_code_status(self, push_code_id):
        """Check Push Code Status

        According to the order of push code usage, there are five states in total: pushed, waiting for user to agree/cancel authorization, push code expired and unknown error. The front end should give different feedback to users based on different states.

        Attributes:
            pushCodeId (str): Push code (unique ID for push login)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-pushcode-status',
            params={
                'pushCodeId': push_code_id,
            },
        )

    def change_push_code_status(self, action, push_code_id):
        """Push Login: APP Side Modifies Push Code Status

        This endpoint is used to modify push code status in GenAuth Token APP push login, corresponding to the process of using push login in browser, clicking login, terminal user receiving push login information, confirming authorization, and canceling authorization. **This interface requires user login status**.

        Attributes:
            action (str): Action to modify push code status:
    - `CONFIRM`: Modify push code status to authorized;
    - `CANCEL`: Modify push code status to cancelled;

            push_code_id (str): Push code (unique ID for push login)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-pushcode-status',
            json={
                'action': action,
                'pushCodeId': push_code_id,
            },
        )

    def send_sms(self, channel, phone_number, phone_country_code=None):
        """Send SMS

        When sending an SMS, you must specify the SMS Channel. Each phone number can only send once per minute for the same Channel.

        Attributes:
            channel (str): SMS channel, specifying the purpose of sending this SMS:
    - `CHANNEL_LOGIN`: For user login
    - `CHANNEL_REGISTER`: For user registration
    - `CHANNEL_RESET_PASSWORD`: For resetting password
    - `CHANNEL_BIND_PHONE`: For binding phone number
    - `CHANNEL_UNBIND_PHONE`: For unbinding phone number
    - `CHANNEL_BIND_MFA`: For binding MFA
    - `CHANNEL_VERIFY_MFA`: For verifying MFA
    - `CHANNEL_UNBIND_MFA`: For unbinding MFA
    - `CHANNEL_COMPLETE_PHONE`: For completing phone number information during registration/login
    - `CHANNEL_IDENTITY_VERIFICATION`: For user identity verification
    - `CHANNEL_DELETE_ACCOUNT`: For account deletion

            phone_number (str): Phone number, without area code. If it's an international phone number, please specify the area code in the phoneCountryCode parameter.
            phone_country_code (str): Phone area code, not required for mainland China phone numbers. GenAuth SMS service does not natively support international phone numbers; you need to configure the corresponding international SMS service in the GenAuth console. The complete list of phone area codes can be found at https://en.wikipedia.org/wiki/List_of_country_calling_codes.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-sms',
            json={
                'channel': channel,
                'phoneNumber': phone_number,
                'phoneCountryCode': phone_country_code,
            },
        )

    def send_email(self, channel, email):
        """Send Email

        When sending an email, you must specify the email Channel. Each email address can only send once per minute for the same Channel.

        Attributes:
            channel (str): Email channel, specifying the purpose of sending this email:
    - `CHANNEL_LOGIN`: For user login
    - `CHANNEL_REGISTER`: For user registration  
    - `CHANNEL_RESET_PASSWORD`: For resetting password
    - `CHANNEL_VERIFY_EMAIL_LINK`: For verifying email address
    - `CHANNEL_UPDATE_EMAIL`: For updating email
    - `CHANNEL_BIND_EMAIL`: For binding email
    - `CHANNEL_UNBIND_EMAIL`: For unbinding email
    - `CHANNEL_VERIFY_MFA`: For verifying MFA
    - `CHANNEL_UNLOCK_ACCOUNT`: For self-service account unlock
    - `CHANNEL_COMPLETE_EMAIL`: For completing email info during registration/login
    - `CHANNEL_DELETE_ACCOUNT`: For account deletion

            email (str): Email address, case insensitive
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-email',
            json={
                'channel': channel,
                'email': email,
            },
        )

    def decrypt_wechat_mini_program_data(self, code, iv, encrypted_data, ext_idp_connidentifier):
        """Decrypt WeChat Mini Program Data

        Decrypt WeChat Mini Program Data

        Attributes:
            code (str): User `code` returned by `wx.login` interface
            iv (str): Initialization vector for symmetric decryption algorithm, returned by WeChat
            encrypted_data (str): Encrypted data (encryptedData) returned from getting WeChat open data
            ext_idp_connidentifier (str): External identity provider connection identifier for WeChat Mini Program
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/decrypt-wechat-miniprogram-data',
            json={
                'code': code,
                'iv': iv,
                'encryptedData': encrypted_data,
                'extIdpConnidentifier': ext_idp_connidentifier,
            },
        )

    def get_wechat_mp_access_token(self, app_id, app_secret):
        """Get WeChat Mini Program/Official Account Access Token

        Get WeChat Mini Program/Official Account Access Token cached on GenAuth server (Deprecated, please use /api/v3/get-wechat-access-token-info)

        Attributes:
            app_id (str): AppId of WeChat Mini Program or Official Account
            app_secret (str): AppSecret of WeChat Mini Program or Official Account
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-wechat-access-token',
            json={
                'appId': app_id,
                'appSecret': app_secret,
            },
        )

    def get_wechat_mp_access_token_info(self, app_id, app_secret):
        """Get WeChat Mini Program/Official Account Access Token

        Get WeChat Mini Program/Official Account Access Token cached on GenAuth server

        Attributes:
            app_id (str): AppId of WeChat Mini Program or Official Account
            app_secret (str): AppSecret of WeChat Mini Program or Official Account
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-wechat-access-token-info',
            json={
                'appId': app_id,
                'appSecret': app_secret,
            },
        )

    def get_login_history(self, app_id=None, client_ip=None, success=None, start=None, end=None, page=None, limit=None):
        """Get Login History

        Get Login History

        Attributes:
            appId (str): Application ID, can filter by application ID. If not provided, get login history for all applications.
            clientIp (str): Client IP, can filter by login client IP. If not provided, get login history for all IPs.
            success (bool): Whether login was successful, can filter by login success status. If not provided, get records including both successful and failed logins.
            start (int): Start time, timestamp in milliseconds
            end (int): End time, timestamp in milliseconds
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum 50, default 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-login-history',
            params={
                'appId': app_id,
                'clientIp': client_ip,
                'success': success,
                'start': start,
                'end': end,
                'page': page,
                'limit': limit,
            },
        )

    def get_logged_in_apps(self, ):
        """Get Logged In Applications

        Get Logged In Applications

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-logged-in-apps',
        )

    def get_accessible_apps(self, ):
        """Get Accessible Applications

        Get Applications with Access Permission

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-accessible-apps',
        )

    def get_tenant_list(self, ):
        """Get Tenant List

        Get Tenant List

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-tenant-list',
        )

    def get_role_list(self, namespace=None):
        """Get Role List

        Get Role List

        Attributes:
            namespace (str): Code of the permission group (permission namespace)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-role-list',
            params={
                'namespace': namespace,
            },
        )

    def get_group_list(self, ):
        """Get Group List

        Get Group List

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-group-list',
        )

    def get_authorized_resources(self, namespace=None, resource_type=None):
        """Get authorized resource list

        This interface is used to get the list of resources authorized to the user.

        Attributes:
            namespace (str): Code of the permission group (permission namespace)
            resourceType (str): Resource type, such as data, API, menu, button
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-authorized-resources',
            params={
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def get_profile(self, with_custom_data=None, with_identities=None):
        """Get user profile

        This endpoint is used to get user profile information. It requires the user's access_token in the request header. The GenAuth server will return corresponding fields based on the scope in the user's access_token.

        Attributes:
            withCustomData (bool): Whether to get custom data
            withIdentities (bool): Whether to get identities
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-profile',
            params={
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
            },
        )

    def update_profile(self, name=None, nickname=None, photo=None, external_id=None, birthdate=None, country=None,
                       province=None, city=None, address=None, street_address=None, postal_code=None, gender=None,
                       username=None, company=None, custom_data=None, identity_number=None):
        """Update user profile

        This interface is used to modify user profile information, including user custom data. If you need to modify email, phone number, or password, please use the corresponding separate interfaces.

        Attributes:
            name (str): User's real name, not unique
            nickname (str): Nickname
            photo (str): Avatar URL
            external_id (str): External ID from third party
            birthdate (str): Date of birth
            country (str): Country
            province (str): Province
            city (str): City
            address (str): Address
            street_address (str): Street address
            postal_code (str): Postal code
            gender (str): Gender
            username (str): Username, unique within user pool
            company (str): Company
            custom_data (dict): Custom data, keys in the input object must be pre-defined in the user pool
            identity_number (str): User ID card number
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-profile',
            json={
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'externalId': external_id,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'gender': gender,
                'username': username,
                'company': company,
                'customData': custom_data,
                'identityNumber': identity_number,
            },
        )

    def bind_email(self, pass_code, email):
        """Bind email

        If the user has not bound an email yet, this interface can be used for users to bind their email independently. If the user has already bound an email and wants to modify it, please use the modify email interface. You need to first call the send email interface to send the email verification code.

        Attributes:
            pass_code (str): Email verification code, can only be used once and has a validity period
            email (str): Email address, case insensitive
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/bind-email',
            json={
                'passCode': pass_code,
                'email': email,
            },
        )

    def unbind_email(self, pass_code):
        """Unbind email

        User unbinds email. If the user has not bound other login methods (phone number, social login account), they cannot unbind the email and will receive an error message.

        Attributes:
            pass_code (str): Email verification code, need to first call the send email interface to receive verification code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-email',
            json={
                'passCode': pass_code,
            },
        )

    def bind_phone(self, pass_code, phone_number, phone_country_code=None):
        """Bind phone number

        If the user has not bound a phone number yet, this interface can be used for users to bind their phone number independently. If the user has already bound a phone number and wants to modify it, please use the modify phone number interface. You need to first call the send SMS interface to send the SMS verification code.

        Attributes:
            pass_code (str): SMS verification code, note that a verification code can only be used once and has an expiration time
            phone_number (str): Phone number without country code. For international phone numbers, please specify the country code in phoneCountryCode parameter
            phone_country_code (str): Phone country code, can be omitted for mainland China numbers. GenAuth SMS service does not have built-in support for international phone numbers, you need to configure corresponding international SMS service in GenAuth console. For complete list of country codes, please refer to https://en.wikipedia.org/wiki/List_of_country_calling_codes
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/bind-phone',
            json={
                'passCode': pass_code,
                'phoneNumber': phone_number,
                'phoneCountryCode': phone_country_code,
            },
        )

    def unbind_phone(self, pass_code):
        """Unbind phone number

        User unbinds phone number. If the user has not bound other login methods (email, social login account), they cannot unbind the phone number and will receive an error message.

        Attributes:
            pass_code (str): SMS verification code, need to first call the send SMS interface to receive verification code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-phone',
            json={
                'passCode': pass_code,
            },
        )

    def get_security_level(self, ):
        """Get password strength and account security level score

        Get user's password strength and account security level score, requires user's access_token in request header.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-security-info',
        )

    def update_password(self, new_password, old_password=None, password_encrypt_type=None):
        """Update password

        This endpoint is used for users to change their password independently. If the user has previously set a password, they need to provide their original password as credentials. If the user has forgotten their current password, please use the forgot password interface.

        Attributes:
            new_password (str): New password
            old_password (str): Original password, required if user currently has a password set
            password_encrypt_type (str): Password encryption type, supports RSA256 and SM2 encryption algorithms. Default is 'none' for no encryption.
    - 'none': No password encryption, transmitted in plaintext
    - 'rsa': Use RSA256 algorithm to encrypt password, needs to use GenAuth service's RSA public key for encryption, please read the Introduction section to learn how to get GenAuth service's RSA256 public key
    - 'sm2': Use SM2 algorithm to encrypt password, needs to use GenAuth service's SM2 public key for encryption, please read the Introduction section to learn how to get GenAuth service's SM2 public key

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-password',
            json={
                'newPassword': new_password,
                'oldPassword': old_password,
                'passwordEncryptType': password_encrypt_type,
            },
        )

    def verify_update_email_request(self, email_pass_code_payload, verify_method):
        """Initiate email update verification request

        When end users want to modify their email independently, they need to provide corresponding verification methods. This interface is used to verify if the user's email modification request is valid. Currently supports verification through email verification code, you need to first call the send email interface to send the corresponding email verification code.

        Attributes:
            email_pass_code_payload (dict): Data for verification using email verification code method
            verify_method (str): Verification method used to modify current email:
    - 'EMAIL_PASSCODE': Verify through email verification code, currently only supports this verification method

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-update-email-request',
            json={
                'emailPassCodePayload': email_pass_code_payload,
                'verifyMethod': verify_method,
            },
        )

    def update_email(self, update_email_token):
        """Update email

        End users independently modify email, need to provide corresponding verification methods, see Initiate email update verification request.
    This parameter requires a one-time temporary credential updateEmailToken, which needs to be obtained from the Initiate email update verification request interface.

        Attributes:
            update_email_token (str): Token for temporary email modification, can be obtained from the Initiate email update verification request interface
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-email',
            json={
                'updateEmailToken': update_email_token,
            },
        )

    def verify_update_phone_request(self, phone_pass_code_payload, verify_method):
        """Initiate phone number update verification request

        When end users want to modify their phone number independently, they need to provide corresponding verification methods. This interface is used to verify if the user's phone number modification request is valid. Currently supports verification through SMS verification code, you need to first call the send SMS interface to send the corresponding SMS verification code.

        Attributes:
            phone_pass_code_payload (dict): Data for verification using phone verification code method
            verify_method (str): Phone number modification verification method:
    - 'PHONE_PASSCODE': Use SMS verification code method for verification, currently only supports this method

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-update-phone-request',
            json={
                'phonePassCodePayload': phone_pass_code_payload,
                'verifyMethod': verify_method,
            },
        )

    def update_phone(self, update_phone_token):
        """Update phone number

        End users independently modify phone number, need to provide corresponding verification methods, see Initiate phone number update verification request.
    This parameter requires a one-time temporary credential updatePhoneToken, which needs to be obtained from the Initiate phone number update verification request interface.

        Attributes:
            update_phone_token (str): Token for temporary phone number modification, can be obtained from the Initiate phone number update verification request interface
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-phone',
            json={
                'updatePhoneToken': update_phone_token,
            },
        )

    def verify_reset_password_request(self, verify_method, phone_pass_code_payload=None, email_pass_code_payload=None):
        """Initiate forgot password request

        When users forget their password, they can use this endpoint to recover it. Users need to use relevant verification methods for verification, currently supports email verification code and phone verification code methods.

        Attributes:
            verify_method (str): Verification method used for forgot password request:
    - 'EMAIL_PASSCODE': Verify through email verification code
    - 'PHONE_PASSCODE': Verify through phone verification code

            phone_pass_code_payload (dict): Data for verification using phone verification code
            email_pass_code_payload (dict): Data for verification using email verification code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-reset-password-request',
            json={
                'verifyMethod': verify_method,
                'phonePassCodePayload': phone_pass_code_payload,
                'emailPassCodePayload': email_pass_code_payload,
            },
        )

    def reset_password(self, password, password_reset_token, password_encrypt_type=None):
        """Reset password

        This endpoint is used after users forget their password to reset it through phone verification code or email verification code methods. This interface requires a temporary credential passwordResetToken for password reset, this parameter needs to be obtained through the Initiate forgot password request interface.

        Attributes:
            password (str): Password
            password_reset_token (str): Token for password reset
            password_encrypt_type (str): Password encryption type, supports RSA256 and SM2 encryption algorithms. Default is 'none' for no encryption.
    - 'none': No password encryption, transmitted in plaintext
    - 'rsa': Use RSA256 algorithm to encrypt password, needs to use GenAuth service's RSA public key for encryption, please read the Introduction section to learn how to get GenAuth service's RSA256 public key
    - 'sm2': Use SM2 algorithm to encrypt password, needs to use GenAuth service's SM2 public key for encryption, please read the Introduction section to learn how to get GenAuth service's SM2 public key

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-password',
            json={
                'password': password,
                'passwordResetToken': password_reset_token,
                'passwordEncryptType': password_encrypt_type,
            },
        )

    def verify_delete_account_request(self, verify_method, phone_pass_code_payload=None, email_pass_code_payload=None,
                                      password_payload=None):
        """Initiate account deletion request

        When users want to delete their account, they need to provide corresponding credentials. Currently supports three verification methods: email verification code, phone verification code, and password.

        Attributes:
            verify_method (str): Verification method for account deletion:
    - `PHONE_PASSCODE`: Verify through phone verification code.
    - `EMAIL_PASSCODE`: Verify through email verification code.
    - `PASSWORD`: If user has neither phone nor email bound, can use password as verification method.

            phone_pass_code_payload (dict): Data for verification using phone verification code
            email_pass_code_payload (dict): Data for verification using email verification code
            password_payload (dict): Data for verification using password
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-delete-account-request',
            json={
                'verifyMethod': verify_method,
                'phonePassCodePayload': phone_pass_code_payload,
                'emailPassCodePayload': email_pass_code_payload,
                'passwordPayload': password_payload,
            },
        )

    def delete_account(self, delete_account_token):
        """Delete account

        This endpoint is used for users to delete their own account. It requires a temporary credential deleteAccountToken which needs to be obtained through the Initiate account deletion request interface.

        Attributes:
            delete_account_token (str): Token for account deletion
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-account',
            json={
                'deleteAccountToken': delete_account_token,
            },
        )

    def list_public_accounts_for_switch_logged_in(self, with_origin_user=None):
        """Query list of public accounts that current logged in user can switch to

        This endpoint is used to query the list of public accounts that the current logged in user can switch to. If there are no public accounts available for switching, an empty array will be returned.

        Attributes:
            withOriginUser (bool): Whether to include current personal user basic information
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-select-login-public-accounts',
            params={
                'withOriginUser': with_origin_user,
            },
        )

    def get_system_info(self, ):
        """Get server public information

        This endpoint can get server's public information, such as RSA256 public key, SM2 public key, GenAuth service version number, etc.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/system',
        )

    def get_country_list(self, ):
        """Get country list

        Dynamically get country list, can be used for country selection on frontend login page and international SMS input box selection, to reduce frontend static resource size.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-country-list',
        )

    def check_permission_by_string_resource(self, resources, action):
        """String type resource authorization

        String type resource authorization, supports permission check for one or more string resources

        Attributes:
            resources (list): String data resource path list,
            action (str): Data resource permission operation, actions like read, get, write etc
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-string-resource',
            json={
                'resources': resources,
                'action': action,
            },
        )

    def check_permission_by_array_resource(self, resources, action):
        """Array type resource authorization

        Array type resource authorization, supports permission check for one or more array resources

        Attributes:
            resources (list): Array data resource path list,
            action (str): Data resource permission operation, actions like read, get, write etc
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-array-resource',
            json={
                'resources': resources,
                'action': action,
            },
        )

    def check_permission_by_tree_resource(self, resources, action):
        """Tree type resource authorization

        Tree type resource authorization, supports permission check for one or more tree resources

        Attributes:
            resources (list): Tree data resource path list,
            action (str): Data resource permission operation, actions like read, get, write etc
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-tree-resource',
            json={
                'resources': resources,
                'action': action,
            },
        )

    def get_user_authorized_resources_list(self, ):
        """Get list of authorized resources for user in logged in application

        Get user's specified resource permission list, user gets the list of resources they have in a certain application.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-auth-resource-list',
        )

    def get_user_auth_resource_permission_list(self, resources):
        """Get user's specified resource permission list

        Get permission list for user's specified resources, user gets permission list for specified resources in a certain application.

        Attributes:
            resources (list): Data resource path list, **tree resources need to specify concrete tree nodes**
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-auth-resource-permission-list',
            json={
                'resources': resources,
            },
        )

    def get_user_auth_resource_struct(self, resource):
        """Get structure list of user's authorized resources

        Get list of user's authorized resources, user gets structure list of authorized resources for a certain resource in an application, returns corresponding authorization list based on different resource types.

        Attributes:
            resource (str): Data resource Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-auth-resource-struct',
            json={
                'resource': resource,
            },
        )

    def init_authentication_options(self, ):
        """Get WebAuthn authentication request initialization parameters

        Get WebAuthn authentication request initialization parameters

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/webauthn/authentication',
        )

    def verify_authentication(self, ticket, authentication_credential, options=None):
        """Verify WebAuthn authentication request credential

        Verify WebAuthn authentication request credential

        Attributes:
            ticket (str): Ticket obtained from Get WebAuthn authentication request initialization parameters interface
            authentication_credential (dict): Authenticator credential information
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/authentication',
            json={
                'ticket': ticket,
                'authenticationCredential': authentication_credential,
                'options': options,
            },
        )

    def init_register_options(self, ):
        """Get webauthn credential creation initialization parameters

        Get webauthn credential creation initialization parameters. **This interface requires user login status**

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/webauthn/registration',
        )

    def verify_register(self, ticket, registration_credential, authenticator_code=None):
        """Verify webauthn binding registration authenticator credential

        Verify webauthn binding registration authenticator credential

        Attributes:
            ticket (str): Ticket from getting credential creation initialization parameters
            registration_credential (dict): Binding authenticator credential information
            authenticator_code (str): Credential information type:
    - `FINGERPRINT`: Fingerprint
    - `FACE`: Face
    - `OTHER` Other
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/registration',
            json={
                'ticket': ticket,
                'registrationCredential': registration_credential,
                'authenticatorCode': authenticator_code,
            },
        )

    def list(self, page=None, limit=None):
        """My device list

        List of devices I have logged in to.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/mydevices/list',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def unbind(self, device_id):
        """Remove device

        Remove a device.

        Attributes:
            device_id (str): Device unique identifier
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/mydevices/unbind',
            json={
                'deviceId': device_id,
            },
        )

    def revoke(self, device_id):
        """Logout from device

        Remove login status of a logged in device.

        Attributes:
            device_id (str): Device unique identifier
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/mydevices/revoke-session',
            json={
                'deviceId': device_id,
            },
        )

    def auth_by_code_identity(self, code, app_id=None, conn_id=None, options=None):
        """WeChat mobile login

        Mobile applications: Use WeChat as external identity source for login.

        Attributes:
            code (str): Client WeChat authorization successful, WeChat returns current authentication authorization code
            app_id (str): Application ID
            conn_id (str): Identity source connection ID
            options (dict): Login parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/authByCodeIdentity',
            json={
                'code': code,
                'appId': app_id,
                'connId': conn_id,
                'options': options,
            },
        )

    def register_new_user(self, key, action):
        """WeChat mobile: Use identity source user information

        When binding inquiry is enabled: Bind to external identity source, create user based on external identity source user information then bind to current identity source and login.

        Attributes:
            key (str): Intermediate state key
            action (str): Operation code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/register',
            json={
                'key': key,
                'action': action,
            },
        )

    def bind_by_email_code(self, key, action, code, email):
        """WeChat mobile: Email verification code mode

        When binding inquiry is enabled: Bind to external identity source, verify user information based on input email, bind to current identity source and login if corresponding user is found; error "User does not exist" if not found.

        Attributes:
            key (str): Intermediate state key
            action (str): Operation code
            code (str): Email verification code (four digits: 1234; six digits: 123456)
            email (str): Email
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byEmailCode',
            json={
                'key': key,
                'action': action,
                'code': code,
                'email': email,
            },
        )

    def bind_by_phone_code(self, key, action, code, phone, phone_country_code=None):
        """WeChat mobile: Phone verification code mode

        When binding inquiry is enabled: Bind to external identity source, verify user information based on input phone, bind to current identity source and login if corresponding user is found; error "User does not exist" if not found.

        Attributes:
            key (str): Intermediate state key
            action (str): Operation code
            code (str): Phone verification code (four digits: 1234; six digits: 123456)
            phone (str): Phone number
            phone_country_code (str): Country code (standard format: plus sign "+" followed by country code digits; current validation compatible with historical user input habits. For example, China country code standard format is "+86", historical user input records include formats like "86, 086, 0086")
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byPhoneCode',
            json={
                'key': key,
                'action': action,
                'code': code,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
            },
        )

    def bind_by_account(self, key, action, password, account):
        """WeChat mobile: Account password mode

        When binding inquiry is enabled: Bind to external identity source, verify user information based on input account (username/phone/email) password, bind to current identity source and login if corresponding user is found; error "User does not exist" if not found.

        Attributes:
            key (str): Intermediate state key
            action (str): Operation code
            password (str): Account password
            account (str): Account (phone/email/username)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byAccount',
            json={
                'key': key,
                'action': action,
                'password': password,
                'account': account,
            },
        )

    def select_account(self, key, action, account):
        """WeChat mobile: Multiple accounts scenario

        When binding inquiry is enabled: Bind external identity source based on selected account, verify user information based on input account ID, bind to current identity source and login if corresponding user is found; error "User does not exist" if not found.

        Attributes:
            key (str): Intermediate state key
            action (str): Operation code
            account (str): Account ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/select',
            json={
                'key': key,
                'action': action,
                'account': account,
            },
        )

    def bind_by_account_id(self, key, action, account_id):
        """WeChat mobile: Account ID mode

        When binding inquiry is enabled: Bind to external identity source, verify user information based on input account ID, bind to current identity source and login if corresponding user is found; error "User does not exist" if not found.

        Attributes:
            key (str): Intermediate state key
            action (str): Operation code
            account_id (str): Account ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byAccountId',
            json={
                'key': key,
                'action': action,
                'accountId': account_id,
            },
        )

    def get_push_login_relation_apps(self, app_id, push_code_id):
        """Get the client applications related to the push login request

        This endpoint is used to check if the current user's login application supports authorization for push login requests when GenAuth token APP receives push login notifications.

        Attributes:
            app_id (str): App ID of the application that initiated the push login
            push_code_id (str): Push code (unique ID for push login)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-pushlogin-relation-apps',
            json={
                'appId': app_id,
                'pushCodeId': push_code_id,
            },
        )

    def gene_fastpass_qrcode_info(self, options=None):
        """Get fast authentication QR code data

        This endpoint is used to get the fast authentication parameters to generate QR codes, which can be scanned by GenAuth token APP to complete fast authentication. **This interface requires user login status**.

        Attributes:
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/gene-fastpass-qrcode-info',
            json={
                'options': options,
            },
        )

    def get_fastpass_params(self, qrcode_id, app_id):
        """Get the list of applications for fast authentication

        This endpoint is used to pull the list of client applications that can be quickly authenticated after scanning the QR code of "User Center" - "Fast Authentication" using GenAuth token APP.

        Attributes:
            qrcodeId (str):
            appId (str):
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-fastpass-client-apps',
            params={
                'qrcodeId': qrcode_id,
                'appId': app_id,
            },
        )

    def get_qr_code_status(self, qrcode_id):
        """Query the status of the "Fast Authentication QR Code" in the personal center

        According to the order of user scanning, there are five states in total: not scanned, scanned, logged in, QR code expired, and unknown error. The front end should give different feedback to users based on different states.

        Attributes:
            qrcodeId (str): Unique ID of QR code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-app-login-qrcode-status',
            params={
                'qrcodeId': qrcode_id,
            },
        )

    def qr_code_app_login(self, action, qrcode_id):
        """APP scan code login

        This endpoint is used in the process of successful scan code login by APP, corresponding to the process of rendering QR codes on the "Personal Center" - "Fast Authentication" page, and the terminal user scanning and successfully logging in.

        Attributes:
            action (str): APP scan code login:
    - `APP_LOGIN`: APP scan code login；

            qrcode_id (str): Unique ID of QR code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/qrcode-app-login',
            json={
                'action': action,
                'qrcodeId': qrcode_id,
            },
        )

    def pre_check_code(self, code_type, sms_code_payload=None, email_code_payload=None):
        """Pre-check if the verification code is correct

        Pre-check if the verification code is valid, this check will not invalidate the verification code.

        Attributes:
            code_type (str): Verification code type
            sms_code_payload (dict): SMS verification code check parameters
            email_code_payload (dict): Email verification code check parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/pre-check-code',
            json={
                'codeType': code_type,
                'smsCodePayload': sms_code_payload,
                'emailCodePayload': email_code_payload,
            },
        )

    def list_credentials_by_page(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/page-authenticator-device',
            json={
            },
        )

    def check_valid_credentials_by_cred_ids(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/check-valid-credentials-by-credIds',
            json={
            },
        )

    def remove_all_credentials(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/remove-credentials-by-authenticator-code',
            json={
            },
        )

    def remove_credential(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/remove-credential/{credentialID}',
            json={
            },
        )

    def verify_mfa_token(self, token):
        """Verify MFA Token

        Verify MFA Token

        Attributes:
            token (str): Value of `mfa_token`
        """
        return self.http_client.request(
            method='POST',
            url='/mfa/token/introspection',
        )

    def send_enroll_factor_request(self, profile, factor_type):
        """Initiate MFA Authentication Factor Binding Request

        When a user has not bound an MFA authentication factor, they can initiate a binding request. Different types of MFA authentication factor binding requests require different parameters, see the profile parameter for details. After initiating the verification request, the GenAuth server will require verification using different means based on the corresponding authentication factor type and passed parameters. This interface will return an enrollmentToken, which you need to include when requesting the "Bind MFA Authentication Factor" interface along with the corresponding credentials.

        Attributes:
            profile (dict): MFA authentication factor details
            factor_type (str): MFA authentication factor type:
    - `OTP`: OTP
    - `SMS`: SMS
    - `EMAIL`: Email
    - `FACE`: Face

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-enroll-factor-request',
            json={
                'profile': profile,
                'factorType': factor_type,
            },
        )

    def enroll_factor(self, enrollment_data, enrollment_token, factor_type):
        """Bind MFA Authentication Factor

        Bind MFA factor.

        Attributes:
            enrollment_data (dict): Verification information required by the corresponding authentication factor when binding MFA authentication factor.
            enrollment_token (str): The enrollmentToken returned by the "Initiate MFA Authentication Factor Binding Request" interface, this token is valid for one minute.
            factor_type (str): MFA authentication factor type:
    - `OTP`: OTP
    - `SMS`: SMS
    - `EMAIL`: Email
    - `FACE`: Face

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/enroll-factor',
            json={
                'enrollmentData': enrollment_data,
                'enrollmentToken': enrollment_token,
                'factorType': factor_type,
            },
        )

    def reset_factor(self, factor_id):
        """Unbind MFA Authentication Factor

        Unbind a user's MFA authentication factor based on Factor ID.

        Attributes:
            factor_id (str): MFA authentication factor ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-factor',
            json={
                'factorId': factor_id,
            },
        )

    def list_enrolled_factors(self, ):
        """Get All Bound MFA Authentication Factors

        GenAuth currently supports four types of MFA authentication factors: SMS, Email verification code, OTP, and Face.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-enrolled-factors',
        )

    def get_factor(self, factor_id):
        """Get a Specific Bound MFA Authentication Factor

        Get details of a specific MFA Factor bound to the user based on Factor ID.

        Attributes:
            factorId (str): MFA Factor ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-factor',
            params={
                'factorId': factor_id,
            },
        )

    def list_factors_to_enroll(self, ):
        """Get Available MFA Authentication Factors

        Get all MFA authentication factors that are enabled in the application but not yet bound by the user. Users can bind new MFA authentication factors from the returned list.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-factors-to-enroll',
        )

    def mfa_otp_verify(self, totp):
        """Verify User's MFA Bound OTP

        Verify user's MFA bound OTP.

        Attributes:
            totp (str): OTP code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/mfa-totp-verify',
            json={
                'totp': totp,
            },
        )

    # ==== AUTO GENERATED AUTHENTICATION METHODS END ====
    def sub_event(self, event_code, callback):
        """Subscribe to Events

        Subscribe to GenAuth public events or custom events

        Attributes:
            eventCode (str): Event code
            callback (callable): Callback function
        """
        assert event_code, "eventCode cannot be empty"
        assert self.access_token, "access_token cannot be empty"
        assert callable(callback), "callback must be an executable function"
        eventUri = self.websocket_host + \
                   self.websocket_endpoint + \
                   "?code=" + event_code + \
                   "&token=" + self.access_token
        print("eventUri:" + eventUri)
        handleMessage(eventUri, callback)

    def put_event(self, event_code, data):
        """Publish Custom Event

        Publish event

        Attributes:
            event_code (str): Event code
            data (json): Event body
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/pub-userEvent",
            json={
                "eventType": event_code,
                "eventData": json.dumps(data)
            },
        )
