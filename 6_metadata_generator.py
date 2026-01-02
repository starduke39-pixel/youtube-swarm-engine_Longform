import os
import google.generativeai as genai
import config

INPUT_DIR = os.path.join(config.BASE_DIR)

# Setup Gemini
genai.configure(api_key=config.GOOGLE_API_KEY)
model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)

def generate_seo_metadata(script_path, channel_name):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"📝 Generating SEO for: {os.path.basename(script_path)}...")
        
        prompt = f"""
        You are a YouTube SEO Expert for the channel '{channel_name}'.
        Read this script and generate: TITLE, DESCRIPTION, TAGS, HASHTAGS.
        
        SCRIPT:
        {content[:3000]}
        """

        response = model.generate_content(prompt)
        metadata = response.text
        
        if metadata:
            output_path = script_path.replace('.txt', '_METADATA.txt')
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(metadata)
            print(f"   ✅ Saved: {os.path.basename(output_path)}")
        
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
