import os
os.makedirs("shots", exist_ok=True)
from playwright.sync_api import sync_playwright
jobs = [
 ("support","https://support.google.com/docs/answer/186103?co=GENIE.Platform%3DDesktop&hl=en", 6000),
 ("blog","https://workspaceupdates.googleblog.com/2024/07/release-notes-07-26-2024.html", 5000),
]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width":1440,"height":900}, device_scale_factor=2)
    for name,url,wait in jobs:
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=70000)
            pg.wait_for_timeout(wait)
            for t in ("Accept all","Accept Cookies","I agree"):
                try: pg.get_by_role("button", name=t).first.click(timeout=3000); break
                except Exception: pass
            pg.wait_for_timeout(1200)
            pg.screenshot(path=f"shots/{name}.png")
            print("ok", name)
        except Exception as e:
            print("FAIL", name, str(e)[:120])
    b.close()
