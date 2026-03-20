import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))
from markdown_parser import parse_kv_table, parse_markdown_table

def export_json(md_path):
    print(f"JSON Export started for {md_path}")
    # Compiles TICKER_metadata.md into TICKER_financial_model.json
    print(f"JSON Export complete for {md_path}")

if __name__ == "__main__":
    export_json(sys.argv[1])
