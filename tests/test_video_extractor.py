import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from data_processing.video_extractor import get_all_video_metadata

def test_extraction():
    # Google for Developers Channel ID: UC_x5XG1OV2P6uZZ5FSM9Ttw
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    print(f"🚀 Testing video metadata extraction for channel: {channel_id}")
    
    df = get_all_video_metadata(channel_id)
    
    if df.empty:
        print("❌ No data extracted or error occurred.")
        return

    print(f"✅ Extracted metadata for {len(df)} videos.")
    print("\n--- Sample Data ---")
    print(df[["title", "view_count", "published_at", "duration_seconds"]].head())
    
    print("\n--- Data Types ---")
    print(df.dtypes)
    
    # Simple validation
    assert len(df) > 0, "DataFrame should not be empty"
    assert "video_id" in df.columns, "Missing video_id column"
    assert df["view_count"].dtype == "int32" or df["view_count"].dtype == "int64", "view_count should be integer"

if __name__ == "__main__":
    test_extraction()
