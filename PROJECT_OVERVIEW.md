# 🛰️ NGO AI Tactical Command: Project Overview

The **NGO AI Tactical Command System** is an enterprise-grade "Intelligence Layer" designed for high-stakes volunteer coordination and disaster response. It transforms unstructured, chaotic field reports into actionable JSON missions using agentic reasoning, semantic vector matching, and proximity-aware triage.

---

## 🏗️ Technical Architecture

The system is built on a decoupled, hardened architecture designed for both performance and reliability in the field.

| Layer | Component | Technology |
| :--- | :--- | :--- |
| **Intelligence** | Reasoning Engine | **Llama-3.1-405B** (NVIDIA NIM) |
| **Orchestration** | Agentic Workflows | **CrewAI** |
| **Vector Engine** | Semantic Memory | **ChromaDB** |
| **Backend** | API Gateway | **FastAPI** (Python 3.12) |
| **Frontend** | Command Interface | **Vanilla JS / CSS** (Glassmorphic) |
| **Geospatial** | Tactical Mapping | **Leaflet.js** |

---

## 📂 System Directory Structure

```text
d:\ai-ngo-dashboard\
├── src/                  # Core Intelligence Layer
│   ├── api/              # FastAPI Server & Endpoints
│   ├── core/             # Business Logic & Algorithms (Engine, Scorer, Gamifier)
│   ├── nlp/              # AI Services (Llama-3.1 Classifier, CrewAI Agents, Vector DB)
│   └── repository/       # Data Access & Persistence
├── frontend/             # Tactical Command Dashboard (HTML5/CSS3/JS)
├── config/               # Global Environment Configuration
├── data/                 # Persistence Layer (JSON Ledgers & Vector DB)
├── docs/                 # System Documentation
└── tests/                # Quality Assurance Suite
```

---

## 🧠 Core Intelligence Capabilities

### 1. Autonomous Extraction (Agentic)
Utilizes **CrewAI** agents to parse unstructured text/PDFs. It extracts mission severity, victim counts, and required resources with human-level accuracy, even in noisy environments.

### 2. Semantic Vector Triage
Powered by **ChromaDB**. Unlike legacy keyword searches, the system understands the *context* of a volunteer's skills. A "Paramedic" might be matched to a "Medical Emergency" even if the exact word "Nurse" is missing.

### 3. Proximity-First Logistics
A weighted scoring algorithm that prioritizes **Fast Responders**. It calculates real-time distances between personnel and incident sites to ensure the quickest possible deployment.

### 4. Tactical Persistence & Recovery
Every mission, deployment, and stock movement is recorded in a hardened JSON ledger. The **Intelligence Recovery Engine** can re-synthesize mission states from historical logs if a data point is lost.

### 5. Sustainability & Gamification
Monitors volunteer fatigue (0-100%). It utilizes a dynamic leveling system (XP) to reward responders while preventing burnout through automated recovery loops.

---

## 🛠️ Deployment Guide

### Prerequisites
- Python 3.12.7+
- Node.js (for the Orchestrated Launcher)
- NVIDIA NIM API Key

### Installation
```bash
pip install -r requirements.txt
echo "NVIDIA_API_KEY=your_key" > .env
```

### Execution
The system includes a **Premium Tactical Launcher** that handles both services simultaneously:
```bash
node launch.js
```
*   **Command Center**: `http://localhost:3000`
*   **Backend API**: `http://localhost:8000`

---

**Status:** `MISSION READY` | `ARCHITECTURE HARDENED` | `INTELLIGENCE ONLINE`