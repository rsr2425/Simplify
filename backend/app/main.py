from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.problem_generator import ProblemGenerator

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
    problems = ProblemGenerator().generate_problems(query.user_query)
    return {"Problems": problems} 
