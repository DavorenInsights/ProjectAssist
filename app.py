import os
import sys

import streamlit as st

st.set_page_config(
    page_title="JET PMO | NEV Funding Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

sys.path.append(os.path.dirname(__file__))
from utils.styles import (
    EXAMPLE_PROJECTS,
    analyze_application,
    format_compact_rand,
    init_session_state,
    inject_styles,
    load_example,
    render_heatmap,
    sidebar_nav,
)

inject_styles()
sidebar_nav()
init_session_state()
review = analyze_application()

st.markdown(
    """
<div class="hero">
    <div class="hero-glow"></div>
    <div class="hero-grid"></div>
    <div class="hero-content">
        <div class="hero-logo-area">
            <div class="jet-logo-badge">
                <span class="logo-jet">JET</span>
                <span class="logo-pmo">PMO</span>
            </div>
        </div>
        <div class="hero-text">
            <div class="hero-tag">New energy vehicles · South Africa</div>
            <h1>Application <span>Support Wizard</span></h1>
            <p>A front-end Streamlit demo designed to improve application quality before formal review. It guides applicants, explains what reviewers usually look for, suggests more realistic financing routes, and produces a standing output that can be refined later.</p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

fields_check = {
    "ps_problem": st.session_state.get("ps_problem", ""),
    "sol_description": st.session_state.get("sol_description", ""),
    "team_overview": st.session_state.get("team_overview", ""),
    "bm_model": st.session_state.get("bm_model", ""),
    "mil_objectives": st.session_state.get("mil_objectives", ""),
    "risk_technical": st.session_state.get("risk_technical", ""),
}
sections_done = sum(1 for value in fields_check.values() if value.strip())
pct = int(sections_done / 6 * 100)
project_name = st.session_state.get("proj_name", "") or "—"
finance_stage = st.session_state.get("finance_stage", "Not yet assessed")

st.markdown(
    f"""
<div class="section-block">
    <div style="font-weight:700; font-size:0.8rem; color:#7A3E2B; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem">Demo status</div>
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-value">{sections_done}/6</div>
            <div class="stat-label">Sections started</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{pct}%</div>
            <div class="stat-label">Completion</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="font-size:1rem; padding-top:0.35rem">{finance_stage}</div>
            <div class="stat-label">Current finance fit</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="font-size:1rem; padding-top:0.35rem; word-break:break-word">{project_name[:18] + '…' if len(project_name) > 18 else project_name}</div>
            <div class="stat-label">Project name</div>
        </div>
    </div>
    <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{pct}%"></div></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Core demo routes</div>', unsafe_allow_html=True)
cols = st.columns(4)
buttons = [
    ("📋 Guided Application", "pages/1_Guided_Application.py", True),
    ("🧭 Financing Fit", "pages/2_TRL_Calculator.py", False),
    ("🔎 Reviewer Signals", "pages/6_Reviewer_Signals.py", False),
    ("📄 Summary & Export", "pages/5_Summary_Export.py", False),
]
for col, (label, page, primary) in zip(cols, buttons):
    with col:
        if st.button(label, use_container_width=True, type="primary" if primary else "secondary"):
            st.switch_page(page)

st.markdown('<div class="section-title">What this demo now shows</div>', unsafe_allow_html=True)
a, b, c, d = st.columns(4)
items = [
    (a, "🧭", "Financing fit", "Uses a practical questionnaire instead of a rigid calculator to indicate which funding route is more realistic right now."),
    (b, "🔎", "Reviewer signals", "Highlights strengths, likely gaps, red flags, and a light application strength heatmap without pretending to be a final decision engine."),
    (c, "📌", "Evidence checklist", "Shows the minimum evidence package that would usually make the application more credible for the selected financing route."),
    (d, "📤", "Standing output", "Creates a clean summary and PDF that can support internal review, refinement, or later application packaging."),
]
for col, icon, title, text in items:
    col.markdown(
        f"""
        <div class="section-block" style="text-align:center; padding:1.2rem">
            <div style="font-size:1.8rem; margin-bottom:0.5rem">{icon}</div>
            <div style="font-weight:700; font-size:0.95rem; color:#7A3E2B; margin-bottom:0.4rem">{title}</div>
            <div style="font-size:0.86rem; color:#5F6B66; line-height:1.6">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

left, right = st.columns([1.25, 1])
with left:
    st.markdown('<div class="section-title">Reviewer heatmap snapshot</div>', unsafe_allow_html=True)
    st.markdown(render_heatmap(review["scores"]), unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-block" style="margin-top:0.8rem">
            <div style="font-weight:700; color:#7A3E2B; margin-bottom:0.45rem">Submission readiness note</div>
            <div style="font-size:0.9rem; color:#5F6B66; line-height:1.65">{review['readiness_note']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown('<div class="section-title">Example projects</div>', unsafe_allow_html=True)
    for key, sector in [("peri_charge", "Infrastructure"), ("nev_training", "Skills and training")]:
        ex = EXAMPLE_PROJECTS[key]
        st.markdown(
            f"""
            <div class="example-card" style="margin-bottom:0.8rem">
                <h4>{ex['label']}</h4>
                <p>{ex['description']}</p>
                <div class="ex-meta">
                    <span class="badge badge-lime">TRL {ex['trl']}</span>
                    <span class="badge badge-blue">{format_compact_rand(ex['funding_ask'])} ask</span>
                    <span class="badge badge-green">{sector}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"Load {ex['label']}", use_container_width=True, key=f"load_{key}"):
            load_example(key)
            analyze_application()
            st.success(f"{ex['label']} loaded.")

st.markdown('<div class="jet-footer">JET PMO · New Energy Vehicles · Application Support Wizard · Final demo build</div>', unsafe_allow_html=True)
