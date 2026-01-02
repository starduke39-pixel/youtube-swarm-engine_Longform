import os

# --- API KEYS ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# --- SETTINGS ---
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "google/gemini-2.0-flash-exp:free"
BASE_DIR = "Production_Factory_LongForm" # Changed folder name so you don't mix them up
ASSETS_DIR = "assets"

# --- VOICE MAPPING ---
VOICE_MAP = {
    "Trivia_Core": "nPczCjz8TkKk1be360ku",
    "Ancient_Echoes": "CwhRBWXzGAHq8TQ4Fs17",
    "Abyss_Archives": "TxGEqnHWrfWFTfGW9XjX",
    "Apex_Lists": "29vD33N1CtxCmqQRPOHJ",
    "Mind_Architect": "ODq5zmih8GrVes37Dizj"
}

# --- LONG FORM PROMPTS (10-20 Minutes) ---
# These prompts generate comprehensive, segmented scripts.
CHANNEL_PROMPTS = {
    "Trivia_Core": "You are a Trivia Host. Write a script for a '50 Question Marathon' video (approx 10 mins). Format: Intro, then 50 questions in rapid succession. Group them by round: 'Round 1: Geography', 'Round 2: History'. Include answer pauses.",
    
    "Ancient_Echoes": "You are a Mythologist. Write a deep-dive 2000-word script about a specific Greek/Norse myth or historical figure. Structure: The Origin, The Conflict, The Betrayal, The Fall. Tone: Relaxing, sleep-inducing, descriptive.",
    
    "Abyss_Archives": "You are a Detective. Write a 2000-word documentary script investigating a specific unsolved mystery or disappearance. Structure: The Incident, The Evidence, The Theories, The Conclusion. Tone: Suspenseful, Noir.",
    
    "Apex_Lists": "You are a Luxury Curator. Write a script for a 'Top 10' video ranking the most expensive items in a category. Start from #10 and work down to #1. Total word count approx 1800 words. Detailed specs for each item.",
    
    "Mind_Architect": "You are a Philosopher. Write a 2000-word video essay about a specific Stoic concept (e.g., Memento Mori) and how to apply it to modern life. Structure: Introduction, Historical Context, 3 Practical Steps, Conclusion."
}
