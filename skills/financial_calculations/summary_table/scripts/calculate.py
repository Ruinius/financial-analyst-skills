import sys
import os
import re
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))
from markdown_parser import parse_markdown_table, parse_kv_table, clean_value

def calculate_summary(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Get data from various tables
    is_items = parse_markdown_table(content, "### Line Items") # Income statement
    ebita_table = parse_kv_table(content, "## EBITA")
    tax_table = parse_kv_table(content, "## Tax Rates")
    ic_table = parse_kv_table(content, "## Invested Capital")
    shares_table = parse_kv_table(content, "## Shares Outstanding")
    growth_table = parse_kv_table(content, "## Organic Growth")

    # Time Period extraction
    time_period = "Q"
    match = re.search(r"\|\s*Time Period\s*\|\s*(.*?)\s*\|", content)
    if match:
        time_period = match.group(1).strip()
    multiplier = 4 if time_period.startswith("Q") else 1

    # Revenue & Interest Expense
    revenue = 0
    interest_expense = 0
    for item in is_items:
        std_name = item.get("Standardized Name", "").lower()
        if "revenue" in std_name and item.get("Calculated", "No") == "Yes":
            revenue = clean_value(item.get("Value", "0"))
        elif std_name == "interest_expense":
            interest_expense = clean_value(item.get("Value", "0"))

    # EBITA Metrics
    ebita = clean_value(ebita_table.get("EBITA", "0"))
    ebita_margin_pct = clean_value(ebita_table.get("EBITA Margin", "0%")) * 100

    # Tax Metrics
    eff_tax_rate = clean_value(tax_table.get("Effective Tax Rate", "0%"))
    adj_tax_rate = clean_value(tax_table.get("Adjusted Tax Rate", "0%"))
    chosen_tax_rate = adj_tax_rate if "Adjusted Tax Rate" in tax_table else eff_tax_rate
    tax_label = "Adjusted Tax Rate" if "Adjusted Tax Rate" in tax_table else "Effective Tax Rate"

    # IC Metrics
    nwc = clean_value(ic_table.get("Net Working Capital", "0"))
    nltoa = clean_value(ic_table.get("Net Long-Term Operating Assets", "0"))
    invested_capital = clean_value(ic_table.get("Invested Capital", "0"))
    capital_turnover = clean_value(ic_table.get("Capital Turnover", "0x"))

    # Shares
    basic_shares = clean_value(shares_table.get("Basic Shares Outstanding", "0"))
    diluted_shares = clean_value(shares_table.get("Diluted Shares Outstanding", "0"))

    # Growth
    simple_growth = clean_value(growth_table.get("Simple Revenue Growth", "0%")) * 100
    organic_growth = clean_value(growth_table.get("Organic Revenue Growth", "0%")) * 100

    # NOPAT & ROIC Calculation
    nopat = ebita * (1 - chosen_tax_rate)
    annualized_nopat = nopat * multiplier
    roic = (annualized_nopat / invested_capital) if invested_capital != 0 else 0
    roic_pct = roic * 100

    out = "\\n\\n---\\n\\n## Financial Summary\\n\\n| Metric | Value | Notes |\\n|--------|-------|-------|\\n"
    out += f"| **Revenue** | {revenue} | |\\n"
    out += f"| **EBITA** | {ebita} | |\\n"
    out += f"| **EBITA Margin** | {ebita_margin_pct:.2f}% | |\\n"
    out += f"| **Effective Tax Rate** | {eff_tax_rate*100:.2f}% | |\\n"
    out += f"| **Adjusted Tax Rate** | {adj_tax_rate*100:.2f}% | |\\n"
    out += f"| **NOPAT** | {nopat:.2f} | Using {tax_label} |\\n"
    out += f"| **Net Working Capital** | {nwc} | |\\n"
    out += f"| **Net Long-Term Operating Assets** | {nltoa} | |\\n"
    out += f"| **Invested Capital** | {invested_capital} | |\\n"
    out += f"| **Capital Turnover** | {capital_turnover:.2f}x | Annualized |\\n"
    out += f"| **ROIC** | {roic_pct:.2f}% | Annualized |\\n"
    out += f"| **Interest Expense** | {interest_expense} | |\\n"
    out += f"| **Basic Shares Outstanding** | {basic_shares} | |\\n"
    out += f"| **Diluted Shares Outstanding** | {diluted_shares} | |\\n"
    out += f"| **Simple Revenue Growth** | {simple_growth:.2f}% | YoY |\\n"
    out += f"| **Organic Revenue Growth** | {organic_growth:.2f}% | Constant currency |\\n\\n"
    
    out += "### Calculation Notes\\n\\n"
    out += "- Computed NOPAT automatically using EBITA x (1 - applicable tax rate)\\n"
    out += f"- Annualization multiplier applied to NOPAT for ROIC calculation: {multiplier}x\\n"
    
    with open(md_path, "a", encoding="utf-8") as f:
        f.write(out)
    print(f"Summary Table calculation complete for {md_path}")

if __name__ == "__main__":
    calculate_summary(sys.argv[1])
