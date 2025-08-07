from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from ..models import Video
from ..schemas import VideoCreate
import logging

logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_or_update_video(self, video_data: VideoCreate) -> Video:
        """Create or update a video in the database"""
        existing_video = self.db.query(Video).filter(Video.id == video_data.id).first()
        
        if existing_video:
            # Update existing video
            for key, value in video_data.dict().items():
                setattr(existing_video, key, value)
            self.db.commit()
            self.db.refresh(existing_video)
            return existing_video
        else:
            # Create new video
            db_video = Video(**video_data.dict())
            self.db.add(db_video)
            self.db.commit()
            self.db.refresh(db_video)
            return db_video
    
    def get_videos_paginated(
        self, 
        page: int = 1, 
        size: int = 10,
        channel_title: Optional[str] = None
    ) -> tuple[List[Video], int]:
        """Get paginated videos sorted by published_at desc"""
        query = self.db.query(Video)
        
        if channel_title:
            query = query.filter(Video.channel_title.ilike(f"%{channel_title}%"))
        
        total = query.count()
        
        videos = (
            query
            .order_by(desc(Video.published_at))
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        
        return videos, total
    
    def get_latest_published_date(self) -> Optional[datetime]:
        """Get the latest published date from stored videos"""
        latest_video = (
            self.db.query(Video)
            .order_by(desc(Video.published_at))
            .first()
        )
        return latest_video.published_at if latest_video else None
    
    def get_video_by_id(self, video_id: str) -> Optional[Video]:
        """Get a single video by ID"""
        return self.db.query(Video).filter(Video.id == video_id).first()
