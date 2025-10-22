from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import os
import uvicorn

app = FastAPI(title="Chat API - Local Development", version="1.0.0")

# For local development, you can set your API key here or use environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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

conversations = {}

def get_llm_response(message: str, conversation_history: list = None) -> str:
    if not API_KEY or API_KEY == "your-gemini-api-key-here":
        return f"Mock response to: {message} (API key not configured)"
    
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        messages = conversation_history or []
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gemini-2.0-flash-exp",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Local Chat API is running", "api_key_configured": API_KEY != "your-gemini-api-key-here"}

@app.post("/")
def chat(request: ChatRequest):
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
        
        return ChatResponse(
            response=response_text,
            conversation_id=conv_id
        )
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting local Chat API server...")
    print("📝 Make sure to set your GEMINI_API_KEY environment variable")
    print("🌐 API will be available at: http://localhost:8000")
    print("📊 API docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
