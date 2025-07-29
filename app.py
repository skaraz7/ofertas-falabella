from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    json_path = os.path.join("data", "ofertas_falabella_completo.json")
    with open(json_path, "r", encoding="utf-8") as f:
        productos = json.load(f)
    return render_template("ofertas.html", productos=productos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
