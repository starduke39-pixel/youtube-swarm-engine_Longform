import os

# --- API KEYS ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# --- OPENROUTER SETTINGS ---
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# --- UPDATED MODEL LIST (Active Free Models) ---
# This list mixes different providers to avoid hitting the same rate limit twice.
MODEL_LIST = [
    "google/gemini-2.0-flash-exp:free",           # Primary (Fastest)
    "meta-llama/llama-3.2-3b-instruct:free",      # Backup 1 (Reliable)
    "mistralai/mistral-7b-instruct:free",         # Backup 2 (Classic)
    "openchat/openchat-7b:free",                  # Backup 3 (Uncensored-ish)
    "huggingfaceh4/zephyr-7b-beta:free",          # Backup 4 (Good writing)
    "microsoft/phi-3-mini-128k-instruct:free",    # Backup 5
    "meta-llama/llama-3-8b-instruct:free"         # Backup 6
]

# --- DIRECTORY SETUP ---
BASE_DIR = "Production_Factory_LongForm"
ASSETS_DIR = "assets"

# --- VOICE MAPPING ---
VOICE_MAP = {
    "Trivia_Core": "nPczCjz8TkKk1be360ku",
    "Ancient_Echoes": "CwhRBWXzGAHq8TQ4Fs17",
    "Abyss_Archives": "TxGEqnHWrfWFTfGW9XjX",
    "Apex_Lists": "29vD33N1CtxCmqQRPOHJ",
    "Mind_Architect": "ODq5zmih8GrVes37Dizj"
}

# --- PROMPTS ---
CHANNEL_PROMPTS = {
    "Trivia_Core": "You are a Trivia Host. Generate 50 trivia questions for a 'General Knowledge' quiz. STRICT FORMAT per line: 'Q: [Question] | A: [Answer]'. Do not add numbering or intro text.",
    "Ancient_Echoes": "You are a Mythologist. Write a deep-dive 2000-word script about a specific Greek/Norse myth. Structure: Origin, Conflict, Conclusion. Tone: Relaxing.",
    "Abyss_Archives": "You are a Detective. Write a 2000-word documentary script investigating a specific unsolved mystery. Tone: Suspenseful, Noir.",
    "Apex_Lists": "You are a Luxury Curator. Write a script for a 'Top 10' video ranking expensive items. Start from #10 down to #1. Total word count approx 1800 words.",
    "Mind_Architect": "You are a Philosopher. Write a 2000-word video essay about a specific Stoic concept and how to apply it to modern life."
}
