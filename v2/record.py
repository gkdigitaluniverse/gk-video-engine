import os, json, time
os.makedirs("rec", exist_ok=True)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    ctx = b.new_context(viewport={"width":1280,"height":800},
        record_video_dir="rec", record_video_size={"width":1280,"height":800},
        device_scale_factor=1.5)
    pg = ctx.new_page()

    # 1) playground: load, type, click HTTP, click Preview
    pg.goto("https://workers.cloudflare.com/playground", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(6000)
    try:
        ed = pg.locator(".monaco-editor").first
        ed.click(timeout=15000)
        pg.wait_for_timeout(600)
        for _ in range(3):
            pg.keyboard.press("Control+End")
        pg.keyboard.type("\n// try your own API here", delay=90)
        pg.wait_for_timeout(900)
    except Exception as e:
        print("editor step:", e)
    for label in ("HTTP","Preview"):
        try:
            pg.get_by_text(label, exact=True).first.click(timeout=8000)
            pg.wait_for_timeout(1800)
        except Exception as e:
            print(f"{label} click:", e)
    pg.wait_for_timeout(1500)
    pg.screenshot(path="rec/pg_end.png")

    # 2) limits page: scroll to the table
    pg.goto("https://developers.cloudflare.com/workers/platform/limits/", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3500)
    for y in (500, 900, 1250, 1500):
        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'smooth'}})")
        pg.wait_for_timeout(1100)
    pg.wait_for_timeout(1200)

    vid = pg.video
    ctx.close()
    b.close()
    if vid:
        vid.save_as("rec/playwright.webm")
        print("saved rec/playwright.webm")
print("done")
