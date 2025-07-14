from typing import Any, Dict, List

import requests


class ProxyAPIClient:
    """
    Класс для работы с api: https://test-rg8.ddns.net
    Запускает новую сессию при инициализации
    Имеет два метода, необходимых для получения save_id:
    get_token - получить токен для последующего post запроса
    post_proxies - post запрос для получения save_id
    """

    def __init__(
        self,
        personal_token: str,
        upstream_proxy: str,
    ):
        self.personal_token = personal_token
        self.base_url = "https://test-rg8.ddns.net"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/task",
            }
        )
        self.session.proxies = {"http": upstream_proxy, "https": upstream_proxy}

    def get_token(self) -> str:
        resp1 = self.session.get(f"{self.base_url}/api/get_token", timeout=3)
        resp1.raise_for_status()

    def post_proxies(self, proxies: List[str]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/post_proxies"
        payload = {
            "user_id": self.personal_token,
            "len": len(proxies),
            "proxies": ", ".join(proxies),
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
