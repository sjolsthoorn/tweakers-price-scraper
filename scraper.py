import requests
import schedule
import time
from bs4 import BeautifulSoup

WEBHOOK_URL = 'DISCORD_URL'
TARGET_URL = 'https://tweakers.net/pricewatch/1808930/samsung-oled-qd-s95b-65-inch-zilver.html'
PRICE_FILE = 'price.txt'

print('|| Tweakers Scrapper v1.0 ||')
print('Checking Tweakers every hour for new price.')
print('Now running...')

def get_price_from_web():
    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.select_one('.price')
    
    if price_element:
        return price_element.text.strip()
    return None

def send_to_discord(price):
    data = {
        "content": f"The price has changed! New price: {price}"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_price():
    current_price = get_price_from_web()
    print('Checking price')
    if not current_price:
        print("Failed to fetch the price!")
        return

    # Check against old price
    try:
        with open(PRICE_FILE, 'r') as f:
            old_price = f.read().strip()

        if old_price != current_price:
            send_to_discord(current_price)
            with open(PRICE_FILE, 'w') as f:
                f.write(current_price)
    except FileNotFoundError:
        send_to_discord(current_price)
        with open(PRICE_FILE, 'w') as f:
            f.write(current_price)

# Schedule the check every hour
schedule.every().hour.do(check_price)

while True:
    schedule.run_pending()
    time.sleep(1)