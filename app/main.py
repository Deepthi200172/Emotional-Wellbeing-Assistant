# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import create_agent_response

app = FastAPI()

# Allow Streamlit frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict this!
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    text: str


@app.post("/chat")
async def chat_endpoint(message: UserMessage):
    response = create_agent_response(message.text)
    return {"response": response}

