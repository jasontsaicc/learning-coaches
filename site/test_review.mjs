import test from "node:test";
import assert from "node:assert/strict";
import { gradeCard, loadSrs, saveSrs, advanceQueue } from "./review.js";
test("old boxes retain schedule and missed cards retry only once", () => {
  const st = { x: { box: 2, due: 10 } };
  gradeCard(st, "x", 2, 100);
  assert.deepEqual(st.x, { box: 3, due: 107 });
  gradeCard(st, "x", 0, 100);
  assert.deepEqual(st.x, { box: 1, due: 101 });
  let queue = [{ id: "x" }],
    retried = new Set();
  advanceQueue(queue, 0, retried);
  assert.equal(queue.length, 1);
  advanceQueue(queue, 0, retried);
  assert.equal(queue.length, 0);
});
test("malformed legacy storage is not overwritten", () => {
  let raw = "[]";
  const storage = { getItem: () => raw, setItem: (k, v) => (raw = v) };
  assert.ok(loadSrs(storage).error);
  assert.equal(saveSrs(storage, {}).ok, false);
  assert.equal(raw, "[]");
});
