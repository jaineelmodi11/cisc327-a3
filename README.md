# CISC/CMPE 327 – Assignment 3 (Library Management – Stubs & Mocks)

**Student:** Jaineel Modi (20405104)  
**Repo:** https://github.com/jaineelmodi11/cisc327-a3

## Quick start

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

# run tests
pytest -q

# coverage (statement + branch)
coverage run --branch -m pytest -q tests/
coverage report -m
coverage html

# open HTML report (macOS)
python - <<'PY'
import webbrowser, pathlib; webbrowser.open((pathlib.Path("htmlcov/index.html")).resolve().as_uri())
PY
```
## Assignment Requirements (what this repo includes)

- Restructured project with **`services/`** (business logic) and **`tests/`**.
- Functions under test in `services/library_service.py`:
  - `pay_late_fees(patron_id, book_id, payment_gateway)`
  - `refund_late_fee_payment(transaction_id, amount, payment_gateway)`
- **Stubbing** database seams with `mocker.patch(...)` (pytest-mock):
  - `services.library_service.get_book_by_id`
  - `services.library_service.calculate_late_fee_for_book`
- **Mocking** the external gateway with `Mock(spec=PaymentGateway)`:
  - `PaymentGateway.process_payment`, `PaymentGateway.refund_payment`
  - Verified via `assert_called_once_with(...)`, `assert_called_once()`, `assert_not_called()`
- **Coverage ≥ 80%** (statement + branch) — achieved 100% on `services/`.
- **Screenshots embedded** (initial & final coverage; tests passing).
- **Guardrails**:
  - Never mock the functions under test.
  - Do not modify `services/payment_service.py` (treat as external).
  - No real DB calls — always stub seams.

## What’s Tested (new cases)

- `test_pay_late_fees_success_calls_gateway_with_correct_params` — gateway called with exact args  
- `test_pay_late_fees_declined_returns_declined` — decline path verified  
- `test_pay_late_fees_invalid_patron_id_does_not_call_gateway` — validation short-circuit (mock not called)  
- `test_pay_late_fees_zero_fee_short_circuits_gateway` — zero-fee early return (mock not called)  
- `test_pay_late_fees_network_error_is_handled` — try/except error path  
- `test_refund_success_calls_gateway` — happy-path refund with exact args  
- `test_refund_invalid_transaction_id_rejected` — invalid txn id (mock not called)  
- `test_refund_invalid_amounts_rejected` — 0, negative, or > $15 (mock not called)  
- `test_pay_late_fees_invalid_book_id_does_not_call_gateway` — validation short-circuit  
- `test_pay_late_fees_unknown_status_defaults_unknown` — default `"unknown"` status

**Stubs (via `mocker.patch`)**  
- `services.library_service.get_book_by_id`  
- `services.library_service.calculate_late_fee_for_book`

**Mocks (via `Mock(spec=PaymentGateway)`)**  
- `PaymentGateway.process_payment`  
- `PaymentGateway.refund_payment`


## Coverage

- **Initial (before seam exclusions):** ~95.7% statements (services), 100% branches  
- **Final:** 100% statements & 100% branches on `services/`

Seam placeholders that intentionally `raise NotImplementedError` are excluded via `# pragma: no cover` and an `exclude_lines` rule in `.coveragerc`. This avoids executing non-behavioral seams just to inflate coverage numbers.

---

## Screenshots (in `/screenshots`)

**Required in report**
- `03-pytest-all-tests-passing.png` — All tests passing (`pytest -q`)
- `02-final-coverage-terminal.png` — Final coverage table (100%)
- `05-coverage-html-index-final.png` — Final HTML coverage index (100%)

**Optional (improvement path)**
- `01-initial-coverage-terminal.png` — Initial coverage (~95.7%)
- `04-coverage-html-index-initial.png` — Initial HTML coverage index (~95.7%)

---

## Project Structure

```text
.
├── services/
│   ├── __init__.py
│   ├── library_service.py
│   └── payment_service.py     # treated as external; do not modify
├── tests/
│   └── test_payment_mock_stub.py
├── conftest.py                # ensures 'services' importable in pytest
├── requirements.txt
├── pytest.ini
├── .coveragerc
└── README.md

```

## Notes & Guardrails

- Business logic is isolated: **stub** data seams; **mock** the external gateway and verify with `assert_called_once_with(...)` / `assert_not_called()`.
- Use `Mock(spec=PaymentGateway)` so attribute/method typos are caught early.
- Treat `services/payment_service.py` as external; **do not modify it**.
- Do not execute seam placeholders that raise `NotImplementedError` just to inflate coverage; exclude them instead (see `.coveragerc` with `# pragma: no cover` + `exclude_lines`).

---

## How to Regenerate the Screenshots

```bash
# tests passing (terminal)
pytest -q

# final coverage (terminal + HTML)
coverage run --branch -m pytest -q tests/
coverage report -m
coverage html
# open the HTML index and click into services/library_service.py
python - <<'PY'
import webbrowser, pathlib
webbrowser.open((pathlib.Path("htmlcov/index.html")).resolve().as_uri())
PY
```

## Inline Screenshots

<details>
<summary><b>All tests passing (pytest -q)</b></summary>

![All tests passing](/screenshots/03-pytest-all-tests-passing.png)
</details>

<details>
<summary><b>Final coverage (terminal)</b></summary>

![Final coverage (terminal)](/screenshots/02-final-coverage-terminal.png)
</details>

<details>
<summary><b>Final coverage (HTML index)</b></summary>

![Final coverage (HTML)](/screenshots/04-html-coverage-final-index.png)
</details>

<!-- Optional improvement path -->
<details>
<summary><b>Initial coverage (terminal)</b></summary>

![Initial coverage (terminal)](/screenshots/01-initial-coverage-terminal.png)
</details>


