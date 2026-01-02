import os
import datetime
import time
import google.generativeai as genai
import config

# Setup Gemini
genai.configure(api_key=config.GOOGLE_API_KEY)
model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)

def generate_content_gemini(prompt):
    """Wrapper to call Gemini with error handling"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"   ❌ Gemini Error: {e}")
        # Simple backoff
        time.sleep(2)
        return None

def generate_ideas(niche):
    print(f"   🧠 Brainstorming topics for {niche}...")
    prompt = f"You are a YouTube Strategist. Give me 5 engaging, long-form (10 minute+) video topics for a channel about {niche}. Return only the titles, one per line, no numbering."
    
    content = generate_content_gemini(prompt)
    
    if content:
        return [line for line in content.split('\n') if line.strip()]
    return []

def generate_script(title, system_role):
    print(f"   ✍️ Writing Script: {title}...")
    prompt = f"{system_role} Write a comprehensive, long-form script for a video titled: '{title}'. Include visual cues in brackets [Like this]. Break it down into sections."
    
    return generate_content_gemini(prompt)

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    production_dir = os.path.join(config.BASE_DIR, f"Run_LongForm_{timestamp}")
    
    if not os.path.exists(production_dir):
        os.makedirs(production_dir)

    print(f"🚀 Starting Gemini Production Run: {timestamp}")

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
