from monobank._core.client.base import BaseAPIClient


class AcquiringAPIClient(BaseAPIClient):
    def __init__(self, token: str, response_serializer=BaseAPIClient.get_json):
        super().__init__(base_url="https://api.monobank.ua/api/", response_serializer=response_serializer)
        self._token = token
        self.headers |= {'X-Token': self._token}
