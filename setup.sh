#!/bin/bash
# CineBook - Complete Deployment Setup Script
# This script automates the setup process

echo "=================================="
echo "🎬 CineBook Installation Script"
echo "=================================="
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi
python_version=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $python_version found"
echo ""

# Check MongoDB
echo "Checking MongoDB installation..."
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB doesn't appear to be installed."
    echo "   Please install MongoDB from https://www.mongodb.com/try/download/community"
    echo "   Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ MongoDB found"
fi
echo ""

# Create virtual environment
echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Copy environment file
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created (please review and update if needed)"
else
    echo "✅ .env file already exists"
fi
echo ""

# Check if MongoDB is running
echo "Checking MongoDB connection..."
if python3 -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000).server_info()" 2>/dev/null; then
    echo "✅ MongoDB is running"
    
    # Seed database
    echo ""
    echo "Seeding database with sample data..."
    python3 seed_db.py
    if [ $? -eq 0 ]; then
        echo "✅ Database seeded successfully"
    else
        echo "⚠️  Database seeding might have failed"
    fi
else
    echo "⚠️  MongoDB connection failed"
    echo "   Make sure MongoDB is running:"
    echo "   - Windows: Run 'mongod' in another terminal"
    echo "   - macOS: brew services start mongodb-community"
    echo "   - Linux: sudo systemctl start mongod"
    echo ""
    echo "   You can seed the database later after starting MongoDB"
fi
echo ""

echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Make sure MongoDB is running"
echo "2. Run Flask backend:"
echo "   python3 app.py"
echo ""
echo "3. In another terminal, serve frontend:"
echo "   python3 -m http.server 8000"
echo ""
echo "4. Open in browser:"
echo "   http://localhost:8000/index.html"
echo ""
echo "📖 Documentation:"
echo "   - Quick Start: QUICK_START.md"
echo "   - Full Docs: README.md"
echo "   - Features: FEATURES.md"
echo ""
echo "=================================="
