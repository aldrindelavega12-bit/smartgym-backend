from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

DB_CONFIG = { 
	"host": "shortline.proxy.rlwy.net", 
	"user": "root", 
	"password": "bRQXvdMKWBmfeaABLzmdOVaCqkmzonoL", 
	"database": "railway", 
	"port": 50506 
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route("/api/sync_attendance", methods=["POST"])
def sync_attendance():

    try:

        data = request.get_json()

        user_id = data.get("user_id")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attendance_sessions
            (user_id, time_in, status)
            VALUES (%s, NOW(), 'ACTIVE')
        """, (user_id,))

        conn.commit()

        conn.close()

        return jsonify({
            "success": True
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
