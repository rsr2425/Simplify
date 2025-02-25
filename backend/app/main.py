from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.app.problem_generator import ProblemGenerationPipeline
from backend.app.problem_grader import ProblemGradingPipeline
from typing import Dict, List
import asyncio

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

# TODO: Make this a list of {problem: str, answer: str}. Would be cleaner for data validation
class FeedbackRequest(BaseModel):
    user_query: str
    problems: list[str]
    user_answers: list[str]

class FeedbackResponse(BaseModel):
    feedback: List[str]

@app.post("/api/crawl/")
async def crawl_documentation(input_data: UrlInput):
    print(f"Received url {input_data.url}")
    return {"status": "received"}

@app.post("/api/problems/")
async def generate_problems(query: UserQuery):
    problems = ProblemGenerationPipeline().generate_problems(query.user_query)
    return {"Problems": problems}

@app.post("/api/feedback", response_model=FeedbackResponse)
async def get_feedback(request: FeedbackRequest):
    if len(request.problems) != len(request.user_answers):
        raise HTTPException(status_code=400, detail="Problems and user answers must have the same length")
    try:
        grader = ProblemGradingPipeline()
        
        grading_tasks = [
            grader.grade(
                query=request.user_query,
                problem=problem,
                answer=user_answer,
            )
            for problem, user_answer in zip(request.problems, request.user_answers)
        ]
        
        feedback_list = await asyncio.gather(*grading_tasks)
        
        return FeedbackResponse(feedback=feedback_list)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
