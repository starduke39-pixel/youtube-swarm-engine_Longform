import os
from moviepy.editor import *
from moviepy.audio.fx.all import volumetric
import config

# --- CONFIGURATION FOR LONG FORM ---
W, H = 1920, 1080
OUTPUT_DIR = os.path.join(config.BASE_DIR, "Rendered_Videos_Long")

# Demo Data (In real run, this comes from the scripts)
QUESTIONS = [
    {"q": "What is the capital of France?", "a": "Paris", "diff": "EASY"},
    {"q": "Which planet is red?", "a": "Mars", "diff": "MEDIUM"},
    {"q": "What year did Titanic sink?", "a": "1912", "diff": "HARD"},
]

def create_trivia_video(output_filename="trivia_landscape_music.mp4"):
    print("🎬 Rendering Trivia Video (With Music)...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    clips = []
    
    # 1. Background Layer
    bg_path = os.path.join(config.ASSETS_DIR, "background.mp4")
    if os.path.exists(bg_path):
        try:
            bg = VideoFileClip(bg_path).resize(width=W)
            if bg.h < H: bg = bg.resize(height=H)
            bg = bg.crop(x1=0, y1=0, width=W, height=H)
        except:
             bg = ColorClip(size=(W, H), color=(20, 20, 40))
    else:
        bg = ColorClip(size=(W, H), color=(20, 20, 40))

    current_time = 0
    audio_clips = [] # List to hold SFX and Voice
    
    # 2. Add Questions
    for item in QUESTIONS:
        # Question Phase (4s)
        try:
            q_txt = (TextClip(item['q'], fontsize=100, color='white', font='Arial-Bold', method='caption', size=(1500, None))
                     .set_position('center')
                     .set_start(current_time)
                     .set_duration(4))
            clips.append(q_txt)
            
            diff_txt = (TextClip(item['diff'], fontsize=60, color='yellow', font='Arial', method='caption')
                        .set_position(('center', 200))
                        .set_start(current_time)
                        .set_duration(4))
            clips.append(diff_txt)

            timer = (ColorClip(size=(1500, 30), color=(255,0,0))
                     .set_position(('center', 900))
                     .set_start(current_time)
                     .set_duration(4))
            clips.append(timer)
        except: pass

        current_time += 4
        
        # Answer Phase (2s)
        try:
            a_txt = (TextClip(item['a'], fontsize=120, color='green', font='Arial-Bold', method='caption', size=(1500, None))
                     .set_position('center')
                     .set_start(current_time)
                     .set_duration(2))
            clips.append(a_txt)
        except: pass
        
        # Add Ding SFX
        ding_path = os.path.join(config.ASSETS_DIR, "ding.mp3")
        if os.path.exists(ding_path):
            try:
                ding = AudioFileClip(ding_path).set_start(current_time)
                audio_clips.append(ding)
            except: pass

        current_time += 2

    # --- 3. Composite Visuals ---
    final_video = CompositeVideoClip([bg.set_duration(current_time)] + clips)
    
    # --- 4. Add Background Music ---
    music_path = os.path.join(config.ASSETS_DIR, "music.mp3")
    
    if os.path.exists(music_path):
        try:
            # Load music, loop it to match video length
            bg_music = AudioFileClip(music_path)
            
            # Loop logic: If video is longer than song, loop song. If song longer, cut song.
            if current_time > bg_music.duration:
                bg_music = bg_music.fx(vfx.loop, duration=current_time)
            else:
                bg_music = bg_music.set_duration(current_time)
                
            # Lower volume to 20% so it doesn't overpower SFX/Voice
            bg_music = bg_music.volumex(0.2)
            
            # Combine Music + SFX
            final_audio = CompositeAudioClip([bg_music] + audio_clips)
            final_video = final_video.set_audio(final_audio)
            print("   🎵 Background Music Added!")
        except Exception as e:
            print(f"   ⚠️ Music Error: {e}")
            # Fallback: just use SFX if music fails
            if audio_clips:
                final_video = final_video.set_audio(CompositeAudioClip(audio_clips))
    else:
        print("   ⚠️ No music.mp3 found. Skipping.")
        if audio_clips:
            final_video = final_video.set_audio(CompositeAudioClip(audio_clips))

    # 5. Save
    save_path = os.path.join(OUTPUT_DIR, output_filename)
    final_video.write_videofile(save_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"✅ Saved: {save_path}")

if __name__ == "__main__":
    create_trivia_video()
