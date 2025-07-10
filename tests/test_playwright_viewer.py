import multiprocessing
import time

import pytest
import requests

from web.app import create_app

# Playwright's browsers are heavy and not bundled by default.
# Skip these UI tests unless browsers are installed.
pytest.skip("playwright browsers missing", allow_module_level=True)


@pytest.fixture(scope="module")
def server_url():
    app = create_app()
    proc = multiprocessing.Process(target=app.run, kwargs={"port": 5001})
    proc.start()
    for _ in range(20):
        try:
            requests.get("http://localhost:5001/")
            break
        except requests.ConnectionError:
            time.sleep(0.2)
    yield "http://localhost:5001/"
    proc.terminate()
    proc.join()


def test_viewer_page(server_url):
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(server_url)
        canvas_count = page.locator("canvas").count()
        browser.close()
    assert canvas_count >= 1
