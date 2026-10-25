#!/usr/bin/env bash
# Link every skills/* into ~/.claude/skills/. Safe to re-run; never replaces a real directory.
set -euo pipefail
cd "$(dirname "$0")/.."
dest="${HOME}/.claude/skills"
mkdir -p "$dest"
for d in skills/*/; do
  name="$(basename "$d")"
  [ "$name" = "_probe" ] && continue
  link="$dest/$name"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "SKIP $name: $link is a real directory, move it away first"
    continue
  fi
  ln -sfn "$(realpath "$d")" "$link"
  echo "linked $name -> $(readlink "$link")"
done
