from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlInput(BaseModel):
    url: str

class UserQuery(BaseModel):
    user_query: str

@app.post("/crawl/")
async def crawl_documentation(input_data: UrlInput):
    print(f"Received url {input_data.url}")
    return {"status": "received"}

@app.post("/problems/")
async def generate_problems(query: UserQuery):
    # For MVP, returning random sample questions
    sample_questions = [
        "What is the main purpose of this framework?",
        "How do you install this tool?",
        "What are the key components?",
        "Explain the basic workflow",
        "What are the best practices?"
    ]
    return {"Problems": sample_questions} 