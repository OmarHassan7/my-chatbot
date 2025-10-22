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
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    
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
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app, lifespan="off")
