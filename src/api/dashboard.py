import streamlit as st
import pandas as pd
import sys
import os
import plotly.graph_objects as go
import plotly.express as px

# Add project root (two levels up from src/api/) so 'src.*' imports resolve correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.engine import process_new_task
from src.core.gamifier import update_volunteer_after_task
from src.nlp.classifier import extract_impact_count


# --- PAGE CONFIG ---
st.set_page_config(page_title="NGO AI Command Center", page_icon="🛡️", layout="wide")

# --- PREMIUM CSS REVAMP ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Solid Dark Background */
    [data-testid="stAppViewContainer"] { background: #111111 !important; color: #e0e0e0 !important; }
    [data-testid="stSidebar"] { background-color: #171717 !important; border-right: 1px solid #2a2a2a !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }
    p, label, .stMetric, span { color: #e0e0e0 !important; }
    
    /* Elegant Serif Headers with Golden Hue */
    h1, h2, h3 { 
        font-family: 'Playfair Display', serif !important; 
        color: #e3c06e !important; 
        letter-spacing: 0.5px; 
        font-weight: 700 !important;
    }
    
    /* Expander Fixes */
    [data-testid="stExpander"] { background-color: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 8px !important; overflow: hidden; }
    [data-testid="stExpander"] details summary { background-color: transparent !important; color: #e3c06e !important; font-family: 'Playfair Display', serif; }
    [data-testid="stExpander"] details summary p { color: #e3c06e !important; font-weight: bold; font-family: 'Playfair Display', serif; }
    [data-testid="stExpander"] details summary:hover { background-color: #222222 !important; }
    
    /* Clean Subtitle / Italic text styling */
    .subtitle { font-family: 'Inter', sans-serif; font-style: italic; color: #a0a0a0; font-size: 0.9em; }
    
    /* Input Areas */
    .stTextArea textarea { background-color: #1a1a1a !important; color: #e0e0e0 !important; border: 1px solid #333 !important; border-radius: 6px !important; }
    .stTextArea textarea:focus { border-color: #e3c06e !important; box-shadow: 0 0 0 1px #e3c06e !important; }
    
    /* Elegant Buttons */
    .stButton>button { 
        background: #1a1a1a !important; 
        border: 1px solid #e3c06e !important; 
        color: #e3c06e !important; 
        font-weight: 600; 
        border-radius: 6px; 
        height: 3em; 
        transition: 0.2s;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button:hover { background: #e3c06e !important; color: #111111 !important; transform: translateY(-1px); }
    
    /* Reasoning Box Styling */
    .reasoning-box {
        background: #161616;
        border-left: 4px solid #81B29A;
        padding: 15px;
        border-radius: 4px;
        margin: 20px 0;
        border-top: 1px solid #222;
        border-right: 1px solid #222;
        border-bottom: 1px solid #222;
    }
    
    .energy-bar-container { background: #222; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- MOCK DATA ---
if 'volunteers' not in st.session_state:
    st.session_state.volunteers = [
        {"id": "V1", "name": "Dr. Amit", "skills": ["Health", "First Aid"], "location_coords": (2, 2), "available": True},
        {"id": "V2", "name": "Sarah", "skills": ["Health"], "location_coords": (10, 10), "available": True},
        {"id": "V3", "name": "John", "skills": ["Health"], "location_coords": (0, 0), "available": True},
        {"id": "V4", "name": "Priya", "skills": ["Relief", "Chef"], "location_coords": (1, 1), "available": True},
        {"id": "V5", "name": "Rahul", "skills": ["General"], "location_coords": (5, 5), "available": True},
        {"id": "V6", "name": "Mike", "skills": ["Logistics", "Heavy Lifting"], "location_coords": (12, 4), "available": True},
        {"id": "V7", "name": "Steve", "skills": ["Logistics", "Driving"], "location_coords": (3, 8), "available": True},
        {"id": "V8", "name": "Anita", "skills": ["Logistics"], "location_coords": (15, 2), "available": True},
        {"id": "V9", "name": "Officer Dave", "skills": ["Safety", "Search"], "location_coords": (8, 8), "available": True},
        {"id": "V10", "name": "Fireman Sam", "skills": ["Safety", "Rescue"], "location_coords": (2, 9), "available": True},
        {"id": "V11", "name": "Karen", "skills": ["Safety"], "location_coords": (6, 3), "available": True},
        {"id": "V12", "name": "Dr. Lisa", "skills": ["Mental Health", "Counseling"], "location_coords": (4, 4), "available": True},
        {"id": "V13", "name": "Tom", "skills": ["Mental Health"], "location_coords": (9, 1), "available": True},
        {"id": "V14", "name": "Emily", "skills": ["Mental Health"], "location_coords": (11, 11), "available": True},
        {"id": "V15", "name": "Green Guru", "skills": ["Environment", "Cleanup"], "location_coords": (1, 12), "available": True},
        {"id": "V16", "name": "Jason", "skills": ["Environment"], "location_coords": (7, 6), "available": True},
        {"id": "V17", "name": "Maya", "skills": ["Environment"], "location_coords": (13, 13), "available": True},
        {"id": "V18", "name": "Data Dan", "skills": ["Admin", "Clerical"], "location_coords": (5, 9), "available": True},
        {"id": "V19", "name": "Alice", "skills": ["Admin"], "location_coords": (2, 14), "available": True},
        {"id": "V20", "name": "Bob", "skills": ["General"], "location_coords": (14, 2), "available": True},
        {"id": "V21", "name": "Zoe", "skills": ["General"], "location_coords": (4, 10), "available": True},
        {"id": "V22", "name": "Kevin", "skills": ["Education"], "location_coords": (8, 2), "available": True},
        {"id": "V23", "name": "Sophia", "skills": ["Health"], "location_coords": (1, 5), "available": True},
        {"id": "V24", "name": "Liam", "skills": ["Relief"], "location_coords": (10, 3), "available": True},
        {"id": "V25", "name": "Chloe", "skills": ["Logistics"], "location_coords": (3, 11), "available": True},
        {"id": "V26", "name": "Ethan", "skills": ["Safety"], "location_coords": (12, 12), "available": True},
        {"id": "V27", "name": "Olivia", "skills": ["Mental Health"], "location_coords": (5, 1), "available": True},
        {"id": "V28", "name": "Noah", "skills": ["Environment"], "location_coords": (9, 9), "available": True},
        {"id": "V29", "name": "Ava", "skills": ["Admin"], "location_coords": (6, 6), "available": True},
        {"id": "V30", "name": "Lucas", "skills": ["General", "Cooking"], "location_coords": (2, 2), "available": True},
        {"id": "V31", "name": "Mia", "skills": ["Education"], "location_coords": (15, 15), "available": True},
        {"id": "V32", "name": "James", "skills": ["Relief"], "location_coords": (4, 15), "available": True},
        {"id": "V33", "name": "Isabella", "skills": ["Safety"], "location_coords": (0, 14), "available": True},
        {"id": "V34", "name": "Logan", "skills": ["Health"], "location_coords": (8, 0), "available": True},
        {"id": "V35", "name": "Charlotte", "skills": ["Logistics"], "location_coords": (1, 1), "available": True},
    ]

# ENFORCE ENERGY & LEVEL SYNC ON EVERY RENDER
from src.core.gamifier import load_stats, get_level_info
current_stats = load_stats()
for v in st.session_state.volunteers:
    if v['id'] in current_stats:
        v['energy'] = current_stats[v['id']].get('energy', 100)
        v['current_level'], _ = get_level_info(current_stats[v['id']].get('total_points', 0))

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric-line/100/ffffff/artificial-intelligence.png", width=80)
    st.title("Mission Control")
    st.write("---")
    
    st.subheader("📝 Deployment Request")
    
    # NEW: CrewAI Document Upload logic
    uploaded_file = st.file_uploader("Upload Incident Report (txt)", type=['txt'])
    if 'draft_desc' not in st.session_state:
        st.session_state.draft_desc = ""
        
    if uploaded_file is not None and st.button("🪄 AI Auto-Extract (CrewAI)"):
        with st.spinner("🤖 Agents extracting report data & translating..."):
            from src.nlp.crew import process_ngo_report
            content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            
            # Execute Crew AI
            extracted_data = process_ngo_report(content)
            st.session_state.draft_desc = extracted_data.get('description', '')
            st.session_state['people_count_val'] = extracted_data.get('people_count', 1)
            
            # Store translations to display
            st.session_state['trans_es'] = extracted_data.get('description_es', '')
            st.session_state['trans_fr'] = extracted_data.get('description_fr', '')
            
    if st.session_state.get('trans_es'):
        st.success("🌍 Translations Generated")
        with st.expander("Show Translations"):
            st.markdown(f"**Spanish:** {st.session_state.get('trans_es')}")
            st.markdown(f"**French:** {st.session_state.get('trans_fr')}")

    task_desc = st.text_area("Help Request Description", value=st.session_state.draft_desc, height=200, placeholder="Describe the disaster or paste a chat message...", key="task_input")
    
    # Keep the state synced with whatever is typed
    if task_desc != st.session_state.draft_desc:
        st.session_state.draft_desc = task_desc
    
    if 'last_text' not in st.session_state:
        st.session_state.last_text = ""
        
    text_changed = task_desc != st.session_state.last_text
    
    # NLP Auto-Detection (Thinking Indicator)
    with st.spinner("🧠 AI Parsing context..."):
        detected_count = extract_impact_count(task_desc)

    # Only override the counter if the text has changed
    if text_changed:
        st.session_state.last_text = task_desc
        if detected_count is not None:
            st.session_state['people_count_val'] = detected_count
        else:
            st.session_state['people_count_val'] = 1 # Reset to 1 if no people detected in new text

    if detected_count is not None:
        st.success(f"🤖 AI Detected: {detected_count} people")
    else:
        st.info("🤖 AI found no numbers, defaulting to 1.")

    people_impacted = st.number_input("People Affected (Override)", min_value=1, key="people_count_val")
    
    st.write("---")
    show_thoughts = st.toggle("🧠 Deep AI Thinking Trace", value=False)
    
    if st.button("🚀 ANALYZE & DEPLOY"):
        with st.spinner("🤖 AI Coordinator formulating tactical plan..."):
            final_count = st.session_state['people_count_val']
            task_data = {"task_id": "T1", "description": task_desc, "people_count": final_count, "location_coords": (0,0)}
            st.session_state.result = process_new_task(task_data, st.session_state.volunteers)
            st.session_state.assigned_done = False
    
    st.write("---")
    with st.expander("🛠️ Admin Tools"):
        if st.button("🔋 Reset Energy Statistics"):
            from src.core.gamifier import load_stats, save_stats
            stats = load_stats()
            for v_id in stats: stats[v_id]['energy'] = 100
            save_stats(stats)
            st.rerun()

# --- MAIN DASHBOARD AREA ---
st.title("🛡️ AI Coordination Layer")
st.write("Real-time Tactical Intelligence for Disaster Response")

if 'result' in st.session_state:
    res = st.session_state.result
    
    # 1. TOP METRICS STRIP
    m1, m2, m3, m4 = st.columns(4)
    cat_val = ", ".join(res['category']) if isinstance(res['category'], list) else str(res['category'])
    
    with m1: st.metric("Category", cat_val)
    with m2: st.metric("Priority Score", f"{res['priority_score']}/100")
    with m3: st.metric("Urgency", res['urgency_level'].upper())
    with m4: st.metric("Resource ROI", f"{res['potential_reward_points']} pts")

    st.write("---")
    
    # 2. SQUAD VISUALIZATION
    st.subheader("⚔️ Recommended Hybrid Squad")
    squad_data = res.get('recommended_squad', [])
    is_split = isinstance(squad_data, dict) and squad_data.get('is_split', False)
    
    def render_volunteer_card(member, role="👤 MEMBER"):
        energy = member.get('energy', 100)
        energy_color = "#28a745" if energy > 60 else "#ffc107" if energy > 30 else "#dc3545"
        border_color = '#ffcc00' if "LEAD" in role else '#007bff'
        skills_str = ", ".join(member.get('skills', []))
        
        # Fast Responder Badge
        fast_badge = ""
        if member.get('is_fast_responder', False):
            fast_badge = '<div style="background-color: #ff4b4b; color: white; font-size: 0.6em; padding: 2px 5px; border-radius: 4px; display: inline-block; margin-bottom: 5px;">🚀 FAST RESPONDER</div>'
        
        html = f"""<div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border-left: 5px solid {border_color}; margin-bottom: 10px;">
{fast_badge}
<p style="font-size: 0.7em; color: #8a8da4; margin: 0; text-transform: uppercase; letter-spacing: 1px;">{role}</p>
<p style="margin: 5px 0; font-weight: bold; color: white; font-size: 1.2em;">{member['name']}</p>
<p style="margin: 0; font-size: 0.8em; color: #007bff;">{skills_str}</p>
<div style="display: flex; justify-content: space-between; margin-top: 10px;">
<span style="font-size: 0.8em; color: #ccc;">Lvl {member['current_level']}</span>
<span style="font-size: 0.8em; color: {energy_color};">{energy}% Energy</span>
</div>
<div class="energy-bar-container"><div style="width: {energy}%; height: 100%; background: {energy_color}; border-radius: 3px;"></div></div>
<p style="margin: 8px 0 0 0; font-size: 0.7em; color: #8a8da4; text-align: right;">Match Score: {member.get('match_score', 0)}%</p>
</div>"""
        st.markdown(html, unsafe_allow_html=True)


    if is_split:
        col_a, col_b = st.columns(2)
        with col_a:
            st.info("🛡️ TEAM ALPHA")
            for i, m in enumerate(squad_data['team_alpha']):
                render_volunteer_card(m, "⭐ ALPHA LEAD" if i == 0 else "👤 MEMBER")
        with col_b:
            st.info("🛡️ TEAM BETA")
            for i, m in enumerate(squad_data['team_beta']):
                render_volunteer_card(m, "⭐ BETA LEAD" if i == 0 else "👤 MEMBER")
        all_members = squad_data['team_alpha'] + squad_data['team_beta']
    else:
        cols = st.columns(4)
        for i, m in enumerate(squad_data):
            with cols[i%4]:
                render_volunteer_card(m, "⭐ LEAD" if i == 0 else "👤 MEMBER")
        all_members = squad_data

    # 3. WHAT I UNDERSTOOD (REASONING SECTION)
    st.write("---")
    st.subheader("💡 What I Understood")
    reasoning = res.get('ai_reasoning', {})
    st.markdown(f"""
    <div class="reasoning-box">
        <p style="margin: 0; color: #00d4ff; font-weight: bold; font-size: 1.1em;">🧠 Intelligence Feedback</p>
        <p style="margin: 10px 0; color: #f0f2f6;"><b>So here is what I understood from your help request:</b><br>{reasoning.get('understood', 'No specific context detected.')}</p>
        <p style="margin: 10px 0; color: #f0f2f6;"><b>So here is what I did for your request:</b><br>{reasoning.get('action', 'No action taken.')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render raw deep thinking trace if enabled
    if show_thoughts and reasoning.get('raw_thinking'):
        with st.expander("👁️ View Internal LLM Cognitive Trace", expanded=True):
            st.info(reasoning['raw_thinking'])

    # 4. DEPLOYMENT & DEPTH
    st.write("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.session_state.get('assigned_done', False):
            st.success("✅ DISPATCHED: Volunteer units are en route.")
        elif st.button("📢 DISPATCH SQUAD"):
            for m in all_members:
                update_volunteer_after_task(m['id'], res['potential_reward_points'], res['category'])
            st.session_state.assigned_done = True
            st.balloons()
            st.rerun()
            
    with c2:
        with st.expander("📊 View Tactical Backlog (All Matches)"):
            all_vols = res.get('suggested_volunteers', [])
            if all_vols:
                # Map the absolute latest energy from our synced session state
                latest_energy = {vol['id']: vol['energy'] for vol in st.session_state.volunteers}
                
                df = pd.DataFrame([{
                    "Name": v['name'],
                    "Strength": int(v['match_score']),
                    "Energy": int(latest_energy.get(v['id'], v['energy'])),
                    "Skills": ", ".join(v['skills'])
                } for v in all_vols])
                
                st.dataframe(
                    df, 
                    use_container_width=True,
                    column_config={
                        "Strength": st.column_config.ProgressColumn("Match Strength", min_value=0, max_value=100, format="%d%%"),
                        "Energy": st.column_config.ProgressColumn("Energy Level", min_value=0, max_value=100, format="%d%%")
                    }
                )

else:
    st.empty()
    st.info("👈 Please enter the help request details in the Mission Control panel to begin.")

# --- IMPACT ANALYTICS SECTION ---
st.write("---")
with st.expander("📈 Enterprise Impact Analytics & ROI", expanded=False):
    st.markdown("### Quarterly NGO Efficiency Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Manual Hours Saved", "1,432 hrs", "+14% this month")
    col2.metric("Disaster Match Accuracy", "98.4%", "+2.1%")
    col3.metric("Volunteer Utilization", "84%", "+5%")
    col4.metric("Avg Response Time", "14 mins", "-3.5 mins (Faster)")
    
    st.write(" ")
    c_chart1, c_chart2, c_chart3 = st.columns(3)
    
    with c_chart1:
        st.markdown("**System Resource Strain**")
        
        # Calculate dynamic system load based on depleted volunteer energy
        total_energy = sum(v.get('energy', 100) for v in st.session_state.volunteers)
        max_energy = len(st.session_state.volunteers) * 100
        avg_energy = (total_energy / max_energy) * 100 if max_energy > 0 else 100
        system_load = round(100 - avg_energy, 1)
        
        # Dynamic color based on severity
        if system_load < 33:
            gauge_color = "#5A9D6A" # Green
        elif system_load < 66:
            gauge_color = "#e3c06e" # Yellow/Gold
        else:
            gauge_color = "#ff4b4b" # Red
            
        # Gauge Chart matching the provided photo style
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = system_load,
            number = {'suffix': "%", 'font': {'color': gauge_color, 'family': 'Inter', 'size': 40}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white'}},
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 33], 'color': "rgba(90, 157, 106, 0.15)"},
                    {'range': [33, 66], 'color': "rgba(227, 192, 110, 0.15)"},
                    {'range': [66, 100], 'color': "rgba(255, 75, 75, 0.15)"}],
            }))
        fig_gauge.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Inter"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    with c_chart2:
        st.markdown("**Tasks by Category (YTD)**")
        # Pie Chart
        pie_data = pd.DataFrame({
            "Category": ["Health", "Relief", "Logistics", "Safety", "Mental Health"], 
            "Quantity": [120, 85, 45, 90, 30]
        })
        fig_pie = px.pie(pie_data, values='Quantity', names='Category', hole=0.4, 
                         color_discrete_sequence=['#e3c06e', '#81B29A', '#3D5A80', '#E07A5F', '#F4F1DE'])
        fig_pie.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Inter"})
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c_chart3:
        st.markdown("**Energy Tracker (Top Units)**")
        # Area graph for dynamic energy levels
        energy_levels = [v.get('energy', 100) for v in st.session_state.volunteers[:10]]
        df_energy = pd.DataFrame({"Unit": [f"V{i+1}" for i in range(len(energy_levels))], "Energy": energy_levels})
        fig_line = px.area(df_energy, x="Unit", y="Energy", color_discrete_sequence=['#e3c06e'])
        fig_line.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Inter"})
        fig_line.update_xaxes(showgrid=False, title="")
        fig_line.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="")
        st.plotly_chart(fig_line, use_container_width=True)
        
    st.caption("Powered by CrewAI Autonomous Agents & Proximity Engine.")
    

