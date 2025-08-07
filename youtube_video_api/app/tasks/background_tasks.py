import asyncio
from datetime import datetime, timezone, timedelta
from typing import List
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.youtube_service import YouTubeService
from ..services.video_service import VideoService

logger = logging.getLogger(__name__)

class BackgroundVideoFetcher:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.youtube_service = YouTubeService()
        self.is_running = False
        
    async def fetch_and_store_videos(self):
        """Background task to fetch and store latest videos"""
        try:
            db = SessionLocal()
            video_service = VideoService(db)
            
            # Get the latest published date to avoid duplicates
            latest_date = video_service.get_latest_published_date()
            
            if latest_date:
                # Fetch videos published after the latest stored video
                published_after = latest_date - timedelta(minutes=1)  # Small buffer
            else:
                # First run - fetch videos from last 24 hours
                published_after = datetime.now(timezone.utc) - timedelta(hours=24)
            
            videos = self.youtube_service.fetch_latest_videos(published_after)
            
            if videos:
                for video_data in videos:
                    video_service.create_or_update_video(video_data)
                
                logger.info(f"Successfully stored {len(videos)} new videos")
            else:
                logger.info("No new videos found")
                
        except Exception as e:
            logger.error(f"Error in background task: {str(e)}")
        finally:
            db.close()
    
    def start(self):
        """Start the background scheduler"""
        if not self.is_running:
            # Schedule the task to run every 10 seconds
            self.scheduler.add_job(
                self.fetch_and_store_videos,
                'interval',
                seconds=int(os.getenv("FETCH_INTERVAL_SECONDS", 10)),
                id='fetch_videos',
                replace_existing=True
            )
            self.scheduler.start()
            self.is_running = True
            logger.info("Background video fetcher started")
    
    def stop(self):
        """Stop the background scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Background video fetcher stopped")
