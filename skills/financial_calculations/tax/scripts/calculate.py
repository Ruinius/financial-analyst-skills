import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))
from markdown_parser import parse_markdown_table, parse_kv_table, clean_value

def calculate_tax(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    is_items = parse_markdown_table(content, "### Line Items")
    # Get pre-calculated EBITA from markdown if available or simply from kv table
    ebita_table = parse_kv_table(content, "## EBITA")
    ebita = clean_value(ebita_table.get("EBITA", "0"))
    
    # adjustments from EBITA step
    ebita_adjs = parse_markdown_table(content, "### Adjustments")

    income_before_taxes = 0
    income_tax_expense = 0
    net_income = 0
    found_tax = False
    
    for item in is_items:
        std_name = item.get("Standardized Name", "").lower()
        if std_name == "income_before_taxes":
            income_before_taxes = clean_value(item.get("Value", "0"))
        elif std_name == "income_tax_provision":
            income_tax_expense = clean_value(item.get("Value", "0"))
            found_tax = True
        elif std_name == "net_income":
            net_income = clean_value(item.get("Value", "0"))

    # Fallback logic for basic effective tax rate
    effective_rate = 0
    if found_tax and income_before_taxes != 0:
        effective_rate = -(income_tax_expense / income_before_taxes)
    elif income_before_taxes != 0:
        effective_rate = (income_before_taxes - net_income) / income_before_taxes
    else:
        effective_rate = 0.21 # Default 21% if all else fails

    # Adjusted Tax Rate logic
    total_tax_adj = 0
    adj_out = []
    
    for item in ebita_adjs:
        name = item.get("Line Name", "").lower()
        val = clean_value(item.get("Value", "0"))
        source = item.get("Source", "Non-GAAP")
        
        marginal_rate = 0.25
        if "impairment" in name or "amortization" in name or "equity" in name:
            marginal_rate = 0.0

        # Based on tax/SKILL.md, tax effect depends on source
        if source == "Income Statement":
            # IS items were negated to add back to EBITA, but here we calculate tax effect
            # Wait, Tax effect = line_value * marginal_rate (based on original value). 
            # In ebita_adjs table, value is ALREADY negated from IS (it's the addback amount).
            tax_effect = val * marginal_rate
        else:
            tax_effect = val * marginal_rate
            
        total_tax_adj += tax_effect
        rate_str = f"{int(marginal_rate*100)}%"
        adj_out.append(f"| {len(adj_out)+1} | {item.get('Line Name')} | {val} | {tax_effect:.2f} | {source} | {rate_str} |")

    adjusted_tax = income_tax_expense + total_tax_adj
    adjusted_rate = -(adjusted_tax / ebita) if ebita != 0 else 0

    date_iso = datetime.now().isoformat()[:10]
    out = "\n\n---\n\n## Tax Rates\n\n| Field | Value |\n|-------|-------|\n"
    out += f"| Income Before Taxes | {income_before_taxes} |\n"
    out += f"| Income Tax Expense | {income_tax_expense} |\n"
    out += f"| Net Income | {net_income} |\n"
    out += f"| Effective Tax Rate | {effective_rate*100:.2f}% |\n"
    out += f"| Adjusted Tax Rate | {adjusted_rate*100:.2f}% |\n"
    out += f"| Calculation Date | {date_iso} |\n\n"
    
    out += "### Adjusted Tax Rate Breakdown\n\n| # | Line Name | Value | Tax Effect | Source | Marginal Rate |\n|---|-----------|-------|------------|--------|---------------|\n"
    if adj_out:
        out += "\n".join(adj_out) + "\n"
    out += f"| | **Reported Tax** | **{income_tax_expense}** | | | |\n"
    out += f"| | **Total Tax Adjustment** | | **{total_tax_adj:.2f}** | | |\n"
    out += f"| | **Adjusted Tax** | **{adjusted_tax:.2f}** | | | |\n"

    with open(md_path, "a", encoding="utf-8") as f:
        f.write(out)
    print(f"Tax calculation complete for {md_path}")

if __name__ == "__main__":
    calculate_tax(sys.argv[1])
