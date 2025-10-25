from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chat API", version="1.0.0")

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

# Store conversations in memory
conversations = {}

def get_llm_response(message: str, conversation_history: list = None) -> str:
    if not API_KEY:
        logger.error("API key not configured")
        raise HTTPException(
            status_code=500, 
            detail="API key not configured. Please set GEMINI_API_KEY environment variable."
        )
    
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        messages = conversation_history or []
        messages.append({"role": "user", "content": message})
        
        logger.info(f"Sending request to Gemini with {len(messages)} messages")
        response = client.chat.completions.create(
            model="gemini-2.0-flash-exp",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM API error: {str(e)}")

@app.get("/")
async def health_check():
    logger.info("Health check requested")
    return {
        "status": "healthy", 
        "message": "Chat API is running",
        "api_key_configured": bool(API_KEY)
    }

@app.post("/")
async def chat(request: ChatRequest):
    logger.info(f"Chat request received: {request.message[:50]}...")
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        conv_id = request.conversation_id or "default"
        if conv_id not in conversations:
            conversations[conv_id] = []
        
        response_text = get_llm_response(
            request.message,
            conversations[conv_id]
        )
        
        conversations[conv_id].append({
            "role": "user",
            "content": request.message
        })
        conversations[conv_id].append({
            "role": "assistant",
            "content": response_text
        })
        
        logger.info(f"Response generated successfully for conversation {conv_id}")
        return ChatResponse(
            response=response_text,
            conversation_id=conv_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)