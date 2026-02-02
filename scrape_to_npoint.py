import os
import requests
import sys
from ntscraper import Nitter

# Configuration
NPOINT_ID = "5c1ef38596efbfb2bfe9"
USERNAME = "UEFrance"

def get_followers():
    try:
        # Initialize the scraper
        scraper = Nitter(log_level=1, skip_instance_check=False)
        
        print(f"Fetching profile info for {USERNAME}...")
        # get_profile_info returns a dict with profile details
        profile = scraper.get_profile_info(USERNAME)
        
        if profile and 'stats' in profile:
            followers_raw = profile['stats'].get('followers', "0")
            # The library usually returns a string or int. 
            # We ensure it's a string and clean it up.
            return str(followers_raw)
            
    except Exception as e:
        print(f"Scraper error: {e}")
    return None

# Execution
followers = get_followers()

if followers:
    print(f"Success! Found {followers} followers.")
    # Send only the 'number' key to npoint
    payload = {"number": followers}
    
    update_url = f"https://api.npoint.io/{NPOINT_ID}"
    res = requests.post(update_url, json=payload)
    
    if res.status_code == 200:
        print(f"Successfully updated npoint: {payload}")
    else:
        print(f"Failed to update npoint. Status code: {res.status_code}")
else:
    print("Failed to retrieve follower count after multiple attempts.")
    sys.exit(1)
