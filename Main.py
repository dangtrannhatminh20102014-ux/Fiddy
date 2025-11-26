from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

KEY_FILE = "keys.json"

# Load key từ file nếu có, nếu không tạo mới
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "r") as f:
        VALID_KEYS = json.load(f)
else:
    VALID_KEYS = []
    with open(KEY_FILE, "w") as f:
        json.dump(VALID_KEYS, f)

# API check key
@app.route("/check_key", methods=["GET"])
def check_key():
    key = request.args.get("key")
    if key in VALID_KEYS:
        return jsonify({"status": "ok", "message": "Key hợp lệ"})
    return jsonify({"status": "error", "message": "Key sai"})

# API add key
@app.route("/add_key", methods=["POST"])
def add_key():
    data = request.json
    key = data.get("key")
    if not key:
        return jsonify({"status": "error", "message": "Không có key"}), 400
    if key in VALID_KEYS:
        return jsonify({"status": "error", "message": "Key đã tồn tại"}), 400

    VALID_KEYS.append(key)
    with open(KEY_FILE, "w") as f:
        json.dump(VALID_KEYS, f)
    return jsonify({"status": "ok", "message": f"Đã thêm key {key}"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
