import os
import sys
import pandas as pd
from googleapiclient.errors import HttpError

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from streamlit_app.youtube_auth import get_youtube_service


def extract_channel_data(channel_ids):
    """
    Extract YouTube channel data.
    - Returns data for valid channel IDs
    - Gracefully ignores invalid IDs
    - Never crashes the application
    """

    youtube = get_youtube_service()
    all_channel_data = []

    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=",".join(channel_ids)
        )
        response = request.execute()

        returned_items = response.get("items", [])

        # Identify invalid IDs
        returned_ids = {item["id"] for item in returned_items}
        invalid_ids = list(set(channel_ids) - returned_ids)

        if invalid_ids:
            print(f"⚠️ Invalid Channel IDs ignored: {invalid_ids}")

        for channel in returned_items:
            snippet = channel.get("snippet", {})
            stats = channel.get("statistics", {})
            thumbnails = snippet.get("thumbnails", {})

            all_channel_data.append({
                "channel_id": channel.get("id"),
                "channel_name": snippet.get("title"),
                "custom_url": snippet.get("customUrl"),
                "description": snippet.get("description"),
                "published_at": snippet.get("publishedAt"),
                "subscriber_count": stats.get("subscriberCount"),
                "video_count": stats.get("videoCount"),
                "view_count": stats.get("viewCount"),
                "thumbnail_default": thumbnails.get("default", {}).get("url"),
                "thumbnail_medium": thumbnails.get("medium", {}).get("url"),
                "thumbnail_high": thumbnails.get("high", {}).get("url"),
            })

        return pd.DataFrame(all_channel_data)

    except HttpError as e:
        print(f"❌ YouTube API error: {e}")
        return pd.DataFrame()

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return pd.DataFrame()
