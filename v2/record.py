import os, glob, shutil
os.makedirs("rec", exist_ok=True)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    ctx = b.new_context(viewport={"width":1280,"height":800},
        record_video_dir="rec", record_video_size={"width":1280,"height":800})
    pg = ctx.new_page()

    pg.goto("https://workers.cloudflare.com/playground", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(7000)

    # click into the editor by coordinates (Monaco hides its textarea)
    pg.mouse.click(430, 420)
    pg.wait_for_timeout(700)
    for _ in range(3):
        pg.keyboard.press("Control+End")
    pg.keyboard.type("\n// your own API here", delay=110)
    pg.wait_for_timeout(1200)

    # click the Preview / HTTP tabs by coordinates in the right pane header
    for x in (700, 790):
        pg.mouse.click(x, 218)
        pg.wait_for_timeout(1900)

    # scroll inside the preview pane
    pg.mouse.move(960, 600)
    pg.mouse.wheel(0, 400)
    pg.wait_for_timeout(1500)
    pg.screenshot(path="rec/pg_end.png")

    # limits page: smooth scroll to the table
    pg.goto("https://developers.cloudflare.com/workers/platform/limits/", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3500)
    for y in (420, 760, 1050, 1300):
        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'smooth'}})")
        pg.wait_for_timeout(1200)
    pg.wait_for_timeout(1000)
    pg.screenshot(path="rec/limits_end.png")

    pg.close()
    ctx.close()
    b.close()

# Playwright writes the webm into rec/ on context close
vids = sorted(glob.glob("rec/*.webm"))
print("webm files:", vids)
if vids:
    shutil.copy(vids[0], "rec/playwright.webm")
    print("copied ->", os.path.getsize("rec/playwright.webm"), "bytes")
print("done")
