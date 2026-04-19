from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Tuple
import uvicorn
import sys
import os

# Set standard paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our AI logic from main.py
from src.main import process_new_task

app = FastAPI(
    title="AI Intelligence Layer API",
    description="Hackathon AI system for task classification, scoring, and volunteer matching.",
    version="1.0.0",
    servers=[{"url": "http://127.0.0.1:5000", "description": "Local Development Server"}]
)

# --- CORS SETUP ---
# This allows your frontend team (React/Vue/etc) to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc)
    allow_headers=["*"], # Allows all headers
)

# --- DATA MODELS ---

class TaskInput(BaseModel):
    task_id: str
    description: str
    people_count: Optional[int] = 1
    location_coords: Optional[Tuple[float, float]] = (0.0, 0.0)

class VolunteerInput(BaseModel):
    id: str
    name: str
    skills: List[str]
    location_coords: Tuple[float, float]
    available: bool

class MatchRequest(BaseModel):
    task: TaskInput
    volunteers: List[VolunteerInput]

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "AI Intelligence Layer is Online", "docs": "/docs"}

@app.post("/process")
def process_ai_request(data: MatchRequest):
    """
    Main AI Endpoint:
    1. Classifies the task (Category + Urgency)
    2. Calculates Priority Score
    3. Ranks Volunteers based on distance, skill, and availability
    """
    # Convert Pydantic models to dictionaries for our internal 
    # functions to handle comfortably
    task_dict = data.task.model_dump()
    volunteers_list = [v.model_dump() for v in data.volunteers]
    
    # Run the intelligence layer logic
    result = process_new_task(task_dict, volunteers_list)
    
    return result

if __name__ == "__main__":
    print("Starting AI Layer Server on http://127.0.0.1:5000")
    uvicorn.run(app, host="127.0.0.1", port=5000)
