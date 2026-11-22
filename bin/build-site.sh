#!/usr/bin/env bash
#
# Assemble the publishable static site into _site/.
#
# DigitalOcean App Platform serves the repo root verbatim, so anything tracked
# in git is world-readable. This script copies only the files that belong on the
# public site; the design mockups (prototype/) and the test harness (tests/)
# never reach the deployed tree.
#
# Wired up in the app spec via:
#   build_command: bash bin/build-site.sh
#   output_dir: _site
#
set -euo pipefail

cd "$(dirname "$0")/.."

OUT="_site"

# Kept in sync with the --exclude list in deploy.sh.
EXCLUDES=(
  .git
  .gitignore
  .playwright-mcp
  README.md
  bin
  deploy.sh
  og-temp.*
  prototype
  tests
  "$OUT"
)

rm -rf "$OUT"
mkdir -p "$OUT"

shopt -s dotglob nullglob
for entry in *; do
  for skip in "${EXCLUDES[@]}"; do
    # shellcheck disable=SC2053 # deliberate glob match for og-temp.*
    if [[ "$entry" == $skip ]]; then
      continue 2
    fi
  done
  cp -R "$entry" "$OUT/"
done

printf 'Built %s (%s entries):\n' "$OUT" "$(find "$OUT" -maxdepth 1 -mindepth 1 | wc -l)"
find "$OUT" -maxdepth 1 -mindepth 1 -printf '  %f\n' | sort
