import streamlit as st
import math
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styles import inject_styles, sidebar_nav

st.set_page_config(page_title="Loan Calculator | JET PMO", page_icon="🧮", layout="wide")
inject_styles()
sidebar_nav()

st.markdown("""
<div class="hero" style="min-height:120px">
    <div class="hero-glow"></div><div class="hero-grid"></div><div class="hero-content" style="padding:1.4rem 2rem"><div class="hero-tag">🧮 Financial Modelling</div>
    <h1>Loan & Payback <span>Calculator</span></h1>
    <p>Model repayment schedules, compare financing scenarios, and understand the true cost of different funding instruments for your NEV project.</p>
</div>
</div>
""", unsafe_allow_html=True)

def format_zar(amount):
    if amount >= 1_000_000:
        return f"R {amount/1_000_000:.2f}M"
    return f"R {amount:,.0f}"

def calc_monthly_payment(principal, annual_rate, years):
    if annual_rate == 0:
        return principal / (years * 12)
    r = annual_rate / 100 / 12
    n = years * 12
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

def calc_total_interest(principal, monthly_payment, years):
    return (monthly_payment * years * 12) - principal

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Loan Calculator", "🔀 Scenario Comparison", "💡 Grant vs Loan Analysis"])

# ─────────────────────────────────────────────
# TAB 1 — Loan Calculator
# ─────────────────────────────────────────────
with tab1:
    st.markdown("### Loan Repayment Calculator")
    st.caption("Calculate monthly repayments, total interest, and see a full amortisation summary for any loan.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Loan Parameters**")
        principal = st.number_input("Loan Amount (R)", min_value=100_000, max_value=500_000_000,
                                     value=5_000_000, step=100_000, format="%d")
        loan_type = st.selectbox("Loan Type", [
            "Commercial Bank (Prime + 3%)",
            "Concessional / DFI Loan",
            "Custom Rate"
        ])
        if loan_type == "Commercial Bank (Prime + 3%)":
            prime = 11.75
            annual_rate = prime + 3
            st.info(f"ℹ️ SA Prime Rate = {prime}%. Effective rate = {annual_rate:.2f}%")
        elif loan_type == "Concessional / DFI Loan":
            annual_rate = st.slider("Concessional Interest Rate (%)", 0.0, 10.0, 4.0, 0.5)
        else:
            annual_rate = st.slider("Custom Annual Interest Rate (%)", 0.0, 25.0, 8.0, 0.25)

        tenor_years = st.slider("Loan Tenor (years)", 1, 25, 7)
        grace_months = st.slider("Grace Period (months — interest only)", 0, 24, 0,
                                  help="During grace period, only interest is paid, not principal.")

    with col2:
        st.markdown("**Results**")
        monthly = calc_monthly_payment(principal, annual_rate, tenor_years)
        total_interest = calc_total_interest(principal, monthly, tenor_years)
        total_cost = principal + total_interest
        effective_total = total_cost
        if grace_months > 0:
            grace_interest = principal * (annual_rate / 100 / 12) * grace_months
            effective_total += grace_interest

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0a1628,#0d3060); border-radius:12px; padding:1.5rem; margin-bottom:1rem'>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem'>
                <div>
                    <div style='color:#7ba7d4; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em'>Monthly Payment</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.6rem; font-weight:800; color:#4ade80'>{format_zar(monthly)}</div>
                </div>
                <div>
                    <div style='color:#7ba7d4; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em'>Total Interest</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.6rem; font-weight:800; color:#fbbf24'>{format_zar(total_interest)}</div>
                </div>
                <div>
                    <div style='color:#7ba7d4; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em'>Total Repayment</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.6rem; font-weight:800; color:white'>{format_zar(total_cost)}</div>
                </div>
                <div>
                    <div style='color:#7ba7d4; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em'>Interest Rate</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.6rem; font-weight:800; color:white'>{annual_rate:.2f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if grace_months > 0:
            grace_interest_monthly = principal * (annual_rate / 100 / 12)
            st.markdown(f"""
            <div class="tip-box">
                <h5>Grace Period ({grace_months} months)</h5>
                <p>During grace period: <strong>R {grace_interest_monthly:,.0f}/month</strong> (interest only)<br>
                After grace period: <strong>{format_zar(monthly)}/month</strong> (full repayment)<br>
                Additional grace period interest cost: <strong>{format_zar(grace_months * grace_interest_monthly)}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # Amortisation bar chart (simplified year-by-year)
        st.markdown("**Year-by-year balance**")
        balance = principal
        r_monthly = annual_rate / 100 / 12
        year_data = []
        for year in range(1, tenor_years + 1):
            interest_this_year = 0
            principal_this_year = 0
            for month in range(12):
                interest_payment = balance * r_monthly
                principal_payment = monthly - interest_payment
                interest_this_year += interest_payment
                principal_this_year += principal_payment
                balance -= principal_payment
                if balance < 0:
                    balance = 0
            year_data.append({"Year": f"Y{year}", "Balance": max(balance, 0)})

        import pandas as pd
        df = pd.DataFrame(year_data)
        st.bar_chart(df.set_index("Year")["Balance"], height=200, use_container_width=True, color="#0d3060")

# ─────────────────────────────────────────────
# TAB 2 — Scenario Comparison
# ─────────────────────────────────────────────
with tab2:
    st.markdown("### Compare Up to 3 Financing Scenarios")
    st.caption("Model different combinations of loan size, rate, and tenor to find the optimal structure for your project.")

    amount = st.number_input("Project Funding Amount (R)", min_value=500_000, max_value=500_000_000,
                               value=10_000_000, step=500_000, format="%d", key="scen_amount")

    st.markdown("#### Define Scenarios")
    scen_cols = st.columns(3)
    scenarios = []

    scenario_defaults = [
        ("Commercial Bank", 14.75, 5),
        ("DFI Concessional", 5.0, 10),
        ("Blended (50/50)", 8.5, 7),
    ]

    for i, (col, (name, rate, tenor)) in enumerate(zip(scen_cols, scenario_defaults)):
        with col:
            st.markdown(f"**Scenario {i+1}**")
            sc_name = st.text_input("Name", value=name, key=f"sc_name_{i}")
            sc_rate = st.number_input("Interest Rate (%)", value=rate, min_value=0.0, max_value=30.0,
                                       step=0.25, key=f"sc_rate_{i}")
            sc_tenor = st.number_input("Tenor (years)", value=tenor, min_value=1, max_value=25,
                                        step=1, key=f"sc_tenor_{i}")
            scenarios.append({"name": sc_name, "rate": sc_rate, "tenor": sc_tenor})

    st.markdown("---")
    st.markdown("#### Results")
    res_cols = st.columns(3)
    for i, (col, sc) in enumerate(zip(res_cols, scenarios)):
        monthly = calc_monthly_payment(amount, sc["rate"], sc["tenor"])
        total_interest = calc_total_interest(amount, monthly, sc["tenor"])
        total = amount + total_interest
        saving = None

        colors = ["#0d3060", "#0a4a2e", "#4a1a0a"]
        accent = ["#4ade80", "#22c55e", "#fbbf24"]

        col.markdown(f"""
        <div style='background:{colors[i]}; border-radius:12px; padding:1.3rem; text-align:center'>
            <div style='font-family:"Syne",sans-serif; font-weight:800; font-size:1rem; color:{accent[i]}; margin-bottom:0.8rem'>{sc["name"]}</div>
            <div style='color:#94b4d4; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em'>Monthly Payment</div>
            <div style='font-family:"Syne",sans-serif; font-size:1.4rem; font-weight:800; color:white'>{format_zar(monthly)}</div>
            <div style='color:#94b4d4; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin-top:0.5rem'>Total Interest</div>
            <div style='font-family:"Syne",sans-serif; font-size:1.1rem; font-weight:700; color:{accent[i]}'>{format_zar(total_interest)}</div>
            <div style='color:#94b4d4; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin-top:0.5rem'>Total Repayable</div>
            <div style='font-family:"Syne",sans-serif; font-size:1.1rem; font-weight:700; color:white'>{format_zar(total)}</div>
            <div style='color:#94b4d4; font-size:0.72rem; margin-top:0.5rem'>{sc["rate"]}% · {sc["tenor"]} years</div>
        </div>
        """, unsafe_allow_html=True)

    # Comparison table
    import pandas as pd
    rows = []
    for sc in scenarios:
        monthly = calc_monthly_payment(amount, sc["rate"], sc["tenor"])
        total_int = calc_total_interest(amount, monthly, sc["tenor"])
        rows.append({
            "Scenario": sc["name"],
            "Rate (%)": sc["rate"],
            "Tenor (yrs)": sc["tenor"],
            "Monthly (R)": f"R {monthly:,.0f}",
            "Total Interest (R)": f"R {total_int:,.0f}",
            "Total Repayable (R)": f"R {amount + total_int:,.0f}",
        })
    st.dataframe(pd.DataFrame(rows).set_index("Scenario"), use_container_width=True)

# ─────────────────────────────────────────────
# TAB 3 — Grant vs Loan Analysis
# ─────────────────────────────────────────────
with tab3:
    st.markdown("### Grant vs Loan — True Cost Analysis")
    st.caption("Compare the real financial benefit of securing a grant versus taking a loan for the same project component.")

    col1, col2 = st.columns(2)
    with col1:
        project_cost = st.number_input("Total Project Cost (R)", min_value=500_000, max_value=200_000_000,
                                        value=8_000_000, step=500_000, format="%d")
        grant_pct = st.slider("Grant Coverage (%)", 0, 100, 40,
                               help="What % of project cost does the grant cover?")
        remaining_pct = 100 - grant_pct
        loan_rate = st.number_input("Loan Interest Rate for Remainder (%)", value=9.0, min_value=0.0,
                                     max_value=25.0, step=0.25)
        loan_tenor = st.slider("Loan Tenor (years)", 1, 20, 7, key="gvl_tenor")

    with col2:
        grant_amount = project_cost * grant_pct / 100
        loan_amount = project_cost * remaining_pct / 100
        monthly_loan = calc_monthly_payment(loan_amount, loan_rate, loan_tenor)
        total_loan_interest = calc_total_interest(loan_amount, monthly_loan, loan_tenor)
        total_cost_with_grant = loan_amount + total_loan_interest
        total_cost_no_grant = calc_total_interest(project_cost, loan_rate, loan_tenor) + project_cost
        saving = total_cost_no_grant - total_cost_with_grant

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0a1628,#0d3060); border-radius:12px; padding:1.5rem; margin-bottom:1rem'>
            <div style='font-family:"Syne",sans-serif; font-weight:800; font-size:1rem; color:#4ade80; margin-bottom:1rem'>With {grant_pct}% Grant Coverage</div>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.8rem'>
                <div>
                    <div style='color:#7ba7d4; font-size:0.72rem; text-transform:uppercase'>Grant (free capital)</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.3rem; font-weight:800; color:#4ade80'>{format_zar(grant_amount)}</div>
                </div>
                <div>
                    <div style='color:#7ba7d4; font-size:0.72rem; text-transform:uppercase'>Loan Needed</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.3rem; font-weight:800; color:white'>{format_zar(loan_amount)}</div>
                </div>
                <div>
                    <div style='color:#7ba7d4; font-size:0.72rem; text-transform:uppercase'>Monthly Repayment</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.3rem; font-weight:800; color:white'>{format_zar(monthly_loan)}</div>
                </div>
                <div>
                    <div style='color:#7ba7d4; font-size:0.72rem; text-transform:uppercase'>Total Interest Cost</div>
                    <div style='font-family:"Syne",sans-serif; font-size:1.3rem; font-weight:800; color:#fbbf24'>{format_zar(total_loan_interest)}</div>
                </div>
            </div>
            <div style='margin-top:1rem; padding-top:1rem; border-top:1px solid #1e3a5f'>
                <div style='color:#7ba7d4; font-size:0.72rem; text-transform:uppercase'>Interest Saving vs 100% Loan</div>
                <div style='font-family:"Syne",sans-serif; font-size:1.6rem; font-weight:800; color:#4ade80'>Save {format_zar(saving)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-box">
        <h5>💡 Key Insight</h5>
        <p>Grant funding is not "free" in terms of time — applications, compliance, and reporting have real costs. But the interest saving on a 40% grant is almost always larger than the administrative cost. For JET/NEV projects, always pursue available grants before commercial debt.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("💰 Back to Financing Options", use_container_width=True):
        st.switch_page("pages/3_Financing_Options.py")
with col2:
    if st.button("📄 View Summary & Export", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Summary_Export.py")
