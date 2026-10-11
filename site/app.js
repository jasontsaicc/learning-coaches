import {
  mountPractice,
  loadPractice,
  savePractice,
  weakQuestions,
  attemptKey,
} from "./exercises.js";
import { drawTree } from "./map.js";
import { openCards, loadSrs, deckOf, dueOf } from "./review.js";
const TITLE = {
  k8s: "Kubernetes / EKS",
  sd: "System Design",
  leetcode: "LeetCode",
  ca: "Cloud Architect",
};
const SUB = {
  k8s: "從機制到實際排障",
  sd: "理解每一個設計取捨",
  leetcode: "把思路變成能寫出的程式",
  ca: "把需求轉成可交付的架構",
};
export const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const isLeaf = (n) => ["topic", "problem"].includes(n.kind);
export const level = (n) =>
  n.status === "in-progress"
    ? n.level
      ? `進行中 · 教練評量 ${n.level}`
      : "進行中 · 尚未評量"
    : n.status === "materials-available"
      ? "已有教材 · 尚未評量"
      : n.planned
        ? "課綱待學"
        : n.level
          ? `教練評量 · ${n.level}`
          : n.practiced
            ? "已練習 · 未評量"
            : "已接觸 · 未評量";
function coachOf(data, n) {
  const byId = new Map(data.nodes.map((x) => [x.id, x]));
  while (n && n.kind !== "coach") n = byId.get(n.parent);
  return n?.id;
}
export function searchContent(data, query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  const out = [],
    files = new Set();
  for (const n of data.nodes) {
    const coachId = coachOf(data, n);
    if (isLeaf(n) && n.label.toLowerCase().includes(q))
      out.push({ kind: "topic", id: n.id, title: n.label, coachId });
    for (const path of n.files ?? []) {
      if (files.has(path)) continue;
      files.add(path);
      const title = data.titles?.[path] ?? path.split("/").pop();
      if (`${title} ${path}`.toLowerCase().includes(q))
        out.push({ kind: "file", id: path, title, path, coachId });
    }
  }
  return out;
}
export function resolveRecent(data, recent) {
  if (!recent) return null;
  if (recent.path)
    return data.nodes.some((n) => n.files?.includes(recent.path))
      ? { path: recent.path }
      : null;
  const ns = data.nodes.filter(
    (n) =>
      isLeaf(n) &&
      n.parent === recent.parent &&
      n.label === recent.label &&
      coachOf(data, n) === recent.coachId,
  );
  return ns.length === 1 ? ns[0] : null;
}
export async function startApp() {
  const app = document.querySelector("#app"),
    dialog = document.querySelector("#dialog"),
    dialogBody = document.querySelector("#dialog-body");
  document.querySelector(".skip-link").onclick = (event) => {
    event.preventDefault();
    app.focus();
    app.scrollIntoView();
  };
  let storage;
  try {
    storage = window.localStorage;
  } catch {
    storage = {
      getItem() {
        throw Error();
      },
      setItem() {
        throw Error();
      },
    };
  }
  let cleanup = () => {},
    request = 0,
    abort,
    readingTimer,
    readError = "";
  let data, practice, practiceError, sessionRecent;
  const close = () => dialog.close();
  document.querySelector("#dialog-close").onclick = close;
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (
        e.clientX < r.left ||
        e.clientX > r.right ||
        e.clientY < r.top ||
        e.clientY > r.bottom
      )
        close();
    }
  });
  function modal(title, html) {
    document.querySelector("#dialog-title").textContent = title;
    dialogBody.innerHTML = html;
    dialog.showModal();
  }
  function recent() {
    if (sessionRecent) return sessionRecent;
    try {
      const raw = storage.getItem("learning-map.reading.v1");
      const value = raw ? JSON.parse(raw) : null;
      if (
        value !== null &&
        (!value || typeof value !== "object" || Array.isArray(value))
      )
        throw Error();
      return value;
    } catch {
      readError = "閱讀位置無法讀取；原資料未覆寫。";
      return null;
    }
  }
  function saveRecent(value) {
    sessionRecent = value;
    try {
      if (readError) throw Error();
      storage.setItem("learning-map.reading.v1", JSON.stringify(value));
    } catch {
      readError = "閱讀位置未保存，目前只在此頁保留。";
      const n = app.querySelector("#read-status");
      if (n) n.textContent = readError;
    }
  }
  const fileLink = (f) =>
    `<a class="file" href="${f.endsWith(".md") ? "#/read/" + encodeURIComponent(f) : "files/" + encodeURI(f)}" ${f.endsWith(".md") ? "" : 'target="_blank" rel="noopener"'}><span>${esc(data.titles?.[f] ?? f.split("/").pop())}</span><span>${f.endsWith(".md") ? "閱讀 →" : "開新頁 ↗"}</span></a>`;
  const chapterCard = (c) => {
    const st = practice.chapters[c.id],
      count = c.questions.filter((q) => !q.variantOf).length,
      weak = weakQuestions(c, st).length;
    return `<article class="chapter-card"><span class="eyebrow">${esc(TITLE[c.coachId])} · 章節練習</span><h3>${esc(c.title)}</h3><p>${esc(c.objectives.map((o) => o.label).join(" · "))}</p><div class="chapter-bottom"><span>${count} 題${weak ? ` · ${weak} 題待重練` : " · 多題型練習"}</span><a class="btn primary" href="#/practice/${c.id}">${st && st.index < st.queue.length ? "接續練習" : "進入章節"} →</a></div></article>`;
  };
  const children = (id) => data.nodes.filter((n) => n.parent === id);
  const leaves = (id) =>
    children(id).flatMap((n) => (isLeaf(n) ? [n] : leaves(n.id)));
  function showTopic(n) {
    saveRecent({ coachId: coachOf(data, n), parent: n.parent, label: n.label });
    const chapters = data.chapters.filter((c) =>
      c.topicRefs.some((r) => r.parent === n.parent && r.label === n.label),
    );
    modal(
      n.label,
      `<p class="badge">${esc(level(n))}</p>${n.point ? `<p class="point">${esc(n.point)}</p>` : ""}${chapters.map((c) => `<p><a class="btn primary" href="#/practice/${c.id}">開始本章練習 →</a></p>`).join("")}${!chapters.length ? '<p class="muted">這個主題的練習尚未建立。</p>' : ""}<div class="files">${(n.files ?? []).map(fileLink).join("")}</div>${!n.files?.length ? "<p>尚無對應筆記，可回課程查看全部教材。</p>" : ""}`,
    );
  }
  function bindTopics() {
    app
      .querySelectorAll("[data-topic]")
      .forEach(
        (b) =>
          (b.onclick = () =>
            showTopic(data.nodes.find((n) => n.id === b.dataset.topic))),
      );
  }
  function home() {
    const coaches = children("me"),
      last = recent(),
      target = resolveRecent(data, last),
      stCh = data.chapters.find((c) => {
        const s = practice.chapters[c.id];
        return s && s.index < s.queue.length;
      }),
      weak = data.chapters.filter(
        (c) => weakQuestions(c, practice.chapters[c.id]).length,
      );
    app.innerHTML = `<section class="welcome"><div><span class="eyebrow">YOUR LEARNING GARDEN</span><h1>讓理解，慢慢長成能力。</h1><p class="lead">接續一個想法，練習一個章節。<br>今天的每一小步，都有它的方向。</p><a class="btn primary" href="#chapters" id="browse-chapters">選一章，開始練習 →</a></div><div class="welcome-art" aria-hidden="true"><img src="img/k8s.svg" alt=""><span class="art-note">理解 · 練習 · 再試一次</span></div></section>
   <div class="daily-grid"><section class="daily"><span class="eyebrow">接著上次的步調</span><h2>${target ? "繼續閱讀" : stCh ? "接續章節練習" : "從好奇的地方開始"}</h2><p>${esc(target ? (last.label ?? data.titles?.[target.path] ?? target.path.split("/").pop()) : (stCh?.title ?? "選擇一門課，找到你想弄懂的下一個觀念。"))}</p>${target ? (target.path ? `<a class="text-link" href="#/read/${encodeURIComponent(target.path)}">回到閱讀位置 →</a>` : `<button class="text-btn" data-topic="${esc(target.id)}">繼續閱讀 →</button>`) : stCh ? `<a class="text-link" href="#/practice/${stCh.id}">繼續練習 →</a>` : '<a class="text-link" href="#/c/k8s">探索課程 →</a>'}<p id="read-status" class="muted">${esc(readError)}</p></section>
   <section class="daily sage"><span class="eyebrow">把不確定變得清楚</span><h2>${weak.length ? `${weak.length} 章可以再練一點` : "用一道題，檢查理解"}</h2><p>選擇、填空、排序與配對。找到你會用的原理。</p><a class="text-link" href="#/practice/${(weak[0] ?? stCh ?? data.chapters[0])?.id ?? ""}">${weak.length ? "回到待重練章節" : "試試章節練習"} →</a></section></div>
   <div class="section-heading"><div><span class="eyebrow">KEEP GROWING</span><h2>我的課程</h2></div><span class="muted">${coaches.length} 個探索方向</span></div><div class="course-grid">${coaches
     .map((c) => {
       const ls = leaves(c.id),
         assessed = ls.filter((n) => n.level).length;
       return `<a class="course-card" href="#/c/${c.id}"><div class="course-art t-${c.id}"><img src="img/${c.id}.svg" alt=""></div><div class="course-body"><h3>${TITLE[c.id]}</h3><p>${SUB[c.id]}</p><div class="course-meta"><span>${ls.filter((n) => !n.planned).length} 個已接觸主題</span><span>↗</span></div><div class="mini-bar"><span style="width:${ls.length ? (assessed / ls.length) * 100 : 0}%"></span></div><small>${assessed} 個有教練評量 · ${data.chapters.filter((x) => x.coachId === c.id).length} 章可練習</small></div></a>`;
     })
     .join("")}</div>
   <div class="section-heading" id="chapters"><div><span class="eyebrow">LEARN BY DOING</span><h2>從一個章節開始</h2></div><span class="muted">首批 ${data.chapters.length} 章 · 持續補齊</span></div><div class="chapter-grid">${data.chapters.map(chapterCard).join("")}</div>${weak.length ? `<h2>待重練章節</h2><div class="files">${weak.map((c) => `<a class="file" href="#/practice/${c.id}">${esc(c.title)}<span>重練 →</span></a>`).join("")}</div>` : ""}`;
    app.querySelector("#browse-chapters").onclick = (e) => {
      e.preventDefault();
      app.querySelector("#chapters").scrollIntoView({
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth",
      });
    };
    bindTopics();
  }
  function course(id) {
    const c = data.nodes.find((n) => n.id === id && n.kind === "coach");
    if (!c) {
      notFound();
      return;
    }
    const phases = children(id).filter((n) => !isLeaf(n)),
      loose = children(id).filter(isLeaf),
      chapters = data.chapters.filter((x) => x.coachId === id),
      files = [
        ...new Set([
          ...(c.files ?? []),
          ...leaves(id).flatMap((n) => n.files ?? []),
        ]),
      ],
      first =
        phases.find((n) => n.status === "in-progress")?.id ?? phases[0]?.id;
    const lesson = (n) =>
      `<button class="lesson" data-topic="${esc(n.id)}"><span class="lesson-dot ${n.planned ? "planned" : ""}">${n.planned ? "○" : n.level === "high" ? "✓" : "↗"}</span><span><strong>${esc(n.label)}</strong><small>${esc(level(n))}</small></span></button>`;
    app.innerHTML = `<a class="back" href="#/">← 我的課程</a><section class="course-header"><div><span class="eyebrow">YOUR LEARNING PATH</span><h1>${TITLE[id]}</h1><p class="lead">${SUB[id]}</p><div class="actions"><button class="btn" id="map">知識地圖 ↗</button>${deckOf(c).length ? '<button class="btn" id="cards">記憶卡片</button>' : ""}</div></div><div class="course-illustration t-${id}"><img src="img/${id}.svg" alt=""></div></section>
  <div class="section-heading"><h2>章節練習</h2><span class="muted">${chapters.length} 章已有題庫</span></div><div class="chapter-grid">${chapters.map(chapterCard).join("")}</div><p class="muted">其餘主題的練習尚未建立。練習分數與教練評量分開記錄。</p>
  <h2>學習路徑</h2><div class="phase-list">${phases.map((p, i) => `<details class="phase" ${p.id === first ? "open" : ""}><summary><span class="phase-number">${String(i + 1).padStart(2, "0")}</span><span><strong>${esc(p.label)}</strong><small>${esc(p.status === "in-progress" ? "進行中" : p.status === "gate-passed" ? "已通過階段檢查" : p.status === "not-started" ? "尚未開始" : (p.status ?? "主題群"))}</small></span><span class="expand">＋</span></summary><div class="phase-content">${p.plan ? `<p class="muted">${esc(p.plan)}</p>` : ""}${children(p.id).filter(isLeaf).map(lesson).join("")}${(p.files ?? []).map(fileLink).join("")}</div></details>`).join("")}</div>${loose.length ? `<h2>其他已學主題</h2>${loose.map(lesson).join("")}` : ""}
  ${
    c.keypoints?.length
      ? `<h2>學習重點</h2>${c.keypoints
          .map(
            (t) =>
              `<details class="phase"><summary><strong>${esc(t.title)}</strong><span>${t.rows.length} 條 ＋</span></summary><div class="point-grid">${t.rows
                .map(
                  (r) =>
                    `<details class="point"><summary>${esc(r[0])}</summary>${r
                      .slice(1)
                      .filter(Boolean)
                      .map((x) => `<p>${esc(x)}</p>`)
                      .join("")}</details>`,
                )
                .join("")}</div></details>`,
          )
          .join("")}`
      : ""
  }<h2>全部筆記與圖解</h2><div class="files">${files.map(fileLink).join("") || '<p class="muted">尚無筆記。</p>'}</div>`;
    bindTopics();
    app.querySelector("#map").onclick = () => {
      modal(
        `${TITLE[id]} · 知識地圖`,
        '<div id="tree"></div><div id="map-selection" aria-live="polite">選取節點可查看名稱和教材。</div>',
      );
      drawTree(dialogBody.querySelector("#tree"), data.nodes, id, {
        onSelect: (n) => {
          const box = dialogBody.querySelector("#map-selection");
          box.innerHTML = `<strong>${esc(n.label)}</strong>${isLeaf(n) ? '<button class="btn" id="map-topic">開啟主題</button>' : (n.files ?? []).map(fileLink).join("")}`;
          box.querySelector("#map-topic")?.addEventListener("click", () => {
            close();
            showTopic(n);
          });
        },
      });
    };
    app.querySelector("#cards")?.addEventListener("click", () => {
      modal("記憶卡片 · 輔助複習", '<div id="cards-body"></div>');
      openCards(dialogBody.querySelector("#cards-body"), c, storage, esc);
    });
  }
  function search() {
    app.innerHTML =
      '<a class="back" href="#/">← 學習首頁</a><span class="eyebrow">FIND A CONNECTION</span><h1>找回學過的想法。</h1><p class="lead">搜尋主題名稱、筆記標題或檔名。</p><form id="search-form"><label for="query">搜尋教材</label><div class="search-row"><input id="query" type="search" placeholder="例如：Cache、probe、linked list" autocomplete="off"><button class="btn primary">搜尋 →</button></div></form><div id="results" aria-live="polite"><p class="muted">輸入一個你想找的概念。</p></div>';
    const run = () => {
      const input = app.querySelector("#query"),
        r = searchContent(data, input.value);
      app.querySelector("#results").innerHTML = !input.value.trim()
        ? '<p class="muted">輸入一個你想找的概念。</p>'
        : `<p class="muted">${r.length} 個結果</p><div class="files">${r.map((x) => (x.kind === "file" ? fileLink(x.path) : `<button class="file" data-topic="${esc(x.id)}"><span>${esc(x.title)}</span><span>${esc(TITLE[x.coachId])} · 主題</span></button>`)).join("")}</div>${!r.length ? '<button class="btn" id="clear">清除搜尋</button>' : ""}`;
      bindTopics();
      app.querySelector("#clear")?.addEventListener("click", () => {
        input.value = "";
        run();
        input.focus();
      });
    };
    app.querySelector("#search-form").onsubmit = (e) => {
      e.preventDefault();
      run();
    };
    app.querySelector("#query").oninput = run;
  }
  async function read(path, token) {
    const owner = data.nodes.find((n) => n.files?.includes(path));
    if (!owner || !path.endsWith(".md")) {
      notFound();
      return;
    }
    const coach = coachOf(data, owner),
      last = recent(),
      saved =
        last?.path === path && Number.isFinite(last.scrollTop)
          ? last.scrollTop
          : 0;
    app.innerHTML = `<a class="back" href="#/c/${coach}">← ${TITLE[coach]}</a><div class="reader-layout"><aside id="toc" aria-label="文章目錄"></aside><article class="md" id="reader"><p>載入教材中…</p></article></div><p id="read-status" role="status">${esc(readError)}</p>`;
    abort = new AbortController();
    try {
      const r = await fetch("files/" + encodeURI(path), {
        signal: abort.signal,
      });
      if (!r.ok) throw Error(r.status);
      const text = await r.text();
      if (token !== request) return;
      const reader = app.querySelector("#reader");
      if (globalThis.marked && globalThis.DOMPurify) {
        reader.innerHTML = DOMPurify.sanitize(marked.parse(text));
      } else {
        const pre = document.createElement("pre");
        pre.textContent = text;
        reader.replaceChildren(pre);
      }
      reader.querySelectorAll("a").forEach((a) => {
        const href = a.getAttribute("href");
        if (href?.startsWith("https://") || href?.startsWith("http://")) {
          a.target = "_blank";
          a.rel = "noopener";
        } else if (href && !href.startsWith("#")) a.removeAttribute("href");
      });
      const heads = [...reader.querySelectorAll("h1,h2,h3")];
      heads.forEach((h, i) => (h.id = `heading-${i}`));
      app.querySelector("#toc").innerHTML =
        '<span class="eyebrow">這篇筆記</span>' +
        heads
          .map(
            (h, i) =>
              `<button class="toc-link" data-heading="${i}">${esc(h.textContent)}</button>`,
          )
          .join("");
      app
        .querySelectorAll("[data-heading]")
        .forEach(
          (b) => (b.onclick = () => heads[+b.dataset.heading].scrollIntoView()),
        );
      saveRecent({ path, coachId: coach, scrollTop: saved });
      requestAnimationFrame(() => {
        if (token === request) window.scrollTo(0, saved);
      });
      const onScroll = () => {
        clearTimeout(readingTimer);
        readingTimer = setTimeout(
          () => saveRecent({ path, coachId: coach, scrollTop: window.scrollY }),
          150,
        );
      };
      window.addEventListener("scroll", onScroll);
      cleanup = () => {
        clearTimeout(readingTimer);
        window.removeEventListener("scroll", onScroll);
        saveRecent({ path, coachId: coach, scrollTop: window.scrollY });
      };
    } catch (e) {
      if (e.name === "AbortError" || token !== request) return;
      app.querySelector("#reader").innerHTML =
        '<h1>教材暫時無法載入</h1><p>請檢查連線，或稍後再試。</p><button class="btn" id="retry-read">重試</button>';
      app.querySelector("#retry-read").onclick = () => read(path, token);
    }
  }
  function notFound() {
    app.innerHTML =
      '<h1>找不到這個學習頁面</h1><p>教材或章節可能已移動。</p><a class="btn primary" href="#/">返回學習首頁</a>';
  }
  function route() {
    cleanup();
    cleanup = () => {};
    abort?.abort();
    close();
    const token = ++request;
    app.className = "";
    let parts;
    try {
      parts = location.hash.slice(2).split("/").map(decodeURIComponent);
    } catch {
      notFound();
      return;
    }
    window.scrollTo(0, 0);
    if (!parts[0]) home();
    else if (parts[0] === "c") course(parts[1]);
    else if (parts[0] === "search") search();
    else if (parts[0] === "read") {
      app.className = "reading";
      read(parts.slice(1).join("/"), token);
    } else if (parts[0] === "practice") {
      const c = data.chapters.find((x) => x.id === parts[1]);
      if (!c) {
        notFound();
        return;
      }
      app.className = "practice-page";
      cleanup = mountPractice(app, c, {
        state: practice.chapters[c.id],
        onExit: () => (location.hash = `#/c/${c.coachId}`),
        onSave: (state) => {
          practice.chapters[c.id] = state;
          const result = savePractice(storage, practice);
          if (!result.ok) practiceError = result.error;
          return result;
        },
      });
      if (practiceError) {
        const p = document.createElement("p");
        p.className = "notice";
        p.setAttribute("role", "alert");
        p.textContent = practiceError;
        app.prepend(p);
      }
    } else notFound();
    const heading = app.querySelector("h1");
    if (heading) {
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    }
  }
  async function load() {
    try {
      const r = await fetch("data.json", { cache: "no-cache" });
      if (!r.ok) throw Error();
      data = await r.json();
      if (
        !Array.isArray(data.nodes) ||
        !Array.isArray(data.chapters) ||
        !data.nodes.some((n) => n.kind === "coach")
      )
        throw Error();
      const loaded = loadPractice(storage);
      practice = loaded.state;
      practiceError = loaded.error;
      window.addEventListener("hashchange", route);
      route();
    } catch {
      app.innerHTML =
        '<h1>學習資料暫時無法載入</h1><p>請檢查連線後再試。</p><button class="btn primary" id="reload">重新載入</button>';
      app.querySelector("#reload").onclick = load;
    }
  }
  await load();
}
