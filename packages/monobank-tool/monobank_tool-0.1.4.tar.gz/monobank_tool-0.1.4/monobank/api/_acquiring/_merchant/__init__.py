from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from monobank._core.client.acquiring import AcquiringAPIClient

from monobank.api._acquiring._merchant.details import DetailsFacade
from monobank.api._acquiring._merchant.invoice import InvoiceFacade
from monobank.api._acquiring._merchant.pubkey import PubkeyFacade
from monobank.api._acquiring._merchant.qr import QRFacade
from monobank.api._acquiring._merchant.statement import StatementFacade
from monobank.api._acquiring._merchant.wallet import WalletFacade


class MerchantFacade:
    def __init__(self, client: "AcquiringAPIClient"):
        self.client = client
        self.invoice = InvoiceFacade(client=client)
        self.details = DetailsFacade(client=client)
        self.pubkey = PubkeyFacade(client=client)
        self.qr = QRFacade(client=client)
        self.statement = StatementFacade(client=client)
        self.wallet = WalletFacade(client=client)
