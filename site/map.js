export function drawTree(box, nodesData, rootId, { onSelect, selected } = {}) {
  const byId = new Map(nodesData.map((n) => [n.id, n]));
  const childrenOf = (id) => nodesData.filter((n) => n.parent === id);
  const isLeaf = (n) => n.kind === "topic" || n.kind === "problem";
  const lvl = (n) =>
    n.planned
      ? "plan"
      : n.level?.startsWith("high")
        ? "high"
        : n.level?.startsWith("med")
          ? "med"
          : n.level?.startsWith("low")
            ? "low"
            : "none";
  if (!globalThis.d3) {
    box.textContent = "地圖暫時無法載入，仍可從課程章節繼續閱讀。";
    return;
  }
  const nodes = [byId.get(rootId)];
  (function walk(id) {
    for (const k of childrenOf(id)) {
      nodes.push(k);
      walk(k.id);
    }
  })(rootId);
  const root = d3
    .stratify()
    .id((n) => n.id)
    .parentId((n) => (n.id === rootId ? null : n.parent))(nodes);
  d3.tree().nodeSize([50, 230])(root);
  box.innerHTML = '<div class="stage"><svg></svg></div>';
  const stage = box.firstChild;
  d3.select(stage.firstChild)
    .selectAll("path")
    .data(root.links())
    .join("path")
    .attr(
      "d",
      d3
        .linkHorizontal()
        .source((l) => [l.source.y + 84, l.source.x])
        .target((l) => [l.target.y - 84, l.target.x]),
    );
  for (const d of root.descendants()) {
    const el = document.createElement(onSelect ? "button" : "div");
    el.className = `tn d${Math.min(d.depth, 2)} ${isLeaf(d.data) ? lvl(d.data) : ""} ${d.id === selected ? "sel" : ""}`;
    el.style.left = d.y + "px";
    el.style.top = d.x + "px";
    el.textContent = d.data.label;
    el.title = d.data.label;
    if (onSelect)
      el.onclick = (e) => {
        e.stopPropagation();
        onSelect(d.data);
      };
    stage.appendChild(el);
  }
  const ns = root.descendants(),
    [x0, x1] = d3.extent(ns, (d) => d.y),
    [y0, y1] = d3.extent(ns, (d) => d.x);
  const k = Math.min(
    1,
    box.clientWidth / (x1 - x0 + 220),
    box.clientHeight / (y1 - y0 + 80),
  );
  const t = d3.zoomIdentity
    .translate(
      (box.clientWidth - (x1 - x0) * k) / 2 - x0 * k,
      (box.clientHeight - (y1 + y0) * k) / 2,
    )
    .scale(k);
  const apply = (t) => {
    stage.style.transform = `translate(${t.x}px,${t.y}px) scale(${t.k})`;
  };
  if (onSelect) {
    const z = d3
      .zoom()
      .scaleExtent([0.2, 2])
      .on("zoom", (e) => apply(e.transform));
    d3.select(box).call(z).call(z.transform, t);
  } else apply(t);
}
