import requests
import traceback

API_KEY = "edd6a658f3c25c564782b1447b1f753c"

def send_sms(number, message):
    try:
        response = requests.post(
            "https://semaphore.co/api/v4/messages",
            data={
                "apikey": API_KEY,
                "number": number,
                "message": message,
                "sendername": "SMARTGYM"
            },
            timeout=15
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        result = response.json()

        if result and "status" in result[0]:
            if result[0]["status"] in ["Pending", "Queued"]:
                return True

        print("SMS FAILED:", result)
        return False

    except Exception as e:
        print("🔥 SMS ERROR:", repr(e))
        traceback.print_exc()
        return False