# AI Intelligence Layer: Smart Volunteer Coordination 🤖

This repository contains the "Intelligence Layer" for a volunteer management system. It is designed to automate task classification, extract actionable JSONs from chaotic field reports using CrewAI agents, and match the best volunteers using ChromaDB vector semantics and Proximity-First Smart Triage.

---

## 🛠️ Tools & Technologies Used

*   **Python (v3.12.7)**: The core programming language for the intelligence logic.
*   **NVIDIA NIM (Llama-3.1-8B-Instruct)**: Our reasoning engine for task classification and cognitive trace generation.
*   **CrewAI**: Orchestration framework for deploying autonomous agents (Extractors, Translators).
*   **ChromaDB**: Local Persistent Vector Database for semantic matching.
*   **Sentence Transformers (all-MiniLM-L6-v2)**: Generating 384-dimensional semantic embeddings for volunteer skills.
*   **FastAPI**: Backend REST API for high-performance integration.
*   **Vanilla JS & CSS**: Responsive, high-performance command center frontend.

---

## 📋 Technical Specifications & Requirements

### Core Environment
*   **Python Version**: `3.12.7`
*   **Package Manager**: `pip`
*   **Environment**: Virtual Environment (`venv`) recommended.

### AI Models & Intelligence
| Component | Model Name | Version/Provider | Purpose |
| :--- | :--- | :--- | :--- |
| **Reasoning LLM** | `meta/llama-3.1-8b-instruct` | NVIDIA NIM API | Classification, Triage, Logic |
| **Embedding Model** | `all-MiniLM-L6-v2` | Sentence-Transformers | Semantic Vector Generation |
| **Orchestration** | `CrewAI` | Latest Stable | Multi-agent task extraction |

### Primary Dependencies
*   `fastapi`: Web framework for API.
*   `chromadb`: Vector storage.
*   `crewai`: Agentic orchestration.
*   `python-dotenv`: Environment variable management.

---

## 📂 Project Structure (Hardened Architecture)

```text
d:\Hackathon Google\
├── config/               # System Configuration
│   └── settings.py       # Global settings & NVIDIA credentials
├── data/                 # Persistence Layer
│   ├── vectordb/         # ChromaDB Persistent Storage
│   ├── sample_tasks.json # Mock tasks for testing
│   ├── sample_volunteers.json
│   └── volunteer_stats.json # Gamification & Fatigue persistence
├── src/                  # Core Intelligence Layer
│   ├── api/              # Entry Points & Application Layer
│   │   └── server.py     # FastAPI Backend Integrations
│   ├── core/             # Domain Logic & Algorithms
│   │   ├── engine.py     # High-level task orchestration
│   │   ├── gamifier.py   # Fatigue, Leveling & Burnout protection
│   │   ├── matcher.py    # Vector search & semantic ranking
│   │   └── scorer.py     # Priority & Severity calculation
│   ├── nlp/              # AI & Cognitive Services
│   │   ├── classifier.py # NVIDIA NIM reasoning engine
│   │   ├── crew.py       # CrewAI Agentic multi-agent pipelines
│   │   ├── summarizer.py # Context condensation
│   │   └── vector_db.py  # ChromaDB interface & embedding generation
│   └── repository/       # Data Access Layer (Persistence abstraction)
├── tests/                # Unit & Integration Testing
├── .env                  # Private API Keys (DO NOT COMMIT)
└── requirements.txt      # Dependency manifest
```

---

## 🧠 Core System Capabilities

*   **Smart Document Extraction**: CrewAI dynamically reads unstructured, chaotic incident reports and extracts severity, actionable steps, and exact victim counts perfectly against chaotic noise.
*   **Multi-Lingual Auto-Translation**: Autonomous agents immediately parse the extracted task into French and Spanish for international responders.
*   **Semantic Vector Matching**: ChromaDB processes the text into vectors and mathematically identifies the absolute best volunteers based on semantic skill correlation, completely removing the limitation of exact keyword checking.
*   **Distance-Aware Smart Triage**: Ranks volunteers using a weighted score that identifies **Fastest Responders** who can arrive before the main squad.
*   **Mega-Squad Scaling**: Automatic tactical splitting into **Team Alpha/Beta** for large-scale incidents (>40 victims) with dedicated Leads.
*   **Volunteer Fatigue & Sustainability**: Live energy tracking (100-0%) and gamified burnout protection.
*   **Enterprise Impact Analytics**: A dynamically updating dashboard showing hours saved, efficiency metrics, and live rosters.

---

## 🛠️ Step-by-Step Run Guide

### 1. Requirements & Setup
Ensure you have Python 3.12+ installed and a valid NVIDIA NIM API Key.
```powershell
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
NVIDIA_API_KEY=your_key_here
```

### 3. Launch the Command Center (Frontend)
```powershell
python -m http.server 3000 --directory frontend
```
*Accessible at: http://127.0.0.1:3000*  
**Test Workflow:** Use the sidebar to upload a report (e.g., `test_report_extreme.txt`) and click `🪄 AI Auto-Extract` to activate the CrewAI agentic pipeline.

### 4. Launch the AI API (Backend)
```powershell
python src/api/server.py
```
*API Documentation: http://127.0.0.1:8000/docs*

---

## 📈 Project Roadmap & Milestones

### ✅ Completed (Hackathon MVP)
- [x] **Enterprise-Grade Refactor**: Migrated from a flat MVP to a decoupled directory structure (`api`, `core`, `nlp`).
- [x] **Autonomous NGO Report Extraction**: Multi-agent CrewAI pipeline auto-generating actionable JSON tasks directly from uploaded chaotic incident reports.
- [x] **NLP Upgrade (Semantic Matching)**: Upgraded from keyword matching to ChromaDB vector embeddings.
- [x] **Multi-lingual Translation**: CrewAI Agents automatically translating live incident reports into Spanish and French.
- [x] **Premium UI Revamp**: Implemented a "Dark Mode Elite" Vanilla JS interface with Inter/Playfair typography and glassmorphism.
- [x] **Smart Triage (Proximity-First)**: Real-time calculation using coordinate distance parsing to find Fast Responders.
- [x] **Mega-Squad Logic**: Handlers for high-impact disasters with dual-leadership teams (Team Alpha/Beta).
- [x] **Workload Balancing**: Prevent volunteer burnout via the dynamic Gamification/Fatigue Tracking System.

### 🚀 Phase 2: Future Vision
- [ ] **Interactive "Glow Up" Map**: Live visual deployment tracking using Folium.
- [ ] **External API Hazard Integration**: Using live traffic overlays (e.g., Google Maps) to actively re-route responders.
- [ ] **Mock Mobile Notifications**: Simulated UI view for volunteer WhatsApp/SMS triggers.
- [ ] **Predictive Resource Forecasting**: Advanced AI to predict regional resource spikes.

---
**Status:** MVP Fully Operational | Enterprise Architecture Hardened | Agentic Intelligence Online