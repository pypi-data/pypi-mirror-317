import os

import singleton
from usso.session import AsyncUssoSession, UssoSession

from .apps.saas import AsyncSaaS, SaaS


class UFaaS(UssoSession, metaclass=singleton.Singleton):

    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: UssoSession | None = None,
    ):
        super().__init__(
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )
        if not ufaas_base_url and client and hasattr(client, "ufaas_base_url"):
            ufaas_base_url = client.ufaas_base_url
        assert ufaas_base_url, "UFAAS_URL is required"
        if ufaas_base_url.endswith("/"):
            ufaas_base_url = ufaas_base_url[:-1]
        self.ufaas_base_url = ufaas_base_url

        self.initiate_apps()

    def initiate_apps(self):
        self.saas = SaaS(client=self)


class AsyncUFaaS(AsyncUssoSession, metaclass=singleton.Singleton):

    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFILES_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: AsyncUssoSession | None = None,
    ):
        super().__init__(
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )
        if not ufaas_base_url and client and hasattr(client, "ufaas_base_url"):
            ufaas_base_url = client.ufaas_base_url
        assert ufaas_base_url, "UFAAS_URL is required"
        if ufaas_base_url.endswith("/"):
            ufaas_base_url = ufaas_base_url[:-1]
        self.ufaas_base_url = ufaas_base_url

        self.initiate_apps()

    def initiate_apps(self):
        self.saas = AsyncSaaS(client=self)
