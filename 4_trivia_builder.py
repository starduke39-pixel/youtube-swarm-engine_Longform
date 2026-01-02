import os
from moviepy.editor import *
import config

# --- CONFIGURATION FOR LONG FORM ---
W, H = 1920, 1080  # CHANGED to Landscape
OUTPUT_DIR = os.path.join(config.BASE_DIR, "Rendered_Videos_Long")

# Demo Data
QUESTIONS = [
    {"q": "What is the capital of France?", "a": "Paris", "diff": "EASY"},
    {"q": "Which planet is red?", "a": "Mars", "diff": "MEDIUM"},
    {"q": "What year did Titanic sink?", "a": "1912", "diff": "HARD"},
]

def create_trivia_video(output_filename="trivia_landscape.mp4"):
    print("🎬 Rendering Trivia Video (Landscape)...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    clips = []
    
    # 1. Background Layer
    bg_path = os.path.join(config.ASSETS_DIR, "background.mp4")
    
    # Safe Background Loading
    if os.path.exists(bg_path):
        try:
            bg = VideoFileClip(bg_path).resize(width=W) # Resize to width for landscape
            # If aspect ratio is wrong, crop center
            if bg.h < H:
                 bg = bg.resize(height=H)
            bg = bg.crop(x1=0, y1=0, width=W, height=H)
        except:
             bg = ColorClip(size=(W, H), color=(20, 20, 40))
    else:
        bg = ColorClip(size=(W, H), color=(20, 20, 40))

    current_time = 0
    
    # 2. Add Questions
    for item in QUESTIONS:
        # Question Phase (4s) - Font sizes adjusted for Landscape
        try:
            q_txt = (TextClip(item['q'], fontsize=100, color='white', font='Arial-Bold', method='caption', size=(1500, None))
                     .set_position('center')
                     .set_start(current_time)
                     .set_duration(4))
            clips.append(q_txt)
            
            diff_txt = (TextClip(item['diff'], fontsize=60, color='yellow', font='Arial', method='caption')
                        .set_position(('center', 200)) # Moved up
                        .set_start(current_time)
                        .set_duration(4))
            clips.append(diff_txt)

            # Timer Bar (Wider for landscape)
            timer = (ColorClip(size=(1500, 30), color=(255,0,0))
                     .set_position(('center', 900)) # Moved down
                     .set_start(current_time)
                     .set_duration(4))
            clips.append(timer)
        except Exception as e:
            print(f"ImageMagick Error: {e}")

        current_time += 4
        
        # Answer Phase (2s)
        try:
            a_txt = (TextClip(item['a'], fontsize=120, color='green', font='Arial-Bold', method='caption', size=(1500, None))
                     .set_position('center')
                     .set_start(current_time)
                     .set_duration(2))
            clips.append(a_txt)
        except: pass
        
        # Audio
        ding_path = os.path.join(config.ASSETS_DIR, "ding.mp3")
        if os.path.exists(ding_path):
            try:
                ding = AudioFileClip(ding_path).set_start(current_time)
            except: pass

        current_time += 2

    # 3. Composite
    final_video = CompositeVideoClip([bg.set_duration(current_time)] + clips)
    
    save_path = os.path.join(OUTPUT_DIR, output_filename)
    final_video.write_videofile(save_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"✅ Saved: {save_path}")

if __name__ == "__main__":
    create_trivia_video()
