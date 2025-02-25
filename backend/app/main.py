from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.app.problem_generator import ProblemGenerationPipeline
from typing import Dict, List

app = FastAPI()

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

class FeedbackInput(BaseModel):
    user_query: str
    problems: list[str]
    user_answers: list[str]

@app.post("/api/crawl/")
async def crawl_documentation(input_data: UrlInput):
    print(f"Received url {input_data.url}")
    return {"status": "received"}

@app.post("/api/problems/")
async def generate_problems(query: UserQuery):
    problems = ProblemGenerationPipeline().generate_problems(query.user_query)
    return {"Problems": problems}

@app.post("/api/feedback/")
async def submit_feedback(feedback: FeedbackInput):
    # check if problems len is equal to user_answers len
    if len(feedback.problems) != len(feedback.user_answers):
        raise HTTPException(status_code=400, detail="Problems and user answers must have the same length")
    
    for problem, user_answer in zip(feedback.problems, feedback.user_answers):
        print(f"Problem: {problem}")
        print(f"User answer: {user_answer}")
    
    return {"status": "success"}

# Serve static files
app.mount("/static", StaticFiles(directory="/app/static/static"), name="static")

# Root path handler
@app.get("/")
async def serve_root():
    return FileResponse("/app/static/index.html")

# Catch-all route for serving index.html
@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    # Skip API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # For all other routes, serve the React index.html
    return FileResponse("/app/static/index.html") 
