from pathlib import Path

from flask import Flask, render_template


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    @app.route("/")
    def index():
        model_dir = Path(app.static_folder) / "models"
        models = [p.name for p in model_dir.glob("*.obj")]
        return render_template("index.html", models=models)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
