from database.db_connection import SessionLocal
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
        channel.description = channel_data_row.get('description')
        channel.created_date = pd.to_datetime(channel_data_row['created_date'])
        channel.subscribers = int(channel_data_row['subscribers'])
        channel.total_videos = int(channel_data_row['total_videos'])
        channel.total_views = int(channel_data_row['total_views'])
        channel.thumbnail_url = channel_data_row.get('thumbnail_url')
        
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
            video.publish_date = pd.to_datetime(row['publish_date'])
            video.duration = int(row.get('duration', 0))
            video.thumbnail_url = row.get('thumbnail_url')
            
            # 1 to 1 Statistics: Check if stats exist
            stats = db.query(VideoStatistics).filter(VideoStatistics.video_id == video_id).first()
            if not stats:
                stats = VideoStatistics(video_id=video_id)
                db.add(stats)
            
            # Update dynamic statistics
            stats.views = int(row['view_count'])
            stats.likes = int(row['like_count'])
            stats.comments = int(row['comment_count'])
            
        db.commit()
    except Exception as e:
        print(f"Error saving videos to DB: {e}")
        db.rollback()
    finally:
        db.close()

def get_videos_from_db(channel_id):
    """Retrieves all videos and their latest statistics for a channel from the database."""
    db = SessionLocal()
    try:
        # One-to-one relationship simplifies the query
        results = db.query(Video, VideoStatistics).\
            join(VideoStatistics, Video.video_id == VideoStatistics.video_id).\
            filter(Video.channel_id == channel_id).all()

        if not results:
            return pd.DataFrame()

        video_list = []
        for video, stats in results:
            video_list.append({
                "video_id": video.video_id,
                "title": video.title,
                "description": video.description,
                "published_at": video.publish_date,
                "duration_seconds": video.duration,
                "view_count": stats.views,
                "like_count": stats.likes,
                "comment_count": stats.comments
            })
        
        df = pd.DataFrame(video_list)
        if not df.empty:
            df['published_at'] = pd.to_datetime(df['published_at'])
            
        return df
    except Exception as e:
        print(f"Error loading videos from DB: {e}")
        return pd.DataFrame()
    finally:
        db.close()
