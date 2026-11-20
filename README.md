# otticode-web

Otticode's web site — static HTML, one stylesheet, self-hosted fonts, no JavaScript.

## Testing

```bash
python3 tests/test_form.py             # markup checks + live Formspree probe (sends no email)
python3 tests/test_form.py --offline   # markup checks only, no network
python3 tests/test_form.py --submit    # ALSO sends one real test email — explicit opt-in
```

The default run posts an invalid email address to the endpoint, which Formspree
rejects with `422 TYPE_EMAIL` before forwarding anything. Use `--submit` when you
actually want to prove delivery end to end.

## Deployment

```bash
./deploy.sh
```

Configuration lives in `deploy.sh`. It excludes `.git/`, `deploy.sh`, `README.md`,
`prototype/` and `tests/`, so nothing from the design work or the test harness can
reach production.
