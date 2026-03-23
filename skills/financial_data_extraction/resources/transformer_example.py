"""
Template script for querying the Tiger-Transformer API.

Usage:
  python resources/transformer_example.py

The Tiger-Transformer standardizes financial line item names using a trained
classification model. It requires the server to be running on localhost:8000.

Endpoints:
  POST /predict/balance-sheet     — Standardize balance sheet line items
  POST /predict/income-statement  — Standardize income statement line items
  GET  /health                    — Check server readiness

Request body:
  {"items": [{"line_name": "...", "line_value": 123, "line_category": "..."}]}

Response (array, one per input item):
  [
    {
      "standardized_name": "cash_and_equivalents",
      "is_calculated": false,
      "is_operating": false,
      "confidence": 0.997
    }
  ]

For income-statement items, the response also includes:
  "is_expense": true/false

IMPORTANT: Send ALL line items in a single batch request. The model uses a
sliding context window (2 items before + 2 items after) to classify each item.
Sending items individually strips this context and causes misclassifications.
"""

import json
import urllib.request
import sys


def predict(endpoint, items):
    """Send items to the Tiger-Transformer and return standardized results."""
    url = f"http://localhost:8000/predict/{endpoint}"
    payload = json.dumps({"items": items}).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="POST",
        headers={"Content-Type": "application/json"},
        data=payload,
    )
    try:
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error calling {endpoint}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # --- Balance Sheet Example ---
    bs_items = [
        {"line_name": "Cash and cash equivalents", "line_value": 2243971, "line_category": "assets"},
        {"line_name": "Inventories", "line_value": 1323602, "line_category": "assets"},
        {"line_name": "Property and equipment, net", "line_value": 1545811, "line_category": "assets"},
        {"line_name": "Total assets", "line_value": 7091941, "line_category": "assets"},
        {"line_name": "Accounts payable", "line_value": 348441, "line_category": "liabilities"},
    ]

    print("=== Balance Sheet Standardization ===")
    bs_results = predict("balance-sheet", bs_items)
    for orig, trans in zip(bs_items, bs_results):
        print(f"  {orig['line_name']:40s} -> {trans['standardized_name']:30s} (conf: {trans['confidence']:.3f})")

    # --- Income Statement Example ---
    is_items = [
        {"line_name": "Net revenue", "line_value": 3205103, "line_category": "income_statement"},
        {"line_name": "Costs of goods sold", "line_value": 1301678, "line_category": "income_statement"},
        {"line_name": "Gross profit", "line_value": 1903425, "line_category": "income_statement"},
        {"line_name": "Income from operations", "line_value": 913890, "line_category": "income_statement"},
        {"line_name": "Net income", "line_value": 669468, "line_category": "income_statement"},
    ]

    print("\n=== Income Statement Standardization ===")
    is_results = predict("income-statement", is_items)
    for orig, trans in zip(is_items, is_results):
        exp = " [EXPENSE]" if trans.get("is_expense") else ""
        print(f"  {orig['line_name']:40s} -> {trans['standardized_name']:30s} (conf: {trans['confidence']:.3f}){exp}")
