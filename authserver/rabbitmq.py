from dataclasses import dataclass
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


@dataclass
class RabbitMQ:
    admin_username: str
    admin_password: str
    host: str = "localhost"
    port: int = 15672

    def get(self, endpoint: str) -> Any:
        url = f"http://{self.host}:{self.port}/api/{endpoint}"
        rsp = requests.get(url, auth=HTTPBasicAuth(self.admin_username, self.admin_password))
        return rsp.json()

    @property
    def vhosts(self) -> list:
        return self.get("vhosts")

    @property
    def users(self) -> list:
        return self.get("users")
