import requests

def send_sms(number, message):
    try:
        response = requests.post(
            "https://semaphore.co/api/v4/messages",
            data={
                'apikey': 'edd6a658f3c25c564782b1447b1f753c',
                'number': number,
                'message': message,
                
            }
        )

        result = response.json()
        print("Response:", result)

        if result and result[0]['status'] == 'Queued':
            print("✅ SMS SENT")
        else:
            print("❌ FAILED", result)

    except Exception as e:
        print("ERROR:", e)


# 🔥 TEST
send_sms("09913354822", "Smart Gym test SMS 💪")