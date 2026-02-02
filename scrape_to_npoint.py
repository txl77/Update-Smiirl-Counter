import os
import requests
from bs4 import BeautifulSoup
import sys

# Configuration
API_KEY = os.getenv('SCRAPINGANT_KEY')
NPOINT_ID = "5c1ef38596efbfb2bfe9"
TARGET_URL = "https://nitter.net/UEFrance"

def parse_nitter_number(text):
    """Converts strings like '10.5K' or '1,200' into pure numbers."""
    text = text.upper().replace(',', '').replace(' ', '').strip()
    if 'K' in text:
        return str(int(float(text.replace('K', '')) * 1000))
    if 'M' in text:
        return str(int(float(text.replace('M', '')) * 1000000))
    return text

def get_followers():
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={API_KEY}"
    
    try:
        response = requests.get(proxy_url, timeout=30)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # Target the specific follower link
        follower_link = soup.find('a', href=lambda x: x and '/followers' in x)
        
        if follower_link:
            raw_count = follower_link.find('span', class_='profile-stat-num').text
            return parse_nitter_number(raw_count)
            
    except Exception as e:
        print(f"Error: {e}")
    return None

# Execution
followers = get_followers()

if followers:
    # We only send the 'number' key as requested
    payload = {"number": followers}
    
    update_url = f"https://api.npoint.io/{NPOINT_ID}"
    res = requests.post(update_url, json=payload)
    
    if res.status_code == 200:
        print(f"Success! Npoint updated with: {payload}")
    else:
        print(f"Failed to update Npoint. Status: {res.status_code}")
else:
    print("Could not retrieve followers.")
    sys.exit(1)
