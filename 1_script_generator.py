import os
import datetime
from openai import OpenAI
import config

# Setup Client for OpenRouter
client = OpenAI(
    base_url=config.OPENROUTER_BASE_URL,
    api_key=config.OPENROUTER_API_KEY,
)

def generate_ideas(niche):
    """Generates 5 video topic ideas using the configured free model."""
    try:
        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a YouTube Strategist."},
                {"role": "user", "content": f"Give me 5 viral 60-second video topics for a channel about {niche}. Return only the titles, one per line, no numbering."}
            ],
            extra_headers={
                "HTTP-Referer": "https://github.com",
                "X-Title": "YouTube Automation Bot",
            }
        )
        content = response.choices[0].message.content
        return [line for line in content.split('\n') if line.strip()]
    except Exception as e:
        print(f"Error generating ideas for {niche}: {e}")
        return []

def generate_script(title, system_prompt):
    """Generates the full script."""
    try:
        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a script for a video titled: '{title}'. Include visual cues in brackets [Like this]."}
            ],
            extra_headers={
                "HTTP-Referer": "https://github.com",
                "X-Title": "YouTube Automation Bot",
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating script for {title}: {e}")
        return "Error generating script."

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    production_dir = os.path.join(config.BASE_DIR, f"Run_{timestamp}")
    
    if not os.path.exists(production_dir):
        os.makedirs(production_dir)

    print(f"🚀 Starting Batch Production Run: {timestamp}")
    print(f"🤖 Using Model: {config.MODEL_NAME}")

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
            # Clean title logic
            clean_title = title.replace('"', '').replace(':', '').replace('/', '').replace('.', '').replace('*', '').strip()
            # Remove leading numbers if the model added them (e.g. "1. Topic")
            if len(clean_title) > 0 and clean_title[0].isdigit():
                clean_title = clean_title.lstrip('0123456789.- ')
                
            if not clean_title: continue
            
            print(f"   ✍️ Writing Script: {clean_title}")
            script_content = generate_script(clean_title, prompt)
            
            # Save to file
            filename = f"{i+1}_{clean_title[:30]}.txt"
            with open(os.path.join(channel_path, filename), "w", encoding='utf-8') as f:
                f.write(f"TITLE: {clean_title}\n\n")
                f.write(script_content)

    print(f"\n✅ Scripts generated in '{production_dir}'")

if __name__ == "__main__":
    main()
