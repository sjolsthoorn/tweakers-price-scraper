urls_and_files = {
    'https://tweakers.net/pricewatch/1808930/samsung-oled-qd-s95b-65-inch-zilver.html': 'price_samsung_tv.txt',
    'https://tweakers.net/pricewatch/1828616/samsung-hw-q800b.html': 'price_samsung_soundbar.txt',
}

import requests
import schedule
import time
from bs4 import BeautifulSoup

WEBHOOK_URL = ''

print('|| Tweakers Scrapper v2.0 ||')
print('Checking Tweakers every hour for new prices.')
print('Now running...')

def get_price_from_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.select_one('.price')
    
    if price_element:
        return price_element.text.strip()
    return None

def send_to_discord(price, url):
    data = {
        "content": f"The price for {url} has changed! New price: {price}"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_price():
    for url, file_name in urls_and_files.items():
        current_price = get_price_from_web(url)
        print(f'Checking price for {url}')
        
        if not current_price:
            print(f"Failed to fetch the price for {url}!")
            continue

        # Check against old price
        try:
            with open(file_name, 'r') as f:
                old_price = f.read().strip()

            if old_price != current_price:
                send_to_discord(current_price, url)
                with open(file_name, 'w') as f:
                    f.write(current_price)
        except FileNotFoundError:
            send_to_discord(current_price, url)
            with open(file_name, 'w') as f:
                f.write(current_price)

check_price();

# Schedule the check every hour
schedule.every().hour.do(check_price)

while True:
    schedule.run_pending()
    time.sleep(1)
