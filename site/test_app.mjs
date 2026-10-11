import test from "node:test";
import assert from "node:assert/strict";
import { searchContent, resolveRecent } from "./app.js";
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
  assert.equal(searchContent(data, "probe").length, 1);
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
