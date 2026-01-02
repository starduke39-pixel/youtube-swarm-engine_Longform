import os
import datetime
import time
import requests
import config

def call_gemini(prompt, system_role="You are a helpful assistant."):
    """Direct HTTP call to Google Gemini API to avoid library issues."""
    if not config.GOOGLE_API_KEY:
        print("   ❌ Error: GOOGLE_API_KEY is missing.")
        return None

    url = f"{config.GEMINI_API_URL}?key={config.GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Gemini API Payload
    payload = {
        "contents": [{
            "parts": [{"text": f"{system_role}\n\n{prompt}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"   ❌ API Error {response.status_code}: {response.text}")
            return None
            
        result = response.json()
        # Parse the JSON response
        return result['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        time.sleep(2)
        return None

def generate_ideas(niche):
    print(f"   🧠 Brainstorming topics for {niche}...")
    prompt = f"Give me 5 engaging, long-form (10 minute+) video topics for a YouTube channel about {niche}. Return only the titles, one per line, no numbering."
    
    content = call_gemini(prompt, "You are a YouTube Strategist.")
    
    if content:
        return [line for line in content.split('\n') if line.strip()]
    return []

def generate_script(title, system_role):
    print(f"   ✍️ Writing Script: {title}...")
    prompt = f"Write a comprehensive, long-form script for a video titled: '{title}'. Include visual cues in brackets [Like this]. Break it down into sections."
    
    return call_gemini(prompt, system_role)

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    production_dir = os.path.join(config.BASE_DIR, f"Run_LongForm_{timestamp}")
    
    if not os.path.exists(production_dir):
        os.makedirs(production_dir)

    print(f"🚀 Starting Gemini (Direct API) Run: {timestamp}")

    for channel_name, role_prompt in config.CHANNEL_PROMPTS.items():
        print(f"\n📺 Processing Channel: {channel_name}...")
        
        channel_path = os.path.join(production_dir, channel_name)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)

        # 1. Get Ideas
        titles = generate_ideas(channel_name)
        
        # 2. Write Scripts
        for i, title in enumerate(titles):
            clean_title = title.replace('"', '').replace(':', '').replace('/', '').replace('.', '').replace('*', '').strip()
            if len(clean_title) > 0 and clean_title[0].isdigit():
                clean_title = clean_title.lstrip('0123456789.- ')
                
            if not clean_title: continue
            
            script_content = generate_script(clean_title, role_prompt)
            
            if script_content:
                filename = f"{i+1}_{clean_title[:30]}.txt"
                with open(os.path.join(channel_path, filename), "w", encoding='utf-8') as f:
                    f.write(f"TITLE: {clean_title}\n\n")
                    f.write(script_content)

    print(f"\n✅ Scripts generated in '{production_dir}'")

if __name__ == "__main__":
    main()
