from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jwt import decode
from requests import (
    ConnectionError,
    HTTPError,
    RequestException,
    Timeout,
    post,
    request,
)
from requests.auth import HTTPBasicAuth

from j_auth_client.exceptions import (
    JAuthAuthenticationException,
    JAuthBaseException,
    JAuthClientException,
    JAuthConnectionException,
    JAuthRequestException,
    JAuthServerException,
    JAuthTimeoutException,
)


class JAuthClient:
    token: str = None
    token_expires_at: datetime = None

    def __init__(
        self,
        username: str,
        password: str,
        auth_url: str,
    ):
        self.username = username
        self.password = password
        self.auth_url = auth_url

    def __authenticate(self):
        try:
            response = self.request(
                method=post,
                url=self.auth_url,
                data={"grant_type": "client_credentials"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                auth=HTTPBasicAuth(self.username, self.password),
                auth_server_authenticated=False,
            )

            self.token = response["access_token"]
            self.token_expires_at = datetime.fromtimestamp(
                int(decode(jwt=self.token, options={"verify_signature": False})["exp"])
            )

        except (JAuthClientException, JAuthServerException) as error:
            raise JAuthRequestException(
                message=f"Error on authentication request: {error.status_code} - {error.message} ",
            )

        except JAuthBaseException as error:
            raise JAuthAuthenticationException(
                message=f"Error on authentication request: {error.message}",
            )

    @property
    def __should_authenticate(self):
        return not self.token or self.token_expires_at < (
            datetime.now() - timedelta(minutes=1)
        )

    def request(
        self,
        method: request,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        auth: Optional[HTTPBasicAuth] = None,
        auth_server_authenticated: Optional[bool] = True,
    ) -> dict:
        json = json or {}
        headers = headers or {}
        data = data or {}

        if auth_server_authenticated and self.__should_authenticate:
            self.__authenticate()
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = method(url=url, headers=headers, json=json, data=data, auth=auth)
            response.raise_for_status()

            return response.json()

        except HTTPError as error:
            if 400 <= error.response.status_code < 500:
                raise JAuthClientException(
                    message=error.response.text,
                    status_code=error.response.status_code,
                )

            if error.response.status_code >= 500:
                raise JAuthServerException(
                    message=error.response.text,
                    status_code=error.response.status_code,
                )

        except ConnectionError as error:
            raise JAuthConnectionException(
                message=f"Error on connection: {error}",
            )

        except Timeout as error:
            raise JAuthTimeoutException(
                message=f"Timeout on request: {error}",
            )

        except RequestException as error:
            raise JAuthRequestException(
                message=f"Error on request: {error}",
            )
