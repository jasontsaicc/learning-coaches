import test from "node:test";
import assert from "node:assert/strict";
import { searchContent, resolveRecent, noteList } from "./app.js";
const data = {
  nodes: [
    { id: "me", kind: "root" },
    { id: "k8s", kind: "coach", parent: "me", files: ["a.md"] },
    { id: "p", kind: "phase", parent: "k8s", files: ["a.md"] },
    {
      id: "t",
      kind: "topic",
      label: "Readiness",
      parent: "p",
      files: ["a.md"],
    },
  ],
  titles: { "a.md": "Probe note" },
};
test("search trims and folds case, deduplicates shared files", () => {
  assert.equal(searchContent(data, "  READINESS ").length, 1);
  assert.equal(searchContent(data, "probe", true).length, 1);
  assert.equal(searchContent(data, "").length, 0);
});
test("recent topic requires unambiguous stable parent and label", () => {
  assert.equal(
    resolveRecent(data, { coachId: "k8s", parent: "p", label: "Readiness" }).id,
    "t",
  );
  assert.equal(resolveRecent(data, { path: "missing.md" }), null);
  assert.equal(
    resolveRecent(
      {
        ...data,
        nodes: [
          ...data.nodes,
          { id: "t2", kind: "topic", label: "Readiness", parent: "p" },
        ],
      },
      { coachId: "k8s", parent: "p", label: "Readiness" },
    ),
    null,
  );
});

test("lesson labels separate activity, materials, plans and assessment", async () => {
  const { level } = await import("./app.js");
  assert.equal(level({ status: "in-progress" }), "進行中 · 尚未評量");
  assert.equal(
    level({ status: "in-progress", level: "med" }),
    "進行中 · 教練評量 med",
  );
  assert.equal(
    level({ planned: true, status: "materials-available" }),
    "已有教材 · 尚未評量",
  );
  assert.equal(level({ planned: true }), "課綱待學");
  assert.equal(level({ status: "practice-recorded" }), "已練習 · 尚無章節評級");
  assert.equal(level({ level: "high" }), "教練評量 · high");
});


test("search defaults to HTML while Markdown remains opt-in", () => {
  const mixed = { ...data, nodes: [...data.nodes,
    { id: "html", kind: "topic", parent: "p", label: "Diagram", files: ["probe.html", "a.md"] }],
    titles: { ...data.titles, "probe.html": "Probe diagram" } };
  assert.deepEqual(searchContent(mixed, "probe").map((x) => x.path), ["probe.html"]);
  assert.equal(searchContent(mixed, "probe", true).length, 2);
});

test("notes are compact links, HTML first, without disclosure panels", () => {
  const rendered = noteList(["a.md", "b.html", "a.md"], (f) => `<a>${f}</a>`);
  assert.ok(rendered.indexOf("b.html") < rendered.indexOf("a.md"));
  assert.equal((rendered.match(/a.md/g) ?? []).length, 1);
  assert.ok(!rendered.includes("<details"));
  assert.ok(!rendered.includes("Markdown 補充資料"));
  assert.ok(noteList(["a.md"], String).includes("a.md"));
});

test('learning paths separate disclosure, note links and missing material', async () => {
  const { learningPath } = await import('./app.js');
  const d = { paths: { k8s: [{ id: 'p', label: 'P3', nodes: [{ id: 'n', label: '<HPA>', source: 'C-3', material: '部分教材', chunks: [{ id: 'c', label: '公式', note: 'portfolio/k8s/notes/hpa.html' }, { id: 'missing', label: 'Lab' }] }] }] }, pathCurrent: { k8s: 'n' } };
  const html = learningPath(d, 'k8s');
  assert.match(html, /aria-expanded="true"/);
  assert.match(html, /aria-controls="n-chunks"/);
  assert.match(html, /&lt;HPA&gt;/);
  assert.match(html, /href="files\/portfolio\/k8s\/notes\/hpa.html"/);
  assert.match(html, /待補 HTML/);
  assert.doesNotMatch(html, /<a[^>]*>Lab/);
  assert.match(learningPath(d, 'k8s', new Map([['n', false]])), /id="n-chunks" hidden/);
  assert.equal(learningPath(d, 'sd'), '');
});
