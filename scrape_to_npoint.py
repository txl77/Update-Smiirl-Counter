import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime

# A list of reliable Nitter instances to try
INSTANCES = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://xcancel.com"
]

def get_followers():
    for instance in INSTANCES:
        url = f"{instance}/UEFrance"
        print(f"Trying {url}...")
        
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for the specific stat-num class
            stats = soup.find_all('span', class_='profile-stat-num')
            
            if len(stats) >= 3:
                # Success! Extract and clean the number
                count = stats[2].text.replace(',', '').replace(' ', '').strip()
                print(f"Found followers: {count}")
                return count
        except Exception as e:
            print(f"Failed on {instance}: {e}")
            continue
            
    return None

# Execution
follower_count = get_followers()

if follower_count:
    NPOINT_URL = "https://api.npoint.io/5c1ef38596efbfb2bfe9"
    payload = {
        "followers": follower_count, 
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    update_res = requests.post(NPOINT_URL, json=payload)
    if update_res.status_code == 200:
        print("Successfully updated Npoint!")
    else:
        print(f"Failed to update Npoint: {update_res.status_code}")
else:
    print("All instances failed. Nitter might be experiencing heavy blocks.")
    sys.exit(1)
