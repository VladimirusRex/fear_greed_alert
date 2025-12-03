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
# Essaie plusieurs APIs avec fallback automatique
# ─────────────────────────────
def get_btc_price():
    # API 1: Binance (la plus fiable et rapide)
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        if response.status_code == 200:
            price = float(response.json()["price"])
            log_message(f"✅ Prix BTC obtenu via Binance: ${price:,.2f}")
            return price
    except Exception as e:
        log_message(f"⚠️ Binance échoué: {e}")

    # API 2: Coinbase
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=5)
        if response.status_code == 200:
            price = float(response.json()["data"]["amount"])
            log_message(f"✅ Prix BTC obtenu via Coinbase: ${price:,.2f}")
            return price
    except Exception as e:
        log_message(f"⚠️ Coinbase échoué: {e}")

    # API 3: CoinGecko (fallback)
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
        if response.status_code == 200:
            price = float(response.json()["bitcoin"]["usd"])
            log_message(f"✅ Prix BTC obtenu via CoinGecko: ${price:,.2f}")
            return price
    except Exception as e:
        log_message(f"⚠️ CoinGecko échoué: {e}")

    # API 4: Kraken (dernier recours)
    try:
        response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSD", timeout=5)
        if response.status_code == 200:
            price = float(response.json()["result"]["XXBTZUSD"]["c"][0])
            log_message(f"✅ Prix BTC obtenu via Kraken: ${price:,.2f}")
            return price
    except Exception as e:
        log_message(f"⚠️ Kraken échoué: {e}")

    # Toutes les APIs ont échoué
    raise Exception("❌ Impossible de récupérer le prix BTC depuis toutes les sources")

# ─────────────────────────────
# 🚀 Fonction principale du script
# Construit le message Telegram selon le niveau de sentiment
# Ajoute un horodatage + emoji visuel
# ─────────────────────────────
def main():
    try:
        # 🕐 Date et heure actuelle
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # 📈 Données du jour
        log_message("🔄 Récupération de l'indice Fear & Greed...")
        value, label = get_fear_and_greed()

        log_message("🔄 Récupération du prix BTC...")
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
        log_message(f"✅ Message envoyé avec succès: {message}")

    except Exception as e:
        error_message = f"❌ Erreur dans le script: {str(e)}"
        log_message(error_message)
        # Envoyer une alerte Telegram en cas d'erreur
        try:
            send_telegram_message(f"⚠️ Erreur Fear & Greed Alert\n{error_message}")
        except:
            log_message("❌ Impossible d'envoyer l'alerte d'erreur via Telegram")

# ─────────────────────────────
# ▶️ Lancement du script
# ─────────────────────────────
if __name__ == "__main__":
    main()
