from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from monobank._core.client.acquiring import AcquiringAPIClient


class DetailsFacade:
    def __init__(self, client: "AcquiringAPIClient"):
        self.client = client

    def __call__(self, params=None, data=None):
        """
        Дані мерчанта

        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/details", params=params, data=data)
