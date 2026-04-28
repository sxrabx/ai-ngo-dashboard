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
  <img src="https://img.shields.io/badge/Vanilla_JS-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
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

**NGO AI Mission Intelligence System** is a production-grade coordination platform that modernises disaster response operations for non-governmental organisations. It combines a real-time Vanilla JS command dashboard with an autonomous AI backend to solve two fundamental challenges in crisis management:

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
│  │   Vanilla JS Frontend   │    │    FastAPI AI Backend      │     │
│  │      (frontend/)        │    │  (src/api/server.py)       │     │
│  │                         │    │                            │     │
│  │  • Mission Control      │    │  • /process endpoint       │     │
│  │  • Personnel Database   │◄───►  • CrewAI Agent Pipeline   │     │
│  │  • Interactive Maps     │    │  • ChromaDB Vector Search  │     │
│  │  • Logistics Hub        │    │  • Squad Assembly Logic    │     │
│  │  • System Health Feed   │    │  • Gamification Engine     │     │
│  └─────────────────────────┘    └────────────────────────────┘     │
│               │                               │                    │
│               ▼                               ▼                    │
│     Leaflet Interactive Map        NVIDIA NIM (Llama 3.1-8b)       │
│     Plotly Gauges & Charts        Sentence-Transformers Embeddings  │
│     JSON Persistence Layer        Offline Heuristic Fallback       │
└────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🖥️ Command Dashboard (`frontend/`)

| Module | Description |
|--------|-------------|
| **Mission Control** | Submit free-text crisis reports or upload PDF damage assessments. AI generates a structured mission plan (category, priority, volunteers needed) automatically. |
| **Operations Hub** | Live metrics — active missions, ready personnel, overall readiness %. Includes a Leaflet interactive map and Plotly readiness gauge. |
| **Personnel Database** | Live roster showing energy levels (colour-coded), XP, rank, and availability. |
| **Logistics Command** | Browse the NGO's asset catalogue — medical kits, rescue gear, survival supplies, satellite uplinks, drone fleet, and mission-ready kit configurations. |
| **System Health** | Real-time uptime, API gateway status, active AI mode (Cloud vs. Offline), and live telemetry feed. |

### 🤖 AI Intelligence Engine

| Capability | Description |
|------------|-------------|
| **AI Mission Generation** | Calls NVIDIA NIM (Llama 3.1-8b-instruct) via the CrewAI pipeline to classify incident category, urgency, and victim count from raw text. |
| **Offline Fallback Mode** | If the NVIDIA NIM API is unavailable, the system automatically switches to `offline_engine.py` — a local heuristics-based classifier — ensuring zero-downtime operation. |
| **Semantic Volunteer Matching** | ChromaDB + `all-MiniLM-L6-v2` (384-dim) embeddings match task requirements to volunteer skill vectors — no keyword matching, purely semantic. |
| **Multi-Tier Squad Assembly** | Squads are dynamically scaled by `people_count` and `priority`: Standard Squad (< 10 victims), Strike Force (10–40), Regiment / Mega-Squad (> 40), with Team Alpha/Beta/Gamma splits. |
| **PDF Report Extraction** | Upload NGO damage assessment PDFs; PyPDF2 extracts text and feeds it directly into the mission generation pipeline. |
| **Gamified Fatigue Tracking** | Volunteer energy depletes on deployment (0–100%). XP and level-up rewards are calculated by `gamifier.py` to sustain morale and prevent burnout. |
| **Multi-lingual Translation** | CrewAI translation agents render incident reports in Spanish and French for international responders. |

---

## 🛠️ Tech Stack

### Python Backend & AI
| Technology | Purpose |
|------------|---------|
| **Python 3.12+** | Core language |
| **FastAPI** | High-performance REST API server |
| **Uvicorn** | ASGI server for FastAPI |
| **CrewAI** | Multi-agent autonomous orchestration |
| **LangChain OpenAI** | LLM integration adapter |
| **LiteLLM** | Unified LLM gateway |
| **NVIDIA NIM API** | Cloud LLM inference — `meta/llama-3.1-8b-instruct` |
| **ChromaDB** | Local persistent vector database |
| **Sentence-Transformers** | `all-MiniLM-L6-v2` — 384-dim semantic embeddings |
| **PyPDF2** | PDF text extraction |
| **python-dotenv / pydantic-settings** | Environment variable management |

### Frontend & Launcher
| Technology | Purpose |
|------------|---------|
| **HTML / CSS / JavaScript** | Static frontend served on port 3000 |
| **Leaflet.js** | Interactive mapping |
| **Plotly.js** | Dynamic data visualization |
| **GSAP / Lucide** | Animations and iconography |
| **Node.js** | Developer launcher script (`launch.js`) |

---

## 📁 Project Structure

```text
ai-ngo-dashboard/
│
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
│   │   └── server.py                 ← FastAPI REST API (port 8000)
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
| **Python** | ≥ 3.12 | Required for all backend code |
| **pip** | Latest | Comes with Python |
| **Node.js** | ≥ 16 | Required only for the CLI launcher (`npm run launch`) |
| **NVIDIA NIM API Key** | — | Get yours at [build.nvidia.com](https://build.nvidia.com) |
| **Git** | Any | For cloning the repository |

---

## 🚀 Installation & Setup

### Option A — Automated Linux Setup (Fedora / Ubuntu)

```bash
git clone https://github.com/sxrabx/ai-ngo-dashboard.git
cd ai-ngo-dashboard
chmod +x setup_fedora.sh
./setup_fedora.sh
source venv_linux/bin/activate
```

### Option B — Manual Setup (Windows / macOS / Linux)

```bash
# 1. Clone & Navigate
git clone https://github.com/sxrabx/ai-ngo-dashboard.git
cd ai-ngo-dashboard

# 2. Virtual Environment
python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. Dependencies
pip install -r requirements.txt
npm run install:deps
```

---

## ▶️ Running the Application

### Option 1 — CLI Launcher (Recommended)

Starts both the static frontend (port 3000) and the FastAPI backend (port 8000).

```bash
npm run launch
```

### Option 2 — Manual Launch

**FastAPI REST API Backend:**
```bash
uvicorn src.api.server:app --reload --port 8000
```

**Static Frontend:**
```bash
python -m http.server 3000 -d frontend
```

---

## 📡 API Reference

Automatically documented at `http://localhost:8000/docs`.

### `POST /process`
Classify an incident and receive a full triage plan.

---

## 📝 Usage Notes

- **AI Mode Indicator:** The dashboard shows whether the system is running in **Cloud (NVIDIA NIM)** or **Offline (Local Heuristics)** mode.
- **Running tests:** `python -m pytest tests/`

---

## 📄 License
MIT License — Copyright (c) 2026 AI Intelligence Team

---

## 🙏 Credits
Built with ❤️ for faster disaster response.
- **AI Inference:** [NVIDIA NIM](https://build.nvidia.com)
- **Agent Orchestration:** [CrewAI](https://crewai.com)
- **Vector Database:** [ChromaDB](https://www.trychroma.com)
