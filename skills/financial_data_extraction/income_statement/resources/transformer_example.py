import urllib.request
import json
import sys

payload = {
    "items": [
        {"line_name": "Subscription revenue", "line_category": "income_statement", "line_order": 0},
        {"line_name": "Product revenue", "line_category": "income_statement", "line_order": 1},
        {"line_name": "Total revenue", "line_category": "income_statement", "line_order": 2},
        # ... your extracted items ...
    ]
}

req = urllib.request.Request('http://localhost:8000/predict/income-statement',
                             method='POST',
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(payload).encode('utf-8'))

try:
    response = urllib.request.urlopen(req)
    predictions = json.loads(response.read().decode('utf-8'))
    # The server returns a JSON array (list) directly: [{"standardized_name": "...", "confidence": 0.99}, ...]
    for i, item in enumerate(predictions):
        print(f"Row {i}: mapped to {item['standardized_name']} (calculated={item.get('is_calculated')})")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)