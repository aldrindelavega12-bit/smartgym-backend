import requests

API_KEY = "edd6a658f3c25c564782b1447b1f753c"

def send_sms(number, message):
    try:
        response = requests.post(
            "https://semaphore.co/api/v4/messages",
            data={
                'apikey': API_KEY,
                'number': number,
                'message': message,
                'sendername': 'SMARTGYM'
            }
        )

        result = response.json()

        if result and 'status' in result[0]:
            if result[0]['status'] in ['Pending', 'Queued']:
                print(f"✅ SMS sent to {number}")
                return True
            else:
                print("❌ Failed:", result)
                return False

    except Exception as e:
        print("ERROR:", e)
        return False
