import os
import time

# --- CRITICAL FIX FOR PILLOW 10+ ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# -----------------------------------

from moviepy.editor import *
import google.generativeai as genai
import config

INPUT_DIR = os.path.join(config.BASE_DIR, "Rendered_Videos_Long")
OUTPUT_DIR = os.path.join(config.BASE_DIR, "Social_Media_Pack")

# Setup Gemini
genai.configure(api_key=config.GOOGLE_API_KEY)
model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)

def create_vertical_clip(video_path, filename):
    print(f"📱 Creating Reel from: {filename}")
    try:
        clip = VideoFileClip(video_path)
        if clip.duration > 60:
            clip = clip.subclip(0, 60)
            
        w, h = clip.size
        # Center Crop Logic
        target_ratio = 9/16
        new_width = h * target_ratio
        x1 = (w / 2) - (new_width / 2)
        x2 = (w / 2) + (new_width / 2)
        
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
        
        prompt = f"You are a social media manager. Turn this YouTube script into a viral 5-tweet thread. Hook in first tweet. Format: TWEET 1: [text] ... TWEET 2: [text].\n\nSCRIPT:\n{content[:4000]}"
        
        response = model.generate_content(prompt)
        thread_content = response.text
        
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
