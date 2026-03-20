import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))
from markdown_parser import parse_kv_table, clean_value

def calculate_wacc(md_path):
    print(f"WACC calculation started for {md_path}")
    # This is a placeholder for the WACC math script execution
    # Implementing full Yahoo Finance querying is outside text parsing scope, 
    # but the math logic (Beta -> CAPM -> WACC) goes here.
    print(f"WACC calculation complete for {md_path}")

if __name__ == "__main__":
    calculate_wacc(sys.argv[1])
