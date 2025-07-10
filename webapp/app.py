from pathlib import Path

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


MODEL_DIR = Path(__file__).resolve().parent / "static" / "models"


@app.route("/")
def index():
    objs = [p.name for p in MODEL_DIR.glob("*.obj")]
    return render_template("index.html", models=objs)


@app.route("/models/<path:filename>")
def models(filename):
    return send_from_directory(MODEL_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
