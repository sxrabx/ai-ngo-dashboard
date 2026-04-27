<h1 align="center">
  <br>
  🛰️ NGO AI Mission Intelligence System
  <br>
</h1>

<p align="center">
  <strong>A full-stack AI command platform for real-time disaster response — intelligent mission generation, semantic volunteer triage, interactive maps, and live inventory management.</strong>
</p>

<p align="center">
  <a href="https://github.com/sxrabx/ai-ngo-dashboard/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/CrewAI-Agents-FF9900?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/NVIDIA-NIM_API-76B900?style=for-the-badge&logo=nvidia&logoColor=white" />
  <img src="https://img.shields.io/badge/Node.js-Launcher-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" />
</p>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Reference](#-api-reference)
- [Usage Notes](#-usage-notes)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🌟 Overview

**NGO AI Mission Intelligence System** is a production-grade coordination platform that modernises disaster response operations for non-governmental organisations. It combines a real-time Streamlit command dashboard with an autonomous AI backend to solve two fundamental challenges in crisis management:

1. **Unstructured Field Reports → Actionable Missions** — Multi-agent CrewAI pipelines powered by NVIDIA NIM (Llama 3.1) parse chaotic, free-text incident reports and PDF documents into structured mission objects with severity ratings, volunteer requirements, and multi-lingual translations.

2. **Inefficient Volunteer Deployment → Intelligent Triage** — A local ChromaDB vector store with Sentence-Transformer embeddings replaces naive keyword matching. Volunteers are scored by semantic skill alignment, proximity, and live energy level — preventing burnout while maximising response speed.

An offline AI fallback mode ensures the platform stays operational even when the NVIDIA NIM API is unavailable.

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────────────────────────────────┐
│                    NGO AI COMMAND PLATFORM                         │
│                                                                    │
│  ┌─────────────────────────┐    ┌────────────────────────────┐     │
│  │   Streamlit Dashboard   │    │    FastAPI AI Backend      │     │
│  │      (app.py)           │    │  (src/api/server.py)       │     │
│  │                         │    │                            │     │
│  │  • Mission Lab          │    │  • /process endpoint       │     │
│  │  • Volunteer Roster     │◄───►  • CrewAI Agent Pipeline   │     │
│  │  • Map Intelligence     │    │  • ChromaDB Vector Search  │     │
│  │  • Inventory & Logistics│    │  • Squad Assembly Logic    │     │
│  │  • System Health / Logs │    │  • Gamification Engine     │     │
│  └─────────────────────────┘    └────────────────────────────┘     │
│               │                               │                    │
│               ▼                               ▼                    │
│     Folium Interactive Map        NVIDIA NIM (Llama 3.1-8b)        │
│     Plotly Gauges & Charts        Sentence-Transformers Embeddings  │
│     JSON Persistence Layer        Offline Heuristic Fallback        │
└────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🖥️ Command Dashboard (`app.py`)

| Module | Description |
|--------|-------------|
| **Dashboard** | Live metrics — active missions, ready personnel, overall readiness %. Includes a Folium interactive map and Plotly readiness gauge. Triggers a CODE RED alert when readiness drops below 30%. |
| **Mission Lab** | Submit free-text crisis reports or upload PDF damage assessments. AI generates a structured mission plan (category, priority, volunteers needed) automatically. |
| **Volunteer Roster** | Live roster showing energy levels (colour-coded), XP, rank, and availability. One-click global energy recovery cycle. |
| **Map Intelligence** | Full-screen Folium map displaying all active missions (red pulse markers) and available volunteers (blue markers) by sector. |
| **Inventory & Logistics** | Browse the NGO's asset catalogue — medical kits, rescue gear, survival supplies, satellite uplinks, drone fleet, and mission-ready kit configurations. |
| **System Health** | Real-time uptime, API gateway status, active AI mode (Cloud vs. Offline), and live telemetry feed. |
| **Logs** | Full operational log viewer showing all system events in reverse chronological order. |

### 🤖 AI Intelligence Engine

| Capability | Description |
|------------|-------------|
| **AI Mission Generation** | Calls NVIDIA NIM (Llama 3.1-8b-instruct) via the CrewAI pipeline to classify incident category, urgency, and victim count from raw text. |
| **Offline Fallback Mode** | If the NVIDIA NIM API is unavailable, the system automatically switches to `offline_engine.py` — a local heuristics-based classifier — ensuring zero-downtime operation. |
| **Semantic Volunteer Matching** | ChromaDB + `all-MiniLM-L6-v2` (384-dim) embeddings match task requirements to volunteer skill vectors — no keyword matching, purely semantic. |
| **Multi-Tier Squad Assembly** | Squads are dynamically scaled by `people_count` and `priority`: Standard Squad (< 10 victims), Strike Force (10–40), Regiment / Mega-Squad (> 40), with Team Alpha/Beta/Gamma splits. |
| **PDF Report Extraction** | Upload NGO damage assessment PDFs; PyPDF2 extracts text and feeds it directly into the mission generation pipeline. |
| **Gamified Fatigue Tracking** | Volunteer energy depletes on deployment (0–100%). XP and level-up rewards are calculated by `gamifier.py` to sustain morale and prevent burnout. |
| **Multi-lingual Translation** | CrewAI translation agents render incident reports in Spanish and French for international responders (secondary dashboard). |

---

## 🛠️ Tech Stack

### Python Backend & AI
| Technology | Purpose |
|------------|---------|
| **Python 3.12+** | Core language |
| **FastAPI** | High-performance REST API server |
| **Uvicorn** | ASGI server for FastAPI |
| **Streamlit** | Interactive command dashboard UI |
| **CrewAI** | Multi-agent autonomous orchestration |
| **LangChain OpenAI** | LLM integration adapter |
| **LiteLLM** | Unified LLM gateway |
| **NVIDIA NIM API** | Cloud LLM inference — `meta/llama-3.1-8b-instruct` |
| **ChromaDB** | Local persistent vector database |
| **Sentence-Transformers** | `all-MiniLM-L6-v2` — 384-dim semantic embeddings |
| **Pandas** | Data manipulation |
| **Plotly** | Interactive gauges and charts |
| **Folium + streamlit-folium** | Interactive deployment maps |
| **PyPDF2** | PDF text extraction |
| **python-dotenv / pydantic-settings** | Environment variable management |

### Launcher & Frontend
| Technology | Purpose |
|------------|---------|
| **Node.js** | Developer launcher script (`launch.js`) |
| **chalk, ora, boxen, cli-table3, open** | Launcher CLI UI libraries |
| **HTML / CSS / JavaScript** | Static frontend (`frontend/`) served on port 3000 |

---

## 📁 Project Structure

```text
ai-ngo-dashboard/
│
├── 📄 app.py                          ← Main Streamlit Command Dashboard
├── 📄 launch.js                       ← Node.js NeoFetch-style CLI launcher
├── 📄 package.json                    ← Launcher npm configuration
├── 📄 requirements.txt                ← Python dependencies
├── 📄 .env.example                    ← Environment variable template
├── 📄 setup_fedora.sh                 ← Automated Linux setup script
│
├── 📂 config/
│   └── settings.py                   ← Pydantic settings (loads .env)
│
├── 📂 src/
│   ├── 📂 api/
│   │   ├── server.py                 ← FastAPI REST API (port 8000)
│   │   └── dashboard.py              ← CrewAI-powered Streamlit dashboard
│   ├── 📂 core/
│   │   ├── engine.py                 ← Task orchestration pipeline
│   │   ├── service.py                ← Volunteer service layer
│   │   ├── scorer.py                 ← Priority & severity calculation
│   │   ├── matcher.py                ← Vector search & semantic ranking
│   │   ├── gamifier.py               ← Fatigue, XP & leveling logic
│   │   ├── inventory_service.py      ← Inventory management service
│   │   └── offline_engine.py         ← Local heuristic AI fallback
│   ├── 📂 nlp/
│   │   ├── classifier.py             ← NVIDIA NIM LLM interface
│   │   ├── crew.py                   ← CrewAI multi-agent pipelines
│   │   ├── summarizer.py             ← Context condensation
│   │   └── vector_db.py              ← ChromaDB interface & embeddings
│   └── 📂 repository/
│       └── volunteer_repository.py   ← Data access layer
│
├── 📂 frontend/
│   ├── index.html                    ← Static frontend entry point
│   ├── style.css                     ← Frontend styles
│   └── app.js                        ← Frontend JavaScript
│
├── 📂 data/                           ← JSON persistence layer
│   ├── volunteers.json
│   ├── missions.json
│   ├── inventory.json
│   ├── deployments.json
│   ├── ngo_reports.json
│   ├── sample_tasks.json
│   ├── sample_volunteers.json
│   └── volunteer_stats.json
│
└── 📂 tests/
    └── test_ai_logic.py              ← Unit & integration tests
```

---

## ✅ Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| **Python** | ≥ 3.12 | Required for all backend and dashboard code |
| **pip** | Latest | Comes with Python |
| **Node.js** | ≥ 16 | Required only for the CLI launcher (`npm run launch`) |
| **NVIDIA NIM API Key** | — | Get yours at [build.nvidia.com](https://build.nvidia.com) |
| **Git** | Any | For cloning the repository |

> **Note:** Node.js is optional. You can run the app directly with Python commands if you prefer.

---

## 🚀 Installation & Setup

### Option A — Automated Linux Setup (Fedora / Ubuntu)

```bash
# Clone the repository
git clone https://github.com/sxrabx/ai-ngo-dashboard.git
cd ai-ngo-dashboard

# Run the automated setup script
chmod +x setup_fedora.sh
./setup_fedora.sh

# Activate the created virtual environment
source venv_linux/bin/activate
```

### Option B — Manual Setup (Windows / macOS / Linux)

```bash
# 1. Clone the repository
git clone https://github.com/sxrabx/ai-ngo-dashboard.git
cd ai-ngo-dashboard

# 2. Create and activate a Python virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install all Python dependencies
pip install -r requirements.txt

# 4. (Optional) Install Node.js launcher dependencies
npm run install:deps
```

---

## 🔐 Configuration

Copy the example environment file and add your API key:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Then open `.env` and set your values:

```env
# Required — your NVIDIA NIM API key
NVIDIA_API_KEY=your_nvidia_api_key_here

# Optional — defaults shown below; change only if using a different endpoint
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1/chat/completions
OPENAI_API_BASE=https://integrate.api.nvidia.com/v1
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NVIDIA_API_KEY` | ✅ Yes | — | API key for NVIDIA NIM (Llama 3.1 inference) |
| `NVIDIA_API_URL` | No | `https://integrate.api.nvidia.com/v1/chat/completions` | NVIDIA NIM chat completions endpoint |
| `OPENAI_API_BASE` | No | `https://integrate.api.nvidia.com/v1` | Base URL used by LangChain/LiteLLM adapter |

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`. Use `.env.example` as the reference template only.

> 💡 **Offline mode:** If `NVIDIA_API_KEY` is missing or the API is unreachable, the system automatically falls back to the local heuristics engine (`src/core/offline_engine.py`) — no crash, degraded-but-operational AI.

---

## ▶️ Running the Application

### Option 1 — CLI Launcher (Recommended)

The Node.js launcher starts both the static frontend (port 3000) and the FastAPI backend (port 8000) with a polished terminal UI.

```bash
# Install launcher CLI dependencies (first time only)
npm run install:deps

# Start the full platform
npm run launch
```

**Controls:** Press `R` to restart all services · Press `Q` to quit.

| Service | URL |
|---------|-----|
| Static Frontend | http://localhost:3000 |
| FastAPI Backend | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |

---

### Option 2 — Manual Launch (Individual Services)

Run each service in its own terminal:

**Main Streamlit Dashboard (recommended entry point):**
```bash
streamlit run app.py
# Opens at http://localhost:8501
```

**FastAPI REST API Backend:**
```bash
uvicorn src.api.server:app --reload --port 8000
# Opens at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

**Static Frontend only:**
```bash
python -m http.server 3000 -d frontend
# Opens at http://localhost:3000
```

**Secondary CrewAI-powered Dashboard** (advanced AI triage view):
```bash
streamlit run src/api/dashboard.py
# Opens at http://localhost:8501
```

---

## 📡 API Reference

The FastAPI backend exposes a REST API documented automatically at `http://localhost:8000/docs`.

### `POST /process`

Classify an incident report and receive a full triage plan with scored volunteer matches and squad assembly.

**Request Body:**
```json
{
  "task": {
    "task_id": "T-100",
    "description": "Massive flooding in Sector Beta, approximately 45 people trapped on rooftops.",
    "people_count": 45,
    "location_coords": [28.61, 77.20]
  },
  "volunteers": [
    {
      "id": "V1",
      "name": "Jane Doe",
      "skills": ["Water Rescue", "Medical"],
      "location_coords": [28.60, 77.19],
      "available": true
    }
  ]
}
```

**Response:** Structured JSON with AI classification, severity score, matched squad (or Mega-Squad splits), and gamification rewards.

---

## 📝 Usage Notes

- **First run with a fresh `data/` directory:** The dashboard will show empty metrics until you add volunteers via `data/volunteers.json`. See `data/sample_volunteers.json` for the expected schema.
- **PDF Upload:** Navigate to **Mission Lab → PDF Extraction** and upload any NGO damage report PDF. The system extracts the first 1,000 characters for mission generation.
- **Code Red Alert:** When average volunteer energy drops below 30%, the dashboard displays a pulsing red alert banner. Use **Volunteer Roster → Initiate Recovery Cycle** to restore energy.
- **AI Mode Indicator:** The sidebar shows whether the system is running in **Cloud (NVIDIA NIM)** or **Offline (Local Heuristics)** mode. Offline mode activates automatically on API failure.
- **Running tests:**
  ```bash
  python -m pytest tests/
  ```

---

## 🗺️ Roadmap

### ✅ Completed (MVP)
- [x] Streamlit Command Dashboard with dark-mode UI and Plotly analytics
- [x] NVIDIA NIM (Llama 3.1) mission generation pipeline
- [x] Offline heuristic AI fallback for zero-downtime operation
- [x] Folium interactive deployment map (missions + volunteers)
- [x] PDF damage report ingestion and mission extraction
- [x] ChromaDB semantic volunteer matching
- [x] Multi-tier squad assembly (Standard / Strike Force / Mega-Squad / Regiment)
- [x] Gamified energy & XP fatigue tracking system
- [x] Inventory & Logistics management module
- [x] FastAPI REST backend with auto-generated Swagger docs
- [x] Node.js NeoFetch-style CLI launcher
- [x] Multi-lingual translation via CrewAI agents

### 🔭 Phase 2: Future Vision
- [ ] Live visual deployment tracking with animated Folium/Plotly maps
- [ ] External hazard API integration (live traffic, weather overlays)
- [ ] Simulated mobile push notifications (WhatsApp/SMS mock)
- [ ] Predictive resource forecasting using historical mission data

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. **Create** your feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes:
   ```bash
   git commit -m 'feat: add some feature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** and describe your changes

Please ensure your code follows the existing project style and does not break existing functionality. Run `python -m pytest tests/` before submitting.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

```
MIT License — Copyright (c) 2026 AI Intelligence Team
```

---

## 🙏 Credits

Built with ❤️ for faster disaster response, smarter volunteer coordination, and more resilient NGOs.

- **AI Inference:** [NVIDIA NIM](https://build.nvidia.com) — `meta/llama-3.1-8b-instruct`
- **Agent Orchestration:** [CrewAI](https://crewai.com)
- **Vector Database:** [ChromaDB](https://www.trychroma.com)
- **Embeddings:** [Sentence-Transformers](https://sbert.net) — `all-MiniLM-L6-v2`
- **Dashboard:** [Streamlit](https://streamlit.io) · [Plotly](https://plotly.com) · [Folium](https://python-visualization.github.io/folium)
- **API:** [FastAPI](https://fastapi.tiangolo.com)

---

<p align="center">
  <sub>🛰️ NGO AI Mission Intelligence System — Operational. Intelligence Online.</sub>
</p>
