from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "bot224917:f58ba06d-41bf-4976-a640-8c7eaab7c20f"
API_URL = f"https://eita.ir/bot{BOT_TOKEN}/sendMessage"

# پیام‌های ثابت
WELCOME_TEXT = """به ربات نذری گروه جهادی محبّان حضرت زهرا (سلام‌الله‌علیها) خوش آمدید.

اینجا جاییه برای نذر قلبی شما؛ هر چقدر دوست داشتید، هر وقت که دلتون خواست.  
کمک‌های شما صرف فعالیت‌های جهادی، فرهنگی و محرومیت‌زدایی می‌شه.

برای شروع، فقط کافیه مبلغ دلخواهتون رو وارد کنید.
"""

ASK_AMOUNT = "لطفاً مبلغ نذر دلخواه‌تون رو به *تومان* وارد کنید:\n\n(مثال: ۵۰۰۰ یا ۲۰۰۰۰)"

PAYMENT_FAKE = lambda amount: f"""اینم لینک پرداخت آزمایشی برای مبلغ {amount} تومان:

[پرداخت نذری شما](https://example.com/fakepay?amount={amount})

بعد از پرداخت، نیت خیرتون رو فراموش نکنید و مطمئن باشید که هر ریال از این نذر در راه رضای خدا و خدمت به خلق مصرف می‌شه.

خدا اجرتون بده و نذر و حاجتتون مقبول درگاه الهی.
یا زهرا (سلام‌الله‌علیها)
"""

user_states = {}

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return "ok"

    # اگر شروع بود
    if text == "/start":
        send_message(chat_id, WELCOME_TEXT)
        send_message(chat_id, ASK_AMOUNT)
        user_states[chat_id] = "waiting_for_amount"
    elif user_states.get(chat_id) == "waiting_for_amount":
        try:
            amount = int(text.strip())
            send_message(chat_id, PAYMENT_FAKE(amount), parse_mode="Markdown")
            user_states.pop(chat_id)
        except:
            send_message(chat_id, "عدد معتبر وارد کن داداشی. مثلاً: 10000")
    else:
        send_message(chat_id, "برای شروع، دستور /start رو بزن.")

    return "ok"

def send_message(chat_id, text, parse_mode=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(API_URL, json=payload)

if __name__ == "__main__":
    app.run(debug=True)