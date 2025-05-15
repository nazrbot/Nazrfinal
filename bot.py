import requests
import time

TOKEN = 'bot224917:f58ba06d-41bf-4976-a640-8c7eaab7c20f'  # توکن خودت
CHAT_ID = 72446171  # آیدی چت یا گروه خودت

def send_message(text):
    url = f'https://eitaayar.ir/api/{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'date': int(time.time()) + 30
    }
    response = requests.post(url, data=payload)
    print('Response:', response.json())

if __name__ == '__main__':
    send_message('سلام! ربات محبان حضرت زهرا آماده‌ست.')
