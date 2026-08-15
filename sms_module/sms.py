import requests

API_KEY = "edd6a658f3c25c564782b1447b1f753c"

SEMAPHORE_URL = "https://semaphore.co/api/v4/messages"


def send_sms(number, message):

    try:

        response = requests.post(
            SEMAPHORE_URL,
            data={
                "apikey": API_KEY,
                "number": number,
                "message": message,
                "sendername": "SMARTGYM"
            },
            timeout=15
        )

        print("========== SEMAPHORE ==========")
        print("NUMBER:", number)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("===============================")

        if response.status_code != 200:
            return False

        result = response.json()

        if not result:
            return False

        status = result[0].get("status")

        if status in ["Pending", "Queued"]:
            print(f"SMS accepted for {number}")
            return True

        print("SMS rejected:", result)
        return False

    except Exception as e:

        print("SMS ERROR:", repr(e))

        return False