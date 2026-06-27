#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Installing Hackathon Codex Agent Pack..."

mkdir -p "$ROOT/team-work"
python3 -m harness.hackathon_harness init
python3 -m harness.hackathon_harness dashboard
chmod +x "$ROOT/bin/hackathon-harness"

echo
echo "Who is using this Codex agent on this machine?"
python3 -m harness.hackathon_harness status
echo
read -r -p "Type your member id or exact name: " MEMBER_CHOICE
python3 -m harness.hackathon_harness select-member "$MEMBER_CHOICE"

echo
echo "Install complete."
echo
echo "Next:"
echo "  1. Open this repository in Codex."
echo "  2. Use the hackathon-teammate skill for teammate work."
echo "  3. Check status with: python3 -m harness.hackathon_harness status"
echo "  4. Leader dashboard: dashboard/index.html"
