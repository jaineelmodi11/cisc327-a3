from __future__ import annotations
from typing import Any, Dict
from .payment_service import PaymentGateway  # treat as external

MAX_REFUND = 15.0

# -------- DB seams you will STUB in tests --------
def get_book_by_id(book_id: str) -> Dict[str, Any]:
    """DB lookup for a book. Intentionally unimplemented — stub in tests."""
    raise NotImplementedError("DB not available in unit tests; stub me.")

def calculate_late_fee_for_book(patron_id: str, book_id: str) -> float:
    """Compute late fee. Intentionally unimplemented — stub in tests."""
    raise NotImplementedError("DB/logic not available in unit tests; stub me.")

# -------- functions under test --------
def pay_late_fees(patron_id: str, book_id: str, payment_gateway: PaymentGateway) -> Dict[str, Any]:
    """Check inputs, ensure book exists, compute fee, then call external gateway."""
    if not patron_id or not isinstance(patron_id, str):
        raise ValueError("Invalid patron_id")
    if not book_id or not isinstance(book_id, str):
        raise ValueError("Invalid book_id")

    _ = get_book_by_id(book_id)  # existence check (value otherwise unused here)

    amount = float(calculate_late_fee_for_book(patron_id, book_id))
    if amount <= 0:
        return {"status": "no_fee", "amount": 0.0}

    try:
        gw_res = payment_gateway.process_payment(
            amount=amount, patron_id=patron_id, book_id=book_id
        )
        status = gw_res.get("status", "unknown")
        merged = {"status": status, "amount": amount}
        merged.update(gw_res)
        return merged
    except Exception as e:
        return {"status": "error", "amount": amount, "error": str(e)}

def refund_late_fee_payment(transaction_id: str, amount: float, payment_gateway: PaymentGateway) -> Dict[str, Any]:
    """Validate inputs and call external refund API with the gateway."""
    if not transaction_id or not isinstance(transaction_id, str):
        raise ValueError("Invalid transaction_id")
    amount = float(amount)
    if amount <= 0:
        raise ValueError("Refund amount must be > 0")
    if amount > MAX_REFUND:
        raise ValueError(f"Refund amount exceeds ${MAX_REFUND:.0f} maximum")

    return payment_gateway.refund_payment(transaction_id, amount)
