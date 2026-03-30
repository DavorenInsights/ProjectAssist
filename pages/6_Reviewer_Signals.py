import os
import sys
from html import escape

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styles import analyze_application, init_session_state, inject_styles, render_heatmap, sidebar_nav

st.set_page_config(page_title="Reviewer Signals | JET PMO", page_icon="🔎", layout="wide")
inject_styles()
sidebar_nav()
init_session_state()
review = analyze_application()

st.markdown("""
<div class="hero" style="min-height:120px">
    <div class="hero-glow"></div><div class="hero-grid"></div>
    <div class="hero-content" style="padding:1.4rem 2rem">
        <div>
            <div class="hero-tag">🔎 Reviewer Signals</div>
            <h1>What Looks Strong, <span>What Still Needs Work</span></h1>
            <p>This page does not replace formal assessment. It provides a light reviewer-style view of the application so applicants can see likely strengths, likely weaknesses, and practical improvements before submission.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Application strength heatmap</div>', unsafe_allow_html=True)
st.markdown(render_heatmap(review["scores"]), unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section-title">What looks stronger</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["strengths"]:
        for item in review["strengths"]:
            st.markdown(f"- {item}")
    else:
        st.write("No material strengths detected yet. Fill in more of the guided application first.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Submission readiness note</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-block">
            <div style="color:#5F6B66; line-height:1.7">{escape(review['readiness_note'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown('<div class="section-title">What still needs work</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["gaps"]:
        for item in review["gaps"]:
            st.markdown(f"- {item}")
    else:
        st.write("No major gaps surfaced from the light rubric.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Red flags reviewers may notice</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["red_flags"]:
        for item in review["red_flags"]:
            st.markdown(f"<span class='badge badge-red'>Watch</span> {escape(item)}", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge badge-green'>No major red flags surfaced from the current light review.</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("Back to guided application", use_container_width=True):
        st.switch_page("pages/1_Guided_Application.py")
with nav2:
    if st.button("Open financing options", use_container_width=True):
        st.switch_page("pages/3_Financing_Options.py")
with nav3:
    if st.button("Open summary", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Summary_Export.py")
