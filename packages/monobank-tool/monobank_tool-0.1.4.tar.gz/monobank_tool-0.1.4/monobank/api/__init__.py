from monobank.api._acquiring._merchant import MerchantFacade
from monobank._core.client.acquiring import AcquiringAPIClient
from monobank._core import serializers

class AcquiringAPI:
    def __init__(self, api_key, response_serializer=serializers.get_json):
        self._api_key = api_key
        self._client = AcquiringAPIClient(token=self._api_key, response_serializer=response_serializer)
        self.merchant = MerchantFacade(client=self._client)
