import os

# --- API KEYS ---
# Ensure you have added GOOGLE_API_KEY to your GitHub Secrets
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# --- GEMINI SETTINGS (DIRECT API) ---
# We use the REST API URL directly to avoid library version issues
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

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
