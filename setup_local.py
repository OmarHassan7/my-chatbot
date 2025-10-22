#!/usr/bin/env python3
"""
Local development script for the Chatbot project
This script helps you run both the frontend and backend locally
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if Node.js is installed
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✅ Node.js: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False
    
    # Check if npm is installed
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        print(f"✅ npm: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ npm not found. Please install npm")
        return False
    
    # Check if Python is installed
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Python not found. Please install Python")
        return False
    
    return True

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run(["pip", "install", "uvicorn"], check=True)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    print("📍 Backend will run on: http://localhost:8000")
    print("📊 API docs will be available at: http://localhost:8000/docs")
    
    # Set environment variable for API key if not set
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not set. The API will return mock responses.")
        print("   Set it with: export GEMINI_API_KEY=your-api-key")
    
    try:
        subprocess.run([sys.executable, "local_server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def start_frontend():
    """Start the frontend development server"""
    print("\n🚀 Starting frontend server...")
    print("📍 Frontend will run on: http://localhost:3000")
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

def main():
    print("🤖 Chatbot Local Development Setup")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Install dependencies
    if not install_frontend_deps():
        sys.exit(1)
    
    if not install_backend_deps():
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Set your GEMINI_API_KEY environment variable")
    print("2. Run the backend: python local_server.py")
    print("3. Run the frontend: npm run dev")
    print("4. Open http://localhost:3000 in your browser")
    print("\n💡 Or run both servers in separate terminals:")
    print("   Terminal 1: python local_server.py")
    print("   Terminal 2: npm run dev")

if __name__ == "__main__":
    main()
