#!/usr/bin/env bash
# Scaffold a new coach from templates/coach/. Stamps the required hooks (and optional ones
# behind flags), substitutes the coach name, and leaves TODO markers for the author to fill.
# The result intentionally FAILS lint-coach.sh until every TODO is filled in.
set -euo pipefail
cd "$(dirname "$0")/.."

usage() { echo "usage: new-coach.sh <name> [--no-lab] [--with-language] [--with-narrative]"; exit 1; }

NAME="${1:-}"; [ -n "$NAME" ] || usage
shift || true

LAB=1; WITH_LANG=0; WITH_NARR=0
for arg in "$@"; do
  case "$arg" in
    --no-lab) LAB=0 ;;
    --with-language) WITH_LANG=1 ;;
    --with-narrative) WITH_NARR=1 ;;
    *) echo "unknown flag: $arg"; usage ;;
  esac
done

# name must be lowercase letters, digits, hyphens (matches skills/<name> convention)
[[ "$NAME" =~ ^[a-z0-9-]+$ ]] || { echo "ERROR: name must be lowercase letters, digits, and hyphens only"; exit 1; }

DEST="skills/$NAME"
[ -e "$DEST" ] && { echo "ERROR: $DEST already exists"; exit 1; }
TMPL="templates/coach"
[ -d "$TMPL" ] || { echo "ERROR: template dir $TMPL not found"; exit 1; }

# __COACH_TITLE__ : title-case the hyphen-separated name (k8s-coach -> "K8s Coach")
TITLE="$(echo "$NAME" | tr '-' ' ' | awk '{ for (i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2) } 1')"

# stamp copies a .tmpl to its destination minus the suffix, substituting the tokens
stamp() {
  local src="$1" dst="$2"
  sed -e "s/__COACH_NAME__/$NAME/g" -e "s/__COACH_TITLE__/$TITLE/g" "$src" > "$dst"
}

mkdir -p "$DEST/references"

stamp "$TMPL/SKILL.md.tmpl" "$DEST/SKILL.md"

# required hooks (always stamped)
for hook in north-star curriculum teaching-elements scorecard-dims phase-gates portfolio; do
  stamp "$TMPL/references/$hook.md.tmpl" "$DEST/references/$hook.md"
done

# lab-manager: stamped unless --no-lab; when omitted, drop its Hook Map row from SKILL.md
if [ "$LAB" -eq 1 ]; then
  stamp "$TMPL/references/lab-manager.md.tmpl" "$DEST/references/lab-manager.md"
else
  grep -v '| lab-manager |' "$DEST/SKILL.md" > "$DEST/SKILL.md.tmp" && mv "$DEST/SKILL.md.tmp" "$DEST/SKILL.md"
fi

# optional hooks (stamped only behind flags; absence is valid per engine defaults)
[ "$WITH_LANG" -eq 1 ] && stamp "$TMPL/references/language.md.tmpl" "$DEST/references/language.md"
[ "$WITH_NARR" -eq 1 ] && stamp "$TMPL/references/narrative.md.tmpl" "$DEST/references/narrative.md"

echo "Scaffolded $DEST"
echo "Next:"
echo "  1. Fill every <!-- TODO: ... --> marker in $DEST and $DEST/references/"
echo "  2. Run ./scripts/lint-coach.sh $NAME  (it will FAIL until all TODOs are filled)"
