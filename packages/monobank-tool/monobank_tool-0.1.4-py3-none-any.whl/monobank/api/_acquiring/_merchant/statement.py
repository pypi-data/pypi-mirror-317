from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from monobank._core.client.acquiring import AcquiringAPIClient


class StatementFacade:
    def __init__(self, client: "AcquiringAPIClient"):
        self.client = client

    def __call__(self, params=None, data=None):
        """
        Виписка за період

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/statement", params=params, data=data)
