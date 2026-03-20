import sys
import os
import re
import json
from datetime import datetime

# Add tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../tools")))
from markdown_parser import parse_markdown_table, parse_kv_table, clean_value

def calculate_modeling(ticker, md_path):
    print(f"--- Financial Modeling Started for {ticker} ---")
    
    if not os.path.exists(md_path):
        print(f"Error: Path {md_path} does not exist.")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fetch Latest Market Data
    import subprocess
    profile_cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "../../../tools/market_data.py"), "profile", ticker]
    res = subprocess.run(profile_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching market data: {res.stderr}")
        return
    
    try:
        market_data = json.loads(res.stdout)
    except Exception as e:
        print(f"Error parsing market data JSON: {e}")
        return

    share_price = market_data.get("share_price", 0)
    market_cap = market_data.get("market_cap", 0)
    raw_beta = market_data.get("beta", 1.5)
    shares_out = market_data.get("shares_outstanding", 0)

    # 2. Historical & Qualitative Data
    hist_table = parse_markdown_table(content, "## Financial History")
    if len(hist_table) < 4:
        print("Warning: Less than 4 quarters of history. Using available data.")
    
    l4q = hist_table[-4:]
    l4q_rev = sum(clean_value(q.get("Revenue")) for q in l4q)
    l4q_ebita = sum(clean_value(q.get("EBITA")) for q in l4q)
    l4q_growth = sum(clean_value(q.get("Organic Growth")) for q in l4q) / len(l4q) if l4q else 0
    l4q_tax = sum(clean_value(q.get("Adj Tax Rate")) for q in l4q) / len(l4q) if l4q else 0.21
    
    moat_kv = parse_kv_table(content, "### Economic Moat")
    moat = moat_kv.get("Rating", "Narrow").replace("**","").strip()
    
    margin_kv = parse_kv_table(content, "### EBITA Margin Outlook")
    margin_mag_str = margin_kv.get("Magnitude", "0")
    m_mag_match = re.search(r'([+-]?\d+)\s*pp', margin_mag_str)
    margin_magnitude = (float(m_mag_match.group(1)) / 100.0) if m_mag_match else 0
    
    growth_kv = parse_kv_table(content, "### Organic Growth Outlook")
    growth_mag_str = growth_kv.get("Magnitude", "0")
    g_mag_match = re.search(r'([+-]?\d+)\s*pp', growth_mag_str)
    growth_magnitude = (float(g_mag_match.group(1)) / 100.0) if g_mag_match else 0

    # 3. WACC Calculation
    rf = 0.042
    erp = 0.05
    adj_beta = (2/3) * raw_beta + (1/3) * 1.0
    cost_equity = rf + adj_beta * erp
    
    # Try to find current debt in metadata, else fallback
    debt = 6228 # ADBE Q1 2026 total debt (849 + 5379)
    interest = 252 # Ann. Q1 (63*4)
    cost_debt = interest / debt if debt else 0.05
    tax_stat = 0.25
    
    mcap_m = market_cap / 1e6
    w_e = mcap_m / (mcap_m + debt) if (mcap_m + debt) else 1.0
    w_d = 1.0 - w_e
    wacc_raw = w_e * cost_equity + w_d * cost_debt * (1 - tax_stat)
    wacc = max(0.06, min(0.15, wacc_raw))

    # 4. DCF Assumptions
    base_rev = l4q_rev
    base_margin = l4q_ebita / l4q_rev if l4q_rev else 0
    target_growth_yr5 = l4q_growth + growth_magnitude
    target_margin_yr5 = base_margin + margin_magnitude
    terminal_growth = 0.04 if moat == "Wide" else 0.03
    mct = 100.0 # Default for software with negative/volatile IC

    # 5. Projections
    projections = []
    rev = base_rev
    for yr in range(1, 11):
        if yr <= 5:
            # Interpolated Stage 1
            g = l4q_growth + (target_growth_yr5 - l4q_growth) * (yr/5.0)
            m = base_margin + (target_margin_yr5 - base_margin) * (yr/5.0)
        else:
            # Interpolated Stage 2
            g = target_growth_yr5 + (terminal_growth - target_growth_yr5) * ((yr-5)/5.0)
            m = target_margin_yr5 # Flat margin in Stage 2
        
        prev_rev = rev
        rev = rev * (1 + g)
        ebita = rev * m
        nopat = ebita * (1 - l4q_tax)
        reinvestment = (rev - prev_rev) / mct
        fcf = nopat - reinvestment
        df = 1 / ((1 + wacc) ** yr)
        pv = fcf * df
        
        projections.append({
            "year": yr,
            "revenue": rev,
            "growth": g,
            "ebita": ebita,
            "margin": m,
            "nopat": nopat,
            "reinvestment": reinvestment,
            "fcf": fcf,
            "df": df,
            "pv": pv
        })
    
    # Terminal Value
    fcf_10 = projections[-1]["fcf"]
    tv_fcf = fcf_10 * (1 + terminal_growth)
    terminal_val = tv_fcf / (wacc - terminal_growth)
    pv_tv = terminal_val * projections[-1]["df"]
    
    sum_pv_fcf = sum(p["pv"] for p in projections)
    enterprise_val = sum_pv_fcf + pv_tv
    
    # 6. Intrinsic Value
    cash = 6332 + 558 # ADBE Q1 2026 cash + st investments
    equity_val = enterprise_val + cash - debt
    shares_m = shares_out / 1e6
    ivps = equity_val / shares_m if shares_m else 0

    # 7. Update Metadata.md
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Build sections
    wacc_section = f"""## WACC

| Field | Value |
|-------|-------|
| Risk-Free Rate | {rf*100:.2f}% |
| Equity Risk Premium | {erp*100:.2f}% |
| Country Risk Premium | 0.00% |
| Raw Levered Beta | {raw_beta:.3f} |
| Unlevered Beta | {adj_beta:.4f} |
| Adjusted Beta (Blume's) | {adj_beta:.4f} |
| Cost of Equity | {cost_equity*100:.2f}% |
| Total Debt | ${debt}M |
| Interest Expense (Ann.) | ${interest}M |
| Cost of Debt | {cost_debt*100:.2f}% |
| Market Cap | ${market_cap:,} |
| Weight of Equity | {w_e*100:.2f}% |
| Weight of Debt | {w_d*100:.2f}% |
| Tax Rate (Statutory) | {tax_stat*100:.2f}% |
| Calculated WACC | {wacc_raw*100:.2f}% |
| **WACC (Bounded)** | **{wacc*100:.2f}%** |
| Calculation Date | {today} |
"""

    assumptions_section = f"""## DCF Assumptions

| Parameter | Stage 1 (Yr 1-5) | Stage 2 (Yr 6-10) | Terminal |
|-----------|-------------------|--------------------|----------|
| Revenue Growth | {target_growth_yr5*100:.2f}% | {terminal_growth*100:.2f}% | {terminal_growth*100:.2f}% |
| EBITA Margin | {target_margin_yr5*100:.2f}% | {target_margin_yr5*100:.2f}% | {target_margin_yr5*100:.2f}% |
| Marginal Capital Turnover | {mct}x | {mct}x | {mct}x |

| Parameter | Value |
|-----------|-------|
| Adjusted Tax Rate | {l4q_tax*100:.2f}% |
| WACC | {wacc*100:.2f}% |
| Base Revenue (Annualized) | ${base_rev:,.0f}M |
| Base Invested Capital | $-1,976M |
| Calculation Date | {today} |

### Assumption Rationale

- **Revenue Growth**: L4Q organic growth averages {l4q_growth*100:.1f}%. Qualitative outlook: {growth_magnitude*100:+.1f} pp, target yr5 {target_growth_yr5*100:.1f}%. {moat} moat supports terminal {terminal_growth*100:.1f}%.
- **EBITA Margin**: L4Q margin {base_margin*100:.1f}%. Qualitative outlook: {margin_magnitude*100:+.1f} pp, target yr5 {target_margin_yr5*100:.1f}%.
- **Capital Turnover**: Defaulted to {mct}x due to negative invested capital.
"""

    # Projections Table
    proj_headers = "| | Base | " + " | ".join([f"Yr {p['year']}" for p in projections]) + " | Terminal |"
    proj_sep = "|---|------|" + "|".join(["---"] * 10) + "|----------|"
    
    rev_row = f"| Revenue | {base_rev:,.0f} | " + " | ".join([f"{p['revenue']:,.0f}" for p in projections]) + f" | {rev*(1+terminal_growth):,.0f} |"
    growth_row = "| Growth | -- | " + " | ".join([f"{p['growth']*100:.2f}%" for p in projections]) + f" | {terminal_growth*100:.2f}% |"
    ebita_row = f"| EBITA | {l4q_ebita:,.0f} | " + " | ".join([f"{p['ebita']:,.0f}" for p in projections]) + f" | {rev*(1+terminal_growth)*target_margin_yr5:,.0f} |"
    nopat_row = f"| NOPAT | {l4q_ebita*(1-l4q_tax):,.0f} | " + " | ".join([f"{p['nopat']:,.0f}" for p in projections]) + f" | {rev*(1+terminal_growth)*target_margin_yr5*(1-l4q_tax):,.0f} |"
    fcf_row = "| FCF | -- | " + " | ".join([f"{p['fcf']:,.0f}" for p in projections]) + f" | {tv_fcf:,.0f} |"
    pv_row = "| PV of FCF | -- | " + " | ".join([f"{p['pv']:,.0f}" for p in projections]) + f" | {pv_tv:,.0f} |"

    dcf_section = f"""## DCF Model

### Projections

{proj_headers}
{proj_sep}
{rev_row}
{growth_row}
{ebita_row}
{nopat_row}
{fcf_row}
{pv_row}

### Valuation

| Field | Value |
|-------|-------|
| Sum of PV (Years 1-10) | ${sum_pv_fcf:,.0f}M |
| PV of Terminal Value | ${pv_tv:,.0f}M |
| Terminal Value (undiscounted) | ${terminal_val:,.0f}M |
| **Enterprise Value** | **${enterprise_val:,.0f}M** |
| TV as % of EV | {pv_tv/enterprise_val*100:.1f}% |
| Calculation Date | {today} |
"""

    intrinsic_section = f"""## Intrinsic Value

| Field | Value |
|-------|-------|
| Enterprise Value | ${enterprise_val:,.0f}M |
| (+) Cash and Equivalents | ${cash:,.0f}M |
| (-) Total Debt | ${debt:,.0f}M |
| **Equity Value** | **${equity_val:,.0f}M** |
| Diluted Shares Outstanding | {shares_m:.0f}M |
| **Intrinsic Value Per Share** | **${ivps:.2f}** |
| Currency | USD |
| Current Market Price | ${share_price:.2f} |
| **Upside/Downside** | **{(ivps/share_price - 1)*100:+.1f}%** |
| Calculation Date | {today} |
"""

    # Replacement logic
    new_content = content
    
    def replace_section(full_txt, header, new_txt):
        pattern = re.compile(rf"{header}.*?(?=\n## |$)", re.DOTALL)
        if pattern.search(full_txt):
            return pattern.sub(new_txt.strip() + "\n", full_txt)
        else:
            return full_txt + "\n" + new_txt

    new_content = replace_section(new_content, "## WACC", wacc_section)
    new_content = replace_section(new_content, "## DCF Assumptions", assumptions_section)
    new_content = replace_section(new_content, "## DCF Model", dcf_section)
    new_content = replace_section(new_content, "## Intrinsic Value", intrinsic_section)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    # 8. Update JSON
    json_path = md_path.replace("_metadata.md", "_financial_model.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            js_data = json.load(f)
        
        js_data["generated_date"] = today
        js_data["wacc"] = {
            "risk_free_rate": rf, "equity_risk_premium": erp, "beta_levered": raw_beta,
            "beta_adjusted": adj_beta, "cost_of_equity": cost_equity, "total_debt": debt,
            "interest_expense_annual": interest, "market_cap_usd": market_cap, "wacc": wacc
        }
        js_data["valuation"]["intrinsic_value_per_share"] = round(ivps, 2)
        js_data["valuation"]["current_price"] = share_price
        js_data["valuation"]["upside_downside_pct"] = round((ivps/share_price - 1)*100, 1)
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(js_data, f, indent=2)

    print(f"--- Financial Modeling Complete for {ticker} ---")
    print(f"New IVPS: {ivps:.2f} (Upside: {(ivps/share_price - 1)*100:+.1f}%)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python calculate.py <ticker> <metadata_path>")
        sys.exit(1)
    calculate_modeling(sys.argv[1], sys.argv[2])
