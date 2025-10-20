from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

# Initialize FastAPI app
app = FastAPI(title="Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

# In-memory conversation storage (replace with database in production)
conversations = {}

def get_llm_response(message: str, conversation_history: list = None) -> str:
    """
    Replace this function with your actual LLM integration
    Examples:
    - OpenAI API
    - Anthropic Claude API
    - Hugging Face models
    - Local models
    """
    
    # Example with OpenAI (uncomment and add your API key)
    # import openai
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # 
    # messages = conversation_history or []
    # messages.append({"role": "user", "content": message})
    # 
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages
    # )
    # return response.choices[0].message.content
    
    # Example with Anthropic Claude (uncomment and add your API key)
    # import anthropic
    # client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # 
    # response = client.messages.create(
    #     model="claude-3-sonnet-20240229",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": message}]
    # )
    # return response.content[0].text
    
    # Placeholder response (replace with actual LLM)
    return f"Echo: {message} (Replace this with your LLM integration)"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Chatbot API is running",
        "version": "1.0.0"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    Receives a message and returns an LLM response
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get or create conversation history
        conv_id = request.conversation_id or "default"
        if conv_id not in conversations:
            conversations[conv_id] = []
        
        # Get LLM response
        response_text = get_llm_response(
            request.message,
            conversations[conv_id]
        )
        
        # Update conversation history
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
async def clear_conversation(conversation_id: str):
    """Clear conversation history"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation cleared"}
    return {"message": "Conversation not found"}

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)