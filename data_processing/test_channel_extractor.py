from channel_extractor import extract_channel_data

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
