# 🛡️ Smart Team Assembly: "The Squad Logic"

## 📌 Executive Summary
As the project scales from matching individuals to managing large-scale NGO operations, the "Single Volunteer" approach is no longer sufficient. This strategy proposes a **Hybrid Squad Assembly Engine** that combines **Veteran Anchors** with **Urgency-Tiered Ratios** to solve for safety, mentorship, and efficiency.

---

## 🚀 The Core Philosophy
**"Never send a Rookie into a high-risk zone alone, and never waste an Expert on a low-skill task."**

By mixing volunteers of different experience levels, we achieve:
1.  **Safety:** Rookies are always supervised by a "Veteran Anchor."
2.  **Mentorship:** Newbies learn real-world skills from Level 5+ experts.
3.  **Efficiency:** High-skill resources are precision-targeted to critical needs.

---

## 🛠️ The Hybrid Model (Anchor + Urgency-Tiered)

The AI Intelligence Layer will dynamically calculate the **Expert-to-Rookie Ratio** based on the task's **Priority Score**.

### Scenario A: High-Urgency / High-Risk (Score 80–100)
*   **Squad Mix:** **75% Experts | 25% Rookies**
*   **Logic:** In life-or-death situations, we prioritize precision. Rookies are included only in "shadowing" roles or for basic assistance.
*   **Example Squad:** 3 Medical Experts + 1 General Rookie (Shadow).

### Scenario B: Standard Operation (Score 40–79)
*   **Squad Mix:** **50% Experts | 50% Rookies**
*   **Logic:** A balanced team for steady operations. Experts lead specific segments while Rookies handle the bulk of the coordination.
*   **Example Squad:** 2 Relief Experts + 2 Logistics Rookies.

### Scenario C: High-Manpower / Low-Risk (Score 1–39)
*   **Squad Mix:** **20% Experts | 80% Rookies**
*   **Logic:** These are "teaching" tasks. One Veteran manages a large group of newcomers to get massive manual work done (e.g., loading supplies).
*   **Example Squad:** 1 Team Lead + 5 Newbie Volunteers.

---

## 🎨 UI/UX Integration (The "Wow" Factor)
In the Intelligence Dashboard, we will add a **"Squad Recommendation"** card that displays:
*   **Team Lead:** The Anchor (Highest Match Score/Level).
*   **The Squad:** A visually distinct list of Rookies and Veterans.
*   **Team Capacity:** A calculation of how many people this specific squad can handle.

---

## 📈 Technical Implementation Plan
1.  **Logic Update (`matcher.py`):** Add a `form_squad` function that takes the `top_volunteers` list and filters them based on the `Priority Score` thresholds.
2.  **UI Update (`dashboard.py`):** Create a new layout section using `st.columns` to display the "Recommended Squad" instead of just a linear table.
3.  **Gamification Link:** Award "Leadership Points" to the Veteran Lead and "Training Points" to the Rookies.

---

## 💡 Discussion Points for Team Members
*   Should we allow volunteers to "Opt-out" of being a Lead if they are tired?
*   Should we limit the number of times a Rookie can shadow an Expert before they qualify for "Level Up"?
*   How do we handle location if the team members are scattered? (Priority goes to the Anchor's location).
