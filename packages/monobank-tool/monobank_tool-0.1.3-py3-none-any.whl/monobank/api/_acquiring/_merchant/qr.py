from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from monobank._core.client.acquiring import AcquiringAPIClient


class QRFacade:
    def __init__(self, client: "AcquiringAPIClient"):
        self.client = client

    def details(self, params=None, data=None):
        """
        Інформація про QR-касу, лише для активованих QR-кас

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/qr/details", params=params, data=data)

    def reset_amount(self, params=None, data=None):
        """
        Видалення суми оплати з QR-каси

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/qr/reset-amount", params=params, data=data)

    def list(self, params=None, data=None):
        """
        Список QR-кас

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/qr/list", params=params, data=data)