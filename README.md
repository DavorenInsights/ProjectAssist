# ⚡ JET PMO — Project Funding Assistant

A guided funding application tool for New Energy Vehicle (NEV) projects under South Africa's Just Energy Transition (JET) programme.

## What it does

This Streamlit app helps project teams build high-quality, funder-ready applications by guiding them through:

- **Guided Application** — structured prompts for all key sections (Problem Statement, Solution, Team, Business Model, Milestones, Risk Register)
- **TRL Calculator** — 10-question Technology Readiness Level assessment with funding guidance
- **Financing Options Explorer** — explains 8 financing instruments (grants, concessional loans, blended finance, DFI project finance, equity, green bonds, commercial debt, carbon finance)
- **Loan & Payback Calculator** — model repayment scenarios, compare financing structures, and analyse grant vs loan savings
- **Summary & PDF Export** — review and export your full application as a formatted PDF

## Quick Start

```bash
git clone https://github.com/YOUR_ORG/jet-pmo-assistant.git
cd jet-pmo-assistant
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the entry point
5. Deploy — no environment variables needed

## Project Structure

```
jet-pmo-assistant/
├── app.py                          # Landing page
├── requirements.txt
├── utils/
│   └── styles.py                   # Shared CSS styles & sidebar
└── pages/
    ├── 1_Guided_Application.py     # 6-section application builder
    ├── 2_TRL_Calculator.py         # TRL 1–9 calculator
    ├── 3_Financing_Options.py      # 8 financing instruments explained
    ├── 4_Loan_Calculator.py        # Loan, scenario & grant calculator
    └── 5_Summary_Export.py         # Review + PDF export
```

## Status

Demo v1.0 — built to test appetite. A full Terms of Reference (TOR) for production development is available on request.

## Future enhancements (post-demo)

- [ ] AI-assisted feedback per application section (Claude API)
- [ ] User accounts and saved applications (database backend)
- [ ] Funder database with eligibility matching
- [ ] Multi-language support (Zulu, Xhosa, Afrikaans)
- [ ] Admin dashboard for PMO to review submissions
- [ ] Integration with JET investment tracking system
