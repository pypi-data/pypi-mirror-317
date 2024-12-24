from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from monobank._core.client.acquiring import AcquiringAPIClient


class WalletFacade:
    def __init__(self, client: "AcquiringAPIClient"):
        self.client = client

    def delete_card(self, params=None, data=None):
        """
        Видалення картки

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.delete("merchant/wallet/card", params=params, data=data)

    def payment(self, params=None, data=None):
        """
        Створення платежу за токеном картки

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/wallet/payment", params=params, data=data)

    def __call__(self, params=None, data=None):
        """
        Список карток у гаманці

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/wallet", params=params, data=data)
