import sys
import os
from datetime import datetime, timezone

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from database.db_config import SessionLocal
from database.models import Channel, Video, VideoStatistics

def test_db_operations():
    print("🔬 Testing database operations...")
    db = SessionLocal()
    try:
        # 1. Create a test channel
        test_channel = Channel(
            channel_id="UC_TEST_ID",
            channel_name="Test Channel",
            subscriber_count=1000,
            video_count=10,
            view_count=5000,
            published_at=datetime.now(timezone.utc)
        )
        db.add(test_channel)
        db.commit()
        print("✅ Channel created.")

        # 2. Create a test video
        test_video = Video(
            video_id="TEST_VID_001",
            channel_id="UC_TEST_ID",
            title="Test Video 1",
            published_at=datetime.now(timezone.utc)
        )
        db.add(test_video)
        db.commit()
        print("✅ Video created.")

        # 3. Create test statistics
        test_stats = VideoStatistics(
            video_id="TEST_VID_001",
            view_count=100,
            like_count=10,
            comment_count=2
        )
        db.add(test_stats)
        db.commit()
        print("✅ Statistics recorded.")

        # 4. Verify retrieval
        retrieved_channel = db.query(Channel).filter(Channel.channel_id == "UC_TEST_ID").first()
        if retrieved_channel and len(retrieved_channel.videos) > 0:
            print(f"✅ Verified: Retrieved channel '{retrieved_channel.channel_name}' with {len(retrieved_channel.videos)} video(s).")
            print(f"📈 Video views: {retrieved_channel.videos[0].statistics[0].view_count}")
        
        # Cleanup
        db.delete(retrieved_channel)
        db.commit()
        print("🧹 Cleanup completed.")
        print("🌟 Verification SUCCESSFUL.")

    except Exception as e:
        db.rollback()
        print(f"❌ Verification FAILED: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db_operations()
