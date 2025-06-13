import requests
import datetime

BOT_TOKEN = "8087581054:AAGhSYcbiOraPHjANJSCg9Bq53aYS62S77U"
CHAT_ID = "1155086635"
LOG_FILE = "/home/user/Desktop/scripts/alert.log"  # <- Chemin vers le log

def log_message(content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {content}\n")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        error_msg = f"❌ Erreur envoi Telegram: {response.text}"
        print(error_msg)
        log_message(error_msg)

def get_fear_and_greed():
    response = requests.get("https://api.alternative.me/fng/?limit=1&format=json")
    data = response.json()
    value = int(data["data"][0]["value"])
    label = data["data"][0]["value_classification"]
    return value, label

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    price = response.json()["bitcoin"]["usd"]
    return price

def main():
    value, label = get_fear_and_greed()
    btc_price = get_btc_price()
    price_str = f"${btc_price:,.0f}"  # Format propre, sans décimales

    if label == "Extreme Fear":
        message = f"🧊 EXTREME FEAR ({value}) → Utiliser 2% pour acheter du BTC à {price_str} 💰"
    elif label == "Fear":
        message = f"🥶 FEAR ({value}) → Utiliser 1% pour acheter du BTC à {price_str} 💰"
    elif label == "Extreme Greed":
        message = f"🔥 EXTREME GREED ({value}) → Utiliser 2% pour vendre du BTC à {price_str} 🚨"
    elif label == "Greed":
        message = f"😈 GREED ({value}) → Utiliser 1% pour vendre du BTC à {price_str} 🚨"
    else:
        message = f"😐 Indice neutre ({value}) → Enjoy your day, rien à faire à part attendre que les marchés s'emballent."

    send_telegram_message(message)
    log_message(message)

if __name__ == "__main__":
    main()
