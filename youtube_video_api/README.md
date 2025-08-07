# YouTube Video Fetcher API

A scalable and optimized API service that continuously fetches latest YouTube videos for a predefined search query and provides paginated access to the stored video data.

## Features

- ✅ **Continuous Background Fetching**: Automatically fetches latest videos every 10 seconds
- ✅ **Scalable Architecture**: Supports multiple YouTube API keys for quota management
- ✅ **Optimized Storage**: PostgreSQL with proper indexing for fast queries
- ✅ **Paginated API**: Efficient pagination with sorting by published date
- ✅ **RESTful Design**: Clean API endpoints following REST principles
- ✅ **Health Monitoring**: Built-in health check endpoints
- ✅ **Docker Ready**: Easy deployment with Docker support

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Background Tasks**: APScheduler
- **API Documentation**: Swagger/OpenAPI
- **Deployment**: Docker

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- YouTube Data API v3 key(s)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd youtube_video_api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up database**
```bash
# Create PostgreSQL database
createdb youtube_videos

# Run migrations
alembic upgrade head
```

6. **Start the application**
```bash
uvicorn app.main:app --reload
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/youtube_videos

# YouTube API Configuration
YOUTUBE_API_KEYS=your_api_key_1,your_api_key_2,your_api_key_3
SEARCH_QUERY=cricket
FETCH_INTERVAL_SECONDS=10
MAX_RESULTS_PER_FETCH=50

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## API Endpoints

### Get Videos (Paginated)
```http
GET /api/v1/videos?page=1&size=10&channel_title=cricket
```

**Response:**
```json
{
  "items": [
    {
      "id": "video_id",
      "title": "Video Title",
      "description": "Video description...",
      "published_at": "2024-01-15T10:30:00Z",
      "channel_title": "Channel Name",
      "thumbnail_url": "https://i.ytimg.com/vi/video_id/hqdefault.jpg",
      "video_url": "https://www.youtube.com/watch?v=video_id"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

### Get Single Video
```http
GET /api/v1/videos/{video_id}
```

### Health Check
```http
GET /health
```

## Docker Deployment

### Using Docker Compose

1. **Create docker-compose.yml**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/youtube_videos
      - YOUTUBE_API_KEYS=${YOUTUBE_API_KEYS}
      - SEARCH_QUERY=${SEARCH_QUERY}
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=youtube_videos
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

2. **Run with Docker Compose**
```bash
docker-compose up --build
```

### Using Docker

```bash
# Build image
docker build -t youtube-video-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://username:password@host:5432/youtube_videos \
  -e YOUTUBE_API_KEYS=your_api_key \
  -e SEARCH_QUERY=cricket \
  youtube-video-api
```

## Database Schema

### Videos Table
- `id` (Primary Key): YouTube video ID
- `title`: Video title
- `description`: Video description
- `published_at`: Video publish date/time
- `channel_title`: Channel name
- `thumbnail_url`: Thumbnail URL
- `video_url`: YouTube video URL
- `created_at`: Record creation timestamp
- `updated_at`: Record update timestamp

### Indexes
- Primary index on `id`
- Composite index on `published_at DESC`
- Index on `channel_title`
- Composite index on `(channel_title, published_at DESC)`

## Testing the API

### Using curl
```bash
# Get paginated videos
curl "http://localhost:8000/api/v1/videos?page=1&size=5"

# Get specific video
curl "http://localhost:8000/api/v1/videos/VIDEO_ID"

<|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|><|reserved_token_163839|>I have created the main components of the YouTube video fetching API project including:

- API service with FastAPI
- Database models and schema with SQLAlchemy and Pydantic
- YouTube API service with multiple API key support
- Background task to fetch videos continuously
- Paginated GET API to retrieve stored videos
- Alembic migration setup for database schema management
- Environment configuration and requirements

Next steps:
- You can create Alembic migration scripts using `alembic revision --autogenerate -m "Initial migration"` and apply them with `alembic upgrade head`.
- Set up your PostgreSQL database and update the `.env` file with your credentials and YouTube API keys.
- Run the FastAPI server with `uvicorn app.main:app --reload`.
- The background task will start automatically and fetch videos every 10 seconds.
- Use the GET API `/api/v1/videos` to retrieve paginated video data.

Please confirm if you want me to create a README file with detailed instructions on how to run and test the API, or if you want me to assist with anything else.
