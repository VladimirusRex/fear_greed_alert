# ───────────────────────────────────────────────────────────────
# Script GitHub Actions : Alerte Telegram Fear & Greed + prix BTC
# Récupère :
# - L’indice de sentiment du marché (via Alternative.me)
# - Le prix du BTC (via CoinGecko)
# Envoie un message Telegram selon le niveau de sentiment.
# ───────────────────────────────────────────────────────────────

import requests
import datetime
import os

# ─────────────────────────────
# 📦 Variables d’environnement
# BOT_TOKEN : token du bot Telegram
# CHAT_ID   : identifiant du canal / utilisateur
# ─────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ─────────────────────────────
# 📋 Fonction de log avec timestamp
# Affiche le message dans les logs GitHub Actions
# ─────────────────────────────
def log_message(content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {content}")

# ─────────────────────────────
# 📤 Fonction d’envoi de message Telegram
# Utilise l’API Telegram Bot
# ─────────────────────────────
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        error_msg = f"❌ Erreur envoi Telegram: {response.text}"
        print(error_msg)
        log_message(error_msg)

# ─────────────────────────────
# 📊 Fonction pour récupérer l’indice Fear & Greed
# Via l’API Alternative.me → renvoie (valeur, label)
# ─────────────────────────────
def get_fear_and_greed():
    response = requests.get("https://api.alternative.me/fng/?limit=1&format=json")
    data = response.json()
    value = int(data["data"][0]["value"])
    label = data["data"][0]["value_classification"]
    return value, label

# ─────────────────────────────
# 💰 Fonction pour récupérer le prix BTC (en USD)
# Via l’API CoinGecko
# ─────────────────────────────
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    price = response.json()["bitcoin"]["usd"]
    return price

# ─────────────────────────────
# 🚀 Fonction principale du script
# Construit le message Telegram selon le niveau de sentiment
# Ajoute un horodatage + emoji visuel
# ─────────────────────────────
def main():
    # 🕐 Date et heure actuelle
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 📈 Données du jour
    value, label = get_fear_and_greed()
    btc_price = get_btc_price()
    price_str = f"${btc_price:,.0f}"

    # 🧠 Mapping du label → message avec emojis + recommandations
    if label == "Extreme Fear":
        sentiment = "🟣 EXTREME FEAR"
        message = f"{now} • {sentiment} ({value})\n→ Utiliser 2% pour acheter du BTC à {price_str} 💰"
    elif label == "Fear":
        sentiment = "🟦 FEAR"
        message = f"{now} • {sentiment} ({value})\n→ Utiliser 1% pour acheter du BTC à {price_str} 💰"
    elif label == "Extreme Greed":
        sentiment = "🔴 EXTREME GREED"
        message = f"{now} • {sentiment} ({value})\n→ Utiliser 2% pour vendre du BTC à {price_str} 🚨"
    elif label == "Greed":
        sentiment = "🟡 GREED"
        message = f"{now} • {sentiment} ({value})\n→ Utiliser 1% pour vendre du BTC à {price_str} 🚨"
    else:
        sentiment = "😐 NEUTRE"
        message = f"{now} • {sentiment} ({value})\n→ Rien à faire, attendre que les marchés bougent."

    # 📤 Envoi et log
    send_telegram_message(message)
    log_message(message)

# ─────────────────────────────
# ▶️ Lancement du script
# ─────────────────────────────
if __name__ == "__main__":
    main()
