from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from monobank._core.client.acquiring import AcquiringAPIClient


class InvoiceFacade:
    def __init__(self, client: "AcquiringAPIClient"):
        self.client = client

    def create(self, params=None, data=None):
        """
        Створення рахунку для оплати

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/invoice/create", params=params, data=data)

    def status(self, params=None, data=None):
        """
        Метод перевірки статусу рахунку при розсинхронізації з боку продавця
        або відсутності webHookUrl при створенні рахунку.

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/invoice/status", params=params, data=data)

    def cancel(self, params=None, data=None):
        """
        Скасування успішної оплати рахунку

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/invoice/cancel", params=params, data=data)

    def remove(self, params=None, data=None):
        """
        Інвалідація рахунку, якщо за ним ще не було здіснено оплати

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/invoice/remove", params=params, data=data)

    def payment_info(self, params=None, data=None):
        """
        Дані про успішну оплату, якщо вона була здійснена

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/invoice/payment-info", params=params, data=data)

    def finalize(self, params=None, data=None):
        """
        Фіналізація суми холду

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/invoice/finalize", params=params, data=data)

    def payment_direction(self, params=None, data=None):
        """
        Створення рахунку та його оплата за реквізитами картки.
        Увага, це апі буде працювати тільки за умови наявності у мерчанта активного PCI DSS сертифіката!

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.post("merchant/invoice/payment-direction", params=params, data=data)

    def fiscal_checks(self, params=None, data=None):
        """
        Метод для отримання даних фіскальних чеків та їх статусів

        :param params: параметри запиту
        :param data: дані запиту
        :return: Serialized response (default get_json)
        """
        return self.client.get("merchant/invoice/fiscal-checks", params=params, data=data)
