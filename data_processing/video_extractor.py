import os
import sys
import pandas as pd
from googleapiclient.errors import HttpError
import isodate

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from streamlit_app.youtube_auth import get_youtube_service

def get_all_video_metadata(channel_id):
    """
    Extract detailed metadata for all videos in a YouTube channel.
    - Uses pagination to handle channels with many videos.
    - Handles missing fields gracefully.
    - Returns a pandas DataFrame with processed numerical fields.
    """
    youtube = get_youtube_service()
    
    try:
        # 1. Get the 'uploads' playlist ID for the channel
        channel_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        if not channel_response.get("items"):
            print(f"⚠️ No channel found with ID: {channel_id}")
            return pd.DataFrame()

        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # 2. Extract all video IDs from the uploads playlist with pagination
        video_ids = []
        next_page_token = None

        while True:
            playlist_response = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])

            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token:
                break

        if not video_ids:
            return pd.DataFrame()

        # 3. Fetch detailed metadata for these video IDs in batches of 50
        all_video_data = []

        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            video_response = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(batch_ids)
            ).execute()

            for video in video_response.get("items", []):
                snippet = video.get("snippet", {})
                stats = video.get("statistics", {})
                content_details = video.get("contentDetails", {})
                
                # Parse duration (ISO 8601 to seconds)
                duration_str = content_details.get("duration", "PT0S")
                duration_seconds = int(isodate.parse_duration(duration_str).total_seconds())

                all_video_data.append({
                    "video_id": video.get("id"),
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "publish_date": snippet.get("publishedAt"),
                    "duration": duration_seconds,
                    "view_count": stats.get("viewCount"),
                    "like_count": stats.get("likeCount"),
                    "comment_count": stats.get("commentCount"),
                    "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                })

        # 4. Process data into a DataFrame
        df = pd.DataFrame(all_video_data)

        if not df.empty:
            # Type conversions for numerical fields
            numeric_cols = ["duration", "view_count", "like_count", "comment_count"]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            
            # Convert publish_date to datetime
            df["publish_date"] = pd.to_datetime(df["publish_date"])

        return df

    except HttpError as e:
        print(f"❌ YouTube API error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Unexpected error in get_all_video_metadata: {e}")
        return pd.DataFrame()
