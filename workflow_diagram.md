# AI Intelligence Layer: Data Flow & Workflows

This document illustrates the automated data flows, orchestration logic, and agentic loops within the AI Triage System.

## 🔄 Core Triage Pipeline (End-to-End)

```mermaid
sequenceDiagram
    participant User as NGO Commander
    participant Streamlit as Dashboard (UI)
    participant CrewAI as NLP Agent Orchestrator
    participant Llama as Llama 3.1 8b (NVIDIA)
    participant Chroma as ChromaDB Vector Store
    participant Engine as Core Squad Engine
    participant DB as Volunteer State JSON

    User->>Streamlit: Uploads chaotic txt Field Report
    Streamlit->>CrewAI: Dispatches Extractor Agents
    CrewAI->>Llama: Parses text, identifies victims, translates (Fr/Es)
    Llama-->>CrewAI: Returns Clean JSON Payload
    CrewAI-->>Streamlit: Render Translated & Cleaned Task
    
    User->>Streamlit: Clicks "ANALYZE & DEPLOY"
    Streamlit->>Engine: process_new_task(Task, Roster)
    
    Engine->>Llama: get_llm_reasoning() (Severity/Priority)
    Engine->>Chroma: query_semantic_match(Embeddings)
    Chroma-->>Engine: Top 10 Semantically Similar IDs
    
    Engine->>DB: load_stats() (Energy Levels)
    DB-->>Engine: Current fatigue/burnout states
    
    Engine->>Engine: Score & Triage Math (Proximity, Energy penalty)
    Engine->>Engine: assemble_squad() (Alpha/Beta Split Logic)
    
    Engine-->>Streamlit: Return Final Deployment Object
    Streamlit->>DB: update_volunteer_after_task() (Deplete Energy)
    Streamlit-->>User: Render Dashboard Analytics & Plotly Graphs
```

## 🧠 Squad Assembly Decision Matrix

```mermaid
flowchart TD
    Start[New Task Assessed] --> CheckCount{Victims > 40?}
    
    CheckCount -- Yes --> IsComplex[Mega-Squad Triggered]
    IsComplex --> FetchExperts[Fetch 2 Veteran Leads]
    FetchExperts --> AlphaBeta[Split: Team Alpha & Team Beta]
    AlphaBeta --> Assign[Deploy Multi-Lead Squad]
    
    CheckCount -- No --> FindMatch[Standard Squad Assembly]
    FindMatch --> QueryChroma[ChromaDB Semantic Search]
    QueryChroma --> GetProximity[Rank by Proximity]
    GetProximity --> FastResponder[Flag 'Fastest Responder']
    FastResponder --> Deploy[Deploy Precision Squad]
```

## 🔋 Gamified Energy Cycle

```mermaid
stateDiagram-v2
    [*] --> 100_Energy: New Volunteer Enlisted
    
    100_Energy --> Dispatched: Assigned to Triage
    Dispatched --> Energy_Depleted: Mission Accomplished (-25 Energy)
    
    Energy_Depleted --> Low_Battery: Energy < 30
    Low_Battery --> Rest_Cycle: System flags for Rest
    Rest_Cycle --> 100_Energy: Admin Recovery / Rest (+10 per cycle)
    
    Energy_Depleted --> Level_Up: +20 XP Gained
    Level_Up --> Badges: 500 XP -> Veteran Badge
```
