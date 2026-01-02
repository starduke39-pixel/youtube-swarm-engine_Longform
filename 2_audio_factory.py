import os
import requests
import config
import re

def generate_audio(text, voice_id, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": config.ELEVENLABS_API_KEY
    }
    
    # Simple cleanup to remove visual cues in brackets []
    clean_text = re.sub(r'\[.*?\]', '', text)
    
    data = {
        "text": clean_text,
        "model_id": "eleven_turbo_v2", 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"   ✅ Audio Saved: {os.path.basename(output_path)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

def run_audio_batch():
    if not os.path.exists(config.BASE_DIR):
        print("No production directory found. Run Step 1 first.")
        return
        
    runs = sorted(os.listdir(config.BASE_DIR))
    if not runs:
        print("No runs found.")
        return
        
    latest_run = os.path.join(config.BASE_DIR, runs[-1])
    print(f"🎙️ Generating Audio for: {latest_run}")

    for channel_name, voice_id in config.VOICE_MAP.items():
        channel_path = os.path.join(latest_run, channel_name)
        
        if os.path.exists(channel_path):
            print(f"\nProcessing {channel_name}...")
            files = [f for f in os.listdir(channel_path) if f.endswith(".txt")]
            
            for filename in files:
                file_path = os.path.join(channel_path, filename)
                
                # Read Script
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove header if present
                text_to_speak = content.split('TITLE:')[-1] 
                
                audio_filename = filename.replace('.txt', '.mp3')
                audio_path = os.path.join(channel_path, audio_filename)
                
                if not os.path.exists(audio_path):
                    generate_audio(text_to_speak, voice_id, audio_path)
                else:
                    print(f"   ⏩ Skipping {audio_filename} (Exists)")

if __name__ == "__main__":
    run_audio_batch()
