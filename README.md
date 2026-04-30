<div align="center">
  <img src="assets/hero_banner.png" alt="NGO AI Tactical Command Hero" width="800">

# 🛰️ NGO AI Tactical Command System

### _Autonomous Mission Intelligence for Disaster Response & Volunteer Triage_

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA_NIM-Llama_3.1_405B-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Search-FF6F00?style=for-the-badge)](https://www.trychroma.com/)
[![License: ISC](https://img.shields.io/badge/License-ISC-8E75FF?style=for-the-badge)](LICENSE)

---

**An elite, full-stack AI platform that transforms chaotic disaster field reports into structured mission intelligence, then automatically deploys the best-matched volunteer squads — all in seconds.**

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Folder Structure](#-folder-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Running the Platform](#-running-the-platform)
- [API Reference](#-api-reference)
- [Usage Notes](#-usage-notes)
- [Project Roadmap](#-project-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🌟 Overview

The **NGO AI Tactical Command System** is a production-grade coordination platform purpose-built to modernize disaster response and volunteer logistics. It tackles the critical bottlenecks of crisis management by combining high-fidelity reasoning with real-time operational data.

1. **Unstructured Field Reports → Actionable Data** — Autonomous multi-agent **CrewAI** pipelines powered by **NVIDIA NIM (Meta Llama 3.1 405B Instruct)** parse messy, unstructured incident reports (text or PDF) into clean mission JSON objects, complete with severity scoring, victim counts, and tactical categorization.

2. **Precision Volunteer Deployment** — A **ChromaDB**-powered semantic vector search replaces brittle keyword matching, finding the best available volunteers based on skill relevance, geographic proximity, and current energy levels to prevent responder burnout.

The result is a unified, real-time command dashboard featuring a premium **Vanilla JS/CSS3** glassmorphic interface, backed by a high-performance **FastAPI** backend and an **offline fallback engine** for resilient field operations.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Llama 405B Extraction** | Flagship-class reasoning via NVIDIA NIM parses unstructured reports and PDFs into structured mission intelligence. |
| 🗺️ **Semantic Squad Matching** | ChromaDB + Sentence-Transformers finds the right volunteers via 384-dimensional skill embeddings. |
| 📍 **Proximity-First Triage** | Distance-aware ranking identifies the fastest responders based on sector-based GPS coordinates. |
| 🦅 **Battalion Scaling** | Large-scale incidents (40+ victims) automatically scale response into **Alpha, Beta, Gamma, and Delta** teams. |
| ⚡ **Fatigue & XP Engine** | Real-time volunteer health tracking (0–100%) and XP-based tactical leveling (Ghost Operative, Vanguard Lead). |
| 🌍 **Auto-Translation** | Missions are automatically translated into multiple languages for international responder coordination. |
| 📊 **Tactical Dashboard** | High-fidelity Glassmorphic UI with Leaflet.js maps, Plotly.js analytics gauges, and live roster telemetry. |
| 📦 **Logistics Sync** | Integrated inventory system that automatically deducts required gear (MREs, Hazmat suits) during dispatch. |
| 🔌 **Heuristic Fallback** | Robust regex-based local intelligence triggers automatically if the NVIDIA NIM API is unreachable. |
| 🚀 **Elite CLI Launcher** | Orchestrated Node.js launcher for seamless backend/frontend service synchronization and health monitoring. |

---

## 🏗️ Architecture

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    NGO AI TACTICAL COMMAND SYSTEM                    │
│                                                                      │
│  ┌─────────────────────────────┐   ┌──────────────────────────────┐  │
│  │   Elite Web Dashboard       │   │      FastAPI REST API        │  │
│  │   (frontend/index.html)     │   │      (src/api/server.py)     │  │
│  │  • Mission Laboratory       │   │  • Llama-3.1-405B Gateway    │  │
│  │  • Personnel Database       │◄──►  • Mission Extraction Engine  │  │
│  │  • Tactical Mapping         │   │  • Inventory Sync Logic      │  │
│  │  • Real-time Analytics      │   │  • Volunteer Roster Mgmt     │  │
│  └─────────────┬───────────────┘   └──────────────┬───────────────┘  │
│                │                                   │                  │
│                ▼                                   ▼                  │
│        Visual Interaction Layer            Intelligence Core         │
│     (Leaflet.js / Plotly.js)        (CrewAI + NVIDIA NIM 405B)       │
│                                            (ChromaDB + S-BERT)       │
└──────────────────────────────────────────────────────────────────────┘
```

### Intelligence Pipeline

```text
Incident Report (Text/PDF) ───► AI Extraction Agents ───► Llama 3.1 405B (NIM)
                                         │
                                         ▼
                                Structured JSON Mission 
                    (Severity, Category, Victim Count, Translations)
                                         │
                                         ▼
                               ChromaDB Vector Search 
                         (Semantic Match + Proximity Scoring)
                                         │
                                         ▼
  ┌───────── < 12 victims ────────┐      │      ┌───────── 40+ victims ─────────┐
  │      RESCUE CELL (Alpha)      │◄─────┴─────►│    BATTALION (Alpha-Delta)    │
  └───────────────────────────────┘             └───────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Python Backend
| Technology | Role |
|---|---|
| **FastAPI** | High-performance async REST API framework. |
| **Meta Llama-3.1-405B** | Flagship reasoning engine via NVIDIA NIM. |
| **CrewAI** | Multi-agent task orchestration for extraction/translation. |
| **ChromaDB** | Persistent local vector database for personnel storage. |
| **Sentence-Transformers** | 384-dim skill embeddings (`all-MiniLM-L6-v2`). |
| **Plotly.js** | Data visualization for tactical analytics. |
| **PyPDF2** | Automated PDF damage report processing. |

### Tactical Frontend
| Technology | Role |
|---|---|
| **Vanilla JS / CSS3** | High-contrast, glassmorphic UI (No heavy frameworks). |
| **Leaflet.js** | Interactive geospatial mapping and pulse animations. |
| **GSAP** | Smooth micro-animations for UI transitions. |
| **Node.js** | Orchestrated CLI launcher (`launch.js`). |

---

## 📁 Folder Structure

```text
ai-ngo-dashboard/
│
├── 📄 launch.js                  ← Orchestrated Node.js launcher
├── 📄 requirements.txt           ← Python dependency manifest
├── 📄 package.json               ← Node.js configuration & ISC License
├── 📄 .env.example               ← Environment variable template
├── 📄 setup_fedora.sh            ← Automated Linux setup script
├── 📄 LICENSE                    ← ISC License Declaration
│
├── 📂 config/
│   └── settings.py               ← Pydantic configuration (API endpoints)
│
├── 📂 src/
│   ├── 📂 api/
│   │   └── server.py             ← FastAPI REST Gateway
│   ├── 📂 core/
│   │   ├── engine.py             ← Mission deployment orchestrator
│   │   ├── service.py            ← Volunteer logic & Roster mgmt
│   │   ├── matcher.py            ← Semantic & Proximity ranking
│   │   ├── gamifier.py           ← XP/Energy & Leveling logic
│   │   └── inventory_service.py  ← Warehouse/Inventory management
│   ├── 📂 nlp/
│   │   ├── classifier.py         ← Llama 405B interface & JSON cleaning
│   │   ├── crew.py               ← CrewAI agent definitions
│   │   └── vector_db.py          ← ChromaDB operations
│   └── 📂 repository/            ← Data persistence layer
│
├── 📂 frontend/
│   ├── index.html                ← Dashboard entry point
│   ├── app.js                    ← Core UI logic
│   └── style.css                 ← Glassmorphic design tokens
│
├── 📂 data/
│   ├── 📂 vectordb/              ← ChromaDB persistent storage
│   ├── missions.json             ← Historical mission ledger
│   ├── volunteers.json           ← Personnel database
│   └── inventory.json            ← Tactical asset inventory
│
└── 📂 tests/                     ← Mission-critical test suite
```

---

## ✅ Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| **Python** | ≥ 3.12 | Required for all backend intelligence services. |
| **Node.js** | ≥ 18 LTS | Required for the orchestrated CLI launcher. |
| **NVIDIA API Key** | — | Required for Llama 3.1 405B reasoning. |

---

## 🚀 Installation & Setup

### Automated Linux Setup (Fedora/Ubuntu)
```bash
git clone https://github.com/sxrabx/ai-ngo-dashboard.git
cd ai-ngo-dashboard
chmod +x setup_fedora.sh
./setup_fedora.sh
```

### Manual Setup
```bash
# 1. Environment Setup
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt
npm install

# 3. Configure API Key
cp .env.example .env
# Open .env and add: NVIDIA_API_KEY=your_key_here
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and configure your credentials:

```env
NVIDIA_API_KEY=nvapi-XXXXXX...
```

| Variable | Description |
|---|---|
| `NVIDIA_API_KEY` | API key for NVIDIA NIM (Meta Llama-3.1-405B). Get yours at [build.nvidia.com](https://build.nvidia.com). |

---

## ▶️ Running the Platform

### 🟢 Orchestrated Launch (Recommended)
This starts both the FastAPI backend and the Vanilla JS frontend simultaneously with a health-monitored CLI.

```bash
node launch.js
```

**Access Points:**
- 🌐 **Web Dashboard**: [http://localhost:3000](http://localhost:3000)
- 🔌 **API Gateway**: [http://localhost:8000](http://localhost:8000)
- 📚 **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Reference

Full interactive documentation is available at `/docs` (Swagger UI).

### `POST /process`
Submit a raw incident report (text) for AI extraction and squad matching.

### `POST /deploy`
Synchronize mission deployment. Deducts inventory stock and volunteer energy while awarding XP in real-time.

---

## 💡 Usage Notes

### Mission Laboratory
1.  Navigate to the **Mission Laboratory**.
2.  Paste a raw field report (e.g., _"Heavy landslides in Sector 7, 12 homes destroyed, 30 civilians needing urgent medical aid and rations."_)
3.  Click **Run Mission Intelligence**.
4.  Llama 405B will extract the mission profile, and the system will recommend a specialized squad (e.g., Strike Force Alpha) and required loadout.
5.  Click **Confirm Dispatch** to commit the deployment to the database.

---

## 🗺️ Project Roadmap

- [x] Llama 3.1 405B Integration (via NVIDIA NIM)
- [x] Multi-agent CrewAI Extraction & Translation
- [x] Semantic Volunteer Matching (ChromaDB)
- [x] Glassmorphic Tactical Dashboard (Vanilla JS)
- [x] Real-time Energy/Fatigue & XP Tracking
- [ ] Real-time Mobile SMS/WhatsApp Notifications
- [ ] Predictive Resource Forecasting with Time-Series AI
- [ ] Multi-Sector Traffic Overlay for Dispatch Optimization

---

## 📄 License

**ISC License**

Copyright (c) 2026

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

_Note: The frontend components in the `/frontend` directory are treated as proprietary property of the repository owner unless otherwise stated._

---

## 🙌 Credits

- **Intelligence Core**: NVIDIA NIM & Meta Llama 3.1 405B
- **Agent Orchestration**: CrewAI Framework
- **Vector Search**: ChromaDB & Sentence-Transformers
- **UI Architecture**: Leaflet.js & Plotly.js

---

<div align="center">

Built with ❤️ for faster disaster response and smarter community coordination.

</div>
"Description:
