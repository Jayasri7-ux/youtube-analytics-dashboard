from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    
    channel_id = Column(String(50), primary_key=True)
    channel_name = Column(String(255), nullable=False)
    custom_url = Column(String(255))
    description = Column(Text)
    published_at = Column(DateTime)
    subscriber_count = Column(BigInteger)
    video_count = Column(BigInteger)
    view_count = Column(BigInteger)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")

class Video(Base):
    __tablename__ = 'videos'
    
    video_id = Column(String(50), primary_key=True)
    channel_id = Column(String(50), ForeignKey('channels.channel_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    published_at = Column(DateTime)
    duration_seconds = Column(Integer)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    channel = relationship("Channel", back_populates="videos")
    statistics = relationship("VideoStatistics", back_populates="video", cascade="all, delete-orphan")

class VideoStatistics(Base):
    __tablename__ = 'video_statistics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(50), ForeignKey('videos.video_id'), nullable=False)
    view_count = Column(BigInteger)
    like_count = Column(BigInteger)
    comment_count = Column(BigInteger)
    record_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    video = relationship("Video", back_populates="statistics")
