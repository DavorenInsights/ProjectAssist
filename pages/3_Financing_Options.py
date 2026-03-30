import os
import sys
from html import escape

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styles import analyze_application, init_session_state, inject_styles, sidebar_nav

st.set_page_config(page_title="Financing Options | JET PMO", page_icon="💰", layout="wide")
inject_styles()
sidebar_nav()
init_session_state()
review = analyze_application()

st.markdown("""
<div class="hero" style="min-height:120px">
    <div class="hero-glow"></div><div class="hero-grid"></div>
    <div class="hero-content" style="padding:1.4rem 2rem">
        <div>
            <div class="hero-tag">💰 Financing Route Explorer</div>
            <h1>Understanding Your <span>Financing Options</span></h1>
            <p>Different project stages require different financing instruments. This page explains the routes at a high level, while the questionnaire and reviewer signals show which route currently looks most plausible.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

finance_stage = st.session_state.get("finance_stage", "Not yet assessed")
finance_notes = st.session_state.get("finance_notes", "Questionnaire not yet completed.")
if finance_stage != "Not yet assessed":
    st.markdown(
        f"""
        <div class="section-block">
            <div style="font-weight:700; color:#7A3E2B; margin-bottom:0.35rem">Current route signal</div>
            <div style="font-size:1.25rem; font-weight:800; color:#07553B; margin-bottom:0.3rem">{escape(finance_stage)}</div>
            <div style="color:#5F6B66; line-height:1.6">{escape(finance_notes)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

instruments = [
    {
        "name": "Government grants",
        "badge": "badge-green",
        "stages": ["Grant-led development", "Pilot and concessional finance"],
        "what": "Non-repayable public support for feasibility, pilots, local capability building, and early enabling work.",
        "watch_for": "A weak or generic problem case, thin evidence, or vague use of funds can still reduce confidence even when grants are the right route.",
    },
    {
        "name": "Technical assistance",
        "badge": "badge-blue",
        "stages": ["Grant-led development", "Pilot and concessional finance"],
        "what": "Advisory support that improves business cases, delivery design, governance, procurement, or implementation planning.",
        "watch_for": "Best used when the project still needs structuring rather than large capital deployment.",
    },
    {
        "name": "Concessional loans",
        "badge": "badge-amber",
        "stages": ["Pilot and concessional finance", "Blended finance and impact capital"],
        "what": "Repayable finance with softer terms, often used where repayment is plausible but the project is not yet ready for full commercial debt.",
        "watch_for": "Needs clearer repayment logic, implementation milestones, and some confidence in demand or savings.",
    },
    {
        "name": "Blended finance",
        "badge": "badge-green",
        "stages": ["Blended finance and impact capital", "Commercialisation and scale finance"],
        "what": "A mix of grants, concessional capital, and commercial capital used to absorb risk and crowd in investment.",
        "watch_for": "The structure must be solving a real risk problem, not just masking an underdeveloped commercial case.",
    },
    {
        "name": "Impact capital",
        "badge": "badge-blue",
        "stages": ["Blended finance and impact capital", "Commercialisation and scale finance"],
        "what": "Capital from investors willing to support social, climate, or transition value alongside financial return.",
        "watch_for": "Needs a clear theory of impact plus enough delivery credibility to justify investment.",
    },
    {
        "name": "Commercial debt",
        "badge": "badge-red",
        "stages": ["Commercialisation and scale finance"],
        "what": "Debt suited to projects with stronger revenues, contracts, asset bases, or predictable cash flows.",
        "watch_for": "Premature use can overstate readiness and expose weak revenue logic very quickly.",
    },
]

st.markdown('<div class="section-title">High-level financing routes</div>', unsafe_allow_html=True)
for instrument in instruments:
    active = finance_stage in instrument["stages"]
    border = "3px solid #0B6B4A" if active else "1px solid #D8E3DD"
    st.markdown(
        f"""
        <div class="section-block" style="margin-bottom:0.8rem; border-left:{border}">
            <div style="display:flex; justify-content:space-between; gap:0.6rem; align-items:flex-start">
                <div>
                    <div style="font-weight:800; color:#07553B; margin-bottom:0.25rem">{escape(instrument['name'])}</div>
                    <div style="color:#5F6B66; line-height:1.6; margin-bottom:0.5rem">{escape(instrument['what'])}</div>
                </div>
                <div><span class="badge {instrument['badge']}">{'Relevant now' if active else 'Possible later'}</span></div>
            </div>
            <div style="font-size:0.88rem; color:#7A3E2B; font-weight:700; margin-bottom:0.2rem">What reviewers often watch for</div>
            <div style="font-size:0.9rem; color:#5F6B66; line-height:1.6">{escape(instrument['watch_for'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section-title">Funding route explainer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["funding_route_explainer"]:
        for heading, text in review["funding_route_explainer"]:
            st.markdown(f"**{heading}**")
            st.write(text)
    else:
        st.write("Complete the financing fit questionnaire first to generate route-specific guidance.")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="section-title">Minimum evidence checklist</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["evidence_checklist"]:
        for item in review["evidence_checklist"]:
            st.markdown(f"- {item}")
    else:
        st.write("No checklist yet. Complete the financing fit questionnaire first.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("Back to financing fit", use_container_width=True):
        st.switch_page("pages/2_TRL_Calculator.py")
with nav2:
    if st.button("Open reviewer signals", use_container_width=True, type="primary"):
        st.switch_page("pages/6_Reviewer_Signals.py")
with nav3:
    if st.button("Open summary", use_container_width=True):
        st.switch_page("pages/5_Summary_Export.py")
