from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..services.video_service import VideoService
from ..schemas import VideoResponse, PaginatedResponse

router = APIRouter(prefix="/api/v1/videos", tags=["videos"])

@router.get("/", response_model=PaginatedResponse)
async def get_videos(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    channel_title: Optional[str] = Query(None, description="Filter by channel title"),
    db: Session = Depends(get_db)
):
    """Get paginated videos sorted by published date (descending)"""
    video_service = VideoService(db)
    videos, total = video_service.get_videos_paginated(
        page=page,
        size=size,
        channel_title=channel_title
    )
    
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=videos,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video_by_id(
    video_id: str,
    db: Session = Depends(get_db)
):
    """Get a single video by ID"""
    video_service = VideoService(db)
    video = video_service.get_video_by_id(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video
