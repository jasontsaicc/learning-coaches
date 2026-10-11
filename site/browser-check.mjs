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
      ["#/c/k8s", "course", ".phase"],
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
  await page.route("**/files/**", async (r) => {
    if (r.request().url().includes("day06")) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      await r.fulfill({ body: "# STALE RESPONSE" });
    } else await r.continue();
  });
  await page.goto(
    url +
      "#/read/" +
      encodeURIComponent("portfolio/sd/notes/day06-07-caching.md"),
  );
  await page.goto(
    url + "#/read/" + encodeURIComponent("portfolio/k8s/notes/p1-pod-probe.md"),
  );
  await page.locator("#reader h1").waitFor();
  assert.ok((await page.locator("#reader").innerText()).includes("Probe"));
  assert.ok(!(await page.locator("#reader").innerText()).includes("STALE"));
  await page.unroute("**/files/**");
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
try {
  await smoke(browser);
  await failures(browser);
  await navigationRegressions(browser);
} finally {
  await browser.close();
}
