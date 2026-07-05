import json
from flask import Flask, request, jsonify

from sync.event_handler import handle_event

app = Flask(__name__)


@app.route("/")
def home():

    return {
        "service": "Enrollment Sync Server",
        "status": "running"
    }


@app.route("/sync/event", methods=["POST"])
def sync_event():

    try:

        # -------- FILE EVENT --------
        if request.files:

            event = {

                "event_type": request.form["event_type"],

                "payload": json.loads(
                    request.form["payload"]
                ),

                "file": request.files["file"]

            }

        # -------- JSON EVENT --------
        else:

            event = request.get_json()

        print("\n========== EVENT RECEIVED ==========")
        print(event)

        result = handle_event(event)

        print("\n========== RESULT ==========")
        print(result)
        print("============================\n")

        return jsonify(result), 200

    except Exception as e:

        print(e)

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

def start_server():

    print("[SYNC] Enrollment Server Started (5002)")

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":

    start_server()