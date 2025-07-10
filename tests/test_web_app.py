import web.app as webapp


def test_index_route(tmp_path, monkeypatch):
    obj_dir = tmp_path / "objs"
    obj_dir.mkdir()
    obj_file = obj_dir / "test.obj"
    obj_file.write_text("o test")

    monkeypatch.setattr(webapp.app, "static_folder", str(tmp_path))

    client = webapp.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"viewer" in resp.data
