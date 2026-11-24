import os, glob, shutil
os.makedirs("rec", exist_ok=True)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    ctx = b.new_context(viewport={"width":1280,"height":800},
        record_video_dir="rec", record_video_size={"width":1280,"height":800})
    pg = ctx.new_page()

    # ---------- 1. PLAYGROUND ----------
    pg.goto("https://workers.cloudflare.com/playground", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(9000)                      # let it boot on camera
    pg.screenshot(path="rec/pg_ready.png")

    pg.mouse.click(430, 420); pg.wait_for_timeout(800)
    for _ in range(3): pg.keyboard.press("Control+End")
    pg.wait_for_timeout(400)
    pg.keyboard.type("\n// your own API here", delay=130)   # real typing
    pg.wait_for_timeout(1800)

    pg.mouse.click(700, 218); pg.wait_for_timeout(2200)     # Preview tab
    pg.mouse.move(960, 560); pg.mouse.wheel(0, 300); pg.wait_for_timeout(1800)
    pg.mouse.click(790, 218); pg.wait_for_timeout(2600)     # HTTP tab
    pg.screenshot(path="rec/pg_http.png")

    # ---------- 2. LIMITS ----------
    pg.goto("https://developers.cloudflare.com/workers/platform/limits/", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3000)
    for txt in ("Accept Cookies", "Accept all", "Accept All"):
        try:
            pg.get_by_role("button", name=txt).first.click(timeout=4000)
            print("cookie banner dismissed:", txt); break
        except Exception: pass
    pg.wait_for_timeout(1200)

    # land exactly on the Account plan limits table (Requests / CPU time rows)
    for y in (300, 520, 640, 690):
        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'smooth'}})")
        pg.wait_for_timeout(1300)
    pg.wait_for_timeout(2000)
    pg.screenshot(path="rec/limits_table.png")

    # hover the Requests row, then the CPU row (real pointer motion)
    try:
        pg.get_by_text("100,000/day").first.hover(timeout=6000); pg.wait_for_timeout(2200)
        pg.get_by_text("10 ms").first.hover(timeout=6000); pg.wait_for_timeout(2200)
    except Exception as e:
        print("hover:", e)
    pg.wait_for_timeout(1500)

    pg.close(); ctx.close(); b.close()

vids = sorted(glob.glob("rec/*.webm"))
print("webm:", vids)
if vids:
    shutil.copy(vids[0], "rec/playwright.webm")
    print("size:", os.path.getsize("rec/playwright.webm"))
print("done")
