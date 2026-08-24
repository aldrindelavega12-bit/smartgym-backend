import json
from flask import Flask, request, jsonify

from sync.event_handler import handle_event


app = Flask(__name__)

# ==========================================
# SHARED FINGERPRINT MANAGER
# ==========================================

fp_manager = None


@app.route("/")
def home():

    return {
        "service": "Enrollment Sync Server",
        "status": "running"
    }


@app.route("/sync/event", methods=["POST"])
def sync_event():

    try:

        # ==========================================
        # FILE EVENT
        # ==========================================

        if request.files:

            event = {

                "event_type": request.form["event_type"],

                "payload": json.loads(
                    request.form["payload"]
                ),

                "file": request.files["file"]

            }

        # ==========================================
        # JSON EVENT
        # ==========================================

        else:

            event = request.get_json()


        print("\n========== EVENT RECEIVED ==========")
        print(event)


        # ==========================================
        # HANDLE EVENT
        # ==========================================

        result = handle_event(
            event,
            fp_manager
        )


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


# ==========================================
# START SERVER
# ==========================================

def start_server(manager=None):

    global fp_manager

    # Receive the SAME FingerprintManager
    # created by main.py

    fp_manager = manager


    print("[SYNC] Enrollment Server Started (5002)")


    app.run(

        host="0.0.0.0",

        port=5002,

        debug=False,

        use_reloader=False

    )


# ==========================================
# STANDALONE MODE
# ==========================================

if __name__ == "__main__":

    start_server()