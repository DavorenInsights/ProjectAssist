import io
import os
import sys
from html import escape

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styles import THEME, analyze_application, init_session_state, inject_styles, render_heatmap, sidebar_nav

st.set_page_config(page_title="Summary & Export | JET PMO", page_icon="📄", layout="wide")
inject_styles()
sidebar_nav()
init_session_state()
review = analyze_application()

st.markdown("""
<div class="hero" style="min-height:120px">
    <div class="hero-glow"></div><div class="hero-grid"></div>
    <div class="hero-content" style="padding:1.4rem 2rem">
        <div>
            <div class="hero-tag">📄 Summary and Export</div>
            <h1>Review the <span>Application Output</span></h1>
            <p>This summary pulls together the guided application, financing fit, reviewer signals, and a practical readiness note into one clean demo output.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Project details</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    project_name = st.text_input("Project name", key="proj_name")
with col2:
    org_name = st.text_input("Organisation", key="proj_org")
with col3:
    funding_ask = st.text_input("Funding ask (R)", key="proj_funding")

finance_stage = st.session_state.get("finance_stage", "Not yet assessed")
finance_notes = st.session_state.get("finance_notes", "")
finance_recommendations = st.session_state.get("finance_recommendations", [])

st.markdown('<div class="section-title">Executive view</div>', unsafe_allow_html=True)
a, b = st.columns([1.1, 1])
with a:
    badges = " ".join([f"<span class='badge badge-green'>{escape(item)}</span>" for item in finance_recommendations])
    st.markdown(
        f"""
        <div class="section-block">
            <div style='font-weight:700; font-size:1rem; color:#7A3E2B; margin-bottom:0.4rem'>Current financing fit</div>
            <div style='font-size:1.35rem; font-weight:800; color:#07553B; margin-bottom:0.35rem'>{escape(finance_stage)}</div>
            <div style='font-size:0.92rem; color:#5F6B66; line-height:1.65; margin-bottom:0.7rem'>{escape(finance_notes or 'Questionnaire not yet completed.')}</div>
            <div>{badges or '<span style="color:#5F6B66">No recommendations saved yet.</span>'}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="section-block" style="margin-top:0.8rem">
            <div style='font-weight:700; font-size:1rem; color:#7A3E2B; margin-bottom:0.4rem'>Submission readiness note</div>
            <div style='font-size:0.92rem; color:#5F6B66; line-height:1.7'>{escape(review['readiness_note'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with b:
    st.markdown(render_heatmap(review["scores"]), unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="section-title">What looks stronger</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    for item in review["strengths"] or ["No strengths surfaced yet. Fill in more sections first."]:
        st.markdown(f"- {item}")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="section-title">What still needs work</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    for item in review["gaps"] or ["No major gaps surfaced yet."]:
        st.markdown(f"- {item}")
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="section-title">Red flags</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["red_flags"]:
        for item in review["red_flags"]:
            st.markdown(f"<span class='badge badge-red'>Watch</span> {escape(item)}", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge badge-green'>No major red flags surfaced.</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

colx, coly = st.columns(2)
with colx:
    st.markdown('<div class="section-title">Funding route explainer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["funding_route_explainer"]:
        for heading, text in review["funding_route_explainer"]:
            st.markdown(f"**{heading}**")
            st.write(text)
    else:
        st.write("Complete the financing fit questionnaire first to generate this section.")
    st.markdown('</div>', unsafe_allow_html=True)
with coly:
    st.markdown('<div class="section-title">Minimum evidence checklist</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    if review["evidence_checklist"]:
        for item in review["evidence_checklist"]:
            st.markdown(f"- {item}")
    else:
        st.write("Complete the financing fit questionnaire first to generate this section.")
    st.markdown('</div>', unsafe_allow_html=True)


def section_block(icon: str, title: str, content_dict: dict) -> None:
    has_content = any(str(value).strip() for value in content_dict.values())
    st.markdown(
        f"""
        <div class='section-block' style='margin-bottom:1rem'>
            <div style='font-weight:700; font-size:1rem; color:#7A3E2B; margin-bottom:1rem'>{icon} {title}</div>
        """,
        unsafe_allow_html=True,
    )
    if has_content:
        for label, value in content_dict.items():
            if str(value).strip():
                st.markdown(f"**{label}**")
                st.markdown(
                    f"""<div style='background:#f8fafc; border-left:3px solid {THEME['green']}; border-radius:0 8px 8px 0; padding:0.8rem 1rem; font-size:0.9rem; color:#334155; line-height:1.6; white-space:pre-wrap'>{escape(str(value))}</div>""",
                    unsafe_allow_html=True,
                )
    else:
        st.markdown("<div style='color:#5F6B66; font-size:0.9rem; font-style:italic'>Not yet completed.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("📌 Problem statement"):
    section_block("📌", "Problem Statement", {
        "Context and background": st.session_state.get("ps_context", ""),
        "Core problem": st.session_state.get("ps_problem", ""),
        "Evidence and data": st.session_state.get("ps_evidence", ""),
        "Impact of inaction": st.session_state.get("ps_impact", ""),
    })
with st.expander("💡 Solution and differentiation"):
    section_block("💡", "Solution and Differentiation", {
        "Solution description": st.session_state.get("sol_description", ""),
        "What you have achieved": st.session_state.get("sol_achieved", ""),
        "Differentiation from market": st.session_state.get("sol_differentiation", ""),
        "Innovation and scalability": st.session_state.get("sol_innovation", ""),
    })
with st.expander("👥 Team and achievements"):
    section_block("👥", "Team and Achievements", {
        "Team overview": st.session_state.get("team_overview", ""),
        "Key achievements": st.session_state.get("team_achievements", ""),
        "Identified gaps and mitigation": st.session_state.get("team_gaps", ""),
    })
with st.expander("📊 Business model and plan"):
    section_block("📊", "Business Model and Plan", {
        "Business model": st.session_state.get("bm_model", ""),
        "Revenue streams and unit economics": st.session_state.get("bm_revenue", ""),
        "Target customers and market size": st.session_state.get("bm_customers", ""),
        "Competitive landscape": st.session_state.get("bm_competition", ""),
    })
with st.expander("🎯 Milestones and objectives"):
    section_block("🎯", "Milestones and Objectives", {
        "Overall objectives": st.session_state.get("mil_objectives", ""),
        "Short-term milestones": st.session_state.get("mil_short", ""),
        "Medium-term milestones": st.session_state.get("mil_medium", ""),
        "Key performance indicators": st.session_state.get("mil_kpis", ""),
    })
with st.expander("⚠️ Risk register"):
    section_block("⚠️", "Risk Register", {
        "Technical risks": st.session_state.get("risk_technical", ""),
        "Market risks": st.session_state.get("risk_market", ""),
        "Regulatory risks": st.session_state.get("risk_regulatory", ""),
        "Financial risks": st.session_state.get("risk_financial", ""),
        "Overall mitigation strategy": st.session_state.get("risk_mitigation", ""),
    })

st.markdown("---")
st.markdown('<div class="section-title">Export to PDF</div>', unsafe_allow_html=True)
if st.button("📄 Generate PDF export", type="primary"):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("Title", parent=styles["Title"], textColor=colors.HexColor(THEME["green_dark"]), fontSize=20)
        subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], textColor=colors.HexColor(THEME["muted"]), fontSize=10, spaceAfter=8)
        section_style = ParagraphStyle("Section", parent=styles["Heading2"], textColor=colors.HexColor(THEME["maroon"]), fontSize=12, spaceBefore=10, spaceAfter=6)
        body_style = ParagraphStyle("Body", parent=styles["Normal"], textColor=colors.HexColor("#333333"), fontSize=9.5, leading=14)

        story = [
            Paragraph("Just Energy Transition · Application Support Wizard Demo", subtitle_style),
            Paragraph(escape(project_name or "Funding Application"), title_style),
            Paragraph(escape(org_name or "Organisation"), subtitle_style),
            Paragraph(f"Funding Ask: R {escape(funding_ask or 'Not specified')}", subtitle_style),
            Paragraph(f"Financing Fit: {escape(finance_stage)}", subtitle_style),
            HRFlowable(width="100%", thickness=1, color=colors.HexColor(THEME["green"])),
            Spacer(1, 8),
        ]

        def add_section(title: str, entries: dict) -> None:
            story.append(Paragraph(title, section_style))
            for label, value in entries.items():
                if str(value).strip():
                    story.append(Paragraph(f"<b>{escape(label)}</b>", body_style))
                    story.append(Paragraph(escape(str(value)).replace("\n", "<br/>"), body_style))
                    story.append(Spacer(1, 4))

        add_section("Executive summary", {
            "Readiness note": review["readiness_note"],
            "What looks stronger": "; ".join(review["strengths"]),
            "What still needs work": "; ".join(review["gaps"]),
            "Red flags": "; ".join(review["red_flags"]),
        })
        add_section("Financing fit", {
            "Guidance": finance_notes,
            "Relevant instruments": ", ".join(finance_recommendations),
        })
        add_section("Funding route explainer", {heading: text for heading, text in review["funding_route_explainer"]})
        add_section("Minimum evidence checklist", {f"Item {i+1}": item for i, item in enumerate(review["evidence_checklist"])})
        add_section("Problem statement", {
            "Context and background": st.session_state.get("ps_context", ""),
            "Core problem": st.session_state.get("ps_problem", ""),
            "Evidence and data": st.session_state.get("ps_evidence", ""),
            "Impact of inaction": st.session_state.get("ps_impact", ""),
        })
        add_section("Solution and differentiation", {
            "Solution description": st.session_state.get("sol_description", ""),
            "What you have achieved": st.session_state.get("sol_achieved", ""),
            "Differentiation from market": st.session_state.get("sol_differentiation", ""),
            "Innovation and scalability": st.session_state.get("sol_innovation", ""),
        })
        add_section("Team and achievements", {
            "Team overview": st.session_state.get("team_overview", ""),
            "Key achievements": st.session_state.get("team_achievements", ""),
            "Identified gaps and mitigation": st.session_state.get("team_gaps", ""),
        })
        add_section("Business model and plan", {
            "Business model": st.session_state.get("bm_model", ""),
            "Revenue streams and unit economics": st.session_state.get("bm_revenue", ""),
            "Target customers and market size": st.session_state.get("bm_customers", ""),
            "Competitive landscape": st.session_state.get("bm_competition", ""),
        })
        add_section("Milestones and objectives", {
            "Overall objectives": st.session_state.get("mil_objectives", ""),
            "Short-term milestones": st.session_state.get("mil_short", ""),
            "Medium-term milestones": st.session_state.get("mil_medium", ""),
            "Key performance indicators": st.session_state.get("mil_kpis", ""),
        })
        add_section("Risk register", {
            "Technical risks": st.session_state.get("risk_technical", ""),
            "Market risks": st.session_state.get("risk_market", ""),
            "Regulatory risks": st.session_state.get("risk_regulatory", ""),
            "Financial risks": st.session_state.get("risk_financial", ""),
            "Overall mitigation strategy": st.session_state.get("risk_mitigation", ""),
        })

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name="jet_pmo_application_summary.pdf", mime="application/pdf")
        st.success("PDF generated.")
    except Exception as exc:
        st.error(f"PDF generation failed: {exc}")
