import os
from html import escape
from typing import Any, Dict, List, Tuple

import streamlit as st

THEME = {
    "green": "#0B6B4A",
    "green_dark": "#07553B",
    "orange": "#B55A1C",
    "orange_dark": "#8F4615",
    "maroon": "#7A3E2B",
    "charcoal": "#2E3A35",
    "muted": "#5F6B66",
    "border": "#D8E3DD",
    "surface": "#FFFFFF",
    "surface_alt": "#F7F7F2",
    "surface_soft": "#EEF4F0",
    "danger": "#A63F3F",
    "amber": "#A86A1B",
}

DEFAULTS = {
    "ps_context": "", "ps_problem": "", "ps_evidence": "", "ps_impact": "",
    "sol_description": "", "sol_achieved": "", "sol_differentiation": "", "sol_innovation": "",
    "team_overview": "", "team_achievements": "", "team_gaps": "",
    "bm_model": "", "bm_revenue": "", "bm_customers": "", "bm_market_size": "", "bm_competition": "",
    "mil_objectives": "", "mil_short": "", "mil_medium": "", "mil_long": "", "mil_kpis": "",
    "risk_technical": "", "risk_market": "", "risk_regulatory": "", "risk_financial": "", "risk_mitigation": "",
    "proj_name": "", "proj_org": "", "proj_funding": "", "trl_result": None,
    "finance_stage": "Not yet assessed", "finance_recommendations": [], "finance_notes": "",
    "review_scores": {}, "review_strengths": [], "review_gaps": [], "review_red_flags": [],
    "readiness_note": "", "funding_route_explainer": [], "evidence_checklist": [],
}

SECTION_MAP = {
    "Problem clarity": ["ps_problem", "ps_context", "ps_evidence", "ps_impact"],
    "Evidence strength": ["ps_evidence", "sol_achieved"],
    "Team credibility": ["team_overview", "team_achievements", "team_gaps"],
    "Commercial logic": ["bm_model", "bm_revenue", "bm_customers", "bm_competition"],
    "Delivery readiness": ["mil_objectives", "mil_short", "mil_kpis"],
    "Risk realism": ["risk_technical", "risk_market", "risk_regulatory", "risk_financial", "risk_mitigation"],
}

STAGE_GUIDANCE = {
    "Grant-led development": {
        "route": [
            ("Why this route fits", "The project still appears to be building its first credible package of technical, market, and execution evidence. Non-repayable or highly catalytic support is more realistic than hard repayment structures at this point."),
            ("Why other routes may be premature", "Commercial debt and larger-scale blended finance usually require clearer delivery proof, stronger governance, and some path to revenue or contracted demand."),
            ("What to improve next", "Strengthen evidence of the problem, show technical proof, secure pilot partners, and define milestones with clearer outputs and timelines."),
        ],
        "checklist": [
            "A clearly evidenced problem statement with quantified need or market signal",
            "Prototype concept, feasibility work, or technical rationale documented",
            "Named delivery partners, pilot hosts, or validation channels",
            "Initial budget and use-of-funds logic",
            "Basic milestone plan with achievable early outputs",
        ],
    },
    "Pilot and concessional finance": {
        "route": [
            ("Why this route fits", "The project has moved beyond pure concept stage and appears suitable for pilot execution, demonstration, or first deployment support with softer repayment terms."),
            ("Why other routes may be premature", "Pure commercial debt may still be too aggressive if repayment depends on unproven uptake, limited operational data, or incomplete governance systems."),
            ("What to improve next", "Show pilot results, customer or partner validation, a clearer operating model, and stronger risk mitigation for delivery and regulation."),
        ],
        "checklist": [
            "Pilot plan with site, partner, or end-user confirmation",
            "Prototype or demonstration data showing technical performance",
            "Indicative costs, pricing logic, or affordability pathway",
            "Basic governance and reporting capacity in place",
            "Material risks identified with practical mitigations",
        ],
    },
    "Blended finance and impact capital": {
        "route": [
            ("Why this route fits", "The project shows a plausible path toward scale, but some catalytic support may still be needed to absorb risk, crowd in capital, or bridge a bankability gap."),
            ("Why other routes may be premature", "Straight commercial capital may still be difficult if contracts, revenues, or deployment evidence are not yet strong enough on their own."),
            ("What to improve next", "Tighten contracted demand, sharpen revenue logic, strengthen delivery capacity, and make the risk allocation clearer for each financing party."),
        ],
        "checklist": [
            "Pilot or early deployment data from a relevant operating environment",
            "Revenue model, pricing assumptions, or contracted demand evidence",
            "Clear implementation milestones with owners and timing",
            "Governance, reporting, and procurement capacity visible",
            "Risk-sharing logic suitable for catalytic or impact-oriented capital",
        ],
    },
    "Commercialisation and scale finance": {
        "route": [
            ("Why this route fits", "The project appears to be approaching or entering scale-up, where stronger contractual evidence, operating capability, and capital structure planning become central."),
            ("Why other routes may be premature", "Purely grant-led support may no longer be the best fit unless it is solving a clearly defined catalytic gap such as first-loss support, localisation, or public-good components."),
            ("What to improve next", "Sharpen financial modelling, repayment logic, delivery sequencing, and investment-readiness evidence such as contracts, demand, governance, and performance history."),
        ],
        "checklist": [
            "Demonstrated operating model with repeatable performance evidence",
            "Revenue, offtake, or contracted demand indicators",
            "Clear capex and opex case with financing structure logic",
            "Strong governance and management controls",
            "Delivery plan that supports lender or investor confidence",
        ],
    },
}


def local_css() -> None:
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def inject_styles() -> None:
    local_css()


def init_session_state(defaults: Dict[str, Any] | None = None) -> None:
    merged = DEFAULTS.copy()
    if defaults:
        merged.update(defaults)
    for key, value in merged.items():
        if key not in st.session_state:
            st.session_state[key] = value


def format_compact_rand(value: Any) -> str:
    try:
        numeric = float(str(value).replace(",", "").replace("R", "").strip())
    except (TypeError, ValueError):
        return str(value) if value not in (None, "") else "—"

    if numeric >= 1_000_000:
        short = numeric / 1_000_000
        formatted = f"R{short:.1f}m"
    elif numeric >= 1_000:
        short = numeric / 1_000
        formatted = f"R{short:.0f}k"
    else:
        formatted = f"R{numeric:,.0f}"

    return formatted.replace(".0m", "m")


def _field_text(key: str) -> str:
    return str(st.session_state.get(key, "") or "").strip()


def _score_fields(keys: List[str]) -> int:
    values = [_field_text(k) for k in keys]
    completed = sum(bool(v) for v in values)
    total_chars = sum(len(v) for v in values)
    ratio = completed / len(keys)
    if completed == 0:
        return 0
    if ratio < 0.5 or total_chars < 120:
        return 1
    if ratio < 0.85 or total_chars < 320:
        return 2
    return 3


def level_label(score: int) -> str:
    return ["Missing", "Emerging", "Developing", "Stronger"][max(0, min(score, 3))]


def analyze_application() -> Dict[str, Any]:
    scores = {name: _score_fields(keys) for name, keys in SECTION_MAP.items()}
    strengths: List[str] = []
    gaps: List[str] = []
    red_flags: List[str] = []

    if scores["Problem clarity"] >= 2:
        strengths.append("The application presents a visible problem narrative rather than a purely generic opportunity statement.")
    else:
        gaps.append("The problem case still needs sharper framing, evidence, and consequences of inaction.")

    if scores["Evidence strength"] >= 2:
        strengths.append("There is some supporting evidence or delivery proof that can help reviewer confidence.")
    else:
        gaps.append("Evidence remains thin. Reviewers will likely ask for stronger data, validation, pilot proof, or market signals.")
        red_flags.append("Weak evidence base may make the application feel aspirational rather than decision-ready.")

    if scores["Team credibility"] >= 2:
        strengths.append("The team section provides enough substance to support basic delivery credibility.")
    else:
        gaps.append("The team section needs clearer roles, achievements, or delivery capability to strengthen credibility.")

    if scores["Commercial logic"] >= 2:
        strengths.append("The commercial case has enough shape to discuss financing more credibly.")
    else:
        gaps.append("Commercial logic is still underdeveloped. Reviewers may struggle to see who pays, why, and on what basis.")
        red_flags.append("Unclear customer and revenue logic can undermine financing discussions even when the technology case is interesting.")

    if scores["Delivery readiness"] >= 2:
        strengths.append("Milestones and outputs provide some sense of execution sequencing.")
    else:
        gaps.append("Milestones need to be more specific, time-bound, and owned to show delivery discipline.")

    if scores["Risk realism"] >= 2:
        strengths.append("The application recognises risks in a way that can support a more mature discussion.")
    else:
        gaps.append("Risk treatment still feels thin or generic and would benefit from more practical mitigations.")
        red_flags.append("Generic risk language can signal weak implementation planning.")

    stage = st.session_state.get("finance_stage", "Not yet assessed")
    if stage == "Commercialisation and scale finance" and scores["Commercial logic"] < 2:
        red_flags.append("The selected financing stage appears more advanced than the current commercial evidence in the application.")
    if stage == "Commercialisation and scale finance" and scores["Evidence strength"] < 2:
        red_flags.append("Scale-oriented finance is indicated, but the underlying operating or pilot evidence still looks limited.")
    if stage == "Grant-led development" and scores["Delivery readiness"] >= 3 and scores["Commercial logic"] >= 2:
        strengths.append("The project may be able to position for more than pure grant support if stronger financial evidence is added.")

    guidance = STAGE_GUIDANCE.get(stage, {"route": [], "checklist": []})
    weak_areas = [name.lower() for name, score in scores.items() if score <= 1]
    if stage == "Not yet assessed":
        readiness_note = "The application has not yet completed the financing fit questionnaire, so the guidance remains incomplete. Finish the questionnaire to generate a more credible route and evidence checklist."
    else:
        if weak_areas:
            weak_str = ", ".join(weak_areas[:3])
            readiness_note = f"This application appears most suitable for {stage.lower()} at present. It would benefit from stronger work on {weak_str} before being positioned as a more investment-ready submission."
        else:
            readiness_note = f"This application appears broadly aligned to {stage.lower()} and already shows a reasonable base for reviewer discussion. The next step is to sharpen the evidence package and keep the narrative tightly aligned to the use of funds."

    result = {
        "scores": scores,
        "strengths": strengths[:4],
        "gaps": gaps[:5],
        "red_flags": red_flags[:5],
        "readiness_note": readiness_note,
        "funding_route_explainer": guidance["route"],
        "evidence_checklist": guidance["checklist"],
    }

    st.session_state["review_scores"] = scores
    st.session_state["review_strengths"] = result["strengths"]
    st.session_state["review_gaps"] = result["gaps"]
    st.session_state["review_red_flags"] = result["red_flags"]
    st.session_state["readiness_note"] = readiness_note
    st.session_state["funding_route_explainer"] = guidance["route"]
    st.session_state["evidence_checklist"] = guidance["checklist"]
    return result


def render_heatmap(scores: Dict[str, int]) -> str:
    tone = {0: "tile-missing", 1: "tile-weak", 2: "tile-medium", 3: "tile-strong"}
    blocks = []
    for name, score in scores.items():
        blocks.append(
            f"<div class='heat-tile {tone.get(score, 'tile-missing')}'><div class='heat-name'>{escape(name)}</div><div class='heat-score'>{escape(level_label(score))}</div></div>"
        )
    return "<div class='heat-grid'>" + "".join(blocks) + "</div>"


def sidebar_nav() -> None:
    with st.sidebar:
        st.markdown("<div class='sidebar-brand'>Just Energy Transition</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-subbrand'>Application Support Wizard</div>", unsafe_allow_html=True)
        st.caption("Demo for improving submission quality before formal assessment.")
        st.markdown("---")
        st.page_link("app.py", label="Home")
        st.page_link("pages/1_Guided_Application.py", label="Guided application")
        st.page_link("pages/2_TRL_Calculator.py", label="Financing fit questionnaire")
        st.page_link("pages/3_Financing_Options.py", label="Financing options")
        st.page_link("pages/4_Loan_Calculator.py", label="Loan calculator")
        st.page_link("pages/5_Summary_Export.py", label="Summary and export")
        st.page_link("pages/6_Reviewer_Signals.py", label="Reviewer signals")
        st.markdown("---")
        st.markdown(
            """
            <div class='sidebar-note'>
                Built as a front-end demo for the NEV portfolio.<br>
                Purpose: help applicants understand what reviewers usually look for and improve weak applications earlier.
            </div>
            """,
            unsafe_allow_html=True,
        )


EXAMPLE_PROJECTS = {
    "peri_charge": {
        "label": "⚡ PeriCharge — EV Charging Hub",
        "org": "GreenFleet SA (Pty) Ltd",
        "funding_ask": "12,500,000",
        "trl": 6,
        "description": "Solar-hybrid DC fast-charging hubs for peri-urban commercial fleets",
        "ps_context": "South Africa's transport sector accounts for approximately 13% of national GHG emissions. The Just Energy Transition pathway commits to a significant shift toward zero-emission vehicles by 2035, yet EV penetration remains below 0.1% of the commercial fleet. The Presidential Climate Commission's JET Implementation Plan identifies charging infrastructure as a critical enabler, particularly for last-mile and commercial logistics operators operating outside major metros.",
        "ps_problem": "Commercial fleets in peri-urban areas cannot transition to EVs because there is no affordable, reliable charging infrastructure outside of Johannesburg, Cape Town, and Durban CBDs. Existing fast chargers require stable 3-phase grid supply and cost upwards of R1.8M per unit — making them inaccessible for depot environments in areas with load-shedding exposure. This is actively blocking fleet operators from accessing green finance and meeting corporate sustainability commitments.",
        "ps_evidence": "A 2023 CSIR survey of 120 commercial fleet operators showed 78% cited charging infrastructure as the primary barrier to EV adoption. SANEDI estimates this infrastructure gap affects approximately 45,000 commercial vehicles across peri-urban Gauteng alone. Conversations with 8 fleet operators in Midrand, Germiston, and Alberton confirmed willingness to pay for a reliable managed charging solution.",
        "ps_impact": "Without intervention, South Africa's commercial fleet will remain ICE-dependent through 2040, locking in an estimated 8Mt CO₂ cumulative emissions and missing an estimated 12,000 potential green jobs in EV servicing and infrastructure. Fleet operators will also face increasing carbon tax liability with no viable compliance pathway.",
        "sol_description": "PeriCharge is a modular DC fast-charging hub designed specifically for peri-urban depot environments. Each hub is solar-hybrid, grid-connected, and remotely managed via our proprietary IoT platform. A single hub can charge 6 commercial EVs simultaneously at 60kW per bay. The built-in 30kWh battery buffer provides 4 hours of backup during load-shedding. Hubs are designed for rapid deployment — typically 6–8 weeks from site selection to commissioning.",
        "sol_achieved": "Completed a 6-month pilot with 3 fleet operators in Midrand (Q3 2023). Delivered 8,200 charging sessions at 99.1% uptime through 47 load-shedding events. Achieved a measured 38% reduction in fuel costs for pilot operators. Signed Letters of Intent with 2 additional operators representing 140 vehicles. Received a Provisional Patent (2023/045678) for our energy management firmware.",
        "sol_differentiation": "Existing DC chargers (GridCars, Rubicon) are designed for urban retail locations. They cost R1.8M+ per unit, require stable 3-phase grid supply, and are not designed for depot environments. PeriCharge costs R620K per hub, operates on single-phase supply with solar-battery backup, and is purpose-built for fleet depot layouts. Our total cost of ownership for a 20-vehicle fleet is 44% lower than the nearest alternative over 5 years.",
        "sol_innovation": "Our proprietary EMS firmware (patent pending) dynamically balances grid draw, solar generation, and battery discharge in real time — reducing peak demand charges by up to 40% compared to conventional chargers. The modular design allows sites to scale from 2 to 20 charging bays without any additional civil engineering. Remote diagnostics mean 80% of faults are resolved without a site visit.",
        "team_overview": "CEO: Thandiwe Dlamini — 12 years in EV infrastructure across South Africa, Kenya, and Ghana. Previously Deputy Director at SANEDI's e-Mobility unit. CTO: Sipho Nkosi — MSc Power Electronics (UCT 2018), previously Senior Engineer at ABB South Africa, holds 2 patents. COO: Priya Naidoo — previously ran operations for GridCo SA, managing R200M in assets. CFO: James van der Merwe — CA(SA), 8 years in green finance at DBSA.",
        "team_achievements": "Together deployed 18 EV charging sites across Gauteng and the Western Cape (2021–2023). Won the SEFA Green Innovation Award 2022. Successfully raised R4.5M in seed funding from Edge Growth and Rethink Capital. Team collectively holds 3 patents and has published 4 peer-reviewed papers on EV infrastructure in sub-Saharan Africa.",
        "team_gaps": "We currently lack in-house legal expertise for energy licensing. We have engaged Bowmans' energy practice on a 12-month retainer (R480K/year). Recruiting a Head of Regulatory Affairs, budgeted in Year 1 OPEX. Building an advisory board with representation from NAAMSA, SANEDI, and an ITA from the University of Pretoria.",
        "bm_model": "PeriCharge operates on a Charging-as-a-Service (CaaS) model. Fleet operators pay a monthly subscription per vehicle covering unlimited charging, preventative maintenance, remote monitoring, and a guaranteed uptime SLA of 98%. We own and operate all hub hardware under 5-year agreements.",
        "bm_revenue": "Primary: Subscription fees at R4,500/vehicle/month. Secondary: Grid services / demand response (~R800K/year across 5 hubs). Future: Verified carbon credits (Gold Standard certification in progress). Unit economics: Hub cost R620K, break-even at 18 vehicles, projected IRR 22% over 7 years at 80% utilisation.",
        "bm_customers": "Primary: Logistics and delivery fleets (10–200 vehicles) operating from fixed depots in Gauteng, Western Cape, and KZN. SAM: ~18,000 commercial EVs by 2028 (NAAMSA forecast). SOM: 2,500 vehicles by Year 3 = R135M ARR. Currently contracted: 3 operators, 80 vehicles.",
        "bm_competition": "GridCars: retail-focused, not designed for fleet depots. Rubicon Energy: premium at R2.2M/unit, priced out of our market. Charge.io: new entrant, no fleet offering. No direct competitor addresses peri-urban depot charging with solar-battery integration at our price point.",
        "mil_objectives": "1. Deploy 10 charging hubs across Gauteng by December 2025\n2. Onboard 200 commercial EVs onto the network\n3. Demonstrate 40% reduction in fleet fuel costs vs ICE baseline\n4. Create 45 permanent direct jobs\n5. Reduce fleet emissions by 1,200 tCO₂/year by end of Year 2",
        "mil_short": "M1 (Month 2): Complete site assessments and grid connection applications for 3 hub locations\nM2 (Month 4): Financial close on JET funding tranche 1\nM3 (Month 6): Deploy and commission Hub 1 (Midrand) and Hub 2 (Germiston)\nM4 (Month 8): Onboard 50 vehicles across both hubs\nM5 (Month 12): Achieve cash flow breakeven on Hub 1; commission Hub 3 and 4",
        "mil_medium": "Year 2: Deploy Hubs 5–8 across Gauteng; expand to Western Cape (Hub 9, Bellville)\nYear 2: Launch carbon credit programme — first verified credits issued Q3 Year 2\nYear 2: 150 vehicles on network, R81M ARR run-rate\nYear 3: Full 10-hub deployment; expansion to KwaZulu-Natal\nYear 3: Series A raise of R50M for national rollout",
        "mil_kpis": "• Hubs deployed and commissioned (Target: 10 by Month 18)\n• EVs onboarded (Target: 200 by Month 18)\n• Hub uptime % (Target: ≥98%)\n• Charging sessions per hub per month (Target: 1,200+)\n• tCO₂ avoided per year (Target: 1,200)\n• Direct jobs created (Target: 45)\n• Revenue per hub per month (Target: R135,000 at steady state)",
        "risk_technical": "Risk: Grid instability and load-shedding disrupts charging operations.\nLikelihood: High. Impact: High.\nMitigation: Solar-battery hybrid provides 4+ hours backup. BMS protects EVs during grid fluctuations. Pilot data: 99.1% uptime across 47 load-shedding events.",
        "risk_market": "Risk: Commercial EV adoption slower than projected.\nLikelihood: Medium. Impact: High.\nMitigation: LOIs from 5 operators already signed. CaaS model removes capex barrier. Hardware can be repurposed for BESS grid services if EV demand lags.",
        "risk_regulatory": "Risk: Delays in municipal permitting for charging infrastructure.\nLikelihood: Medium. Impact: Medium.\nMitigation: Specialist town planning consultants engaged in Gauteng and Western Cape. 3-month permitting buffer in all project schedules. Relationships established with Eskom Distribution and City Power key accounts.",
        "risk_financial": "Risk: ZAR depreciation increases cost of imported components (~40% of COGS).\nLikelihood: Medium. Impact: Medium.\nMitigation: Forward exchange contracts in place. Local manufacturing partnership in development with Tshwane-based electronics firm (target: 60% local by Year 2).",
        "risk_mitigation": "Formal Risk Register reviewed monthly by Board, quarterly by ITA (Prof. A. Swanepoel, University of Pretoria). 15% contingency in all project cost estimates. JET-specialist legal counsel (Bowmans) reviews regulatory compliance quarterly. R500K emergency credit facility with Nedbank.",
    },
    "nev_training": {
        "label": "🎓 NEV Skills Academy",
        "org": "FutureWork SA (NPC)",
        "funding_ask": "6,800,000",
        "trl": 5,
        "description": "Accredited EV technician training programme for township auto workshops",
        "ps_context": "South Africa's automotive sector employs approximately 110,000 people directly, with a further 420,000 in downstream services. The JET transition to New Energy Vehicles will fundamentally disrupt this sector — ICE servicing skills become obsolete as EV penetration grows. Most independent workshops serving township communities have had no access to EV training, certification, or tooling.",
        "ps_problem": "There is no affordable, accessible pathway for existing automotive technicians in township workshops to upskill for EV servicing. TVET college EV curricula remain under development. OEM training programmes are expensive and designed for franchised dealerships only. This creates a skills cliff: as EVs enter the fleet, township workshops lose customers and revenue while qualified EV technicians remain scarce.",
        "ps_evidence": "A 2023 AIDC survey of 340 independent workshops in Gauteng showed 94% had zero EV training and 0% had EV diagnostic equipment. MERSETA estimates 28,000 automotive technicians will require reskilling by 2030. 71% of workshop owners expressed strong interest in EV training if affordable and QCTO-accredited.",
        "ps_impact": "Without a reskilling pathway, an estimated 28,000 technicians risk unemployment as EV penetration grows. Township workshops — many owned by Black entrepreneurs — face closure as their customer base transitions to EVs they cannot service. This directly reverses JET's stated objective of an inclusive and just energy transition.",
        "sol_description": "NEV Skills Academy delivers a 6-week accredited EV Technician Fundamentals programme combining online learning modules with hands-on practical training using real EV components. We operate a mobile training unit — a converted vehicle transporter fitted with EV drivetrain components, HV safety equipment, and diagnostic tools — that travels to township workshops and TVET colleges.",
        "sol_achieved": "Pilot cohort: 24 technicians across 3 workshops in Soweto and Tembisa (Q2 2023). 22 of 24 completed; 19 passed practical assessment. Provisional QCTO accreditation letter received. Partnerships signed with Volvo Cars SA and BYD SA dealer network for post-training job placement. Mobile training unit prototype built and tested.",
        "sol_differentiation": "Existing EV training is either OEM-specific (R18,000–R45,000, dealership-only) or theoretical (TVET, no practical component). NEV Skills Academy is OEM-agnostic, QCTO-accredited, and comes to the workshop. Cost per trainee: R4,200 — 88% cheaper than OEM alternatives. Only provider with a mobile practical training unit in Sub-Saharan Africa.",
        "sol_innovation": "The mobile unit removes the single biggest barrier to township training — logistics and travel cost. Our blended learning model (online theory + in-person practical) allows technicians to complete theory in their own time without closing the workshop. AR-assisted diagnostic training module in development for Year 2 (currently TRL 4).",
        "team_overview": "Executive Director: Nomsa Khumalo — 15 years in TVET education, previously Deputy Principal at Ekurhuleni East TVET College. Technical Director: Kevin Sithole — Master EV Technician, 11 years at BMW Group SA, Level 3 HV Safety certified. Partnerships Manager: Ayanda Mokoena — previously at MERSETA, specialist in SETA funding and QCTO accreditation. Board includes representatives from AIDC, MERSETA, and Harambee Youth Employment Accelerator.",
        "team_achievements": "Pilot cohort delivered (24 trainees, 92% pass rate). Mobile unit designed, built, and tested. Provisional QCTO accreditation in process. R1.2M raised from National Skills Fund (NSF) pre-seed grant. Featured in Business Day and Mail & Guardian JET coverage. Winner: SEFA Social Enterprise Development Award 2023.",
        "team_gaps": "Currently rely on 2 contracted master trainers — need to build a roster of 6. Train the Trainer programme budgeted in Year 1. Lack dedicated financial management — engaged Outsourced CFO SA for 18 months while recruiting permanent CFO.",
        "bm_model": "Hybrid revenue model: (1) SETA-funded training — accredited MERSETA provider enabling access to mandatory and discretionary grant funding. (2) Direct fee — R4,200 per trainee from workshops and fleet operators. (3) Corporate partnerships — EV importers pay a partnership fee for preferred access to our graduate pool.",
        "bm_revenue": "Year 1: 200 trainees × R4,200 = R840K + R2.1M MERSETA discretionary grants = R2.94M. Year 2: 500 trainees + 3 corporate partnerships × R350K = R5.25M. Year 3: 1,000 trainees/year — financially self-sustaining.",
        "bm_customers": "Primary: Independent automotive workshop owners seeking to upskill staff. Secondary: TVET colleges wanting practical EV content delivery. Tertiary: Fleet operators and EV importers needing a pipeline of qualified technicians. B2G: Government fleet managers as fleets transition.",
        "bm_competition": "No direct competitors offering mobile, accredited, township-focused EV technician training in SA. Indirect: OEM training (expensive, brand-specific), TVET colleges (theoretical only). First-mover advantage, QCTO accreditation, and mobile model create a defensible position.",
        "mil_objectives": "1. Train and certify 500 EV technicians by end of Year 2\n2. Achieve full QCTO accreditation by Q2 Year 1\n3. Operate 2 mobile training units covering all 9 provinces by Year 3\n4. Achieve financial self-sustainability (no grant dependency) by Year 3\n5. Place 400 graduates in employment or self-employment",
        "mil_short": "M1 (Month 1): Receive full QCTO accreditation\nM2 (Month 3): Launch Cohort 2 — 40 trainees, Gauteng\nM3 (Month 4): Mobile Unit 2 commissioned (Western Cape)\nM4 (Month 6): 100 certified graduates; launch placement programme\nM5 (Month 12): 200 certified graduates; MERSETA grant disbursement confirmed",
        "mil_medium": "Year 2: Unit 3 deployed (KZN); 500 total certified graduates\nYear 2: Launch AR diagnostic training module\nYear 2: 5 corporate partnership agreements signed\nYear 3: National coverage — all 9 provinces; 1,000 graduates per year\nYear 3: Financial self-sustainability achieved",
        "mil_kpis": "• Trainees enrolled and certified per cohort\n• Assessment pass rate (Target: ≥85%)\n• Graduate employment / business launch rate (Target: ≥75%)\n• Cost per certified trainee (Target: ≤R4,200)\n• Mobile units operational\n• MERSETA grant disbursement success rate\n• Employer satisfaction score (Target: ≥4/5)",
        "risk_technical": "Risk: QCTO accreditation delayed or conditions imposed requiring curriculum changes.\nLikelihood: Low-Medium. Impact: High (blocks MERSETA funding).\nMitigation: Provisional accreditation in hand; dedicated QCTO consultant engaged. Full accreditation expected Q2 Year 1 based on assessor feedback.",
        "risk_market": "Risk: Workshops unable to afford R4,200 fee.\nLikelihood: Medium. Impact: Medium.\nMitigation: MERSETA funding means formal employers pay nothing out of pocket. Training voucher scheme (NSF-funded) subsidises 50% of trainees in Year 1 for informal workshops.",
        "risk_regulatory": "Risk: MERSETA changes discretionary grant criteria or funding allocation.\nLikelihood: Low. Impact: High.\nMitigation: Diversifying revenue to reduce MERSETA dependency to <40% by Year 2. Corporate partnerships and direct fees provide buffer.",
        "risk_financial": "Risk: Mobile unit maintenance and repair costs exceed budget.\nLikelihood: Medium. Impact: Low-Medium.\nMitigation: Annual maintenance contracts with certified automotive engineering firm. 10% contingency in unit operating budget. Full insurance cover in place.",
        "risk_mitigation": "Risks reviewed monthly by Board and at each cohort debrief. Independent evaluator engaged for Year 1 impact assessment. Legal counsel (Webber Wentzel NPC practice) advises on QCTO and MERSETA compliance. Financials audited by independent CA(SA) annually.",
    },
}


def load_example(key: str) -> None:
    ex = EXAMPLE_PROJECTS[key]
    fields = [
        "ps_context", "ps_problem", "ps_evidence", "ps_impact",
        "sol_description", "sol_achieved", "sol_differentiation", "sol_innovation",
        "team_overview", "team_achievements", "team_gaps",
        "bm_model", "bm_revenue", "bm_customers", "bm_competition",
        "mil_objectives", "mil_short", "mil_medium", "mil_kpis",
        "risk_technical", "risk_market", "risk_regulatory", "risk_financial", "risk_mitigation",
    ]
    for field in fields:
        st.session_state[field] = ex.get(field, "")
    st.session_state["proj_name"] = ex.get("label", "").split("—")[-1].strip() if "—" in ex.get("label", "") else ex.get("label", "")
    st.session_state["proj_org"] = ex.get("org", "")
    st.session_state["proj_funding"] = ex.get("funding_ask", "")
    trl = ex.get("trl", None)
    st.session_state["trl_result"] = trl
    if trl in (1, 2, 3, 4):
        st.session_state["finance_stage"] = "Grant-led development"
    elif trl in (5, 6):
        st.session_state["finance_stage"] = "Pilot and concessional finance"
    else:
        st.session_state["finance_stage"] = "Commercialisation and blended finance"
