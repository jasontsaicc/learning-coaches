const DAYS = [0, 1, 3, 7, 14, 30];
export const today = () => Math.floor(Date.now() / 864e5);
export const deckOf = (c) =>
  (c.keypoints || []).flatMap((t) =>
    t.rows.map((r) => ({
      id: `${c.id}|${t.title}|${r[0]}`,
      q: r[0],
      prompt: t.prompt,
      a: r.slice(1).filter(Boolean),
    })),
  );
export const dueOf = (deck, st) =>
  deck.filter((x) => (st[x.id]?.due ?? 0) <= today());
export function gradeCard(st, id, g, day = today()) {
  const box = st[id]?.box ?? 0,
    next =
      g === 0
        ? 1
        : g === 1
          ? Math.max(box, 1)
          : Math.min(box + 1, DAYS.length - 1);
  st[id] = { box: next, due: day + DAYS[next] };
}
export function advanceQueue(queue, grade, retried) {
  const x = queue.shift();
  if (grade === 0 && !retried.has(x.id)) {
    retried.add(x.id);
    queue.push(x);
  }
}
export function loadSrs(storage) {
  try {
    const st = JSON.parse(storage.getItem("srs") ?? "{}");
    if (
      !st ||
      Array.isArray(st) ||
      typeof st !== "object" ||
      !Object.values(st).every(
        (v) =>
          v &&
          Number.isInteger(v.box) &&
          v.box >= 0 &&
          v.box < 6 &&
          Number.isFinite(v.due),
      )
    )
      throw Error();
    return { state: st, error: null };
  } catch {
    return { state: {}, error: "舊複習紀錄無法讀取，原資料未覆寫。" };
  }
}
export function saveSrs(storage, st) {
  try {
    if (loadSrs(storage).error) throw Error();
    storage.setItem("srs", JSON.stringify(st));
    return { ok: true };
  } catch {
    return { ok: false, error: "卡片紀錄未保存，請保持此頁開啟。" };
  }
}
export function openCards(container, c, storage, esc) {
  const loaded = loadSrs(storage),
    st = loaded.state,
    deck = deckOf(c),
    queue = dueOf(deck, st).slice(0, 20),
    total = queue.length,
    retried = new Set();
  let notice = loaded.error || "",
    done = 0;
  function show(flipped = false) {
    const x = queue[0];
    if (!x) {
      container.innerHTML = `<h2>本輪完成</h2><p>已練習 ${total} 張；目前仍有 ${dueOf(deck, st).length} 張到期。</p><p class="muted">卡片是輔助記憶，自評不改變教練評量。複習日以 UTC 更新。</p>${notice ? `<p role="alert">${esc(notice)}</p>` : ""}`;
      return;
    }
    container.innerHTML = `<p class="eyebrow">記憶複習 · ${Math.min(done, total)}/${total}</p><h2>${esc(x.q)}</h2><p>${esc(x.prompt)}</p>${flipped ? `<div class="point">${x.a.map((a) => `<p>${esc(a)}</p>`).join("")}</div>` : ""}<div class="actions">${flipped ? '<button class="btn" data-grade="0">不會</button><button class="btn" data-grade="1">模糊</button><button class="btn primary" data-grade="2">會了</button>' : '<button class="btn primary" id="flip">先說一遍，再看答案</button>'}</div>${notice ? `<p role="alert">${esc(notice)}</p>` : ""}`;
    container
      .querySelector("#flip")
      ?.addEventListener("click", () => show(true));
    container.querySelectorAll("[data-grade]").forEach(
      (b) =>
        (b.onclick = () => {
          const g = +b.dataset.grade;
          gradeCard(st, x.id, g);
          const r = saveSrs(storage, st);
          if (!r.ok) notice = r.error;
          const remains = g === 0 && !retried.has(x.id);
          advanceQueue(queue, g, retried);
          if (!remains) done++;
          show();
        }),
    );
  }
  show();
}
