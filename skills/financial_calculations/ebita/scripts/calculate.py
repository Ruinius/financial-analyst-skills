import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))
from markdown_parser import parse_markdown_table, parse_kv_table, clean_value

def calculate_ebita(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Get Income Statement Line Items
    is_items = parse_markdown_table(content, "### Line Items") # assuming unique within IS
    
    # Get GAAP Reconciliation items if available
    gaap_items = parse_markdown_table(content, "### Adjustments")
    
    # Get Revenue
    revenue = 0
    for item in is_items:
        if "revenue" in item.get("Standardized Name", "").lower() and item.get("Calculated", "No") == "Yes":
            revenue = clean_value(item.get("Value", "0"))
            break
            
    # Step 2: Starting Point
    starting_val = 0
    starting_name = "Operating Income"
    for item in is_items:
        if item.get("Standardized Name") == "operating_income":
            starting_val = clean_value(item.get("Value", "0"))
            break
    else:
        for item in is_items:
            if item.get("Standardized Name") == "income_before_taxes":
                starting_val = clean_value(item.get("Value", "0"))
                starting_name = "Income Before Taxes"
                break
                
    ebita = starting_val
    adjustments_out = []
    adj_id = 1
    
    # Step 3: GAAP Adjs
    for item in gaap_items:
        if item.get("Operating", "Yes") == "No":
            val = clean_value(item.get("Value", "0"))
            if val != 0:
                ebita += val
                adjustments_out.append(f"| {adj_id} | {item.get('Line Name')} | {val} | GAAP Reconciliation |")
                adj_id += 1
                
    # Step 4: IS Non-Operating additions
    found_op_inc = False
    for item in is_items:
        if item.get("Standardized Name") == "operating_income" or item.get("Standardized Name") == "income_before_taxes":
            found_op_inc = True
        
        # We only look above Operating Income
        if not found_op_inc and item.get("Operating", "Yes") == "No" and item.get("Calculated", "Yes") == "No":
            val = clean_value(item.get("Value", "0"))
            if val != 0:
                # negate and add
                ebita += -val
                adjustments_out.append(f"| {adj_id} | {item.get('Line Name')} | {-val} | Income Statement |")
                adj_id += 1
                
    ebita_margin = (ebita / revenue) * 100 if revenue else 0
    
    # Append
    from datetime import datetime
    date_iso = datetime.now().isoformat()[:10]
    out = "\n\n---\n\n## EBITA\n\n| Field | Value |\n|-------|-------|\n"
    out += f"| Starting Point | {starting_name} |\n"
    out += f"| Starting Value | {starting_val} |\n| EBITA | {ebita} |\n"
    out += f"| EBITA Margin | {ebita_margin:.2f}% |\n| Calculation Date | {date_iso} |\n\n"
    
    if adjustments_out:
        out += "### Adjustments\n\n| # | Line Name | Value | Source |\n|---|-----------|-------|--------|\n"
        out += "\n".join(adjustments_out) + "\n"
        
    with open(md_path, "a", encoding="utf-8") as f:
        f.write(out)
    print(f"EBITA calculation complete for {md_path}")

if __name__ == "__main__":
    calculate_ebita(sys.argv[1])
