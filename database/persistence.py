from database.db_config import SessionLocal
from database.models import Channel, Video, VideoStatistics
from datetime import datetime
import pandas as pd

def save_channel_to_db(channel_data_row):
    """Saves or updates channel data in the database."""
    db = SessionLocal()
    try:
        channel_id = channel_data_row['channel_id']
        
        # Check if exists
        channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
        
        if not channel:
            channel = Channel(channel_id=channel_id)
            db.add(channel)
            
        channel.channel_name = channel_data_row['channel_name']
        channel.custom_url = channel_data_row.get('custom_url')
        channel.description = channel_data_row.get('description')
        channel.published_at = pd.to_datetime(channel_data_row['published_at'])
        channel.subscriber_count = int(channel_data_row['subscriber_count'])
        channel.video_count = int(channel_data_row['video_count'])
        channel.view_count = int(channel_data_row['view_count'])
        
        db.commit()
    except Exception as e:
        print(f"Error saving channel to DB: {e}")
        db.rollback()
    finally:
        db.close()

def save_videos_to_db(video_df, channel_id):
    """Saves or updates video data and statistics in the database."""
    db = SessionLocal()
    try:
        for _, row in video_df.iterrows():
            video_id = row['video_id']
            
            # Upsert Video
            video = db.query(Video).filter(Video.video_id == video_id).first()
            if not video:
                video = Video(video_id=video_id, channel_id=channel_id)
                db.add(video)
                
            video.title = row['title']
            video.description = row.get('description', '')
            video.published_at = pd.to_datetime(row['published_at'])
            # Duration is expected to be parsed already in video_extractor
            video.duration_seconds = int(row.get('duration_seconds', 0))
            
            # Add new statistics record
            stats = VideoStatistics(
                video_id=video_id,
                view_count=int(row['view_count']),
                like_count=int(row['like_count']),
                comment_count=int(row['comment_count'])
            )
            db.add(stats)
            
        db.commit()
    except Exception as e:
        print(f"Error saving videos to DB: {e}")
        db.rollback()
    finally:
        db.close()
