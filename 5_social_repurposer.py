import os
import time

# --- CRITICAL FIX FOR PILLOW 10+ ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# -----------------------------------

from moviepy.editor import *
from openai import OpenAI
import config

INPUT_DIR = os.path.join(config.BASE_DIR, "Rendered_Videos_Long")
OUTPUT_DIR = os.path.join(config.BASE_DIR, "Social_Media_Pack")

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

def create_vertical_clip(video_path, filename):
    print(f"📱 Creating Reel from: {filename}")
    try:
        clip = VideoFileClip(video_path)
        if clip.duration > 60:
            clip = clip.subclip(0, 60)
            
        w, h = clip.size
        target_ratio = 9/16
        new_width = h * target_ratio
        x1 = (w / 2) - (new_width / 2)
        x2 = (w / 2) + (new_width / 2)
        
        # The resize function here was causing the crash
        cropped_clip = clip.crop(x1=x1, y1=0, x2=x2, y2=h).resize(height=1920)
        
        output_path = os.path.join(OUTPUT_DIR, f"REEL_{filename}")
        cropped_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        print(f"✅ Reel Saved: {output_path}")
    except Exception as e:
        print(f"❌ Error processing video: {e}")

def generate_twitter_thread(script_path, channel_name):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"🐦 Generating Tweets for {channel_name}...")
        
        messages = [
            {"role": "system", "content": "You are a social media manager."},
            {"role": "user", "content": f"Turn this YouTube script into a viral 5-tweet thread.\n\nSCRIPT:\n{content[:4000]}"}
        ]
        
        thread_content = get_completion_with_retry(messages)
        
        if thread_content:
            base_name = os.path.basename(script_path).replace('.txt', '')
            output_filename = f"THREAD_{channel_name}_{base_name}.txt"
            with open(os.path.join(OUTPUT_DIR, output_filename), "w", encoding="utf-8") as f:
                f.write(thread_content)
            print(f"✅ Thread saved: {output_filename}")
        
    except Exception as e:
        print(f"❌ Error generating thread: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Process Video to Reel
    if os.path.exists(INPUT_DIR):
        video_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".mp4")]
        if not video_files:
             print("   ⚠️ No videos found to resize. Skipping Reels.")
        for video in video_files:
            create_vertical_clip(os.path.join(INPUT_DIR, video), video)
        
    # 2. Process Scripts to Tweets
    for channel_name in config.CHANNEL_PROMPTS.keys():
        channel_path = os.path.join(config.BASE_DIR, channel_name)
        if os.path.exists(channel_path):
            script_files = [f for f in os.listdir(channel_path) if f.endswith(".txt")]
            if script_files:
                generate_twitter_thread(os.path.join(channel_path, script_files[0]), channel_name)

if __name__ == "__main__":
    main()
