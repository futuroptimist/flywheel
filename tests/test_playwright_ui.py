import shutil
import threading
from pathlib import Path

import pytest
from werkzeug.serving import make_server

from web.app import app


@pytest.fixture()
def serve(tmp_path):
    obj_dir = tmp_path / "objs"
    obj_dir.mkdir()
    (obj_dir / "cube.obj").write_text("o test")

    static_src = Path(__file__).resolve().parents[1] / "web" / "static"
    shutil.copytree(static_src, tmp_path, dirs_exist_ok=True)
    app.static_folder = str(tmp_path)
    server = make_server("127.0.0.1", 5055, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    try:
        yield "http://127.0.0.1:5055"
    finally:
        server.shutdown()
        thread.join()


def test_drag_zoom_reset(page, serve):
    page.goto(serve)
    page.wait_for_selector("#viewer")
    page.mouse.move(100, 100)
    page.mouse.down()
    page.mouse.move(150, 150)
    page.mouse.up()
    page.mouse.wheel(0, -200)
    page.keyboard.press("r")
