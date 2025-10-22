# Local Development Setup

This guide will help you run the chatbot locally for development and testing.

## Quick Start

### Option 1: Automated Setup (Windows)

```bash
# Run the setup script
setup_local.bat
```

### Option 2: Manual Setup

1. **Install Dependencies**

   ```bash
   # Install frontend dependencies
   npm install

   # Install backend dependencies
   pip install -r requirements.txt
   pip install uvicorn
   ```

2. **Set Environment Variables**

   ```bash
   # Set your Gemini API key
   export GEMINI_API_KEY=your-gemini-api-key-here

   # Or on Windows:
   set GEMINI_API_KEY=your-gemini-api-key-here
   ```

3. **Start the Servers**

   **Terminal 1 - Backend:**

   ```bash
   python local_server.py
   ```

   Backend will run on: http://localhost:8000

   **Terminal 2 - Frontend:**

   ```bash
   npm run dev
   ```

   Frontend will run on: http://localhost:3000

4. **Test the Application**
   - Open http://localhost:3000 in your browser
   - The chatbot should automatically connect to the local API
   - Try sending a message!

## API Testing

You can also test the API directly:

- **Health Check:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Test Chat:** Send POST request to http://localhost:8000 with JSON body:
  ```json
  {
    "message": "Hello, how are you?"
  }
  ```

## Troubleshooting

### Common Issues:

1. **Port Already in Use**

   - Backend (8000): Change port in `local_server.py`
   - Frontend (3000): Next.js will automatically use next available port

2. **API Key Not Working**

   - Make sure `GEMINI_API_KEY` is set correctly
   - Check the API key is valid and has proper permissions

3. **CORS Errors**

   - The local server is configured to allow localhost:3000
   - If using a different port, update CORS settings in `local_server.py`

4. **Dependencies Issues**
   - Make sure Python 3.8+ is installed
   - Make sure Node.js 16+ is installed
   - Try updating pip: `pip install --upgrade pip`

## Development Tips

- The local server includes mock responses when API key is not configured
- Use browser dev tools to see detailed API logs
- The API documentation at `/docs` shows all available endpoints
- Hot reload is enabled for both frontend and backend

## Next Steps

Once local development is working:

1. Test all functionality locally
2. Deploy to Vercel when ready
3. The production version will automatically use `/api/chat` endpoint
