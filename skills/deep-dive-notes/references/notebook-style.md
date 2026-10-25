# Notebook style

Apply this token set and these devices in place of artifact-design's free choice.

- Font: LXGW WenKai TC (Google Fonts) for body and headings, IBM Plex Mono for code/labels, fallback Noto Sans TC.
- Ground: cool graph paper (#F6F8FA with 22px grid lines rgba(90,130,170,.16)), dark mode = chalkboard green #1A2320.
- Ink #23313E. Semantic colors as highlighters: who yellow #FFE98A, see cyan #BDEEF6, may pink #F9CDE0, via `mark` with a half-height gradient.
- Figures sit on "taped" white cards (tape strip on top). Mistakes get a red left-border "我錯在這" line.
- 2×2 / scenario tables become comic panels: one mini SVG per case showing where the process stops.

## Course accent

One `--accent` per coach so a page shows which course it belongs to at a glance. Use it for the header band, layer badges, tape strips, progress bar, and links. Body text stays ink; the highlighter colors above stay the same in every course.

| Coach | Light | Dark |
|---|---|---|
| k8s | #326CE5 blue | #74A0F0 |
| sd | #0B7285 teal | #3BC9DB |
| leetcode | #2B8A3E green | #69DB7C |
| terraform | #7048E8 violet | #B197FC |
| ca | #D9480F AWS orange | #FFA94D |
| general | #495057 graphite | #ADB5BD |

Set it on `:root` and in both dark-mode blocks.
