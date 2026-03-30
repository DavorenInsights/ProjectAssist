import os
import sys
from html import escape

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styles import analyze_application, init_session_state, inject_styles, sidebar_nav

st.set_page_config(page_title="Financing Fit Questionnaire | JET PMO", page_icon="🧭", layout="wide")
inject_styles()
sidebar_nav()
init_session_state()

st.markdown("""
<div class="hero" style="min-height:120px">
    <div class="hero-glow"></div><div class="hero-grid"></div>
    <div class="hero-content" style="padding:1.4rem 2rem">
        <div>
            <div class="hero-tag">🧭 Financing Fit Questionnaire</div>
            <h1>Project Stage and <span>Financing Fit</span></h1>
            <p>This page replaces a rigid readiness calculator with a practical questionnaire. The aim is to guide applicants toward a more realistic funding route and show what evidence would usually make the case stronger.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Answer the questions below</div>', unsafe_allow_html=True)
st.caption("This is not a funding decision. It is a guidance layer to help applicants understand what type of capital may fit better and what may still be missing.")

q1 = st.radio("1. What best describes the current state of the solution?", [
    "Concept only or research stage",
    "Prototype built and tested in controlled conditions",
    "Pilot or demonstration in a relevant environment",
    "Commercially deployed or ready for near-term rollout",
], index=None)
q2 = st.radio("2. What evidence do you already have?", [
    "Mainly technical rationale or early desk research",
    "Lab, bench, or prototype evidence",
    "Pilot performance data and partner feedback",
    "Revenue, offtake, or repeat customer evidence",
], index=None)
q3 = st.radio("3. How strong is the project’s repayment capacity right now?", [
    "No repayment capacity yet; grant support would be needed",
    "Limited repayment capacity; concessional terms would help",
    "Moderate repayment capacity with some contracted demand",
    "Strong repayment capacity supported by revenues or contracts",
], index=None)
q4 = st.radio("4. What is the main use of funds?", [
    "Research, design, or feasibility work",
    "Prototype refinement or pilot execution",
    "Early commercial rollout or productive asset deployment",
    "Scale-up of an already demonstrated model",
], index=None)
q5 = st.radio("5. What best describes your organisation today?", [
    "Research team, startup, or early-stage vehicle",
    "Early operating entity with a small team and some partners",
    "Established entity with governance, reporting, and delivery capacity",
    "Established commercial operator with strong systems and financial controls",
], index=None)
q6 = st.radio("6. What kind of support would help most right now?", [
    "Non-repayable support and technical assistance",
    "Grant plus concessional or patient capital",
    "Blended finance or impact-oriented capital",
    "Commercial debt or institutional investment",
], index=None)

if st.button("Assess financing fit", type="primary"):
    answers = [q1, q2, q3, q4, q5, q6]
    if any(answer is None for answer in answers):
        st.warning("Please answer all questions to generate a financing fit result.")
    else:
        score_map = {
            0: "Grant-led development",
            1: "Pilot and concessional finance",
            2: "Blended finance and impact capital",
            3: "Commercialisation and scale finance",
        }
        selections = [
            [
                "Concept only or research stage",
                "Mainly technical rationale or early desk research",
                "No repayment capacity yet; grant support would be needed",
                "Research, design, or feasibility work",
                "Research team, startup, or early-stage vehicle",
                "Non-repayable support and technical assistance",
            ],
            [
                "Prototype built and tested in controlled conditions",
                "Lab, bench, or prototype evidence",
                "Limited repayment capacity; concessional terms would help",
                "Prototype refinement or pilot execution",
                "Early operating entity with a small team and some partners",
                "Grant plus concessional or patient capital",
            ],
            [
                "Pilot or demonstration in a relevant environment",
                "Pilot performance data and partner feedback",
                "Moderate repayment capacity with some contracted demand",
                "Early commercial rollout or productive asset deployment",
                "Established entity with governance, reporting, and delivery capacity",
                "Blended finance or impact-oriented capital",
            ],
            [
                "Commercially deployed or ready for near-term rollout",
                "Revenue, offtake, or repeat customer evidence",
                "Strong repayment capacity supported by revenues or contracts",
                "Scale-up of an already demonstrated model",
                "Established commercial operator with strong systems and financial controls",
                "Commercial debt or institutional investment",
            ],
        ]
        scores = []
        for answer in answers:
            for idx, bucket in enumerate(selections):
                if answer in bucket:
                    scores.append(idx)
                    break
        stage_index = round(sum(scores) / len(scores))
        stage = score_map[stage_index]

        recommendations = {
            "Grant-led development": ["Government grants", "Technical assistance", "Research partnerships", "Challenge funds"],
            "Pilot and concessional finance": ["Pilot grants", "Concessional loans", "Patient capital", "Public-private co-funding"],
            "Blended finance and impact capital": ["Blended finance", "Impact investors", "DFI support", "Results-based or catalytic finance"],
            "Commercialisation and scale finance": ["Commercial debt", "Structured DFI finance", "Equity growth capital", "Green or climate-linked instruments"],
        }
        notes = {
            "Grant-led development": "The project appears early. The priority is to build stronger technical, market, and execution evidence before positioning for repayable finance.",
            "Pilot and concessional finance": "The project shows enough progress to justify more than pure grant support, but it still needs patient capital and supportive terms.",
            "Blended finance and impact capital": "The project is moving toward bankability but may still need catalytic support to close risk gaps and crowd in capital.",
            "Commercialisation and scale finance": "The project appears mature enough to discuss larger-scale deployment capital, subject to diligence, contracts, and financial strength.",
        }

        st.session_state["finance_stage"] = stage
        st.session_state["finance_recommendations"] = recommendations[stage]
        st.session_state["finance_notes"] = notes[stage]
        review = analyze_application()

        st.success(f"Financing fit identified: {stage}")
        st.markdown(
            f"""
            <div class="section-block">
                <div class="section-title" style="margin-top:0">Recommended direction</div>
                <div style="font-size:1rem; font-weight:700; color:#07553B; margin-bottom:0.5rem">{escape(stage)}</div>
                <div style="font-size:0.92rem; color:#5F6B66; line-height:1.6; margin-bottom:0.9rem">{escape(notes[stage])}</div>
                <div style="font-weight:700; color:#7A3E2B; margin-bottom:0.4rem">Most likely relevant instruments</div>
                <div style="line-height:1.8">{"".join([f"<span class='badge badge-green'>{escape(item)}</span>" for item in recommendations[stage]])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-title">What this route usually needs next</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-block"><div style="font-weight:700; color:#7A3E2B; margin-bottom:0.5rem">Funding route explainer</div>', unsafe_allow_html=True)
            for heading, text in review["funding_route_explainer"]:
                st.markdown(f"**{heading}**")
                st.write(text)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="section-block"><div style="font-weight:700; color:#7A3E2B; margin-bottom:0.5rem">Minimum evidence checklist</div>', unsafe_allow_html=True)
            for item in review["evidence_checklist"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Open financing options", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Financing_Options.py")
with col2:
    if st.button("Open reviewer signals", use_container_width=True):
        st.switch_page("pages/6_Reviewer_Signals.py")
with col3:
    if st.button("Back to guided application", use_container_width=True):
        st.switch_page("pages/1_Guided_Application.py")
