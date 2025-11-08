import pytest
from unittest.mock import Mock
from services.payment_service import PaymentGateway  # spec only
from services.library_service import pay_late_fees, refund_late_fee_payment

# Patch targets: patch WHERE USED (module path), not where defined
STUB_FEE_TARGET = "services.library_service.calculate_late_fee_for_book"
STUB_BOOK_TARGET = "services.library_service.get_book_by_id"

# ---------- pay_late_fees() ----------
def test_pay_late_fees_success_calls_gateway_with_correct_params(mocker):
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B1", "title": "Clean Code"})
    mocker.patch(STUB_FEE_TARGET, return_value=7.50)

    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = {"status": "success", "transaction_id": "tx_123"}

    res = pay_late_fees("P1", "B1", gateway)

    assert res["status"] == "success"
    assert res["amount"] == 7.50
    assert res["transaction_id"] == "tx_123"
    gateway.process_payment.assert_called_once_with(amount=7.50, patron_id="P1", book_id="B1")

def test_pay_late_fees_declined_returns_declined(mocker):
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B9"})
    mocker.patch(STUB_FEE_TARGET, return_value=3.00)

    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = {"status": "declined", "reason": "insufficient_funds"}

    res = pay_late_fees("P9", "B9", gateway)
    assert res["status"] == "declined"
    gateway.process_payment.assert_called_once()

def test_pay_late_fees_invalid_patron_id_does_not_call_gateway(mocker):
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B2"})
    mocker.patch(STUB_FEE_TARGET, return_value=5.00)

    gateway = Mock(spec=PaymentGateway)
    with pytest.raises(ValueError):
        pay_late_fees("", "B2", gateway)
    gateway.process_payment.assert_not_called()

def test_pay_late_fees_zero_fee_short_circuits_gateway(mocker):
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B3"})
    mocker.patch(STUB_FEE_TARGET, return_value=0.0)

    gateway = Mock(spec=PaymentGateway)
    res = pay_late_fees("P3", "B3", gateway)
    assert res["status"] == "no_fee"
    assert res["amount"] == 0.0
    gateway.process_payment.assert_not_called()

def test_pay_late_fees_network_error_is_handled(mocker):
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B4"})
    mocker.patch(STUB_FEE_TARGET, return_value=4.25)

    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.side_effect = ConnectionError("timeout")

    res = pay_late_fees("P4", "B4", gateway)
    assert res["status"] == "error"
    assert "timeout" in res["error"].lower()
    gateway.process_payment.assert_called_once()

# ---------- refund_late_fee_payment() ----------
def test_refund_success_calls_gateway():
    gateway = Mock(spec=PaymentGateway)
    gateway.refund_payment.return_value = {"status": "refunded", "transaction_id": "tx_abc", "amount": 5.00}

    res = refund_late_fee_payment("tx_abc", 5.00, gateway)
    assert res["status"] == "refunded"
    gateway.refund_payment.assert_called_once_with("tx_abc", 5.00)

@pytest.mark.parametrize("bad_txn", ["", None])
def test_refund_invalid_transaction_id_rejected(bad_txn):
    gateway = Mock(spec=PaymentGateway)
    with pytest.raises(ValueError):
        refund_late_fee_payment(bad_txn, 5.0, gateway)
    gateway.refund_payment.assert_not_called()

@pytest.mark.parametrize("bad_amount", [0.0, -1.0, 16.0])  # zero, negative, exceeds $15
def test_refund_invalid_amounts_rejected(bad_amount):
    gateway = Mock(spec=PaymentGateway)
    with pytest.raises(ValueError):
        refund_late_fee_payment("tx_ok", bad_amount, gateway)
    gateway.refund_payment.assert_not_called()

def test_pay_late_fees_invalid_book_id_does_not_call_gateway(mocker):
    # even if DB seams are present, we fail early on invalid book_id
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B2"})
    mocker.patch(STUB_FEE_TARGET, return_value=5.0)

    gateway = Mock(spec=PaymentGateway)
    with pytest.raises(ValueError):
        pay_late_fees("P2", "", gateway)
    gateway.process_payment.assert_not_called()

def test_pay_late_fees_unknown_status_defaults_unknown(mocker):
    mocker.patch(STUB_BOOK_TARGET, return_value={"id": "B5"})
    mocker.patch(STUB_FEE_TARGET, return_value=2.5)

    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = {}  # no 'status' key

    res = pay_late_fees("P5", "B5", gateway)
    assert res["status"] == "unknown"
    assert res["amount"] == 2.5
    gateway.process_payment.assert_called_once_with(amount=2.5, patron_id="P5", book_id="B5")
