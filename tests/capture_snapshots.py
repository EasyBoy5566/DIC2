"""Capture the published website for the README (requires Playwright Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = 'https://easyboy5566.github.io/DIC2/'
OUT = Path(__file__).resolve().parents[1] / 'docs' / 'screenshots'
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width':1440,'height':1000}, device_scale_factor=1, locale='zh-TW')
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    response = page.goto(URL, wait_until='networkidle')
    assert response.status == 200
    for problem, name in [('startup','startup-desktop'),('custom','mpg-desktop')]:
        page.select_option('#problem', problem)
        page.click('#loadExample')
        page.wait_for_function("!document.getElementById('run').disabled")
        page.click('#run')
        page.wait_for_function("document.getElementById('status').textContent.startsWith('分析完成')", timeout=120000)
        page.wait_for_timeout(1200)
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT/f'{name}.png'),full_page=True)
        if problem == 'startup':
            page.screenshot(path=str(OUT/'overview.png'))
            page.set_viewport_size({'width':390,'height':844})
            page.wait_for_timeout(1200)
            page.screenshot(path=str(OUT/'startup-mobile.png'),full_page=True)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.set_viewport_size({'width':1440,'height':1000})
    assert not errors, errors
    print('Captured 4 screenshots from ' + URL)
    browser.close()
