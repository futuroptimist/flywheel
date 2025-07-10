from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    obj_dir = Path(app.static_folder) / "objs"
    obj_files = sorted(obj_dir.glob("*.obj"))
    obj_file = obj_files[0].name if obj_files else ""
    return render_template("index.html", obj_file=obj_file)


if __name__ == "__main__":
    app.run(debug=True)
