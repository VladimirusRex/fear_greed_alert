# Fear & Greed Alert Bot

Ce script est un bot Telegram qui surveille l'indice de peur et d'avidité (Fear & Greed Index) des marchés financiers et le prix du Bitcoin (BTC) en USD. Il envoie des alertes personnalisées via Telegram en fonction des niveaux d'émotion du marché, suggérant des actions d'achat ou de vente avec des pourcentages prédéfinis.

## Fonctionnalités
- Récupère l'indice Fear & Greed via l'API d'Alternative.me.
- Obtient le prix actuel du Bitcoin via l'API de CoinGecko.
- Envoie des messages Telegram avec des recommandations :
  - **Extreme Fear** : Acheter 2% de BTC.
  - **Fear** : Acheter 1% de BTC.
  - **Extreme Greed** : Vendre 2% de BTC.
  - **Greed** : Vendre 1% de BTC.
  - **Neutre** : Pas d'action, attendre.
- Enregistre les logs avec horodatage.

## Prérequis
- **Python 3.x** installé.
- Les bibliothèques suivantes (installez-les avec `pip`):
  - `requests` : Pour les appels API.
  - `python-telegram-bot` (facultatif, si tu étends avec un bot interactif).
- **Variables d'environnement** :
  - `BOT_TOKEN` : Token de ton bot Telegram (obtenu via @BotFather).
  - `CHAT_ID` : ID de la conversation Telegram où envoyer les messages.

## Installation
1. Clone ce repository :
   ```bash
   git clone <[URL-du-repo](https://github.com/VladimirusRex/fear_greed_alert.git)>
   cd feargreedalert
