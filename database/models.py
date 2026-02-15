from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    
    channel_id = Column(String(100), primary_key=True)
    channel_name = Column(String(200), nullable=False)
    description = Column(Text)
    subscribers = Column(Integer)
    total_videos = Column(Integer)
    total_views = Column(BigInteger)
    created_date = Column(DateTime)
    thumbnail_url = Column(Text)
    
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")

class Video(Base):
    __tablename__ = 'videos'
    
    video_id = Column(String(100), primary_key=True)
    channel_id = Column(String(100), ForeignKey('channels.channel_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    publish_date = Column(DateTime)
    duration = Column(Integer)
    thumbnail_url = Column(Text)
    
    channel = relationship("Channel", back_populates="videos")
    statistics = relationship("VideoStatistics", back_populates="video", uselist=False, cascade="all, delete-orphan")

class VideoStatistics(Base):
    __tablename__ = 'video_statistics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(100), ForeignKey('videos.video_id'), unique=True, nullable=False)
    views = Column(BigInteger)
    likes = Column(BigInteger)
    comments = Column(BigInteger)
    
    video = relationship("Video", back_populates="statistics")
