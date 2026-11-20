#!/usr/bin/env python3
"""
Pre-flight check for the Formspree contact form on the Otticode site.

    python3 tests/test_form.py             # static checks + live endpoint probe (no email sent)
    python3 tests/test_form.py --offline   # static checks only
    python3 tests/test_form.py --submit    # ALSO sends one real email — explicit opt-in

The default run never delivers a message: the live probe posts an invalid email
address, which Formspree rejects with 422 before it forwards anything.

Exit code 0 = every check passed.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
TIMEOUT = 15
UA = "Mozilla/5.0 (X11; Linux x86_64) otticode-form-test/1.0"

PASS, FAIL = "PASS", "FAIL"
HONEYPOT = "_gotcha"
results = []


def check(name, fn):
    try:
        fn()
    except AssertionError as exc:
        results.append((FAIL, name, str(exc) or "assertion failed"))
    except Exception as exc:  # noqa: BLE001 - report, don't crash the suite
        results.append((FAIL, name, f"{type(exc).__name__}: {exc}"))
    else:
        results.append((PASS, name, ""))


class FormParser(HTMLParser):
    """Minimal collector for forms, their controls and their labels."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self._form = None
        self._label = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self._form = {"attrs": attrs, "controls": [], "labels": []}
            self.forms.append(self._form)
        elif self._form is None:
            return
        elif tag == "label":
            self._label = {"for": attrs.get("for"), "text": ""}
            self._form["labels"].append(self._label)
        elif tag in ("input", "textarea", "select", "button"):
            self._form["controls"].append({"tag": tag, **attrs})

    def handle_data(self, data):
        if self._label is not None:
            self._label["text"] += data

    def handle_endtag(self, tag):
        if tag == "label":
            self._label = None
        elif tag == "form":
            self._form = None


def done():
    for status, name, detail in results:
        mark = "ok  " if status == PASS else "FAIL"
        print(f"[{mark}] {name}" + (f"\n         {detail}" if detail else ""))
    failed = sum(1 for r in results if r[0] == FAIL)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


def post(endpoint, fields, accept="application/json"):
    body = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "User-Agent": UA,
            "Accept": accept,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def get(endpoint):
    req = urllib.request.Request(endpoint, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="skip the network probe")
    ap.add_argument("--submit", action="store_true", help="send one real email")
    args = ap.parse_args()

    parser = FormParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    forms = parser.forms

    # ---- structure -------------------------------------------------------
    check("index.html has exactly one <form>", lambda: (
        _assert(len(forms) == 1, f"found {len(forms)}")
    ))

    form = forms[0] if forms else {"attrs": {}, "controls": [], "labels": []}
    action = form["attrs"].get("action", "")
    match = re.fullmatch(r"https://formspree\.io/f/([a-z0-9]+)", action)

    check("form action is a Formspree endpoint", lambda: (
        _assert(match is not None, f"action={action!r}")
    ))
    check('form uses method="POST"', lambda: (
        _assert(form["attrs"].get("method", "").upper() == "POST",
                f"method={form['attrs'].get('method')!r}")
    ))

    named = [c for c in form["controls"]
             if c.get("name") and c.get("name") != HONEYPOT
             and c.get("type", "text").lower() not in ("submit", "button", "hidden")]
    hidden = [c for c in form["controls"] if c.get("type", "").lower() == "hidden"]

    def every_control_is_labelled():
        label_for = {l["for"] for l in form["labels"] if l["for"]}
        unlabelled = [c.get("name") for c in named if c.get("id") not in label_for]
        _assert(not unlabelled, f"no <label for> on: {unlabelled}")

    check("every field has a <label for>", every_control_is_labelled)

    def no_orphan_labels():
        controls = {c.get("id") for c in form["controls"] if c.get("id")}
        orphans = [l["for"] for l in form["labels"] if l["for"] and l["for"] not in controls]
        _assert(not orphans, f"labels pointing at nothing: {orphans}")

    check("no <label> points at a missing field", no_orphan_labels)

    def expected_fields():
        names = {c.get("name") for c in named}
        missing = {"name", "email", "message"} - names
        _assert(not missing, f"missing: {sorted(missing)}")

    check("name, email and message are all submitted", expected_fields)

    def email_is_validated():
        email = next((c for c in named if c.get("name") == "email"), None)
        _assert(email is not None, "no email field")
        _assert(email.get("type") == "email", f"type={email.get('type')!r}")

    check('email uses type="email"', email_is_validated)

    def required_marked():
        # the browser should block empty submissions
        missing = [c.get("name") for c in named
                   if "required" not in c and c.get("aria-required") != "true"]
        _assert(not missing, f"not required: {missing}")

    check("all visible fields are marked required", required_marked)

    def next_page_exists():
        nxt = next((c for c in hidden if c.get("name") == "_next"), None)
        _assert(nxt is not None, "no hidden _next field")
        target = urllib.parse.urlparse(nxt.get("value", ""))
        path = target.path.lstrip("/") or "index.html"
        _assert((ROOT / path).exists(), f"_next points at a missing file: {path}")

    check("_next points at a real local page", next_page_exists)

    def no_inert_handler():
        onsubmit = form["attrs"].get("onsubmit", "")
        _assert("return false" not in onsubmit.replace(" ", "").lower(),
                "onsubmit disables the form")

    check("form is not disabled by an onsubmit handler", no_inert_handler)

    def privacy_page_exists():
        html = PAGE.read_text(encoding="utf-8")
        _assert("privacy.html" in html, "no privacy link")
        _assert((ROOT / "privacy.html").exists(), "privacy.html is missing")

    check("privacy link resolves", privacy_page_exists)

    def unique_ids():
        ids = [c.get("id") for c in form["controls"] if c.get("id")]
        dupes = {i for i in ids if ids.count(i) > 1}
        _assert(not dupes, f"duplicate ids: {sorted(dupes)}")

    check("no duplicate ids inside the form", unique_ids)

    def honeypot_present():
        _assert(any(c.get("name") == "_gotcha" for c in form["controls"]),
                "no _gotcha honeypot field (Formspree drops bots silently without it)")

    check("spam honeypot (_gotcha) is present", honeypot_present)

    # ---- live endpoint ---------------------------------------------------
    if not args.offline and match:
        endpoint = f"https://formspree.io/f/{match.group(1)}"

        def endpoint_responds():
            status, body = get(endpoint)
            # 405 "Form should POST" means the endpoint exists and is POST-only.
            _assert(status in (200, 405), f"GET returned {status}: {body[:120]}")

        check(f"endpoint {endpoint} responds", endpoint_responds)

        def endpoint_is_active():
            status, body = post(endpoint, {"email": "not-an-email"})
            _assert(status == 422, f"expected 422, got {status}: {body[:160]}")
            payload = json.loads(body)
            codes = {e.get("code") for e in payload.get("errors", [])}
            _assert("TYPE_EMAIL" in codes, f"unexpected errors: {sorted(codes)}")

        check("endpoint is active and validates email (nothing sent)", endpoint_is_active)

        if args.submit:
            def send_one():
                status, body = post(endpoint, {
                    "name": "Form test",
                    "email": "test@example.com",
                    "message": "Automated connectivity test from tests/test_form.py",
                })
                _assert(status == 200, f"expected 200, got {status}: {body[:200]}")

            check("real submission accepted (a test email was delivered)", send_one)

    return done()


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    sys.exit(main())
