import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

def get_youtube_service():
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise Exception("YOUTUBE_API_KEY not found. Please check your .env file.")

    youtube = build(
        serviceName="youtube",
        version="v3",
        developerKey=api_key
    )

    return youtube
