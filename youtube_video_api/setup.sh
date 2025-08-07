#!/bin/bash

# YouTube Video Fetcher API - Automated Setup Script

echo "🚀 YouTube Video Fetcher API Setup"
echo "=================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client not found. Install PostgreSQL or use Docker"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Check if database exists
echo "🔍 Checking database..."
if [ -f .env ]; then
    source .env
    if psql -lqt | cut -d \| -f 1 | grep -qw "youtube_videos"; then
        echo "✅ Database exists"
    else
        echo "⚠️  Database 'youtube_videos' does not exist"
        echo "Please create it with: createdb youtube_videos"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Create database: createdb youtube_videos"
echo "3. Run migrations: alembic upgrade head"
echo "4. Start server: uvicorn app.main:app --reload"
echo ""
echo "Or use Docker: docker-compose up --build"
