import os
import time
from openai import OpenAI
import config

INPUT_DIR = os.path.join(config.BASE_DIR)

client = OpenAI(
    base_url=config.OPENROUTER_BASE_URL,
    api_key=config.OPENROUTER_API_KEY,
)

def get_completion_with_retry(messages):
    for model in config.MODEL_LIST:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                extra_headers={"HTTP-Referer": "https://github.com"}
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                print(f"   ⚠️ Rate limit ({model}), switching...")
                time.sleep(1)
                continue
            else:
                continue
    return None

def generate_seo_metadata(script_path, channel_name):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"📝 Generating SEO for: {os.path.basename(script_path)}...")
        
        prompt = f"""
        You are a YouTube SEO Expert for the channel '{channel_name}'.
        Read this script and generate: TITLE, DESCRIPTION, TAGS, HASHTAGS.
        SCRIPT: {content[:3000]}
        """

        messages=[
            {"role": "system", "content": "You are a YouTube Growth Expert."},
            {"role": "user", "content": prompt}
        ]
        
        metadata = get_completion_with_retry(messages)
        
        if metadata:
            output_path = script_path.replace('.txt', '_METADATA.txt')
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(metadata)
            print(f"   ✅ Saved: {os.path.basename(output_path)}")
        else:
            print(f"   ❌ Failed to generate metadata for {script_path}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"No input directory found: {INPUT_DIR}")
        return

    for channel_name in config.CHANNEL_PROMPTS.keys():
        channel_path = os.path.join(INPUT_DIR, channel_name)
        
        if os.path.exists(channel_path):
            files = [f for f in os.listdir(channel_path) if f.endswith(".txt") and not f.endswith("_METADATA.txt")]
            
            if files:
                print(f"\n--- Processing {channel_name} ---")
                for filename in files:
                    generate_seo_metadata(os.path.join(channel_path, filename), channel_name)

if __name__ == "__main__":
    main()
