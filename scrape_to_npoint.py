import requests
from bs4 import BeautifulSoup
import json
import sys

# 1. Scrape Nitter
URL = "https://nitter.net/UEFrance"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

try:
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    stats = soup.find_all('span', class_='profile-stat-num')
    
    # Nitter order: Tweets, Following, Followers, Likes
    follower_count = stats[2].text.replace(',', '').strip()
except Exception as e:
    print(f"Scraping failed: {e}")
    sys.exit(1)

# 2. Update Npoint
# Use your specific Npoint ID: 5c1ef38596efbfb2bfe9
NPOINT_URL = "https://api.npoint.io/5c1ef38596efbfb2bfe9"
payload = {"followers": follower_count, "last_updated": "2026-02-02"} # Update date dynamically if needed

update_res = requests.post(NPOINT_URL, json=payload)

if update_res.status_code == 200:
    print("Successfully updated Npoint!")
else:
    print(f"Failed to update Npoint: {update_res.status_code}")
