# Complete Setup Guide - YouTube Video Fetcher API

## 🚀 Quick Start (5 minutes)

### Option 1: GitHub Clone & Run

1. **Clone from GitHub**
```bash
git clone https://github.com/yourusername/youtube-video-fetcher-api.git
cd youtube-video-fetcher-api
```

2. **Quick Setup Script**
```bash
# Make setup script executable
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Create GitHub Repository**
```bash
# On GitHub, create a new repository named "youtube-video-fetcher-api"
# Then clone it locally
git clone https://github.com/YOUR_USERNAME/youtube-video-fetcher-api.git
cd youtube-video-fetcher-api
```

2. **Copy all project files** (if you have them locally)
```bash
# Copy all files from the created project
cp -r youtube_video_api/* youtube-video-fetcher-api/
```

3. **Initialize Git**
```bash
cd youtube-video-fetcher-api
git init
git add .
git commit -m "Initial commit: YouTube Video Fetcher API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/youtube-video-fetcher-api.git
git push -u origin main
```

## 📋 Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] PostgreSQL 12+ installed
- [ ] YouTube Data API v3 key(s) obtained
- [ ] Git installed

## 🔧 Step-by-Step Setup

### 1. Get YouTube API Keys
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API key)
5. Copy your API key(s)

### 2. Database Setup
```bash
# Create PostgreSQL database
createdb youtube_videos

# Or using Docker
docker run --name postgres-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=youtube_videos -p 5432:5432 -d postgres:13
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

### 4. Install & Run
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Docker Quick Start

```bash
# Using Docker Compose (easiest)
docker-compose up --build

# Or using Docker
docker build -t youtube-video-api .
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://username:password@host:5432/youtube_videos \
  -e YOUTUBE_API_KEYS=your_api_key \
  -e SEARCH_QUERY=cricket \
  youtube-video-api
```

## ✅ Testing Your Setup

### 1. Check API is running
```bash
curl http://localhost:8000/health
```

### 2. Test video fetching
```bash
# Wait 10-20 seconds for initial fetch
curl http://localhost:8000/api/v1/videos
```

### 3. View Swagger Documentation
Open browser: http://localhost:8000/docs

## 🔄 GitHub Actions (Optional)

Create `.github/workflows/deploy.yml` for automatic deployment:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to server
      run: |
        # Add your deployment commands here
```

## 📱 One-Click Deploy Options

### Heroku
```bash
# Install Heroku CLI
heroku create youtube-video-fetcher-api
git push heroku main
```

### Railway
```bash
# Install Railway CLI
railway login
railway init
railway up
```

## 🔍 Troubleshooting

### Common Issues

1. **Database connection error**
   - Check PostgreSQL is running
   - Verify DATABASE_URL in .env
   - Ensure database exists

2. **YouTube API quota exceeded**
   - Add multiple API keys in .env
   - Reduce FETCH_INTERVAL_SECONDS

3. **Port already in use**
   - Change port in docker-compose.yml or use: `uvicorn app.main:app --reload --port 8001`

## 📞 Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify .env configuration
3. Ensure all prerequisites are installed
4. Check the README.md for detailed instructions
