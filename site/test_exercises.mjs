import test from "node:test";
import assert from "node:assert/strict";
import {
  gradeQuestion,
  makeRound,
  recordAttempt,
  loadPractice,
  savePractice,
} from "./exercises.js";
const choice = {
  id: "q",
  revision: 1,
  type: "choice",
  multiple: true,
  options: [{ id: "a" }, { id: "b" }, { id: "c" }],
  answer: ["a", "b"],
};
test("multi-choice requires exact set, not partial or repeated choices", () => {
  assert.equal(gradeQuestion(choice, ["b", "a"]).correct, true);
  for (const a of [["a"], ["a", "b", "c"], ["a", "a", "b"]])
    assert.equal(gradeQuestion(choice, a).correct, false);
});
test("fill normalizes only declared rules, empty is not numeric zero", () => {
  const q = {
    type: "fill",
    answer: { kind: "text", accepted: ["None"], caseSensitive: true },
  };
  assert.equal(gradeQuestion(q, " None ").correct, true);
  assert.equal(gradeQuestion(q, "none").correct, false);
  q.answer.caseSensitive = false;
  assert.equal(gradeQuestion(q, "NONE").correct, true);
  q.answer = { kind: "number", value: 0, tolerance: 0.1 };
  assert.equal(gradeQuestion(q, "").correct, false);
  assert.equal(gradeQuestion(q, "0.1").correct, true);
  assert.equal(gradeQuestion(q, "0.11").correct, false);
});
test("orders accept declared alternatives, matching supports classification", () => {
  const q = {
    type: "order",
    items: [{ id: "a" }, { id: "b" }, { id: "c" }],
    answer: [
      ["a", "b", "c"],
      ["b", "a", "c"],
    ],
  };
  assert.equal(gradeQuestion(q, ["b", "a", "c"]).correct, true);
  assert.equal(gradeQuestion(q, ["a", "a", "c"]).correct, false);
  const m = { type: "match", answer: { a: "x", b: "x" } };
  assert.equal(gradeQuestion(m, { a: "x", b: "x" }).correct, true);
  assert.equal(gradeQuestion(m, { a: "x" }).correct, false);
});
test("attempt keeps first evidence and separates revisions and hints", () => {
  let st = recordAttempt({ attempts: {} }, choice, ["a"], {
    hintUsed: false,
    confidence: "unsure",
  });
  st = recordAttempt(st, choice, ["a", "b"], {
    hintUsed: true,
    confidence: "sure",
  });
  assert.equal(st.attempts["q@1"].firstAttempt.correct, false);
  assert.equal(st.attempts["q@1"].latestAttempt.correct, true);
  assert.equal(st.attempts["q@1"].latestAttempt.hintUsed, true);
  st = recordAttempt(st, { ...choice, revision: 2 }, ["a", "b"], {
    hintUsed: false,
    confidence: "sure",
  });
  assert.equal(st.attempts["q@2"].firstAttempt.correct, true);
  assert.equal(st.attempts["q@1"].firstAttempt.correct, false);
});
test("round excludes variants and storage failure never overwrites corrupt state", () => {
  assert.deepEqual(
    makeRound({ questions: [{ id: "a" }, { id: "b", variantOf: "a" }] }),
    ["a"],
  );
  for (const raw of [
    "null",
    "[]",
    '{"version":1,"chapters":[]}',
    '{"version":1,"chapters":{"a":{}}}',
  ]) {
    let value = raw;
    const storage = {
      getItem: () => value,
      setItem: (k, v) => {
        value = v;
      },
    };
    assert.ok(loadPractice(storage).error);
    assert.equal(savePractice(storage, { version: 1, chapters: {} }).ok, false);
    assert.equal(value, raw);
  }
  const blocked = {
    getItem() {
      throw Error("blocked");
    },
    setItem() {
      throw Error("quota");
    },
  };
  assert.ok(loadPractice(blocked).error);
  assert.equal(savePractice(blocked, { version: 1, chapters: {} }).ok, false);
});

test("corrupt draft cannot reach an interactive question", () => {
  const raw = JSON.stringify({
    version: 1,
    chapters: {
      a: {
        queue: ["q"],
        index: 0,
        attempts: {},
        draft: { id: "q@1", hintUsed: false, answer: null },
      },
    },
  });
  assert.ok(loadPractice({ getItem: () => raw }).error);
});

test("successful newer variant resolves a weak item without rewriting first evidence", async () => {
  const { weakQuestions } = await import("./exercises.js");
  const original = { ...choice, id: "original" },
    variant = { ...choice, id: "variant", variantOf: "original" };
  const c = { questions: [original, variant] };
  let state = recordAttempt({ attempts: {} }, original, ["a"], {
    confidence: "sure",
  });
  state = recordAttempt(state, variant, ["a", "b"], { confidence: "sure" });
  state.attempts["variant@1"].latestAttempt.time =
    state.attempts["original@1"].latestAttempt.time + 1;
  assert.equal(weakQuestions(c, state).length, 0);
  assert.equal(state.attempts["original@1"].firstAttempt.correct, false);
  assert.equal(
    weakQuestions(
      { ...c, questions: [original, { ...variant, revision: 2 }] },
      state,
    ).length,
    1,
  );
});

test("order evidence snapshots the answer instead of retaining the draft array", () => {
  const q = {
    id: "order",
    revision: 1,
    type: "order",
    items: [{ id: "a" }, { id: "b" }],
    answer: [["a", "b"]],
  };
  const draft = ["b", "a"];
  const st = recordAttempt({ attempts: {} }, q, draft, {});
  draft.reverse();
  assert.deepEqual(st.attempts["order@1"].firstAttempt.answer, ["b", "a"]);
});
