import os
from moviepy.editor import *
import config

# --- CONFIGURATION ---
W, H = 1920, 1080
OUTPUT_DIR = os.path.join(config.BASE_DIR, "Rendered_Videos_Long")

def parse_questions_from_script():
    """Finds the latest generated script and extracts Q&A pairs."""
    questions = []
    
    # Path where Step 1 saves scripts
    trivia_folder = os.path.join(config.BASE_DIR, "Trivia_Core")
    
    if not os.path.exists(trivia_folder):
        print("⚠️ No script folder found. Using defaults.")
        return get_default_questions()

    # Find text files
    files = [f for f in os.listdir(trivia_folder) if f.endswith(".txt")]
    if not files:
        print("⚠️ No script files found. Using defaults.")
        return get_default_questions()
        
    # Read the first available script
    with open(os.path.join(trivia_folder, files[0]), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"📖 Reading script: {files[0]}")
    
    # Parse lines looking for 'Q: ... | A: ...' format
    for line in lines:
        if "Q:" in line and "A:" in line:
            try:
                parts = line.split('|')
                q_part = parts[0].split('Q:')[1].strip()
                a_part = parts[1].split('A:')[1].strip()
                questions.append({"q": q_part, "a": a_part, "diff": "TRIVIA"})
            except:
                continue
                
    if not questions:
        print("⚠️ Could not parse questions from script. Format mismatch.")
        return get_default_questions()
        
    return questions

def get_default_questions():
    return [
        {"q": "What is the capital of France?", "a": "Paris", "diff": "EASY"},
        {"q": "Which planet is red?", "a": "Mars", "diff": "MEDIUM"},
        {"q": "What year did Titanic sink?", "a": "1912", "diff": "HARD"},
    ]

def create_trivia_video(output_filename="trivia_dynamic.mp4"):
    print("🎬 Rendering Trivia Video...")
    
    # LOAD DYNAMIC QUESTIONS
    QUESTIONS = parse_questions_from_script()
    print(f"Loaded {len(QUESTIONS)} questions.")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    clips = []
    
    # 1. Background
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
    audio_clips = []
    
    # 2. Add Questions
    for item in QUESTIONS:
        # Question Phase (4s)
        try:
            q_txt = (TextClip(item['q'], fontsize=90, color='white', font='Arial-Bold', method='caption', size=(1500, None))
                     .set_position('center')
                     .set_start(current_time)
                     .set_duration(4))
            clips.append(q_txt)
            
            # Timer
            timer = (ColorClip(size=(1500, 30), color=(255,0,0))
                     .set_position(('center', 900))
                     .set_start(current_time)
                     .set_duration(4))
            clips.append(timer)
        except: pass

        current_time += 4
        
        # Answer Phase (2s)
        try:
            a_txt = (TextClip(item['a'], fontsize=110, color='green', font='Arial-Bold', method='caption', size=(1500, None))
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
                audio_clips.append(ding)
            except: pass

        current_time += 2

    # 3. Composite
    final_video = CompositeVideoClip([bg.set_duration(current_time)] + clips)
    
    # 4. Music
    music_path = os.path.join(config.ASSETS_DIR, "music.mp3")
    if os.path.exists(music_path):
        try:
            bg_music = AudioFileClip(music_path)
            # Simple loop compatible with v1.0.3
            if current_time > bg_music.duration:
                # Manual loop implementation if afx fails
                bg_music = afx.audio_loop(bg_music, duration=current_time)
            else:
                bg_music = bg_music.set_duration(current_time)
            bg_music = bg_music.volumex(0.2)
            final_audio = CompositeAudioClip([bg_music] + audio_clips)
            final_video = final_video.set_audio(final_audio)
        except:
             if audio_clips: final_video = final_video.set_audio(CompositeAudioClip(audio_clips))
    else:
        if audio_clips: final_video = final_video.set_audio(CompositeAudioClip(audio_clips))

    save_path = os.path.join(OUTPUT_DIR, output_filename)
    final_video.write_videofile(save_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"✅ Saved: {save_path}")

if __name__ == "__main__":
    create_trivia_video()
