-- YouTube Analytics Database Schema (PostgreSQL)

-- Table 1: Channels
CREATE TABLE channels (
    channel_id VARCHAR(100) PRIMARY KEY,
    channel_name VARCHAR(200) NOT NULL,
    description TEXT,
    subscribers INT,
    total_videos INT,
    total_views BIGINT,
    created_date TIMESTAMP,
    thumbnail_url TEXT
);

-- Table 2: Videos
CREATE TABLE videos (
    video_id VARCHAR(100) PRIMARY KEY,
    channel_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    publish_date TIMESTAMP,
    duration INT,
    thumbnail_url TEXT,
    CONSTRAINT fk_channel FOREIGN KEY (channel_id) REFERENCES channels (channel_id) ON DELETE CASCADE
);

-- Table 3: Video Statistics
CREATE TABLE video_statistics (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(100) NOT NULL UNIQUE,
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    CONSTRAINT fk_video FOREIGN KEY (video_id) REFERENCES videos (video_id) ON DELETE CASCADE
);
