import http.client
import urllib.parse
import json

API_KEY = "edd6a658f3c25c564782b1447b1f753c"

def send_sms(number, message):
    try:

        payload = urllib.parse.urlencode({
            "apikey": API_KEY,
            "number": number,
            "message": message,
            "sendername": "SMARTGYM"
        })

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        connection = http.client.HTTPSConnection(
            "semaphore.co",
            timeout=15
        )

        connection.request(
            "POST",
            "/api/v4/messages",
            body=payload,
            headers=headers
        )

        response = connection.getresponse()

        response_body = response.read().decode("utf-8")

        connection.close()

        print("========== SEMAPHORE ==========")
        print("NUMBER:", number)
        print("HTTP STATUS:", response.status)
        print("RESPONSE:", response_body)
        print("===============================")

        if response.status != 200:
            print("❌ Semaphore HTTP error:", response.status)
            return False

        result = json.loads(response_body)

        if not result:
            print("❌ Empty Semaphore response")
            return False

        status = result[0].get("status")

        if status in ["Pending", "Queued"]:
            print(f"✅ SMS accepted for {number}")
            return True

        print("❌ Semaphore rejected:", result)
        return False

    except Exception as e:
        print("🔥 SMS ERROR:", repr(e))
        return False