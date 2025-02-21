import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file in project root
load_dotenv(find_dotenv())

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set")
