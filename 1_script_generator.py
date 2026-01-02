import os
import datetime
import time
from openai import OpenAI
import config

# Setup Client
client = OpenAI(
    base_url=config.OPENROUTER_BASE_URL,
    api_key=config.OPENROUTER_API_KEY,
)

def get_completion_with_retry(messages):
    """Tries to get a response using the model list with fallback logic."""
    
    for model in config.MODEL_LIST:
        try:
            # print(f"   🤖 Trying model: {model}...") 
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                extra_headers={
                    "HTTP-Referer": "https://github.com",
                    "X-Title": "YouTube Automation Bot",
                }
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Rate limit" in error_msg:
                print(f"   ⚠️ Rate limit hit on {model}. Switching...")
                time.sleep(5) # Short cool-off
                continue # Try next model
            else:
                print(f"   ❌ Error on {model}: {e}")
                continue
                
    print("   ❌ All models failed.")
    return None

def generate_ideas(niche):
    messages = [
        {"role": "system", "content": "You are a YouTube Strategist."},
        {"role": "user", "content": f"Give me 5 engaging, long-form (10 minute+) video topics for a channel about {niche}. Return only the titles, one per line, no numbering."}
    ]
    
    content = get_completion_with_retry(messages)
    
    if content:
        return [line for line in content.split('\n') if line.strip()]
    return []

def generate_script(title, system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Write a comprehensive, long-form script for a video titled: '{title}'. Include visual cues in brackets [Like this]. Break it down into sections."}
    ]
    return get_completion_with_retry(messages)

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    production_dir = os.path.join(config.BASE_DIR, f"Run_LongForm_{timestamp}")
    
    if not os.path.exists(production_dir):
        os.makedirs(production_dir)

    print(f"🚀 Starting Production Run: {timestamp}")

    for channel_name, prompt in config.CHANNEL_PROMPTS.items():
        print(f"\n📺 Processing Channel: {channel_name}...")
        
        channel_path = os.path.join(production_dir, channel_name)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)

        # 1. Get Ideas
        print("   Thinking of ideas...")
        titles = generate_ideas(channel_name)
        
        # 2. Write Scripts
        for i, title in enumerate(titles):
            clean_title = title.replace('"', '').replace(':', '').replace('/', '').replace('.', '').replace('*', '').strip()
            if len(clean_title) > 0 and clean_title[0].isdigit():
                clean_title = clean_title.lstrip('0123456789.- ')
                
            if not clean_title: continue
            
            print(f"   ✍️ Writing Script: {clean_title}")
            script_content = generate_script(clean_title, prompt)
            
            if script_content:
                filename = f"{i+1}_{clean_title[:30]}.txt"
                with open(os.path.join(channel_path, filename), "w", encoding='utf-8') as f:
                    f.write(f"TITLE: {clean_title}\n\n")
                    f.write(script_content)

    print(f"\n✅ Scripts generated in '{production_dir}'")

if __name__ == "__main__":
    main()
