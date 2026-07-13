# AGENTS.md

## Cursor Cloud specific instructions

This repo is the **Resend Python SDK** — a client library (published to PyPI as `resend`).
There is **no server, database, or long-running service**; the only external dependency is the
Resend REST API (`https://api.resend.com`), which the unit tests mock. Standard dev commands live
in `tox.ini` (envs: `format`, `lint`, `mypy`, `py`); the update script pre-installs the toolchain.

Non-obvious caveats for this environment:

- **Use `python3`, not `python`** (there is no `python` shim). Console scripts like `tox` install
  to `~/.local/bin`, which may not be on `PATH`; call `python3 -m <tool>` or add it to `PATH`.
- **`flake8<5.0.0` (pinned in `tox.ini`) is incompatible with Python 3.12** (the system default),
  failing with `'EntryPoints' object has no attribute 'get'`. CI only lints/type-checks/tests on
  Python 3.8–3.11. **Python 3.11 is installed** for this reason. Force tox to use it via basepython
  overrides:
  - Lint:  `tox -e lint -x testenv:lint.basepython=python3.11`
  - Mypy:  `tox -e mypy -x testenv:mypy.basepython=python3.11`
  - Tests: `tox -e py -x testenv:py.basepython=python3.11`
- Tests/mypy also run fine directly on Python 3.12 (`python3 -m pytest --doctest-modules tests`);
  **only flake8 requires 3.11**. `tox` defaults `basepython` to the interpreter it runs under
  (3.12), so the overrides above are needed to match CI.
- The `examples/` scripts hit the **real** Resend API and require `RESEND_API_KEY` (and optionally
  `RESEND_API_URL` to point at a different base URL). They are not needed for tests/lint/build.
