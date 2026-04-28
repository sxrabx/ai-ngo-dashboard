"""
Lightweight FastAPI server that loads data from JSON files directly.
This version doesn't require heavy ML dependencies and starts immediately.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import os

app = FastAPI(
    title="NGO AI Intelligence Layer",
    version="1.0.0",
    description="Lightweight API serving volunteer and mission data"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data loader functions
def load_json(path):
    """Safely load JSON files"""
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
    return []

# Endpoints
@app.get("/")
def home():
    """Serve frontend"""
    return FileResponse("frontend/index.html")

@app.get("/style.css")
def get_css():
    return FileResponse("frontend/style.css")

@app.get("/app.js")
def get_js():
    return FileResponse("frontend/app.js")

@app.get("/roster")
def get_roster():
    """Returns the full volunteer roster"""
    volunteers = load_json("data/volunteers.json")
    return volunteers if volunteers else []

@app.get("/inventory")
def get_inventory():
    """Returns inventory data"""
    inventory = load_json("data/inventory.json")
    return inventory if inventory else []

@app.get("/inventory/stats")
def get_inventory_stats():
    """Returns inventory statistics"""
    stats = load_json("data/settings.json")
    return stats if stats else {}

@app.get("/missions")
def get_missions():
    """Returns missions data"""
    missions = load_json("data/missions.json")
    return missions if missions else []

@app.get("/activities")
def get_activities():
    """Returns nearby activities"""
    activities = load_json("data/nearby_activities.json")
    return activities if activities else []

@app.post("/process")
def process_ai_request(data: dict):
    """Process task request - returns mock response for now"""
    return {
        "status": "pending",
        "message": "Task received and queued for processing",
        "task": data
    }

@app.post("/recommend-gear")
def recommend_gear(data: dict):
    """Recommend gear based on mission"""
    description = data.get("description", "")
    return {
        "recommendations": ["Tent", "First Aid Kit", "Water Filters"],
        "reason": "Standard emergency response gear"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "NGO AI Backend is operational",
        "volunteer_count": len(load_json("data/volunteers.json")),
        "missions_count": len(load_json("data/missions.json"))
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting NGO AI Backend on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
