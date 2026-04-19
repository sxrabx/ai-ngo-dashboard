# Team Discussion Log: Manpower Scaling & Squad Splitting

**Goal:** This document preserves the exact breakthrough discussion regarding the NGO's ability to handle large-scale disasters.

---

### [The Request]
**USER:** *"based on number of people affected the ai should assign number of volunteers to join in 1 group because for example if affected ppl are 40 and 4 r going as volunteers then it will be difficult."*

### [The AI Response & Suggestion]
**AI:** *"That is a very logical requirement! Sending 4 people to help 40 is definitely not enough manpower. I will update the Squad Assembly Engine to use a Dynamic Manpower Ratio."*

**AI Suggested Strategy:**
1. **Dynamic Scaling:** Instead of a fixed 4-person squad, the AI will calculate the squad size based on the number of victims: `1 extra volunteer for every 5 additional people affected`.
2. **The 40 Victim Scenario:** For 40 victims, the AI automatically expands the squad to 10 volunteers.

### [The Better Approach Discussion]
**USER:** *"what do u think will be a better approach any suggestion?"*

**AI Proposed Options:**
- **Option 1: Volunteer Fatigue Tracking** (Energy bars to prevent burnout).
- **Option 2: Multi-Squad Splitting** (Alpha/Beta teams for large groups).
- **Option 3: Proximity-First Triage** (Closest person leads until expert arrives).

### [The Decision]
**USER:** *"which one should we do or combine them all or any other way u suggest??"*

**AI Conclusion:**
*"For a high-impact hackathon demo, I suggests combining **Workload Fatigue** and **Multi-Squad Deployment**. This makes your AI look like a 'Sustainable Commander' that thinks about both the victims and the volunteers."*

---
## Final Implementation Agreement
- **Sustainability:** Volunteers lose 25 Energy per task; rest at 0.
- **Organization:** Large groups (40+) split into Team Alpha and Team Beta with separate leads.
- **Impact:** Judges see "Organizational Intelligence" instead of just simple matching.

---
*Transcript preserved for the Hackathon Team.*
