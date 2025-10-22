@echo off
echo 🤖 Chatbot Local Development Setup
echo ====================================

echo.
echo 🔍 Checking if Node.js is installed...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js is installed

echo.
echo 🔍 Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python
    pause
    exit /b 1
)
echo ✅ Python is installed

echo.
echo 📦 Installing frontend dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed

echo.
echo 📦 Installing backend dependencies...
call pip install -r requirements.txt
call pip install uvicorn
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Set your GEMINI_API_KEY environment variable
echo 2. Run the backend: python local_server.py
echo 3. Run the frontend: npm run dev
echo 4. Open http://localhost:3000 in your browser
echo.
echo 💡 Or run both servers in separate terminals:
echo    Terminal 1: python local_server.py
echo    Terminal 2: npm run dev

pause
