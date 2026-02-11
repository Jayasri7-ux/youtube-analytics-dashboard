import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from data_processing.channel_extractor import extract_channel_data

if __name__ == "__main__":
    channel_ids = [
        "UC_x5XG1OV2P6uZZ5FSM9Ttw",   # Google Developers
        "UCsooa4yRKGN_zEE8iknghZA",   # TED
        "UC16niRr50-MSBwiO3YDb3RA"    # freeCodeCamp
    ]

    df = extract_channel_data(channel_ids)

    print(df)
    print("\nDataFrame Columns:")
    print(df.columns)
