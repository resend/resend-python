#!/usr/bin/env bash
#
# smoke_test_release.sh
#
# Smoke-test a released version of the resend Python SDK in a clean, isolated
# Docker container, the way we validate releases:
#
#   1. spin up a fresh python image (nothing pre-installed)
#   2. `pip install resend==<version>` straight from PyPI (as a customer would)
#   3. run a handful of sending-related examples/ files against a real API key
#
# The examples/ folder doubles as our quick smoke-test suite. We don't run all
# of them — just the sending-focused ones (simple_email, attachments, batch...).
#
# Usage:
#   ./scripts/smoke_test_release.sh <version> <api_key> [example ...]
#
# Examples:
#   ./scripts/smoke_test_release.sh 2.33.0 re_xxxxxxxx
#   ./scripts/smoke_test_release.sh 2.33.0 re_xxxxxxxx simple_email with_attachments
#
# Notes:
#   - <example> args are bare names, without the examples/ prefix or .py suffix.
#   - The container is --rm (removed on exit); nothing is installed on your host.
#   - Exit code is non-zero if any example fails, so it's CI-friendly.

set -euo pipefail

# --- args -------------------------------------------------------------------

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <version> <api_key> [example ...]" >&2
  echo "  e.g. $0 2.33.0 re_xxxxxxxx simple_email with_attachments" >&2
  exit 1
fi

VERSION="$1"
API_KEY="$2"
shift 2

# --- preflight: check host dependencies -------------------------------------
#
# Docker is the only thing this script needs on the host — the SDK, Python and
# everything else live inside the container. Fail fast with a clear message
# instead of a cryptic error mid-run.

missing_deps=0

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: 'docker' is not installed or not on your PATH." >&2
  echo "  Install Docker Desktop: https://docs.docker.com/get-docker/" >&2
  missing_deps=1
elif ! docker info >/dev/null 2>&1; then
  echo "Error: Docker is installed but the daemon isn't running." >&2
  echo "  Start Docker Desktop (or the docker service) and try again." >&2
  missing_deps=1
fi

if [[ $missing_deps -ne 0 ]]; then
  exit 1
fi

# Default sending-focused smoke set. Override by passing example names as args.
if [[ $# -gt 0 ]]; then
  EXAMPLES=("$@")
else
  EXAMPLES=(
    simple_email
    with_attachments
    with_b64_attachments
    with_html_file_as_b64_attachment
    with_inline_attachments
    batch_email_send
  )
fi

# --- locate repo root (this script lives in <repo>/scripts) -----------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ ! -d "$REPO_ROOT/examples" || ! -d "$REPO_ROOT/resources" ]]; then
  echo "Error: expected examples/ and resources/ under $REPO_ROOT" >&2
  exit 1
fi

PYTHON_IMAGE="${PYTHON_IMAGE:-python:3.12-slim}"

echo "Smoke-testing resend==$VERSION in a clean $PYTHON_IMAGE container"
echo "Examples: ${EXAMPLES[*]}"
echo

# --- run --------------------------------------------------------------------
#
# examples/ and resources/ are mounted read-only in the same relative layout
# the examples expect (they read ../resources/<file>). The SDK itself is NOT
# mounted — it's pulled from PyPI so we test exactly what customers get.

# `docker run` sits in an `|| status=$?` list so that a failing example
# (non-zero exit from the container) doesn't trip `errexit` and abort before we
# reach the summary block below. We capture the status and report it ourselves.
status=0
docker run --rm \
  -e RESEND_API_KEY="$API_KEY" \
  -e SDK_VERSION="$VERSION" \
  -e EXAMPLES="${EXAMPLES[*]}" \
  -v "$REPO_ROOT/examples:/app/examples:ro" \
  -v "$REPO_ROOT/resources:/app/resources:ro" \
  -w /app \
  "$PYTHON_IMAGE" \
  bash -c '
    set -u
    echo "==> pip install resend==$SDK_VERSION"
    if ! pip install --quiet --no-cache-dir --disable-pip-version-check "resend==$SDK_VERSION"; then
      echo "  ❌ FAILED to install resend==$SDK_VERSION from PyPI." >&2
      echo "     Check the version exists on PyPI and that the network is reachable." >&2
      exit 1
    fi
    echo "==> installed: $(pip show resend | grep -i "^Version:")"
    echo

    fail=0
    passed=()
    failed=()
    for ex in $EXAMPLES; do
      file="examples/$ex.py"
      echo "======================================================================"
      echo "  Running $file"
      echo "======================================================================"
      if [[ ! -f "$file" ]]; then
        echo "  SKIP (not found): $file"
        failed+=("$ex (missing)")
        fail=1
        continue
      fi
      if python "$file"; then
        echo "  ✅ PASS: $ex"
        passed+=("$ex")
      else
        echo "  ❌ FAIL: $ex"
        failed+=("$ex")
        fail=1
      fi
      echo
    done

    echo "======================================================================"
    echo "  Summary for resend==$SDK_VERSION"
    echo "======================================================================"
    echo "  Passed: ${passed[*]:-none}"
    echo "  Failed: ${failed[*]:-none}"
    exit $fail
  ' || status=$?

echo
if [[ $status -eq 0 ]]; then
  echo "✅ Smoke test passed for resend==$VERSION"
else
  echo "❌ Smoke test FAILED for resend==$VERSION (exit $status)"
fi
exit $status
