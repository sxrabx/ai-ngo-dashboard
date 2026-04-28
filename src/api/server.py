from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Tuple
import uvicorn
import sys
import os
import json
import threading
import time
import traceback

# Set standard paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import our AI logic from main.py
from src.core.service import VolunteerService
from src.core.inventory_service import InventoryService
from src.core.engine import process_new_task
from src.core.gamifier import bulk_update_volunteers_after_task, recover_energy

# Initialize Services
vol_service = VolunteerService()
inv_service = InventoryService()

app = FastAPI(
    title="AI Intelligence Layer API",
    description="Hackathon AI system for task classification, scoring, and volunteer matching.",
    version="1.0.0",
    servers=[{"url": "http://127.0.0.1:8000", "description": "Local Development Server"}]
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

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# --- ENDPOINTS ---

# Mount static files from frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/style.css")
def get_css():
    return FileResponse("frontend/style.css")

@app.get("/app.js")
def get_js():
    return FileResponse("frontend/app.js")

@app.post("/process")
def process_ai_request(data: MatchRequest):
    """
    Main AI Endpoint:
    1. Classifies the task (Category + Urgency)
    2. Calculates Priority Score
    3. Ranks Volunteers based on distance, skill, and availability
    """
    # Convert Pydantic models to dictionaries
    task_dict = data.task.model_dump()
    
    # If no volunteers are provided, use the master list from our service
    if not data.volunteers:
        volunteers_list = vol_service.get_all_volunteers()
    else:
        volunteers_list = [v.model_dump() for v in data.volunteers]
    
    # Run the intelligence layer logic
    result = process_new_task(task_dict, volunteers_list)
    
    return result

@app.get("/roster")
def get_roster():
    """Returns the full volunteer roster with live stats."""
    return vol_service.get_all_volunteers()

@app.post("/roster/reset-energy")
def reset_roster_energy():
    """Emergency override to restore all energy levels."""
    vol_service.reset_all_energy()
    return {"status": "Success", "message": "Neural fatigue cleared."}

@app.get("/inventory")
def get_inventory():
    """Returns the full inventory data."""
    return inv_service.get_all_items()

@app.get("/inventory/stats")
def get_inventory_stats():
    """Returns inventory overview metrics."""
    return inv_service.get_stats()

@app.post("/inventory/add")
def add_inventory_item(data: dict):
    """Adds or updates an inventory item with immediate sync."""
    name = data.get("name")
    category = data.get("category", "Logistics")
    qty = data.get("qty", 0)
    
    if not name:
        return {"status": "Error", "message": "Name required"}
        
    res = inv_service.update_stock(name, qty, category)
    return {"status": "Success", "updated": res}

@app.post("/recommend-gear")
def recommend_gear(data: dict):
    """Infers recommended gear based on mission description and scale."""
    description = data.get("description", "")
    people_count = data.get("people_count", 1)
    return inv_service.infer_recommendations(description, people_count=people_count)

@app.get("/activities")
def get_activities():
    """Returns the list of nearby NGO/community activities."""
    path = "data/nearby_activities.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

class InventoryItem(BaseModel):
    name: str
    qty: int

class DispatchRequest(BaseModel):
    squad_ids: List[str]
    items: List[InventoryItem]
    xp_reward: int
    category: str
    urgency: Optional[str] = "Medium"

@app.post("/deploy")
@app.post("/dispatch")
def confirm_dispatch(data: DispatchRequest):
    """
    Synchronizes the dispatch with high-performance bulk processing.
    """
    try:
        # Fatigue Logic: Critical: -30, High: -20, Medium: -15, Low: -10
        energy_map = {
            "CRITICAL": 30,
            "HIGH": 20,
            "MEDIUM": 15,
            "LOW": 10
        }
        
        lookup_urgency = data.urgency.upper() if data.urgency else "MEDIUM"
        cost = energy_map.get(lookup_urgency, 15)

        # 1. Update Volunteers (Bulk Optimized)
        bulk_update_volunteers_after_task(data.squad_ids, data.xp_reward, data.category, energy_cost=cost)
        
        # 2. Update Inventory (Deduct items)
        deducted_items = inv_service.deduct_items(data.items)
        
        return {
            "status": "Success",
            "message": f"Deployment confirmed for {len(data.squad_ids)} units.",
            "deducted": deducted_items
        }
    except Exception as e:
        print(f"CRITICAL DISPATCH ERROR: {str(e)}")
        traceback.print_exc()
        return {"status": "Error", "message": str(e)}

# Recovery Loop: +5% every 5 minutes

def recovery_worker():
    while True:
        time.sleep(300) # 5 minutes
        try:
            from src.core.gamifier import recover_energy
            from src.repository.volunteer_repository import VolunteerRepository
            repo = VolunteerRepository()
            all_volunteers = repo.load_all()
            for v_id in all_volunteers:
                recover_energy(v_id, amount=5)
            print("Recovery cycle complete: +5% energy restored to all units.")
        except Exception as e:
            print(f"Recovery cycle failed: {e}")

# Start recovery thread in background
recovery_thread = threading.Thread(target=recovery_worker, daemon=True)
recovery_thread.start()

if __name__ == "__main__":
    print("Starting AI Layer Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
