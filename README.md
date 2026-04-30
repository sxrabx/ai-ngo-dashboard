<div align="center">
  <img src="assets/hero_banner.png" alt="NGO.AI Tactical Hero" width="800">

  # 🛰️ NGO AI Tactical Command System
  **An elite AI-driven coordination platform for real-time disaster response — featuring autonomous mission intelligence, semantic volunteer triage, and high-fidelity tactical mapping.**

  [![License: ISC](https://img.shields.io/badge/License-ISC-8E75FF?style=for-the-badge)](LICENSE)
  [![Python: 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
  [![FastAPI: Powered](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![Model: Llama 3.1 405B](https://img.shields.io/badge/Model-Llama_3.1_405B-76B900?style=for-the-badge&logo=meta&logoColor=white)](https://build.nvidia.com)
  [![Engine: CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-FF9900?style=for-the-badge)](https://crewai.com)
</div>

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Notes](#-usage-notes)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🌟 Overview
The **NGO AI Tactical Command System** is a production-grade coordination platform designed to modernise disaster response. It centralises fragmented field reports and community needs into a unified "Intelligence Layer," enabling NGO coordinators to mobilize resources with surgical precision.

### Why this exists:
*   **Chaos to Action**: Multi-agent **CrewAI** pipelines powered by **NVIDIA NIM (Llama 3.1 405B)** parse unstructured incident reports and PDFs into structured missions with automated severity ratings and resource requirements.
*   **Smart Triage**: A local **ChromaDB** vector store replaces naive keyword matching. Personnel are ranked by semantic skill alignment, real-time GPS proximity, and mission readiness (fatigue tracking).

---

## 🏗️ Architecture
```text
┌────────────────────────────────────────────────────────────────────┐
│                    NGO AI COMMAND PLATFORM                         │
│                                                                    │
│  ┌─────────────────────────┐    ┌────────────────────────────┐     │
│  │   Tactical Frontend     │    │     Intelligence Backend   │     │
│  │      (Vanilla JS)       │    │      (FastAPI + Python)    │     │
│  │                         │    │                            │     │
│  │  • Mission Control      │    │  • Llama-3.1-405B (NIM)    │     │
│  │  • Personnel Roster     │◄───►  • CrewAI Agent Pipelines  │     │
│  │  • Interactive Maps     │    │  • ChromaDB Vector Search  │     │
│  │  • Logistics Command    │    │  • Smart Scorer Algorithm  │     │
│  └─────────────────────────┘    └────────────────────────────┘     │
│               │                               │                    │
│               ▼                               ▼                    │
│     Leaflet Geospatial Map         NVIDIA NIM (Llama-3.1)          │
│     Plotly Intelligence Gauges    Local Heuristic Fallback Engine  │
│     JSON Persistence Ledger        Autonomous Agent Framework      │
└────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### 🖥️ Tactical Dashboard
| Module | Description |
| :--- | :--- |
| **Mission Control** | Submit raw reports or upload PDFs. AI generates categories, priorities, and squad loadouts automatically. |
| **Personnel Database** | Real-time roster with energy monitoring (0-100%), XP-based leveling, and availability tracking. |
| **Impact Radar** | Interactive Leaflet.js map showing missions (red pulse) and volunteer locations (blue markers) by sector. |
| **Logistics Command** | Integrated warehouse management tracking "In Use" vs "Available" assets across all deployments. |
| **System Health** | Live telemetry for API gateway, uptime, and active AI mode (Cloud vs Offline Fallback). |

---

## 🛠️ Tech Stack

- **Reasoning Model**: Meta Llama 3.1 405B (via NVIDIA NIM)
- **Orchestration**: CrewAI (Multi-agent extraction & translation)
- **Vector Engine**: ChromaDB (Persistent semantic storage)
- **Backend**: FastAPI (High-performance Python 3.12)
- **Frontend**: Vanilla JS / CSS3 (Elite Glassmorphic Tactical UI)
- **Visuals**: Leaflet.js (Geospatial) & Plotly.js (Intelligence Gauges)

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.12+
- Node.js (for the orchestrated launcher)
- NVIDIA NIM API Key

### 2. Deployment
```bash
# Clone the repository
git clone https://github.com/sxrabx/ai-ngo-dashboard.git
cd ai-ngo-dashboard

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "NVIDIA_API_KEY=your_key_here" > .env
```

### 3. Launch the Command Center
```bash
node launch.js
```
*   **Dashboard**: `http://localhost:3000`
*   **API Gateway**: `http://localhost:8000`

---

## 📄 License
This project is licensed under the ISC License (as declared in package.json). The frontend package is marked private with no explicit license file — treat all code as proprietary unless otherwise stated by the repository owner.

---
**Developed for Mission-Critical Community Response.**
