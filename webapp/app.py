from pathlib import Path

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


MODEL_DIR = Path(__file__).resolve().parent / "static" / "models"
SCAD_DIR = Path(__file__).resolve().parent.parent / "hardware" / "cad"


def ensure_obj_models():
    """Convert SCAD files from hardware/cad into OBJ models in static/models.
    Uses the OpenSCAD CLI if available. Only re-exports when the source file is
    newer than the existing .obj or the .obj is missing. Silently ignores
    failures so the web app still runs even if OpenSCAD isn’t installed.
    """
    if not MODEL_DIR.exists():
        MODEL_DIR.mkdir(parents=True, exist_ok=True)

    for scad_path in SCAD_DIR.glob("*.scad"):
        obj_path = MODEL_DIR / f"{scad_path.stem}.obj"
        try:
            if (
                not obj_path.exists()
                or scad_path.stat().st_mtime > obj_path.stat().st_mtime
            ):
                import shutil
                import subprocess
                import tempfile

                import trimesh

                if shutil.which("openscad") is None:
                    print(
                        "[WARN] OpenSCAD executable not found – cannot export "
                        "SCAD models."
                    )
                    break

                with tempfile.TemporaryDirectory() as tmpdir:
                    stl_path = Path(tmpdir) / f"{scad_path.stem}.stl"

                    # Export SCAD -> STL (STL is always supported)
                    print(
                        f"[INFO] Exporting {scad_path.name} -> "
                        f"{stl_path.name} (intermediate STL)…"
                    )
                    subprocess.run(
                        [
                            "openscad",
                            "-o",
                            str(stl_path),
                            str(scad_path),
                        ],
                        check=True,
                    )

                    # Convert STL -> OBJ using trimesh
                    msg = "[INFO] Converting %s -> %s …" % (
                        stl_path.name,
                        obj_path.name,
                    )
                    print(msg)
                    mesh = trimesh.load_mesh(stl_path, file_type="stl")
                    mesh.export(obj_path, file_type="obj")
        except Exception as exc:
            print(f"[ERROR] Failed to export {scad_path.name}: {exc}")


@app.route("/")
def index():
    # Ensure OBJ models are up to date with SCAD sources.
    ensure_obj_models()
    objs = sorted(p.name for p in MODEL_DIR.glob("*.obj"))
    return render_template("index.html", models=objs)


@app.route("/models/<path:filename>")
def models(filename):
    return send_from_directory(MODEL_DIR, filename)


if __name__ == "__main__":
    # Hard-coded port chosen arbitrarily within the dynamic/private range.
    port = 42165
    print(f"Starting Flask development server on port {port}…")
    app.run(debug=True, port=port)
