from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

SECRET = "mysecret123"  # your chosen secret

# Root route — for browser test
@app.route('/')
def home():
    return "✅ Flask API is running. Use POST /api to send requests."

# API route — for curl / GForm / instructor task
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json(force=True)

    # Secret verification
    if not data or data.get("secret") != SECRET:
        return jsonify({"status": "error", "message": "invalid secret"}), 403

    # Print incoming task in terminal
    print("📩 Incoming task JSON:", json.dumps(data, indent=2))

    # Save task to file so you can inspect later
    task_file = "task.json"
    with open(task_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Task saved to {os.path.abspath(task_file)}")

    # Respond back to sender (instructors)
    return jsonify({
        "status": "ok",
        "message": "Task accepted",
        "note": "Round 1 request received"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
