class PaymentGateway:
    def process_payment(self, *, amount: float, patron_id: str, book_id: str) -> dict:  # keyword-only use in our tests
        raise NotImplementedError
    def refund_payment(self, transaction_id: str, amount: float) -> dict:
        raise NotImplementedError
