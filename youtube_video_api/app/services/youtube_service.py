import requests
import os
from datetime import datetime, timezone
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.api_keys = [key.strip() for key in os.getenv("YOUTUBE_API_KEYS", "").split(",") if key.strip()]
        if not self.api_keys:
            raise ValueError("No YouTube API keys provided")
        self.current_key_index = 0
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.search_query = os.getenv("SEARCH_QUERY", "cricket")
        self.max_results = int(os.getenv("MAX_RESULTS_PER_FETCH", 50))
        
    def get_current_api_key(self) -> str:
        return self.api_keys[self.current_key_index]
    
    def switch_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Switched to API key {self.current_key_index + 1}")
    
    def fetch_latest_videos(self, published_after: Optional[datetime] = None) -> List[Dict]:
        """Fetch latest videos from YouTube API"""
        if not published_after:
            published_after = datetime.now(timezone.utc).replace(microsecond=0)
        
        params = {
            'part': 'snippet',
            'q': self.search_query,
            'type': 'video',
            'order': 'date',
            'publishedAfter': published_after.isoformat() + 'Z',
            'maxResults': self.max_results,
            'key': self.get_current_api_key()
        }
        
        try:
            response = requests.get(f"{self.base_url}/search", params=params)
            
            if response.status_code == 403 and "quotaExceeded" in response.text:
                logger.warning("Quota exceeded, switching API key")
                self.switch_api_key()
                params['key'] = self.get_current_api_key()
                response = requests.get(f"{self.base_url}/search", params=params)
            
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                snippet = item['snippet']
                video_data = {
                    'id': item['id']['videoId'],
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'published_at': datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
                    'channel_title': snippet['channelTitle'],
                    'thumbnail_url': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else None,
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video_data)
            
            logger.info(f"Fetched {len(videos)} videos")
            return videos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching videos: {str(e)}")
            return []
