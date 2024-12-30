import abc

from opentelemetry.trace import SpanKind

from ovinc_client.constants import OVINC_CLIENT_TIMEOUT, ResponseData
from ovinc_client.trace.utils import start_as_current_span


class Component:
    """
    Component
    """


class Endpoint:
    """
    Endpoint
    """

    def __init__(self, client, base_url: str):
        self._client = client
        self.base_url = base_url

    async def __call__(self, params: dict, timeout: float = OVINC_CLIENT_TIMEOUT) -> ResponseData:
        with start_as_current_span(span_name=self.__class__.__name__, kind=SpanKind.CLIENT):
            return await self._client.call_api(method=self.method, url=self.url, params=params, timeout=timeout)

    @property
    def url(self) -> str:
        return self.base_url.rstrip("/") + "/" + self.path.lstrip("/")

    @property
    @abc.abstractmethod
    def method(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def path(self) -> str:
        raise NotImplementedError
