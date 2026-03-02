"""
Validate a stock ticker using Yahoo Finance.

Usage:
    python validate_ticker.py AAPL
    python validate_ticker.py MSFT --verbose

Returns JSON to stdout:
    {"valid": true, "ticker": "AAPL", "company_name": "Apple Inc.", "error": null}
    {"valid": false, "ticker": "XYZZ", "company_name": null, "error": "No data found"}
"""

import argparse
import json
import sys

try:
    import yfinance as yf
except ImportError:
    print(json.dumps({
        "valid": False,
        "ticker": None,
        "company_name": None,
        "error": "yfinance not installed. Run: pip install yfinance"
    }))
    sys.exit(1)


def validate_ticker(ticker: str, verbose: bool = False) -> dict:
    """
    Validate a ticker symbol using Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        verbose: If True, print debug information
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "valid": False,
        "ticker": ticker.upper().strip(),
        "company_name": None,
        "error": None,
    }
    
    if not ticker or not ticker.strip():
        result["error"] = "Empty ticker provided"
        return result
    
    ticker = ticker.upper().strip()
    
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        if verbose:
            print(f"[DEBUG] Yahoo Finance info keys: {list(info.keys())[:10]}...", file=sys.stderr)
        
        # Check if we got meaningful data back
        # yfinance returns a dict with just 'trailingPegRatio' for invalid tickers
        short_name = info.get("shortName")
        long_name = info.get("longName")
        market_cap = info.get("marketCap")
        
        company_name = short_name or long_name
        
        if company_name:
            result["valid"] = True
            result["company_name"] = company_name
            if verbose:
                print(f"[DEBUG] Found company: {company_name}", file=sys.stderr)
                if market_cap:
                    print(f"[DEBUG] Market cap: {market_cap:,}", file=sys.stderr)
        else:
            result["error"] = "No company name found — ticker may be invalid"
            if verbose:
                print(f"[DEBUG] No shortName or longName in response", file=sys.stderr)
                
    except Exception as e:
        result["error"] = f"Yahoo Finance lookup failed: {str(e)}"
        if verbose:
            print(f"[DEBUG] Exception: {e}", file=sys.stderr)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Validate a stock ticker via Yahoo Finance")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug info to stderr")
    args = parser.parse_args()
    
    result = validate_ticker(args.ticker, verbose=args.verbose)
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
