// v11 — real captures for the "push protection" video.
// Every image here is a live page from github.com / docs.github.com, captured today.
const { chromium } = require("playwright");
const fs = require("fs");
fs.mkdirSync("public/shots", { recursive: true });

const SHOTS = [
  { out: "repo-security.png", url: "https://github.com/gkdigitaluniverse/gk-video-engine/security", needle: "Security" },
  { out: "docs-push.png", url: "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", needle: "blocks pushes" },
  { out: "docs-before.png", url: "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", needle: "How push protection works" },
  { out: "docs-subset.png", url: "https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope", needle: "subset of the most identifiable" },
  { out: "docs-50mb.png", url: "https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope", needle: "larger than 50 MB" },
  { out: "docs-patterns.png", url: "https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns", needle: "Supported patterns" },
  { out: "awesome-532.png", url: "https://github.com/advanced-security/awesome-secret-scanning", needle: "Number of Partner Secret Types" },
  { out: "docs-scanning.png", url: "https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning", needle: "About secret scanning" },
];

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({
    viewport: { width: 1280, height: 860 },
    deviceScaleFactor: 2,
    locale: "en-US",
    colorScheme: "light",
  });
  const page = await ctx.newPage();
  for (const s of SHOTS) {
    try {
      await page.goto(s.url, { waitUntil: "domcontentloaded", timeout: 60000 });
      await page.waitForTimeout(3000);
      if (s.needle) {
        try {
          const loc = page.getByText(s.needle, { exact: false }).first();
          await loc.scrollIntoViewIfNeeded({ timeout: 10000 });
          await page.waitForTimeout(600);
          const box = await loc.boundingBox();
          if (box) { await page.evaluate((y) => window.scrollBy(0, y - 300), box.y); await page.waitForTimeout(500); }
        } catch (e) { console.log("needle miss", s.out, String(e).slice(0, 100)); }
      }
      await page.screenshot({ path: "public/shots/" + s.out });
      console.log("ok", s.out, page.url());
    } catch (e) {
      console.log("FAIL", s.out, String(e).slice(0, 160));
    }
  }
  await b.close();
})();

// rerun 2 — upload path fixed
