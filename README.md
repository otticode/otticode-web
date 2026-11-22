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

### DigitalOcean App Platform (primary)

App `otticode-app` builds and deploys automatically on every push to `main`:

- <https://otticode-app-rgosu.ondigitalocean.app>

The app spec runs `bash bin/build-site.sh` and serves `_site/`. App Platform would
otherwise publish the repo root verbatim, so the build step is what keeps
`prototype/`, `tests/`, `README.md` and dotfiles off the public site.

To preview exactly what gets published:

```bash
bash bin/build-site.sh && ls -R _site
```

### VPS (legacy)

```bash
./deploy.sh
```

`deploy.sh` is untracked and lives only on the machine that holds the SSH access.
It rsyncs to `otticode.com` and carries its own `--exclude` list, kept in sync
with `bin/build-site.sh`.
