import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))
from markdown_parser import parse_markdown_table, parse_kv_table, clean_value

def calculate_ic(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    bs_items = parse_markdown_table(content, "### Line Items") # Ensure finding the BS table by name if there are multiple. "Line Items" is both IS and BS.
    
    # We should distinguish BS from IS. Let's find Balance Sheet items: BS has Category column.
    bs_only = [x for x in bs_items if "Category" in x]
    
    is_items = [x for x in parse_markdown_table(content, "### Line Items") if "Expense" in x]
    
    # Get Revenue
    revenue = 0
    for item in is_items:
        if "revenue" in item.get("Standardized Name", "").lower() and item.get("Calculated", "No") == "Yes":
            revenue = clean_value(item.get("Value", "0"))
            break
            
    # Get Time Period
    meta = parse_kv_table(content, "## Document Classification") # Might need robust finding
    time_period = "Q" # default
    # scan content for time_period
    import re
    match = re.search(r"\|\s+Time Period\s+\|\s+(.*?)\s+\|", content)
    if match:
        time_period = match.group(1).strip()
    
    multiplier = 4 if time_period.startswith("Q") else 1
    ann_rev = revenue * multiplier
    
    oca_items = []
    ocl_items = []
    onca_items = []
    oncl_items = []
    
    for item in bs_only:
        val = clean_value(item.get("Value", "0"))
        if item.get("Calculated", "Yes") == "Yes" or item.get("Operating", "Yes") == "No":
            continue
            
        cat = item.get("Category", "")
        name = item.get("Line Name", "")
        if cat == "current_assets":
            oca_items.append((name, val))
        elif cat == "current_liabilities":
            ocl_items.append((name, val))
        elif cat == "noncurrent_assets":
            onca_items.append((name, val))
        elif cat == "noncurrent_liabilities":
            oncl_items.append((name, val))
            
    oca = sum(x[1] for x in oca_items)
    ocl = sum(x[1] for x in ocl_items)
    nwc = oca - ocl
    
    onca = sum(x[1] for x in onca_items)
    oncl = sum(x[1] for x in oncl_items)
    nltoa = onca - oncl
    
    ic = nwc + nltoa
    turnover = (ann_rev / ic) if ic != 0 else 0
    
    date_iso = datetime.now().isoformat()[:10]
    out = "\n\n---\n\n## Invested Capital\n\n| Field | Value |\n|-------|-------|\n"
    out += f"| Net Working Capital | {nwc} |\n"
    out += f"| Net Long-Term Operating Assets | {nltoa} |\n"
    out += f"| Invested Capital | {ic} |\n"
    out += f"| Capital Turnover | {turnover:.2f}x |\n"
    out += f"| Calculation Date | {date_iso} |\n\n"
    
    def render_breakdown(title, title_val, name_assets, arr_assets, name_liab, arr_liab):
        res = f"### {title} Breakdown\n\n| Component | Items | Total |\n|-----------|-------|-------|\n"
        res += f"| {name_assets} | " + ", ".join([x[0] for x in arr_assets]) + f" | {sum([x[1] for x in arr_assets])} |\n"
        res += f"| {name_liab} | " + ", ".join([x[0] for x in arr_liab]) + f" | {sum([x[1] for x in arr_liab])} |\n"
        res += f"| **{title}** | | **{title_val}** |\n\n"
        return res
        
    out += render_breakdown("Net Working Capital", nwc, "Operating Current Assets", oca_items, "Operating Current Liabilities", ocl_items)
    out += render_breakdown("Net Long-Term Operating Assets", nltoa, "Operating Noncurrent Assets", onca_items, "Operating Noncurrent Liabilities", oncl_items)
    
    with open(md_path, "a", encoding="utf-8") as f:
        f.write(out)
    print(f"Invested Capital calculation complete for {md_path}")

if __name__ == "__main__":
    calculate_ic(sys.argv[1])
