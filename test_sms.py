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
        print("\nResponse:", result)

        if result and 'status' in result[0]:
            if result[0]['status'] == 'Queued':
                print("✅ SMS SENT SUCCESSFULLY")
            else:
                print("❌ FAILED:", result)
        else:
            print("⚠️ Unexpected response:", result)

    except Exception as e:
        print("ERROR:", e)


number = input("Enter phone (639XXXXXXXXX): ")
name = input("Enter name: ")

message = f"Hello {name}, your gym payment is due. - SMARTGYM"

send_sms(number, message)
