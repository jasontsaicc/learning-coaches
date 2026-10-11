const KEY = "learning-map.practice.v1";
const object = (x) => !!x && typeof x === "object" && !Array.isArray(x);
export const attemptKey = (q) => `${q.id}@${q.revision}`;
export function gradeQuestion(q, a) {
  let correct = false,
    details = [];
  if (q.type === "choice") {
    correct =
      Array.isArray(a) &&
      a.length === new Set(a).size &&
      a.length === q.answer.length &&
      q.answer.every((id) => a.includes(id));
    details = q.options.map((x) => ({
      id: x.id,
      correct:
        q.answer.includes(x.id) === (Array.isArray(a) && a.includes(x.id)),
    }));
  } else if (q.type === "fill") {
    const text = String(a ?? "").trim();
    if (q.answer.kind === "number")
      correct =
        text !== "" &&
        Number.isFinite(Number(text)) &&
        Math.abs(Number(text) - q.answer.value) <= q.answer.tolerance;
    else
      correct = q.answer.accepted.some((x) =>
        q.answer.caseSensitive
          ? x.trim() === text
          : x.trim().toLowerCase() === text.toLowerCase(),
      );
  } else if (q.type === "order") {
    correct =
      Array.isArray(a) &&
      q.answer.some(
        (order) =>
          a.length === order.length && order.every((id, i) => a[i] === id),
      );
  } else if (q.type === "match") {
    details = Object.entries(q.answer).map(([id, target]) => ({
      id,
      correct: object(a) && a[id] === target,
    }));
    correct =
      object(a) &&
      Object.keys(a).length === details.length &&
      details.every((x) => x.correct);
  }
  return { correct, details };
}
export const makeRound = (chapter) =>
  chapter.questions
    .filter((q) => !q.variantOf)
    .slice(0, 6)
    .map((q) => q.id);
export function recordAttempt(
  state,
  q,
  answer,
  { hintUsed = false, confidence = "unsure", skipped = false } = {},
) {
  const result = {
    answer: structuredClone(answer),
    hintUsed,
    confidence,
    skipped,
    correct: !skipped && gradeQuestion(q, answer).correct,
    time: Date.now(),
  };
  const key = attemptKey(q),
    old = state.attempts?.[key];
  return {
    ...state,
    attempts: {
      ...state.attempts,
      [key]: {
        firstAttempt: old?.firstAttempt ?? result,
        latestAttempt: result,
      },
    },
  };
}
function validState(st) {
  const attempt = (a) =>
    object(a) &&
    typeof a.correct === "boolean" &&
    typeof a.hintUsed === "boolean" &&
    typeof a.skipped === "boolean" &&
    ["sure", "unsure"].includes(a.confidence) &&
    Number.isFinite(a.time) &&
    Object.hasOwn(a, "answer");
  return (
    object(st) &&
    st.version === 1 &&
    object(st.chapters) &&
    Object.values(st.chapters).every(
      (c) =>
        object(c) &&
        Array.isArray(c.queue) &&
        c.queue.every((x) => typeof x === "string") &&
        Number.isInteger(c.index) &&
        c.index >= 0 &&
        c.index <= c.queue.length &&
        object(c.attempts) &&
        Object.values(c.attempts).every(
          (a) =>
            object(a) && attempt(a.firstAttempt) && attempt(a.latestAttempt),
        ) &&
        (c.draft === undefined ||
          (object(c.draft) &&
            typeof c.draft.id === "string" &&
            typeof c.draft.hintUsed === "boolean" &&
            ["sure", "unsure"].includes(c.draft.confidence) &&
            (typeof c.draft.answer === "string" ||
              (Array.isArray(c.draft.answer) &&
                c.draft.answer.every((x) => typeof x === "string")) ||
              (object(c.draft.answer) &&
                Object.values(c.draft.answer).every(
                  (x) => typeof x === "string",
                ))))),
    )
  );
}
export function loadPractice(storage) {
  try {
    const raw = storage.getItem(KEY);
    if (raw === null)
      return { state: { version: 1, chapters: {} }, error: null };
    const state = JSON.parse(raw);
    if (!validState(state)) throw Error("invalid state");
    return { state, error: null };
  } catch {
    return {
      state: { version: 1, chapters: {} },
      error: "無法讀取練習紀錄；原紀錄未覆寫，本次可暫時練習。",
    };
  }
}
export function savePractice(storage, state) {
  try {
    if (loadPractice(storage).error || !validState(state))
      throw Error("invalid state");
    storage.setItem(KEY, JSON.stringify(state));
    return { ok: true, error: null };
  } catch {
    return { ok: false, error: "練習紀錄未保存；請保持此頁開啟。" };
  }
}
export function weakQuestions(chapter, state) {
  return chapter.questions.filter(
    (q) =>
      !q.variantOf &&
      (() => {
        const a = state?.attempts?.[attemptKey(q)]?.latestAttempt;
        if (!a) return false;
        const related = chapter.questions
          .filter((v) => v.variantOf === q.id)
          .map((v) => state?.attempts?.[attemptKey(v)]?.latestAttempt)
          .filter((v) => v && v.time >= a.time);
        const latest = [a, ...related].sort((x, y) => y.time - x.time)[0];
        return (
          !latest.correct || latest.hintUsed || latest.confidence !== "sure"
        );
      })(),
  );
}

const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const TYPE = {
  choice: "選擇題",
  fill: "填空題",
  order: "排序題",
  match: "配對與分類",
};
export function mountPractice(container, chapter, { state, onSave, onExit }) {
  let st = state ?? { queue: makeRound(chapter), index: 0, attempts: {} };
  const byId = new Map(chapter.questions.map((q) => [q.id, q]));
  const primary = chapter.questions.filter((q) => !q.variantOf);
  let notice =
    primary.length < 5 ||
    new Set(primary.map((q) => q.type)).size < 3 ||
    new Set(primary.map((q) => q.objectiveId)).size < 2
      ? "本章目前提供試練，題庫尚未完整覆蓋章節目標。"
      : "";
  if (st.queue.some((id) => !byId.has(id))) {
    st = { ...st, queue: makeRound(chapter), index: 0, draft: undefined };
    notice = "題庫已更新，已重新開始本章；舊作答證據仍保留。";
  }
  let feedback = false;
  const persist = () => {
    const r = onSave(st);
    if (r?.error) notice = r.error;
    const status = container.querySelector("#save-status");
    if (status) status.textContent = notice;
  };
  function summary() {
    const primary = chapter.questions.filter((q) => !q.variantOf);
    const evidence = primary.map(
      (q) => st.attempts[attemptKey(q)]?.firstAttempt,
    );
    const independent = evidence.filter(
      (a) => a?.correct && !a.hintUsed,
    ).length;
    const hinted = evidence.filter((a) => a?.correct && a.hintUsed).length;
    const unresolved = evidence.filter(
      (a) => a && !a.correct && !a.skipped,
    ).length;
    const skipped = primary.length - independent - hinted - unresolved;
    const weak = weakQuestions(chapter, st);
    container.innerHTML = `<div class="practice-top"><span class="eyebrow">CHAPTER REVIEW</span><button class="text-btn" id="exit">返回課程 ↗</button></div>
      <h1>每一步，都更清楚一點。</h1><p class="lead">${esc(chapter.title)} · 本輪完成。以下保留首次作答的證據。</p>
      ${notice ? `<p role="alert" class="notice">${esc(notice)}</p>` : ""}
      <div class="result-grid">${[
        [independent, "首次無提示答對"],
        [hinted, "首次提示後答對"],
        [unresolved, "首次答錯"],
        [skipped, "略過／尚未作答"],
      ]
        .map(([n, t]) => `<div><strong>${n}</strong><span>${t}</span></div>`)
        .join("")}</div>
      <h2>回到學習目標</h2><div class="objective-list">${chapter.objectives
        .map((o) => {
          const qs = primary.filter((q) => q.objectiveId === o.id),
            first = qs.filter((q) => {
              const a = st.attempts[attemptKey(q)]?.firstAttempt;
              return a?.correct && !a.hintUsed;
            }).length;
          return `<div><span>${esc(o.label)}</span><span>${first}/${qs.length} 首次無提示</span></div>`;
        })
        .join("")}</div>
      <p class="muted">目前 ${weak.length} 個主題目需要再練。重做答對不會改寫首次結果。</p>
      <div class="actions">${weak.length ? '<button class="btn primary" id="retry">練習弱項變式 →</button>' : ""}<button class="btn" id="again">再練本章</button></div>
      <section class="challenge"><span class="eyebrow">把理解帶到實作</span><h2>下一步，親手驗證</h2><p>${esc(chapter.challenge.prompt)}</p><ul>${chapter.challenge.criteria.map((x) => `<li>${esc(x)}</li>`).join("")}</ul><span class="badge">待實作／教練驗證</span></section>`;
    container.querySelector("#exit").onclick = onExit;
    container.querySelector("#again").onclick = () => {
      st = { ...st, queue: makeRound(chapter), index: 0, draft: undefined };
      persist();
      render();
    };
    container.querySelector("#retry")?.addEventListener("click", () => {
      let fallback = false;
      st = {
        ...st,
        queue: weak.map((q) => {
          const v = chapter.questions.find((x) => x.variantOf === q.id);
          if (!v) fallback = true;
          return v?.id ?? q.id;
        }),
        index: 0,
        draft: undefined,
      };
      notice = fallback
        ? "部分題目尚無變式，將重做原題；原題重做不代表已能遷移應用。"
        : "這次改變情境，檢查是否能轉用原理。";
      persist();
      render();
    });
  }
  function render() {
    if (!chapter.questions.length) {
      container.innerHTML = `<h1>${esc(chapter.title)}</h1><p>本章練習尚未建立。</p><button class="btn" id="exit">返回課程</button>`;
      container.querySelector("#exit").onclick = onExit;
      return;
    }
    if (st.index >= st.queue.length) {
      summary();
      return;
    }
    const q = byId.get(st.queue[st.index]);
    const draft =
      st.draft?.id === attemptKey(q) &&
      (q.type === "fill"
        ? typeof st.draft.answer === "string"
        : q.type === "match"
          ? object(st.draft.answer)
          : Array.isArray(st.draft.answer) &&
            st.draft.answer.every((id) =>
              (q.options ?? q.items).some((x) => x.id === id),
            ) &&
            (q.type !== "order" ||
              new Set(st.draft.answer).size === q.items.length))
        ? st.draft
        : {
            id: attemptKey(q),
            answer:
              q.type === "order"
                ? [...q.items].reverse().map((x) => x.id)
                : q.type === "match"
                  ? {}
                  : q.type === "choice"
                    ? []
                    : "",
            hintUsed: false,
            confidence: "unsure",
          };
    st = { ...st, draft };
    const old = st.attempts[attemptKey(q)];
    let controls = "";
    if (q.type === "choice")
      controls = `<fieldset><legend>${q.multiple ? "選出所有符合的答案" : "選出一個答案"}</legend>${q.options.map((o) => `<label class="option"><input type="${q.multiple ? "checkbox" : "radio"}" name="answer" value="${o.id}" ${draft.answer.includes(o.id) ? "checked" : ""}><span>${esc(o.text)}</span></label>`).join("")}</fieldset>`;
    if (q.type === "fill")
      controls = `<label class="fill-label">你的答案 <input id="fill" autocomplete="off" ${q.answer.kind === "number" ? 'inputmode="decimal"' : ""} value="${esc(draft.answer)}" placeholder="在這裡輸入…">${esc(q.answer.unit ?? "")}</label>`;
    if (q.type === "order")
      controls = `<p class="muted">用上下按鈕調整順序。</p><ol class="order-list">${draft.answer.map((id, i) => `<li><span>${esc(q.items.find((x) => x.id === id).text)}</span><button type="button" data-move="${i}" data-step="-1" aria-label="第 ${i + 1} 項向上" ${i === 0 ? "disabled" : ""}>↑</button><button type="button" data-move="${i}" data-step="1" aria-label="第 ${i + 1} 項向下" ${i === draft.answer.length - 1 ? "disabled" : ""}>↓</button></li>`).join("")}</ol>`;
    if (q.type === "match")
      controls = `<div class="match-list">${q.items.map((i) => `<label><span>${esc(i.text)}</span><select data-match="${i.id}"><option value="">選擇對應項目</option>${q.targets.map((t) => `<option value="${t.id}" ${draft.answer[i.id] === t.id ? "selected" : ""}>${esc(t.text)}</option>`).join("")}</select></label>`).join("")}</div>`;
    container.innerHTML = `<div class="practice-top"><a class="text-btn" href="#/c/${esc(chapter.coachId)}">← ${esc(chapter.title)}</a><span>${st.index + 1} / ${st.queue.length}</span></div>
      <progress value="${st.index}" max="${st.queue.length}" aria-label="本輪進度"></progress>
      ${notice ? `<p role="alert" class="notice">${esc(notice)}</p>` : ""}
      <div class="question-card"><span class="eyebrow">${TYPE[q.type]}${q.variantOf ? " · 變式挑戰" : ""}</span><h1 tabindex="-1" id="question-title">${esc(q.prompt)}</h1>
      <p class="objective">本題目標 · ${esc(chapter.objectives.find((o) => o.id === q.objectiveId).label)}</p>
      ${old ? '<p class="muted">你已練過這一題；這次結果不會改寫首次紀錄。</p>' : ""}
      <form id="answer-form">${controls}<label class="confidence">作答信心 <select id="confidence"><option value="unsure">不確定，想驗證看看</option><option value="sure" ${draft.confidence === "sure" ? "selected" : ""}>確定，能說明原因</option></select></label>
      <div class="actions"><button class="btn primary" type="submit" id="submit">檢查答案 →</button><button class="text-btn" type="button" id="hint">${draft.hintUsed ? "提示已使用" : "給我一點提示"}</button><button class="text-btn" type="button" id="skip">先略過</button></div></form>
      <p id="save-status" class="muted" role="status">${esc(notice)}</p><div id="hint-text">${draft.hintUsed ? `<p class="hint">${esc(q.hint)}</p>` : ""}</div><div id="feedback" aria-live="polite"></div></div>`;
    feedback = false;
    const form = container.querySelector("form");
    const complete = () =>
      q.type === "choice"
        ? draft.answer.length > 0
        : q.type === "fill"
          ? String(draft.answer).trim() !== ""
          : q.type === "match"
            ? q.items.every((i) => draft.answer[i.id])
            : true;
    const update = () => {
      container.querySelector("#submit").disabled = !complete();
      persist();
    };
    form.addEventListener("change", (e) => {
      if (e.target.name === "answer")
        draft.answer = [...form.querySelectorAll("[name=answer]:checked")].map(
          (x) => x.value,
        );
      if (e.target.dataset.match)
        draft.answer = {
          ...draft.answer,
          [e.target.dataset.match]: e.target.value,
        };
      if (e.target.id === "confidence") draft.confidence = e.target.value;
      update();
    });
    form.querySelector("#fill")?.addEventListener("input", (e) => {
      draft.answer = e.target.value;
      update();
    });
    form.querySelectorAll("[data-move]").forEach(
      (b) =>
        (b.onclick = () => {
          const i = +b.dataset.move,
            j = i + +b.dataset.step;
          [draft.answer[i], draft.answer[j]] = [
            draft.answer[j],
            draft.answer[i],
          ];
          persist();
          render();
          container
            .querySelector(`[data-move="${j}"][data-step="${b.dataset.step}"]`)
            ?.focus();
        }),
    );
    container.querySelector("#hint").onclick = () => {
      draft.hintUsed = true;
      persist();
      container.querySelector("#hint-text").innerHTML =
        `<p class="hint">${esc(q.hint)}</p>`;
      container.querySelector("#hint").textContent = "提示已使用";
    };
    function submit(skipped = false) {
      if (feedback || (!skipped && !complete())) return;
      feedback = true;
      st = recordAttempt(st, q, skipped ? null : draft.answer, {
        ...draft,
        skipped,
      });
      st.draft.submitted = true;
      persist();
      showFeedback();
    }
    function showFeedback() {
      feedback = true;
      form
        .querySelectorAll("input,select,button")
        .forEach((x) => (x.disabled = true));
      const a = st.attempts[attemptKey(q)].latestAttempt;
      const answer =
        q.type === "choice"
          ? q.options
              .filter((o) => q.answer.includes(o.id))
              .map((o) => o.text)
              .join("；")
          : q.type === "fill"
            ? q.answer.kind === "number"
              ? q.answer.value
              : q.answer.accepted.join(" / ")
            : q.type === "order"
              ? q.answer[0]
                  .map((id) => q.items.find((i) => i.id === id).text)
                  .join(" → ")
              : q.items
                  .map(
                    (i) =>
                      `${i.text} → ${q.targets.find((t) => t.id === q.answer[i.id]).text}`,
                  )
                  .join("；");
      const explanations =
        q.type === "choice"
          ? q.options
              .map(
                (o) =>
                  `<li><strong>${esc(o.text)}</strong>：${esc(o.feedback)}</li>`,
              )
              .join("")
          : q.type === "match"
            ? q.items
                .map((i) => `<li>${esc(i.text)}：${esc(i.feedback)}</li>`)
                .join("")
            : "";
      container.querySelector("#feedback").innerHTML =
        `<section class="feedback ${a.correct ? "correct" : "rethink"}"><h2 tabindex="-1">${a.skipped ? "先記下這個觀念" : a.correct ? (a.hintUsed ? "提示後答對" : old ? "練習後答對" : "答對了") : "再想清楚這一步"}</h2><p><strong>參考答案：</strong>${esc(answer)}</p><p>${esc(q.explanation)}</p>${explanations ? `<ul>${explanations}</ul>` : ""}${q.source.path.endsWith(".md") ? `<a href="#/read/${encodeURIComponent(q.source.path)}">` : `<a href="files/${encodeURI(q.source.path)}" target="_blank" rel="noopener">`}回到教材 · ${esc(q.source.section)} ↗</a>${notice ? `<p role="alert">${esc(notice)}</p>` : ""}<p><button class="btn primary" id="next">${st.index + 1 === st.queue.length ? "看看本輪結果" : "下一題 →"}</button></p></section>`;
      container.querySelector("#feedback h2").focus();
      container.querySelector("#next").onclick = () => {
        st = { ...st, index: st.index + 1, draft: undefined };
        persist();
        render();
        container.querySelector("h1")?.focus();
      };
    }
    form.onsubmit = (e) => {
      e.preventDefault();
      submit();
    };
    container.querySelector("#skip").onclick = () => submit(true);
    container.querySelector("#submit").disabled = !complete();
    if (draft.submitted && old) showFeedback();
  }
  render();
  return () => {
    container.replaceChildren();
  };
}
