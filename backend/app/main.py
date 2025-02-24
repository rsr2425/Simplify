from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.app.problem_generator import ProblemGenerator

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

@app.post("/api/crawl/")
async def crawl_documentation(input_data: UrlInput):
    print(f"Received url {input_data.url}")
    return {"status": "received"}

@app.post("/api/problems/")
async def generate_problems(query: UserQuery):
    problems = ProblemGenerator().generate_problems(query.user_query)
    return {"Problems": problems}

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
