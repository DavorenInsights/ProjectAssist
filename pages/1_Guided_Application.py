import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styles import inject_styles, sidebar_nav

st.set_page_config(page_title="Guided Application | JET PMO", page_icon="📋", layout="wide")
inject_styles()
sidebar_nav()

# ── Session state init ─────────────────────────────────────────────────────────
defaults = {
    # Problem Statement
    "ps_context": "", "ps_problem": "", "ps_evidence": "", "ps_impact": "",
    # Solution
    "sol_description": "", "sol_achieved": "", "sol_differentiation": "", "sol_innovation": "",
    # Team
    "team_overview": "", "team_achievements": "", "team_gaps": "",
    # Business Model
    "bm_model": "", "bm_revenue": "", "bm_customers": "", "bm_market_size": "", "bm_competition": "",
    # Milestones
    "mil_objectives": "", "mil_short": "", "mil_medium": "", "mil_long": "", "mil_kpis": "",
    # Risk Register
    "risk_technical": "", "risk_market": "", "risk_regulatory": "", "risk_financial": "", "risk_mitigation": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" style="min-height:130px">
    <div class="hero-glow"></div>
    <div class="hero-grid"></div>
    <div class="hero-content" style="padding:1.6rem 2.2rem; align-items:center">
        <div class="hero-logo-area">
            <div class="jet-logo-badge"><span class="logo-jet">JET</span><span class="logo-pmo">PMO</span></div>
        </div>
        <div class="hero-text">
            <div class="hero-tag">📋 Application Builder</div>
            <h1 style="font-size:1.8rem">Guided <span>Application</span></h1>
            <p style="font-size:0.85rem">Complete each section with structured prompts and JET/NEV-specific tips. Everything saves to your session and exports to PDF.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Progress indicator ─────────────────────────────────────────────────────────
sections = ["Problem Statement","Solution","Team","Business Model","Milestones","Risk Register"]
filled = sum([
    bool(st.session_state.ps_context or st.session_state.ps_problem),
    bool(st.session_state.sol_description),
    bool(st.session_state.team_overview),
    bool(st.session_state.bm_model),
    bool(st.session_state.mil_objectives),
    bool(st.session_state.risk_technical),
])
pct = int((filled / 6) * 100)

st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem'>
    <span style='font-size:0.85rem; font-weight:600; color:#0a1628'>Application Progress</span>
    <span style='font-size:0.85rem; color:#64748b'>{filled}/6 sections started · {pct}%</span>
</div>
<div class="progress-bar-wrap">
    <div class="progress-bar-fill" style="width:{pct}%"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("📌 Section 1 — Problem Statement", expanded=True):
    st.markdown("""
    <div class="tip-box">
        <h5>💡 What funders want to see</h5>
        <p>A strong problem statement demonstrates that you deeply understand the challenge, have evidence it exists at scale, and can articulate the consequences of doing nothing. For NEV projects, link explicitly to South Africa's JET commitments and the transition away from ICE vehicles.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("""
        <div class="tip-box">
            <h5>🎯 JET/NEV Tips</h5>
            <p>• Reference SA's NDC targets<br>
            • Mention EV adoption barriers (cost, range anxiety, grid)<br>
            • Quantify emissions or jobs at stake<br>
            • Link to Presidential Climate Commission findings</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("**1.1 — Context & Background**")
        st.caption("Describe the broader landscape. What is happening in South Africa's energy/transport sector that makes this problem relevant now?")
        st.session_state.ps_context = st.text_area(
            "Context", value=st.session_state.ps_context, height=100,
            placeholder="e.g. South Africa's transport sector accounts for ~13% of national GHG emissions. The JET pathway commits to a significant shift toward zero-emission vehicles by 2035, yet EV penetration remains below 0.1% of the fleet...",
            label_visibility="collapsed", key="ps_context_input"
        )
        st.session_state.ps_context = st.session_state.ps_context_input

        st.markdown("**1.2 — The Core Problem**")
        st.caption("State the specific problem your project addresses. Be precise — avoid vague language like 'there is a need for'.")
        st.session_state.ps_problem = st.text_area(
            "Problem", value=st.session_state.ps_problem, height=100,
            placeholder="e.g. Commercial fleets in peri-urban areas cannot transition to EVs because there is no affordable, reliable charging infrastructure outside of major metros. This is blocking fleet operators from accessing green finance...",
            label_visibility="collapsed", key="ps_problem_input"
        )
        st.session_state.ps_problem = st.session_state.ps_problem_input

        st.markdown("**1.3 — Evidence & Data**")
        st.caption("What data, research, or market evidence proves this problem is real and significant?")
        st.session_state.ps_evidence = st.text_area(
            "Evidence", value=st.session_state.ps_evidence, height=100,
            placeholder="e.g. A 2023 CSIR survey of 120 fleet operators showed 78% cited charging infrastructure as the primary barrier to EV adoption. SANEDI estimates this gap affects ~45,000 commercial vehicles...",
            label_visibility="collapsed", key="ps_evidence_input"
        )
        st.session_state.ps_evidence = st.session_state.ps_evidence_input

        st.markdown("**1.4 — Impact of Inaction**")
        st.caption("What happens if this problem is NOT solved? Quantify where possible.")
        st.session_state.ps_impact = st.text_area(
            "Impact of inaction", value=st.session_state.ps_impact, height=80,
            placeholder="e.g. Without intervention, SA's commercial fleet will remain ICE-dependent through 2040, locking in an estimated 8Mt CO₂ cumulative emissions and missing 12,000 potential green jobs in EV servicing...",
            label_visibility="collapsed", key="ps_impact_input"
        )
        st.session_state.ps_impact = st.session_state.ps_impact_input

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — SOLUTION & MARKET DIFFERENTIATION
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("💡 Section 2 — Solution & Market Differentiation"):
    st.markdown("""
    <div class="tip-box">
        <h5>💡 What funders want to see</h5>
        <p>Clearly describe what you have built or are building, what makes it better than what already exists, and what you have already achieved. Avoid vague claims — funders compare many applications and remember specific, credible achievements.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("""
        <div class="tip-box">
            <h5>🎯 JET/NEV Tips</h5>
            <p>• Explain how your solution fits into the NEV value chain<br>
            • Mention any IP, patents, or proprietary tech<br>
            • Be specific: "30% cheaper than X" beats "cost-effective"<br>
            • Describe your localisation strategy</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("**2.1 — Solution Description**")
        st.caption("Describe your solution clearly. What is it, how does it work, and who does it serve?")
        st.session_state.sol_description = st.text_area(
            "Solution", value=st.session_state.sol_description, height=110,
            placeholder="e.g. We have developed a modular DC fast-charging hub designed for peri-urban depot environments. Each unit is solar-hybrid, grid-connected, and remotely managed via our IoT platform. It can charge 6 commercial EVs simultaneously at 60kW...",
            label_visibility="collapsed", key="sol_desc_input"
        )
        st.session_state.sol_description = st.session_state.sol_desc_input

        st.markdown("**2.2 — What You Have Already Achieved**")
        st.caption("What proof points, pilots, or milestones have you completed? This builds funder confidence.")
        st.session_state.sol_achieved = st.text_area(
            "Achievements", value=st.session_state.sol_achieved, height=100,
            placeholder="e.g. Completed a 6-month pilot with 3 fleet operators in Midrand (Q3 2023). Charged 8,200 sessions, 99.1% uptime. Signed LOIs with 2 additional operators representing 140 vehicles...",
            label_visibility="collapsed", key="sol_ach_input"
        )
        st.session_state.sol_achieved = st.session_state.sol_ach_input

        st.markdown("**2.3 — How Is It Better Than What Is in the Market?**")
        st.caption("Compare directly to alternatives. What do competitors or existing solutions offer, and where do you outperform them?")
        st.session_state.sol_differentiation = st.text_area(
            "Differentiation", value=st.session_state.sol_differentiation, height=110,
            placeholder="e.g. Existing DC chargers (e.g. GridCars, Rubicon) are designed for urban retail locations, cost R1.8M+ per unit, and require stable 3-phase grid supply. Our solution costs R620K, works on single-phase, and integrates a 30kWh battery buffer for load-shedding resilience...",
            label_visibility="collapsed", key="sol_diff_input"
        )
        st.session_state.sol_differentiation = st.session_state.sol_diff_input

        st.markdown("**2.4 — Innovation & Scalability**")
        st.caption("What is genuinely new about your approach, and how can it scale?")
        st.session_state.sol_innovation = st.text_area(
            "Innovation", value=st.session_state.sol_innovation, height=90,
            placeholder="e.g. Our proprietary energy management firmware (patent pending) dynamically balances grid draw with solar and battery, reducing peak demand charges by up to 40%. The modular design means sites can be scaled from 2 to 20 bays without civil engineering changes...",
            label_visibility="collapsed", key="sol_inn_input"
        )
        st.session_state.sol_innovation = st.session_state.sol_inn_input

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — TEAM & ACHIEVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("👥 Section 3 — Team & Achievements"):
    st.markdown("""
    <div class="tip-box">
        <h5>💡 What funders want to see</h5>
        <p>Funders invest in teams as much as ideas. Demonstrate that your team has the right mix of technical, commercial, and operational expertise — and that you have a track record of delivery. Be honest about gaps and how you will address them.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("""
        <div class="tip-box">
            <h5>🎯 JET/NEV Tips</h5>
            <p>• Include B-BBEE and transformation credentials<br>
            • Highlight women and youth in leadership<br>
            • Mention any industry partnerships (OEMs, utilities)<br>
            • Advisory boards add credibility</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("**3.1 — Team Overview**")
        st.caption("Who are the key people? Include names, roles, and why they are the right team for this project.")
        st.session_state.team_overview = st.text_area(
            "Team", value=st.session_state.team_overview, height=130,
            placeholder="e.g. CEO: Jane Dlamini — 12 years in EV infrastructure across 3 African markets. CTO: Sipho Nkosi — Masters in Power Electronics (UCT), previously at ABB SA. COO: Thabo Mokoena — ran operations for GridCo, managing R200M in infrastructure assets...",
            label_visibility="collapsed", key="team_ov_input"
        )
        st.session_state.team_overview = st.session_state.team_ov_input

        st.markdown("**3.2 — Key Achievements as a Team**")
        st.caption("What has the team delivered together? Include previous projects, contracts won, or recognitions.")
        st.session_state.team_achievements = st.text_area(
            "Achievements", value=st.session_state.team_achievements, height=100,
            placeholder="e.g. Together deployed 18 EV charging sites across Gauteng and Western Cape (2021–2023). Won the SEFA Green Innovation Award 2022. Successfully raised R4.5M in seed funding from Edge Growth...",
            label_visibility="collapsed", key="team_ach_input"
        )
        st.session_state.team_achievements = st.session_state.team_ach_input

        st.markdown("**3.3 — Identified Gaps & How You Will Address Them**")
        st.caption("No team is perfect. Showing self-awareness builds trust. Describe gaps and your mitigation plan.")
        st.session_state.team_gaps = st.text_area(
            "Gaps", value=st.session_state.team_gaps, height=90,
            placeholder="e.g. We currently lack in-house legal and regulatory expertise. We have engaged Bowmans (specialist energy law firm) on a retainer. We are also recruiting a Head of Regulatory Affairs, budgeted in Year 1...",
            label_visibility="collapsed", key="team_gap_input"
        )
        st.session_state.team_gaps = st.session_state.team_gap_input

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — BUSINESS MODEL / PLAN
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("📊 Section 4 — Business Model & Plan"):
    st.markdown("""
    <div class="tip-box">
        <h5>💡 What funders want to see</h5>
        <p>A credible path to financial sustainability. Funders — especially DFIs and blended finance vehicles — want to see that your model can generate returns or at least cover costs without perpetual subsidies. Be specific about revenue streams, unit economics, and market size.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("""
        <div class="tip-box">
            <h5>🎯 JET/NEV Tips</h5>
            <p>• Include energy-as-a-service or charging-as-a-service models<br>
            • Quantify willingness to pay from fleet operators<br>
            • Show how carbon credits may supplement revenue<br>
            • Reference REIPPPP or similar precedent models</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("**4.1 — Business Model**")
        st.caption("How do you make money? Describe your revenue model in simple terms.")
        st.session_state.bm_model = st.text_area(
            "Model", value=st.session_state.bm_model, height=100,
            placeholder="e.g. We operate on a Charging-as-a-Service (CaaS) model. Fleet operators pay a monthly subscription (R4,500/vehicle) that covers unlimited charging, maintenance, and remote monitoring. We own and operate all hardware...",
            label_visibility="collapsed", key="bm_mod_input"
        )
        st.session_state.bm_model = st.session_state.bm_mod_input

        st.markdown("**4.2 — Revenue Streams & Unit Economics**")
        st.caption("What are your revenue lines? What are the key unit economics (cost per unit, margin, payback period)?")
        st.session_state.bm_revenue = st.text_area(
            "Revenue", value=st.session_state.bm_revenue, height=100,
            placeholder="e.g. Primary: subscription fees (R4,500/vehicle/month). Secondary: grid services / demand response (R800K/year at 5 sites). Unit economics: Hub cost R620K, break-even at 18 vehicles, IRR 22% over 7 years...",
            label_visibility="collapsed", key="bm_rev_input"
        )
        st.session_state.bm_revenue = st.session_state.bm_rev_input

        st.markdown("**4.3 — Target Customers & Market Size**")
        st.caption("Who are your customers? How large is the addressable market?")
        st.session_state.bm_customers = st.text_area(
            "Customers", value=st.session_state.bm_customers, height=90,
            placeholder="e.g. Primary: logistics and delivery fleets (10–200 vehicles) in SA metros and peri-urban areas. SAM: ~18,000 commercial EVs by 2028 (NAAMSA forecast). SOM: 2,500 vehicles by 2026 = R135M ARR...",
            label_visibility="collapsed", key="bm_cust_input"
        )
        st.session_state.bm_customers = st.session_state.bm_cust_input

        st.markdown("**4.4 — Competitive Landscape**")
        st.caption("Who else is operating in this space? Why will customers choose you?")
        st.session_state.bm_competition = st.text_area(
            "Competition", value=st.session_state.bm_competition, height=90,
            placeholder="e.g. Key players: GridCars (urban retail focused), Rubicon (high-end, expensive), Charge.io (new entrant, no fleet offering). Our advantage: lowest total cost of ownership for fleets, load-shedding resilience, and local servicing network...",
            label_visibility="collapsed", key="bm_comp_input"
        )
        st.session_state.bm_competition = st.session_state.bm_comp_input

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — MILESTONES & OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("🎯 Section 5 — Milestones & Objectives"):
    st.markdown("""
    <div class="tip-box">
        <h5>💡 What funders want to see</h5>
        <p>Clear, time-bound milestones linked to how you will use the funding. Funders use milestones to track progress and release tranches. Make them SMART — Specific, Measurable, Achievable, Relevant, Time-bound.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("""
        <div class="tip-box">
            <h5>🎯 JET/NEV Tips</h5>
            <p>• Align milestones to funding tranches<br>
            • Include jobs created at each phase<br>
            • Link to TRL progression (see TRL Calculator)<br>
            • Include regulatory/permitting milestones</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("**5.1 — Overall Objectives**")
        st.caption("What are the 3–5 high-level objectives this project aims to achieve?")
        st.session_state.mil_objectives = st.text_area(
            "Objectives", value=st.session_state.mil_objectives, height=100,
            placeholder="e.g. 1. Deploy 10 charging hubs across Gauteng by Dec 2025. 2. Onboard 200 commercial EVs onto the network. 3. Demonstrate 40% reduction in fleet fuel costs. 4. Create 45 permanent jobs. 5. Reduce fleet emissions by 1,200 tCO₂/year...",
            label_visibility="collapsed", key="mil_obj_input"
        )
        st.session_state.mil_objectives = st.session_state.mil_obj_input

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**5.2 — Short-term Milestones (0–12 months)**")
            st.session_state.mil_short = st.text_area(
                "Short", value=st.session_state.mil_short, height=130,
                placeholder="M1 (Month 3): Secure site permits for 3 hub locations\nM2 (Month 6): Deploy and commission Hub 1 & 2\nM3 (Month 9): Onboard 50 vehicles\nM4 (Month 12): Achieve cash flow breakeven on Hub 1",
                label_visibility="collapsed", key="mil_st_input"
            )
            st.session_state.mil_short = st.session_state.mil_st_input

        with col_b:
            st.markdown("**5.3 — Medium-term Milestones (1–3 years)**")
            st.session_state.mil_medium = st.text_area(
                "Medium", value=st.session_state.mil_medium, height=130,
                placeholder="Y2: Deploy 5 hubs, 150 vehicles on network\nY2: Launch carbon credit offtake agreement\nY3: Expand to KZN, 10 hubs total\nY3: Series A raise of R50M",
                label_visibility="collapsed", key="mil_med_input"
            )
            st.session_state.mil_medium = st.session_state.mil_med_input

        st.markdown("**5.4 — Key Performance Indicators (KPIs)**")
        st.caption("What will you measure to prove success?")
        st.session_state.mil_kpis = st.text_area(
            "KPIs", value=st.session_state.mil_kpis, height=90,
            placeholder="• Number of charging hubs deployed\n• Number of EVs onboarded\n• Charging sessions per month\n• Uptime % (target: >98%)\n• tCO₂ avoided per year\n• Jobs created (direct + indirect)\n• Revenue per hub per month",
            label_visibility="collapsed", key="mil_kpi_input"
        )
        st.session_state.mil_kpis = st.session_state.mil_kpi_input

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — RISK REGISTER
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("⚠️ Section 6 — Risk Register"):
    st.markdown("""
    <div class="tip-box">
        <h5>💡 What funders want to see</h5>
        <p>Showing you have thought through risks demonstrates maturity and builds funder confidence. A blank or vague risk register is a red flag. For each risk, describe the likelihood, potential impact, and your mitigation strategy.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("""
        <div class="tip-box">
            <h5>🎯 JET/NEV Tips</h5>
            <p>• Include Eskom/grid reliability as a risk<br>
            • Address EV demand adoption risk<br>
            • Consider policy/regulatory changes<br>
            • Include FX risk if importing hardware<br>
            • Address B-BBEE compliance risk</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        risk_cols = st.columns(2)

        with risk_cols[0]:
            st.markdown("**6.1 — Technical Risks**")
            st.session_state.risk_technical = st.text_area(
                "Technical", value=st.session_state.risk_technical, height=110,
                placeholder="Risk: Grid instability / load-shedding disrupts charging operations.\nLikelihood: High. Impact: High.\nMitigation: Battery buffer + solar hybrid design provides 4h backup. Remote monitoring enables proactive management...",
                label_visibility="collapsed", key="risk_tech_input"
            )
            st.session_state.risk_technical = st.session_state.risk_tech_input

            st.markdown("**6.2 — Market / Demand Risks**")
            st.session_state.risk_market = st.text_area(
                "Market", value=st.session_state.risk_market, height=110,
                placeholder="Risk: EV adoption slower than projected, reducing fleet customer base.\nLikelihood: Medium. Impact: High.\nMitigation: LOIs from 5 fleet operators already signed. Hardware can be repurposed for grid storage if EV demand lags...",
                label_visibility="collapsed", key="risk_mkt_input"
            )
            st.session_state.risk_market = st.session_state.risk_mkt_input

        with risk_cols[1]:
            st.markdown("**6.3 — Regulatory / Policy Risks**")
            st.session_state.risk_regulatory = st.text_area(
                "Regulatory", value=st.session_state.risk_regulatory, height=110,
                placeholder="Risk: Delays in municipal permitting for charging infrastructure.\nLikelihood: Medium. Impact: Medium.\nMitigation: Engaged specialist town planning consultants in each metro. Budgeted 3-month permitting buffer in project schedule...",
                label_visibility="collapsed", key="risk_reg_input"
            )
            st.session_state.risk_regulatory = st.session_state.risk_reg_input

            st.markdown("**6.4 — Financial Risks**")
            st.session_state.risk_financial = st.text_area(
                "Financial", value=st.session_state.risk_financial, height=110,
                placeholder="Risk: ZAR depreciation increases cost of imported charger components.\nLikelihood: Medium. Impact: Medium.\nMitigation: Forward contracts for USD procurement. Investigating local manufacturing partnerships for key components...",
                label_visibility="collapsed", key="risk_fin_input"
            )
            st.session_state.risk_financial = st.session_state.risk_fin_input

        st.markdown("**6.5 — Overall Mitigation Strategy**")
        st.caption("Summarise your overall approach to risk management.")
        st.session_state.risk_mitigation = st.text_area(
            "Mitigation", value=st.session_state.risk_mitigation, height=90,
            placeholder="We maintain a Risk Register reviewed monthly by the Board. A contingency budget of 15% is included in all project budgets. Our independent technical advisor (ITA) will review technical decisions quarterly. We have engaged a JET-specialist legal team for regulatory matters...",
            label_visibility="collapsed", key="risk_mit_input"
        )
        st.session_state.risk_mitigation = st.session_state.risk_mit_input

# ── Footer nav ─────────────────────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3 = st.columns([1,1,2])
with col1:
    if st.button("🔬 Go to TRL Calculator", use_container_width=True):
        st.switch_page("pages/2_TRL_Calculator.py")
with col2:
    if st.button("📄 View Summary & Export", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Summary_Export.py")
