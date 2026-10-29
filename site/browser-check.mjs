// Optional integration check: uses an externally installed Playwright, not a runtime dependency.
import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";
const { chromium } = await import(
  process.env.PLAYWRIGHT_MODULE || "playwright"
);
const url = process.env.SITE_URL || "http://127.0.0.1:8124/";
const browser = await chromium.launch({
  headless: true,
  ...(process.env.CHROMIUM_PATH
    ? { executablePath: process.env.CHROMIUM_PATH }
    : {}),
  args: process.env.CHROMIUM_NO_SANDBOX === "1" ? ["--no-sandbox"] : [],
});
async function smoke(browser) {
  const page = await browser.newPage({
      viewport: { width: 1280, height: 960 },
    }),
    errors = [];
  page.on("pageerror", (e) => errors.push(e.message));

  await mkdir("/tmp/learning-site-preview", { recursive: true });
  {
    await page.goto(url);
    await page
      .getByRole("heading", { name: "讓理解，慢慢長成能力。" })
      .waitFor();
    await page.screenshot({
      path: "/tmp/learning-site-preview/home-desktop.png",
      fullPage: true,
    });
    await page.goto(url + "#/c/k8s");
    const notes = page.locator(".path-node").filter({ hasText: "健康與發布" }).first();
    const toggle = notes.locator(".path-toggle");
    await toggle.click();
    assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
    const primary = notes.locator('.path-chunks a').first();
    await primary.waitFor();
    const [popup] = await Promise.all([page.waitForEvent('popup'), primary.click()]);
    await popup.waitForLoadState();
    assert.ok(popup.url().endsWith('.html'));
    await popup.close();
    for (const width of [1280, 360]) {
      await page.setViewportSize({ width, height: 960 });
      await page.screenshot({ path: `/tmp/learning-site-preview/html-notes-${width}.png`, fullPage: true });
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    }
    await page.setViewportSize({ width: 1280, height: 960 });
    const built = await (await page.request.get(url + "data.json")).json();
    for (const coach of ["k8s", "sd", "leetcode", "ca"]) {
      await page.goto(url + "#/c/" + coach);
      await page.locator(built.paths?.[coach] ? ".learning-path" : ".phase-list").waitFor();
      if (built.paths?.[coach]) {
        const nodes = built.paths[coach].flatMap((p) => p.nodes);
        assert.equal(await page.locator('.path-node').count(), nodes.length);
        for (const n of nodes) for (const chunk of n.chunks) {
          const row = page.locator(`[id="${chunk.id}"]`);
          assert.equal(await row.locator('a').count(), chunk.note ? 1 : 0);
        }
        await page.locator('#path-collapse').click();
        const button = page.locator('.path-toggle').first();
        await button.focus();
        await page.keyboard.press('Enter');
        assert.equal(await button.getAttribute('aria-expanded'), 'true');
        await page.keyboard.press('Space');
        assert.equal(await button.getAttribute('aria-expanded'), 'false');
      }
      assert.equal(await page.locator('.markdown-notes').count(), 0);
      for (const size of await page.locator('.md-link').evaluateAll((links) => links.map((a) => getComputedStyle(a).fontSize)))
        assert.equal(size, '12px');
      const byId = new Map(built.nodes.map((n) => [n.id, n]));
      const belongs = (n) => {
        while (n && n.kind !== "coach") n = byId.get(n.parent);
        return n?.id === coach;
      };
      const nodes = built.nodes.filter(belongs);
      const expected = [...new Set(nodes.flatMap((n) => n.files ?? []))];
      const hrefs = await page.locator("#app a[href]").evaluateAll((links) => links.map((a) => a.getAttribute("href")));
      for (const f of expected) assert.ok(hrefs.includes(f.endsWith(".md") ? "#/read/" + encodeURIComponent(f) : "files/" + encodeURI(f)), `missing note: ${f}`);
      for (const n of (built.paths?.[coach] ? [] : nodes).filter((n) => ["topic", "problem"].includes(n.kind))) {
        const node = page.locator(".lesson-node").filter({ has: page.locator(`[data-topic="${n.id}"]`) });
        for (const f of (n.files ?? []).filter((f) => f.endsWith(".html")))
          assert.equal(await node.locator(`a[href="files/${encodeURI(f)}"]`).count(), 1);
      }
    }
    await page.goto(url + "#/search");
    await page.locator("#query").fill("p1-pod-probe.md");
    assert.equal(await page.locator('#results a[href*="#/read/"]').count(), 0);
    await page.getByLabel("包含 Markdown 補充資料").check();
    await page.locator('#results a[href*="#/read/"]').first().waitFor();
    await page.goto(url + "#/practice/k8s-probes");
    await page.locator("#answer-form").waitFor();
    await page.locator("[name=answer][value=b]").check();
    await page.locator("#confidence").selectOption("sure");
    await page.getByRole("button", { name: "檢查答案" }).click();
    await page.getByRole("heading", { name: "答對了", exact: true }).waitFor();
    await page.locator("#next").click();
    await page.locator("[data-match=i0]").selectOption("t2");
    await page.locator("[data-match=i1]").selectOption("t0");
    await page.locator("[data-match=i2]").selectOption("t1");
    await page.getByRole("button", { name: "檢查答案" }).click();
    await page.locator("#next").click();
    await page.locator("#fill").fill("0");
    await page.reload();
    await page.locator("#fill").waitFor();
    assert.equal(await page.locator("#fill").inputValue(), "0");
    await page.locator("#hint").click();
    await page.getByRole("button", { name: "檢查答案" }).click();
    await page
      .getByRole("heading", { name: "提示後答對", exact: true })
      .waitFor();
    await page.locator("#next").click();
    await page.screenshot({
      path: "/tmp/learning-site-preview/order-desktop.png",
      fullPage: true,
    });
    await page.locator("#skip").click();
    await page.locator("#next").click();
    await page.locator("[name=answer][value=a]").check();
    await page.locator("[name=answer][value=b]").check();
    await page.getByRole("button", { name: "檢查答案" }).click();
    await page.locator("#next").click();
    await page.locator("[name=answer][value=c]").check();
    await page.getByRole("button", { name: "檢查答案" }).click();
    await page.locator("#next").click();
    await page
      .getByRole("heading", { name: "每一步，都更清楚一點。" })
      .waitFor();
    await page.screenshot({
      path: "/tmp/learning-site-preview/result-desktop.png",
      fullPage: true,
    });
    await page.locator("#retry").click();
    await page.locator("#answer-form").waitFor();
    await page.goto(url + "#/search");
    await page.locator("#query").fill("caching");
    assert.ok((await page.locator("#results .file").count()) > 0);
    await page.goto(
      url +
        "#/read/" +
        encodeURIComponent("portfolio/sd/notes/day06-07-caching.md"),
    );
    await page.locator("#reader h1").waitFor();
    await page.screenshot({
      path: "/tmp/learning-site-preview/reader-desktop.png",
      fullPage: true,
    });
    await page.goto(url + "#/c/k8s");
    await page.locator("#map").click();
    await page.locator("#tree").waitFor();
    await page.locator("#dialog-close").click();
    assert.equal(
      await page.locator("#map").evaluate((e) => document.activeElement === e),
      true,
    );
    await page.locator("#cards").click();
    await page.locator("#flip").waitFor();
    await page.locator("#dialog-close").click();
    await page.setViewportSize({ width: 360, height: 800 });
    for (const [route, name, selector] of [
      ["", "home", "#chapters"],
      ["#/c/k8s", "course", ".path-node"],
      ["#/practice/sd-cache-aside", "practice", "#answer-form"],
      [
        "#/read/" +
          encodeURIComponent("portfolio/sd/notes/day06-07-caching.md"),
        "reader",
        "#reader h1",
      ],
    ]) {
      await page.goto(url + route);
      await page.locator(selector).first().waitFor();
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
        true,
        `${name} overflows`,
      );
      await page.screenshot({
        path: `/tmp/learning-site-preview/${name}-mobile.png`,
        fullPage: true,
      });
    }
    assert.deepEqual(errors, []);
    console.log(
      "browser: desktop/mobile, all input types, resume, results, search, reading, map, cards OK",
    );
  }
}
async function failures(browser) {
  const page = await browser.newPage(),
    errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.route("**/data.json", (r) =>
    r.fulfill({ status: 503, body: "unavailable" }),
  );
  await page.goto(url);
  await page.getByRole("heading", { name: "學習資料暫時無法載入" }).waitFor();
  await page.unroute("**/data.json");
  await page.locator("#reload").click();
  await page.locator("#chapters").waitFor();
  const staleRequested = Promise.withResolvers(),
    releaseStale = Promise.withResolvers();
  await page.route("**/files/**", async (r) => {
    if (r.request().url().includes("day06")) {
      staleRequested.resolve();
      await releaseStale.promise;
      await r.fulfill({ body: "# STALE RESPONSE" });
    } else await r.continue();
  });
  await page.goto(
    url +
      "#/read/" +
      encodeURIComponent("portfolio/sd/notes/day06-07-caching.md"),
  );
  await staleRequested.promise;
  await page.goto(
    url + "#/read/" + encodeURIComponent("portfolio/k8s/notes/p1-pod-probe.md"),
  );
  await page.locator("#reader h1").waitFor();
  releaseStale.resolve();
  await page.unrouteAll({ behavior: "wait" });
  assert.ok((await page.locator("#reader").innerText()).includes("Probe"));
  assert.ok(!(await page.locator("#reader").innerText()).includes("STALE"));
  await page.route("**/files/**", (r) =>
    r.fulfill({ status: 404, body: "gone" }),
  );
  await page.goto(
    url +
      "#/read/" +
      encodeURIComponent("portfolio/sd/notes/day06-07-caching.md"),
  );
  await page.locator("#retry-read").waitFor();
  await page.unroute("**/files/**");
  await page.locator("#retry-read").click();
  await page.locator("#reader h1").waitFor();
  await page.goto(url + "#/practice/lc-linked-list-cycle");
  await page.locator("#answer-form").waitFor();
  await page.evaluate(() => {
    Storage.prototype.setItem = function () {
      throw new DOMException("quota", "QuotaExceededError");
    };
  });
  await page.locator("[name=answer][value=b]").check();
  await page
    .getByText("練習紀錄未保存；請保持此頁開啟。", { exact: true })
    .first()
    .waitFor();
  await page.getByRole("button", { name: "檢查答案" }).click();
  await page.locator("#next").click();
  await page.locator("#fill").fill("and");
  await page.getByRole("button", { name: "檢查答案" }).click();
  await page.locator("#next").click();
  // Solve the reverse-initialized order with actual move buttons, then keyboard submit.
  for (let target = 0; target < 3; target++) {
    for (let i = 3; i > target; i--)
      await page.locator(`[data-move="${i}"][data-step="-1"]`).click();
  }
  await page.locator("#submit").focus();
  await page.keyboard.press("Enter");
  await page.getByRole("heading", { name: "答對了", exact: true }).waitFor();
  assert.deepEqual(errors, []);
  await page.close();
  const fallback = await browser.newPage();
  await fallback.route("**/cdnjs.cloudflare.com/**", (r) => r.abort());
  await fallback.goto(url + "#/c/k8s");
  await fallback.locator("#map").click();
  await fallback
    .getByText("地圖暫時無法載入，仍可從課程章節繼續閱讀。")
    .waitFor();
  await fallback.locator("#dialog-close").click();
  await fallback.goto(
    url + "#/read/" + encodeURIComponent("portfolio/k8s/notes/p1-pod-probe.md"),
  );
  await fallback.locator("#reader pre").waitFor();
  await fallback.close();
  console.log(
    "failure cases: data retry, stale request, note 404 retry, quota notice, order via keyboard, CDN fallbacks OK",
  );
}

async function navigationRegressions(browser) {
  const p = await browser.newPage();
  await p.goto(url);
  await p.locator("#chapters").waitFor();
  await p.locator(".skip-link").focus();
  await p.keyboard.press("Enter");
  assert.equal(await p.locator("#chapters").count(), 1);
  await p.goto(url + "#/practice/k8s-probes");
  await p.locator("[name=answer][value=b]").check();
  await p.locator("#submit").click();
  await p.locator("#next").waitFor();
  await p.reload();
  await p.locator("#next").waitFor();
  assert.equal(await p.locator("#submit").isDisabled(), true);
  await p.close();
}
async function learningFlow(browser) {
  const page = await browser.newPage();
  const note = "portfolio/k8s/notes/p1-pod-probe.md";
  await page.goto(url);
  await page.locator("#chapters").waitFor();
  await page.goto(url + "#/practice/k8s-probes");
  await page.locator('[name=answer][value=b]').check();
  await page.goto(url + "#/read/" + encodeURIComponent(note));
  await page.locator("#reader h1").waitFor();
  await page.goto(url);
  await page.locator("#chapters").waitFor();
  assert.equal(await page.locator('.daily-grid a[href="#/practice/k8s-probes"]').filter({ hasText: "繼續練習" }).count(), 1, "reading must not hide unfinished practice");
  await page.getByRole("link", { name: "回到閱讀位置" }).click();
  await page.locator("#reader h1").waitFor();
  assert.equal(await page.locator('#reading-practice a[href="#/practice/k8s-probes"]').count(), 1, "source note offers its chapter practice");
  assert.equal(await page.locator('#reading-practice a[href="#/practice/ca-vpc-peering"]').count(), 0);
  await page.locator('#reading-practice a[href="#/practice/k8s-probes"]').click();
  assert.equal(await page.locator('[name=answer][value=b]').isChecked(), true, "reading round trip keeps draft");
  await page.locator("#submit").click();
  await page.locator("#next").click();
  for (let i = 1; i < 6; i++) {
    await page.locator("#skip").click();
    await page.locator("#next").click();
  }
  await page.getByRole("heading", { name: "每一步，都更清楚一點。", exact: true }).waitFor();
  const before = await page.evaluate(() => localStorage.getItem("learning-map.practice.v1"));
  assert.equal(await page.locator("#question-review details").count(), 6, "completed round offers every primary question");
  const first = page.locator("#question-review details").first();
  await first.locator("summary").click();
  assert.match(await first.innerText(), /首次作答[\s\S]*參考答案[\s\S]*解說/);
  const skipped = page.locator("#question-review details").nth(1);
  await skipped.locator("summary").click();
  assert.match(await skipped.innerText(), /已略過/);
  assert.equal(await page.evaluate(() => localStorage.getItem("learning-map.practice.v1")), before, "review never rewrites evidence");
  await page.reload();
  await page.locator("#question-review").waitFor();
  assert.equal(await page.locator("#question-review details").count(), 6);
  // Historical evidence can differ from the latest attempt; old revisions cannot pass a new question.
  await page.evaluate(() => {
    const state = JSON.parse(localStorage.getItem("learning-map.practice.v1"));
    const attempts = state.chapters["k8s-probes"].attempts;
    attempts["ready@1"].latestAttempt = { ...attempts["ready@1"].firstAttempt, answer: ["a"], correct: false, time: Date.now() };
    attempts["roles@0"] = attempts["roles@1"];
    delete attempts["roles@1"];
    attempts["restarts@1"].latestAttempt = { ...attempts["restarts@1"].firstAttempt, answer: '<img src=x onerror="window.reviewInjected=true">', skipped: false };
    localStorage.setItem("learning-map.practice.v1", JSON.stringify(state));
  });
  await page.reload();
  const readyReview = page.locator('[data-review-question="ready"]');
  await readyReview.locator("summary").click();
  assert.match(await readyReview.innerText(), /首次作答[\s\S]*無提示答對[\s\S]*最新作答[\s\S]*答錯/);
  const revised = page.locator('[data-review-question="roles"]');
  await revised.locator("summary").click();
  assert.match(await revised.innerText(), /尚未作答/);
  const fillReview = page.locator('[data-review-question="restarts"]');
  await fillReview.locator("summary").click();
  assert.match(await fillReview.innerText(), /<img src=x/);
  assert.equal(await page.locator("#question-review img").count(), 0, "saved answer is text, never executable HTML");
  await page.setViewportSize({ width: 360, height: 800 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  await page.screenshot({ path: "/tmp/learning-site-preview/question-review-mobile.png", fullPage: true });
  await page.locator("#retry").click();
  await page.locator("#question-title").waitFor();
  assert.deepEqual(await page.evaluate(() => JSON.parse(localStorage.getItem("learning-map.practice.v1")).chapters["k8s-probes"].attempts["ready@1"].firstAttempt), JSON.parse(before).chapters["k8s-probes"].attempts["ready@1"].firstAttempt);
  await page.close();
  console.log("learning flow: reading + resume, related practice, per-question review and retry OK");
}

try {
  await mkdir("/tmp/learning-site-preview", { recursive: true });
  await learningFlow(browser);
  await smoke(browser);
  await failures(browser);
  await navigationRegressions(browser);
} finally {
  await browser.close();
}
