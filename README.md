# CISC/CMPE 327 – Assignment 3 (Library Management – Stubs & Mocks)

**Student:** Jaineel Modi (20405104)  
**Repo:** https://github.com/jaineelmodi11/cisc327-a3

## Quick start

```bash
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
