#!/bin/bash

# SNARE Development Setup and Run Script

echo "🔧 Setting up SNARE Development Environment..."

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Backend setup
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Frontend setup
echo "📦 Installing frontend dependencies..."
cd snare-web-frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the development servers:"
echo "  Backend:  source .venv/bin/activate && python run_server.py"
echo "  Frontend: cd snare-web-frontend && npm run dev"
echo ""
echo "🌐 Access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
