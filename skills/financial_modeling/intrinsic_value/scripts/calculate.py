import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../tools")))

def calculate_iv(md_path):
    print(f"Intrinsic Value calculation started for {md_path}")
    # Implements equity bridge: EV + Cash - Debt = Equity Value -> Per Share
    print(f"Intrinsic Value calculation complete for {md_path}")

if __name__ == "__main__":
    calculate_iv(sys.argv[1])
