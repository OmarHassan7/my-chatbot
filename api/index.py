from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import os
from mangum import Mangum

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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

@app.get("/api")
def root():
    return {
        "status": "online",
        "message": "Chatbot API is running",
        "version": "1.0.0"
    }

@app.post("/api/chat")
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
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/conversation/{conversation_id}")
def clear_conversation(conversation_id: str):
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation cleared"}
    return {"message": "Conversation not found"}

# Mangum handler for Vercel
handler = Mangum(app, lifespan="off")