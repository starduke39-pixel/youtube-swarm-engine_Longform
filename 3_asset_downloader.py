import os
import requests
import config
import random  # Added for variety

# UPDATED SETTINGS
VIDEOS_PER_SEARCH = 10 
ORIENTATION = "landscape" 

def search_and_download(query, save_folder):
    print(f"\n🔍 Searching Pexels for: '{query}'...")
    
    # RANDOMIZATION MAGIC:
    # Pick a random page between 1 and 10 so we don't get the same videos every time
    random_page = random.randint(1, 10)
    
    headers = {'Authorization': config.PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={VIDEOS_PER_SEARCH}&orientation={ORIENTATION}&size=medium&page={random_page}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error connecting to Pexels: {response.status_code}")
            return

        data = response.json()
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        videos = data.get('videos', [])
        if not videos:
            print(f"   ⚠️ No videos found on page {random_page}. Trying page 1.")
            # Fallback to page 1 if random page is empty
            url = f"https://api.pexels.com/videos/search?query={query}&per_page={VIDEOS_PER_SEARCH}&orientation={ORIENTATION}&size=medium&page=1"
            response = requests.get(url, headers=headers)
            videos = response.json().get('videos', [])

        for video in videos:
            # Pick the HD version (1920x1080 or 1280x720)
            video_files = video.get('video_files', [])
            target_file = next((v for v in video_files if v['width'] >= 1280), video_files[0])
            
            download_url = target_file['link']
            file_name = f"{video['id']}.mp4"
            full_path = os.path.join(save_folder, file_name)
            
            if not os.path.exists(full_path):
                print(f"   ⬇️ Downloading: {file_name}")
                with open(full_path, 'wb') as f:
                    f.write(requests.get(download_url).content)
            else:
                print(f"   ⏩ Skipping {file_name}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    asset_dir = os.path.join(config.BASE_DIR, "Stock_Footage_Landscape")
    
    # Keywords
    search_map = {
        "Ancient_Echoes": ["Greek Temple", "Clouds Timelapse", "Fire", "Forest", "Galaxy"],
        "Abyss_Archives": ["Crime Scene tape", "Ocean Waves", "Glitch", "Foggy Forest", "Old Documents"],
        "Apex_Lists": ["Yacht", "Mansion Interior", "Gold Bullion", "Champagne", "Private Jet"],
        "Mind_Architect": ["Chess Board", "Statue", "Man Writing", "Sunrise", "Mountain"],
        "Trivia_Core": ["Clock Ticking", "Neural Network", "Abstract Blue", "Thinking Man"]
    }

    for channel, keywords in search_map.items():
        channel_asset_dir = os.path.join(asset_dir, channel)
        for keyword in keywords:
            search_and_download(keyword, channel_asset_dir)

if __name__ == "__main__":
    main()
