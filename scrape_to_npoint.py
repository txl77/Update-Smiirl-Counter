import os
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime

# Get API Key from GitHub Secrets
API_KEY = os.getenv('SCRAPINGANT_KEY')
TARGET_URL = "https://nitter.net/UEFrance"
# The proxy URL (ScrapingAnt example)
PROXY_URL = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={API_KEY}"

def get_followers():
    try:
        print(f"Requesting through proxy...")
        response = requests.get(PROXY_URL, timeout=20)
        
        if response.status_code != 200:
            print(f"Proxy error: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Nitter's followers are specifically in the 'nav-item' or 'profile-stat-num'
        # We search for the link that contains '/followers'
        follower_link = soup.find('a', href='/UEFrance/followers')
        if follower_link:
            count_span = follower_link.find('span', class_='profile-stat-num')
            if count_span:
                return count_span.text.replace(',', '').replace(' ', '').strip()
        
        # Backup: try the 3rd stat-num if the link-specific search fails
        stats = soup.find_all('span', class_='profile-stat-num')
        if len(stats) >= 3:
            return stats[2].text.replace(',', '').replace(' ', '').strip()

    except Exception as e:
        print(f"Error: {e}")
    return None

follower_count = get_followers()

if follower_count:
    # Update Npoint
    NPOINT_URL = "https://api.npoint.io/5c1ef38596efbfb2bfe9"
    payload = {
        "followers": follower_count, 
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    res = requests.post(NPOINT_URL, json=payload)
    print(f"Npoint update: {res.status_code}")
else:
    print("Failed to retrieve data even with proxy.")
    sys.exit(1)
