#!/bin/bash

# 🚀 AIpply API Deployment Script
# This script helps you deploy AIpply API quickly

set -e  # Exit on any error

echo "🚀 AIpply API Deployment Script"
echo "================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file and add your OPENAI_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  Please set your OPENAI_API_KEY in .env file"
    echo "   Get your key from: https://platform.openai.com/api-keys"
    exit 1
fi

echo "✅ Environment configuration looks good!"

# Function to deploy to Heroku
deploy_heroku() {
    echo "🔧 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Please install it first:"
        echo "   https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Check if logged in
    if ! heroku auth:whoami &> /dev/null; then
        echo "🔐 Please login to Heroku:"
        heroku login
    fi
    
    # Create app if it doesn't exist
    if [ -z "$HEROKU_APP_NAME" ]; then
        read -p "Enter Heroku app name (or press Enter for auto-generated): " HEROKU_APP_NAME
    fi
    
    if [ -n "$HEROKU_APP_NAME" ]; then
        heroku create "$HEROKU_APP_NAME" || echo "App might already exist, continuing..."
    else
        heroku create || echo "App might already exist, continuing..."
    fi
    
    # Add PostgreSQL addon
    echo "🗄️  Adding PostgreSQL database..."
    heroku addons:create heroku-postgresql:hobby-dev || echo "PostgreSQL might already exist"
    
    # Set environment variables
    echo "🔑 Setting environment variables..."
    heroku config:set OPENAI_API_KEY="$(grep OPENAI_API_KEY .env | cut -d'=' -f2)"
    heroku config:set ENVIRONMENT=production
    
    # Deploy
    echo "📦 Deploying application..."
    git push heroku main
    
    echo "🎉 Deployment successful!"
    echo "🌐 Your app is available at: $(heroku apps:info --json | jq -r '.app.web_url')"
    echo "📚 API docs: $(heroku apps:info --json | jq -r '.app.web_url')/docs"
}

# Function to run locally with Docker
run_local() {
    echo "🐳 Running locally with Docker..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker first:"
        echo "   https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose not found. Please install Docker Compose first"
        exit 1
    fi
    
    # Build and run
    echo "🔨 Building Docker image..."
    docker-compose build
    
    echo "🚀 Starting services..."
    docker-compose up -d
    
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Test health endpoint
    echo "🧪 Testing health endpoint..."
    if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Application is running successfully!"
        echo "🌐 Frontend: http://localhost:8000"
        echo "📚 API docs: http://localhost:8000/docs"
        echo "🔍 Health check: http://localhost:8000/api/health"
    else
        echo "❌ Health check failed. Check logs:"
        docker-compose logs
    fi
}

# Function to run locally with Python
run_python() {
    echo "🐍 Running locally with Python..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Please install Python 3.11+ first"
        exit 1
    fi
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate || source venv/Scripts/activate
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    # Run application
    echo "🚀 Starting application..."
    python main_enhanced.py
}

# Main menu
echo ""
echo "Choose deployment option:"
echo "1) Deploy to Heroku (Production)"
echo "2) Run locally with Docker"
echo "3) Run locally with Python"
echo "4) Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        deploy_heroku
        ;;
    2)
        run_local
        ;;
    3)
        run_python
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo "📖 For more detailed instructions, see:"
echo "   - QUICK_START.md"
echo "   - DEPLOYMENT_GUIDE.md"
echo "   - SECURITY_CONFIG.md"
echo "   - DATABASE_SETUP.md"
