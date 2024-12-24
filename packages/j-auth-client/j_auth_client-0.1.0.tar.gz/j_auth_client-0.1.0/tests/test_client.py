import unittest

from j_auth_client.client import JAuthClient


class TestJAuthClient(unittest.TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.auth_url = "https://auth.example.com"

        self.j_auth_client_instance = JAuthClient(
            username=self.username,
            password=self.password,
            auth_url=self.auth_url,
        )

    def test_client(self):
        assert self.j_auth_client_instance.token is None
        assert self.j_auth_client_instance.token_expires_at is None
        assert self.j_auth_client_instance.username == self.username
        assert self.j_auth_client_instance.password == self.password
        assert self.j_auth_client_instance.auth_url == self.auth_url
