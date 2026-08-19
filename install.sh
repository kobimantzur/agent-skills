#!/usr/bin/env bash
# Install these skills into every agent on this machine that reads SKILL.md.
# Symlinks, so `git pull` updates them everywhere.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
TARGETS=("$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills")
installed=0

for target in "${TARGETS[@]}"; do
  parent="$(dirname "$target")"
  [ -d "$parent" ] || continue          # agent not installed here — skip
  mkdir -p "$target"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    ln -sfn "${skill%/}" "$target/$name"
    echo "  linked $name -> $target/$name"
    installed=$((installed+1))
  done
done

if [ "$installed" -eq 0 ]; then
  echo "No agent directories found (~/.claude, ~/.agents, ~/.codex)."
  echo "Create one and re-run, or copy skills/<name>/ wherever your agent reads skills."
  exit 1
fi
echo "Done. Restart your agent to pick them up."
