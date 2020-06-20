import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any, List

import requests
from requests.auth import HTTPBasicAuth, AuthBase


@dataclass
class RabbitMQ:
    admin_username: str = os.environ["RABBITMQ_ADMIN_USER"]
    admin_password: str = os.environ["RABBITMQ_ADMIN_PASSWORD"]
    host: str = "localhost"
    port: int = 15672

    def get(self, endpoint: str) -> Any:
        rsp = requests.get(
            self.url(endpoint),
            auth=self.auth,
        )
        rsp.raise_for_status()
        return rsp.json()

    def put(self, endpoint: str, body: dict) -> requests.Response:
        rsp = requests.put(
            self.url(endpoint),
            json=body,
            auth=self.auth,
        )
        rsp.raise_for_status()
        return rsp

    def post(self, endpoint: str, body: dict) -> requests.Response:
        rsp = requests.post(
            self.url(endpoint),
            json=body,
            auth=self.auth,
        )
        rsp.raise_for_status()
        return rsp

    def url(self, endpoint: str) -> str:
        return f"http://{self.host}:{self.port}/api/{endpoint}"

    @property
    def auth(self) -> AuthBase:
        return HTTPBasicAuth(self.admin_username, self.admin_password)

    @property
    def vhosts(self) -> list:
        return self.get("vhosts")

    @property
    def users(self) -> list:
        return self.get("users")

    def put_user(self, username: str, password: str, tags: List[str] = None) -> requests.Response:
        if tags is None:
            tags = []

        return self.put(
            f"users/{username}",
            dict(
                password_hash=self.hash_password(password),
                tags=",".join(tags),
            )
        )

    def put_topic_permissions(
            self,
            username: str,
            write: str,
            read: str,
            vhost: str = "%2f",
    ) -> requests.Response:

        return self.put(
            f"topic-permissions/{vhost}/{username}",
            dict(
                exchange="amq.topic",
                write=write,
                read=read,
            )
        )

    def get_topic_permissions(self, username: str, vhost: str = "%2f") -> list:
        return self.get(f"topic-permissions/{vhost}/{username}")

    def delete_users(self, users: List[str]) -> None:
        self.post(
            "users/bulk-delete",
            dict(users=users),
        )

    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_bytes(4)
        password_bytes = password.encode("utf-8")
        salted_password = salt + password_bytes
        hasher = hashlib.sha256()
        hasher.update(salted_password)
        hashed_password = hasher.digest()
        resalted_password = salt + hashed_password
        return base64.b64encode(resalted_password).decode("utf-8")
