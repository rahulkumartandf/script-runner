from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

SCRIPTS_DIR = "scripts"

@app.route("/")
def home():
    return {"status": "ok", "message": "Script Runner API"}

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()
    script_name = data.get("script")

    if not script_name or not script_name.endswith(".py"):
        return jsonify({"error": "Invalid script"}), 400

    script_path = os.path.join(SCRIPTS_DIR, script_name)

    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True, text=True, check=True
        )
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
