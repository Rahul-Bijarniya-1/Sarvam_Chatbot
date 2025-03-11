# config.py - Store configuration settings

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Settings
# In config.py
GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3"),
    os.getenv("GROQ_API_KEY_4")
    # Add more keys as needed
]

# GROQ_API_KEY = os.getenv("GROQ_API_KEY_2")

# Application Settings
APP_TITLE = "FoodieSpot Restaurant Reservations"
DEBUG_MODE = True  # Set to False for production

# Data Settings
RESTAURANTS_FILE = "data/restaurants.json"
RESERVATIONS_FILE = "data/reservations.json"